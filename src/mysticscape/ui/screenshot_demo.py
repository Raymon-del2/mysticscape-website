import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mysticscape")
        self.setGeometry(100, 100, 1200, 800)
        
        # Dark theme
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QLabel { color: white; font-size: 24px; }
        """)
        
        # Main widget
        main = QWidget()
        self.setCentralWidget(main)
        layout = QVBoxLayout(main)
        
        # Add demo content
        title = QLabel("Mysticscape 3D Creative Suite")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

def take_screenshot():
    app = QApplication(sys.argv)
    window = DemoWindow()
    window.show()
    
    # Take screenshot after window is shown
    def capture():
        screen = QScreen.grabWindow(app.primaryScreen(), window.winId())
        screen.save("screenshot.png")
        app.quit()
    
    # Wait a bit for window to render before capturing
    app.processEvents()
    capture()
    
    app.exec()

if __name__ == "__main__":
    take_screenshot()
