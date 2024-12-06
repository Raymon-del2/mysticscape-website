import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QMenuBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen

class ScreenshotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mysticscape")
        self.resize(1200, 800)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #2b2b2b;
            }
            QLabel {
                color: white;
                font-size: 24px;
            }
            QMenuBar {
                background-color: #1e1e1e;
                color: white;
            }
        """)
        
        # Menu bar
        menubar = self.menuBar()
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Render")
        menubar.addMenu("Help")
        
        # Main widget
        main = QWidget()
        self.setCentralWidget(main)
        layout = QVBoxLayout(main)
        
        # Title
        title = QLabel("Welcome to Mysticscape")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Professional 3D Creative Suite")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px; color: #aaaaaa;")
        layout.addWidget(subtitle)

def take_screenshot():
    app = QApplication(sys.argv)
    window = ScreenshotWindow()
    window.show()
    
    # Take screenshot
    def capture():
        screen = QScreen.grabWindow(app.primaryScreen(), window.winId())
        screen.save("mysticscape_screenshot.png")
        app.quit()
    
    # Wait for window to render
    app.processEvents()
    capture()
    
    app.exec()

if __name__ == "__main__":
    take_screenshot()
