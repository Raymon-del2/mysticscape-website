"""
Splash screen and mascot system for Mystic Scape
"""

import os
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QMovie
from PyQt6.QtWidgets import QSplashScreen, QApplication, QProgressBar, QVBoxLayout, QWidget

class MysticScapeSplash(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | 
                          Qt.WindowType.FramelessWindowHint)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the splash screen UI"""
        # Create main widget and layout
        content = QWidget(self)
        layout = QVBoxLayout(content)
        
        # Load splash image
        splash_path = Path(__file__).parent / "resources" / "splash.png"
        if splash_path.exists():
            pixmap = QPixmap(str(splash_path))
            self.setPixmap(pixmap)
        
        # Add progress bar
        self.progress = QProgressBar(self)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 0.5px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Load mascot
        self.setup_mascot()
        
    def setup_mascot(self):
        """Load and display the 3D mascot"""
        mascot_path = Path(__file__).parent / "resources" / "mascot.fbx"
        if mascot_path.exists():
            # TODO: Implement 3D mascot loading and animation
            # This will require integration with a 3D viewer widget
            pass
            
    def progress_value(self, value):
        """Update progress bar value"""
        self.progress.setValue(value)
        QApplication.processEvents()
        
    def show_message(self, message):
        """Show status message"""
        self.showMessage(message, Qt.AlignmentFlag.AlignBottom | 
                        Qt.AlignmentFlag.AlignCenter, Qt.GlobalColor.white)
        
    def finish(self, window):
        """Finish splash screen with fade effect"""
        self.progress_value(100)
        QTimer.singleShot(500, lambda: super().finish(window))

class ResourceManager:
    """Manage application resources including splash screen and mascot"""
    
    def __init__(self):
        self.resource_dir = Path(__file__).parent / "resources"
        self.resource_dir.mkdir(exist_ok=True)
        
    def set_splash_image(self, image_path: str):
        """Set custom splash screen image"""
        target = self.resource_dir / "splash.png"
        try:
            import shutil
            shutil.copy2(image_path, target)
            return True
        except Exception as e:
            print(f"Failed to set splash image: {e}")
            return False
            
    def set_mascot_model(self, fbx_path: str):
        """Set custom 3D mascot model"""
        target = self.resource_dir / "mascot.fbx"
        try:
            import shutil
            shutil.copy2(fbx_path, target)
            return True
        except Exception as e:
            print(f"Failed to set mascot model: {e}")
            return False
