"""
Enhanced 3D navigation controls and camera management
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional
from PyQt6.QtCore import QPoint

class NavigationMode(Enum):
    ORBIT = "orbit"
    PAN = "pan"
    ZOOM = "zoom"
    FLY = "fly"
    WALK = "walk"

@dataclass
class CameraPreset:
    name: str
    position: np.ndarray
    target: np.ndarray
    up: np.ndarray

class Navigation3D:
    def __init__(self):
        self.mode = NavigationMode.ORBIT
        self.camera_presets = {
            "Front": CameraPreset("Front", np.array([0, 0, 5]), np.array([0, 0, 0]), np.array([0, 1, 0])),
            "Top": CameraPreset("Top", np.array([0, 5, 0]), np.array([0, 0, 0]), np.array([0, 0, -1])),
            "Right": CameraPreset("Right", np.array([5, 0, 0]), np.array([0, 0, 0]), np.array([0, 1, 0])),
            "Perspective": CameraPreset("Perspective", np.array([5, 5, 5]), np.array([0, 0, 0]), np.array([0, 1, 0]))
        }
        self.init_navigation()

    def init_navigation(self):
        """Initialize navigation parameters"""
        self.camera_pos = self.camera_presets["Perspective"].position.copy()
        self.camera_target = self.camera_presets["Perspective"].target.copy()
        self.camera_up = self.camera_presets["Perspective"].up.copy()
        self.last_pos = QPoint()
        self.orbit_speed = 0.5
        self.pan_speed = 0.01
        self.zoom_speed = 0.1
        self.fly_speed = 0.1
        self.walk_speed = 0.1

    def set_mode(self, mode: NavigationMode):
        """Set navigation mode"""
        self.mode = mode

    def set_camera_preset(self, preset_name: str):
        """Set camera to a preset view"""
        if preset_name in self.camera_presets:
            preset = self.camera_presets[preset_name]
            self.camera_pos = preset.position.copy()
            self.camera_target = preset.target.copy()
            self.camera_up = preset.up.copy()

    def orbit(self, dx: float, dy: float):
        """Orbit camera around target"""
        # Convert to spherical coordinates
        dir_vector = self.camera_pos - self.camera_target
        radius = np.linalg.norm(dir_vector)
        theta = np.arctan2(dir_vector[0], dir_vector[2])
        phi = np.arctan2(np.sqrt(dir_vector[0]**2 + dir_vector[2]**2), dir_vector[1])

        # Update angles
        theta -= dx * self.orbit_speed
        phi = np.clip(phi + dy * self.orbit_speed, 0.1, np.pi - 0.1)

        # Convert back to Cartesian coordinates
        self.camera_pos = self.camera_target + radius * np.array([
            np.sin(phi) * np.sin(theta),
            np.cos(phi),
            np.sin(phi) * np.cos(theta)
        ])

    def pan(self, dx: float, dy: float):
        """Pan camera in view plane"""
        forward = self.camera_target - self.camera_pos
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, self.camera_up)
        right = right / np.linalg.norm(right)
        up = np.cross(right, forward)
        up = up / np.linalg.norm(up)

        offset = (-right * dx + up * dy) * self.pan_speed
        self.camera_pos += offset
        self.camera_target += offset

    def zoom(self, delta: float):
        """Zoom camera in/out"""
        forward = self.camera_target - self.camera_pos
        forward = forward / np.linalg.norm(forward)
        self.camera_pos += forward * delta * self.zoom_speed

    def fly(self, dx: float, dy: float):
        """Fly camera in view direction"""
        forward = self.camera_target - self.camera_pos
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, self.camera_up)
        right = right / np.linalg.norm(right)
        
        self.camera_pos += (forward * -dy + right * dx) * self.fly_speed
        self.camera_target += (forward * -dy + right * dx) * self.fly_speed

    def walk(self, dx: float, dy: float):
        """Walk camera on ground plane"""
        forward = self.camera_target - self.camera_pos
        forward[1] = 0  # Project onto ground plane
        forward = forward / np.linalg.norm(forward)
        right = np.cross(forward, np.array([0, 1, 0]))
        
        self.camera_pos += (forward * -dy + right * dx) * self.walk_speed
        self.camera_target += (forward * -dy + right * dx) * self.walk_speed

    def focus_on_point(self, point: np.ndarray, distance: Optional[float] = None):
        """Focus camera on a specific point"""
        self.camera_target = point
        if distance is not None:
            forward = self.camera_pos - self.camera_target
            forward = forward / np.linalg.norm(forward)
            self.camera_pos = self.camera_target + forward * distance
