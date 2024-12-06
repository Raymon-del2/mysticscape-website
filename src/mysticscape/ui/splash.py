"""
Enhanced splash screen with 3D mascot support for Mystic Scape
"""

import os
import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap, QMovie, QPainter, QColor, QFont
from PyQt6.QtWidgets import (QSplashScreen, QApplication, QProgressBar, 
                           QVBoxLayout, QWidget, QLabel, QOpenGLWidget)
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import trimesh

class MascotViewer(QOpenGLWidget):
    """OpenGL widget for displaying 3D mascot"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh = None
        self.rotation = 0
        
        # Start rotation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)  # 20 FPS
        
    def load_mascot(self, fbx_path):
        """Load mascot FBX model"""
        try:
            self.mesh = trimesh.load(fbx_path)
            self.update()
            return True
        except Exception as e:
            print(f"Failed to load mascot: {e}")
            return False
            
    def rotate(self):
        """Rotate mascot model"""
        self.rotation += 2
        self.update()
        
    def initializeGL(self):
        """Initialize OpenGL"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 1, 0])
        
    def resizeGL(self, w, h):
        """Handle widget resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100.0)
        
    def paintGL(self):
        """Render mascot"""
        if not self.mesh:
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(0, 0, -5)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Render mesh
        glBegin(GL_TRIANGLES)
        for face in self.mesh.faces:
            for vertex_index in face:
                vertex = self.mesh.vertices[vertex_index]
                glVertex3f(*vertex)
        glEnd()

class EnhancedSplash(QSplashScreen):
    """Enhanced splash screen with 3D mascot"""
    
    finished = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the splash screen UI"""
        # Create main widget and layout
        self.content = QWidget(self)
        self.layout = QVBoxLayout(self.content)
        
        # Add title
        self.title = QLabel("Mystic Scape", self)
        self.title.setStyleSheet("""
            QLabel {
                color: #4CAF50;
                font-size: 24px;
                font-weight: bold;
            }
        """)
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add mascot viewer
        self.mascot = MascotViewer(self)
        self.mascot.setFixedSize(200, 200)
        self.layout.addWidget(self.mascot, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add progress bar
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress.setFixedWidth(300)
        self.layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add status label
        self.status = QLabel("Loading...", self)
        self.status.setStyleSheet("color: #333;")
        self.layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set fixed size
        self.setFixedSize(400, 500)
        
    def load_resources(self):
        """Load splash screen resources"""
        resources_dir = Path(__file__).parent / "resources"
        
        # Load mascot
        mascot_path = resources_dir / "mascot" / "mascot.fbx"
        if mascot_path.exists():
            self.mascot.load_mascot(str(mascot_path))
            
    def update_progress(self, value, message=""):
        """Update progress bar and status message"""
        self.progress.setValue(value)
        if message:
            self.status.setText(message)
        QApplication.processEvents()
        
    def finish(self, window):
        """Finish splash screen with fade effect"""
        self.finished.emit()
        super().finish(window)

def create_splash_screen():
    """Create and configure splash screen"""
    splash = EnhancedSplash()
    splash.load_resources()
    
    # Demo progress updates
    def simulate_loading():
        steps = [
            (10, "Loading core engine..."),
            (30, "Initializing 3D viewport..."),
            (50, "Loading plugins..."),
            (70, "Setting up workspace..."),
            (90, "Preparing UI..."),
            (100, "Ready!")
        ]
        
        for progress, message in steps:
            QTimer.singleShot(progress * 50, 
                            lambda p=progress, m=message: splash.update_progress(p, m))
    
    QTimer.singleShot(0, simulate_loading)
    return splash

if __name__ == "__main__":
    # Demo usage
    app = QApplication(sys.argv)
    splash = create_splash_screen()
    splash.show()
    
    # Simulate main window
    QTimer.singleShot(5000, app.quit)
    sys.exit(app.exec())
