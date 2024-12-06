"""
Blender-style splash screen with FBX mascot
"""
import sys
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QSplashScreen, QProgressBar, 
                           QVBoxLayout, QWidget, QLabel)
from .fbx_mascot_viewer import FBXMascotViewer

class BlenderSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the splash screen UI"""
        # Main widget
        self.content = QWidget(self)
        self.layout = QVBoxLayout(self.content)
        
        # Studio name
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
        
        # Add mascot viewer
        self.mascot = FBXMascotViewer(self)
        self.mascot.setFixedSize(300, 300)
        self.layout.addWidget(self.mascot, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Software name
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
        
        # Version
        self.version = QLabel("Version 1.0.0", self)
        self.version.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        self.layout.addWidget(self.version, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Progress bar
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
        
        # Status
        self.status = QLabel("Starting...", self)
        self.status.setStyleSheet("color: #aaaaaa; font-size: 12px;")
        self.layout.addWidget(self.status, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Window settings
        self.setFixedSize(600, 500)
        self.setStyleSheet("background-color: #232323;")
        
    def update_progress(self, value, message=""):
        """Update progress bar and status"""
        self.progress.setValue(value)
        if message:
            self.status.setText(message)
        QApplication.processEvents()

def show_splash():
    """Create and show splash screen"""
    splash = BlenderSplash()
    splash.show()
    
    # Loading steps
    def update_progress():
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
    
    QTimer.singleShot(0, update_progress)
    return splash

if __name__ == "__main__":
    # Test the splash screen
    app = QApplication(sys.argv)
    splash = show_splash()
    QTimer.singleShot(3000, app.quit)
    sys.exit(app.exec())
