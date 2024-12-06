"""
3D Viewport implementation using OpenGL
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt6.QtOpenGLWidgets import QOpenGLWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent, QWheelEvent
import numpy as np

class Viewport3D(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_camera()
        self.init_navigation()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_camera(self):
        """Initialize camera parameters"""
        self.camera_pos = np.array([0.0, 0.0, 5.0])
        self.camera_target = np.array([0.0, 0.0, 0.0])
        self.camera_up = np.array([0.0, 1.0, 0.0])
        self.fov = 45.0
        self.near = 0.1
        self.far = 1000.0

    def init_navigation(self):
        """Initialize navigation parameters"""
        self.last_pos = QPoint()
        self.rotating = False
        self.panning = False
        self.rotation = np.array([0.0, 0.0, 0.0])
        self.zoom_speed = 0.1
        self.rotation_speed = 0.5
        self.pan_speed = 0.01

    def initializeGL(self):
        """Initialize OpenGL settings"""
        glClearColor(0.2, 0.2, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)

    def resizeGL(self, width, height):
        """Handle viewport resize"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / height
        gluPerspective(self.fov, aspect, self.near, self.far)
        glMatrixMode(GL_MODELVIEW)

    def paintGL(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Position camera
        gluLookAt(*self.camera_pos, *self.camera_target, *self.camera_up)

        # Apply transformations
        glRotatef(self.rotation[0], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[1], 0.0, 1.0, 0.0)
        glRotatef(self.rotation[2], 0.0, 0.0, 1.0)

        self.draw_grid()
        self.draw_axes()

    def draw_grid(self):
        """Draw reference grid"""
        glBegin(GL_LINES)
        glColor3f(0.3, 0.3, 0.3)
        
        grid_size = 10
        step = 1
        
        for i in range(-grid_size, grid_size + 1, step):
            glVertex3f(i, 0, -grid_size)
            glVertex3f(i, 0, grid_size)
            glVertex3f(-grid_size, 0, i)
            glVertex3f(grid_size, 0, i)
            
        glEnd()

    def draw_axes(self):
        """Draw coordinate axes"""
        glBegin(GL_LINES)
        # X axis (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(1, 0, 0)
        # Y axis (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1, 0)
        # Z axis (blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1)
        glEnd()

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        self.last_pos = event.pos()
        if event.button() == Qt.MouseButton.LeftButton:
            self.rotating = True
        elif event.button() == Qt.MouseButton.RightButton:
            self.panning = True

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.rotating = False
        elif event.button() == Qt.MouseButton.RightButton:
            self.panning = False

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events"""
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        if self.rotating:
            self.rotation[1] += dx * self.rotation_speed
            self.rotation[0] += dy * self.rotation_speed
            self.update()
        elif self.panning:
            right = np.cross(self.camera_target - self.camera_pos, self.camera_up)
            right = right / np.linalg.norm(right)
            up = np.cross(right, self.camera_target - self.camera_pos)
            up = up / np.linalg.norm(up)
            
            self.camera_pos += (-right * dx + up * dy) * self.pan_speed
            self.camera_target += (-right * dx + up * dy) * self.pan_speed
            self.update()

        self.last_pos = event.pos()

    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel events for zooming"""
        delta = event.angleDelta().y()
        forward = self.camera_target - self.camera_pos
        forward = forward / np.linalg.norm(forward)
        
        self.camera_pos += forward * delta * self.zoom_speed
        self.update()
