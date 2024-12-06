"""
Main entry point for Mystic Scape application
"""

import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from mysticscape.ui.simple_splash import show_splash_screen
from mysticscape.ui.main_window import MainWindow

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    """Main application entry point"""
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        app = QApplication(sys.argv)
        
        # Show splash screen
        splash = show_splash_screen()
        
        # Create main window
        window = MainWindow()
        
        # Show main window when ready
        def show_main():
            window.show()
            splash.finish(window)
        
        QTimer.singleShot(3000, show_main)
        
        return app.exec()

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
