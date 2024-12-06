"""
Advanced Blender-style splash screen with 3D mascot for Mystic Scape
"""

import os
import sys
from pathlib import Path
from typing import Optional
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QPoint
from PyQt6.QtGui import (QPixmap, QMovie, QPainter, QColor, QFont, 
                        QLinearGradient, QPainterPath)
from PyQt6.QtWidgets import (QSplashScreen, QApplication, QProgressBar, 
                           QVBoxLayout, QWidget, QLabel, QOpenGLWidget)
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import trimesh
from PIL import Image, ImageDraw, ImageFont

class BlenderStyleMascot(QOpenGLWidget):
    """OpenGL widget for displaying 3D mascot with Blender-style rendering"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh: Optional[trimesh.Trimesh] = None
        self.rotation = 0
        self.light_position = [5.0, 5.0, 10.0, 1.0]
        self.material_ambient = [0.2, 0.2, 0.2, 1.0]
        self.material_diffuse = [0.8, 0.8, 0.8, 1.0]
        self.material_specular = [1.0, 1.0, 1.0, 1.0]
        self.material_shininess = 50.0
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
    def load_mascot(self, fbx_path: str) -> bool:
        """Load mascot FBX model with textures"""
        try:
            # Load mesh with texture coordinates
            self.mesh = trimesh.load(fbx_path)
            
            # Normalize mesh size and center it
            self.mesh.vertices -= self.mesh.center_mass
            scale = 2.0 / self.mesh.scale
            self.mesh.vertices *= scale
            
            self.update()
            return True
        except Exception as e:
            print(f"Failed to load mascot: {e}")
            return False
            
    def animate(self):
        """Animate mascot with smooth rotation"""
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
        self.update()
        
    def initializeGL(self):
        """Initialize OpenGL with Blender-style lighting"""
        glClearColor(0.05, 0.05, 0.05, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        # Set light properties
        glLightfv(GL_LIGHT0, GL_POSITION, self.light_position)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
    def resizeGL(self, w: int, h: int):
        """Handle widget resize with proper aspect ratio"""
        aspect = w / h if h > 0 else 1
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, aspect, 0.1, 100.0)
        
    def paintGL(self):
        """Render mascot with Blender-style materials"""
        if not self.mesh:
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Position camera
        glTranslatef(0, 0, -5)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Set material properties
        glMaterialfv(GL_FRONT, GL_AMBIENT, self.material_ambient)
        glMaterialfv(GL_FRONT, GL_DIFFUSE, self.material_diffuse)
        glMaterialfv(GL_FRONT, GL_SPECULAR, self.material_specular)
        glMaterialf(GL_FRONT, GL_SHININESS, self.material_shininess)
        
        # Render mesh with smooth shading
        glEnable(GL_SMOOTH)
        glBegin(GL_TRIANGLES)
        for face in self.mesh.faces:
            # Calculate face normal for lighting
            vertices = self.mesh.vertices[face]
            normal = np.cross(vertices[1] - vertices[0], 
                            vertices[2] - vertices[0])
            normal = normal / np.linalg.norm(normal)
            
            for vertex_index in face:
                glNormal3fv(normal)
                glVertex3fv(self.mesh.vertices[vertex_index])
        glEnd()

class BlenderStyleSplash(QSplashScreen):
    """Blender-style splash screen with 3D mascot"""
    
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the Blender-style UI"""
        # Create main widget and layout
        self.content = QWidget(self)
        self.layout = QVBoxLayout(self.content)
        
        # Add Mystic Scape title
        self.title = QLabel("MYSTIC SCAPE", self)
        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 32px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add version info
        self.version = QLabel("v1.0.0 | Lucid Realms Studios", self)
        self.version.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        self.layout.addWidget(self.version, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add mascot viewer
        self.mascot = BlenderStyleMascot(self)
        self.mascot.setFixedSize(400, 300)
        self.layout.addWidget(self.mascot, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add progress bar
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 3px;
                text-align: center;
                height: 20px;
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 5px;
                margin: 0.5px;
            }
        """)
        self.progress.setFixedWidth(400)
        self.layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add status label
        self.status = QLabel("Loading...", self)
        self.status.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        self.layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set window size and style
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #232323;")
        
    def load_resources(self):
        """Load splash screen resources"""
        resources_dir = Path(__file__).parent / "resources"
        
        # Load mascot
        mascot_path = resources_dir / "mascot" / "mascot.fbx"
        if mascot_path.exists():
            self.mascot.load_mascot(str(mascot_path))
            
    def update_progress(self, value: int, message: str = ""):
        """Update progress bar and status message"""
        self.progress.setValue(value)
        if message:
            self.status.setText(message)
        QApplication.processEvents()
        
    def mousePressEvent(self, event):
        """Handle mouse press for dragging"""
        self.dragPos = event.globalPosition().toPoint()
        
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if hasattr(self, 'dragPos'):
            newPos = event.globalPosition().toPoint()
            self.move(self.pos() + newPos - self.dragPos)
            self.dragPos = newPos
            
    def finish(self, window):
        """Finish splash screen with fade effect"""
        self.finished.emit()
        
        # Create fade out animation
        for i in range(100, -1, -5):
            self.setWindowOpacity(i / 100.0)
            QApplication.processEvents()
            QTimer.singleShot(5, lambda: None)
        
        super().finish(window)

def create_splash_screen():
    """Create and configure Blender-style splash screen"""
    splash = BlenderStyleSplash()
    splash.load_resources()
    
    # Configure loading steps
    steps = [
        (10, "Loading core engine..."),
        (20, "Initializing render engines..."),
        (35, "Loading plugins..."),
        (50, "Setting up workspace..."),
        (65, "Initializing OpenUSD..."),
        (80, "Loading user preferences..."),
        (90, "Preparing UI..."),
        (100, "Ready to create!")
    ]
    
    # Simulate loading with realistic delays
    for progress, message in steps:
        QTimer.singleShot(progress * 30, 
                        lambda p=progress, m=message: splash.update_progress(p, m))
    
    return splash

if __name__ == "__main__":
    # Demo usage
    app = QApplication(sys.argv)
    
    # Create and show splash screen
    splash = create_splash_screen()
    splash.show()
    
    # Simulate main window delay
    QTimer.singleShot(5000, app.quit)
    sys.exit(app.exec())
