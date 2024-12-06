"""
Simple Blender-style splash screen for Mystic Scape with Leo mascot
"""

import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QPainter
from PyQt6.QtWidgets import (QApplication, QSplashScreen, QProgressBar, 
                           QVBoxLayout, QWidget, QLabel, QOpenGLWidget)
from OpenGL.GL import *
from OpenGL.GLU import *
from .mascot.leo_model import LeoMascotViewer

class MascotWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mascot_viewer = None
        self.last_time = 0
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
    def initializeGL(self):
        """Initialize OpenGL and mascot"""
        self.mascot_viewer = LeoMascotViewer()
        glClearColor(0.137, 0.137, 0.137, 1.0)  # Match splash background
        
    def resizeGL(self, w, h):
        """Handle resize"""
        if self.mascot_viewer:
            self.mascot_viewer.resize(w, h)
            
    def paintGL(self):
        """Render mascot"""
        if self.mascot_viewer:
            self.mascot_viewer.render()
            
    def animate(self):
        """Update animation"""
        if self.mascot_viewer:
            current_time = QTimer.currentTime().msecsSinceStartOfDay() / 1000.0
            if self.last_time == 0:
                self.last_time = current_time
            dt = current_time - self.last_time
            self.last_time = current_time
            
            self.mascot_viewer.update(dt)
            self.update()

class SimpleSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup simple Blender-style UI"""
        # Main widget
        self.content = QWidget(self)
        self.layout = QVBoxLayout(self.content)
        
        # Add studio name
        self.studio = QLabel("Lucid Realms Studios", self)
        self.studio.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        self.layout.addWidget(self.studio, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add Leo mascot
        self.mascot = MascotWidget(self)
        self.mascot.setFixedSize(200, 200)
        self.layout.addWidget(self.mascot, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add software name
        self.title = QLabel("MYSTIC SCAPE", self)
        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 36px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        self.layout.addWidget(self.title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add version
        self.version = QLabel("Version 1.0.0", self)
        self.version.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        self.layout.addWidget(self.version, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add progress bar
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1px solid #555555;
                border-radius: 2px;
                text-align: center;
                height: 10px;
                background-color: #2a2a2a;
                color: #ffffff;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.progress.setFixedWidth(300)
        self.layout.addWidget(self.progress, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Add status label
        self.status = QLabel("Starting...", self)
        self.status.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        self.layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set window size and style
        self.setFixedSize(500, 400)  # Made taller for mascot
        self.setStyleSheet("background-color: #232323;")
        
    def update_progress(self, value, message=""):
        """Update progress bar and status message"""
        self.progress.setValue(value)
        if message:
            self.status.setText(message)
        QApplication.processEvents()

def show_splash_screen():
    """Create and show splash screen"""
    splash = SimpleSplash()
    splash.show()
    
    # Loading steps
    def update_splash():
        steps = [
            (10, "Loading core engine..."),
            (30, "Setting up workspace..."),
            (50, "Loading plugins..."),
            (70, "Preparing 3D viewport..."),
            (90, "Initializing UI..."),
            (100, "Ready!")
        ]
        
        for progress, message in steps:
            QTimer.singleShot(progress * 30, 
                            lambda p=progress, m=message: splash.update_progress(p, m))
    
    QTimer.singleShot(0, update_splash)
    return splash

if __name__ == "__main__":
    # Test the splash screen
    app = QApplication(sys.argv)
    splash = show_splash_screen()
    
    # Simulate delay
    QTimer.singleShot(3000, app.quit)
    sys.exit(app.exec())
