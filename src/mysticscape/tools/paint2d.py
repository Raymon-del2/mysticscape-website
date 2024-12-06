"""
2D Painting tools and canvas implementation
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QColorDialog
from PyQt6.QtGui import QPainter, QPen, QColor, QMouseEvent, QPaintEvent, QImage
from PyQt6.QtCore import Qt, QPoint

class BrushTool:
    def __init__(self):
        self.size = 5
        self.color = QColor(0, 0, 0)
        self.opacity = 1.0
        self.pressure_sensitive = True

    def configure(self, size=None, color=None, opacity=None, pressure_sensitive=None):
        if size is not None:
            self.size = size
        if color is not None:
            self.color = color
        if opacity is not None:
            self.opacity = opacity
        if pressure_sensitive is not None:
            self.pressure_sensitive = pressure_sensitive

class Canvas2D(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.init_canvas()

    def init_ui(self):
        """Initialize the UI components"""
        self.setMinimumSize(800, 600)
        self.brush = BrushTool()
        self.last_point = None
        self.drawing = False

    def init_canvas(self):
        """Initialize the drawing canvas"""
        self.image = QImage(self.size(), QImage.Format.Format_RGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.undo_stack = []
        self.redo_stack = []

    def paintEvent(self, event: QPaintEvent):
        """Handle paint events"""
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()
            self.save_state()

    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events"""
        if self.drawing:
            painter = QPainter(self.image)
            pen = QPen()
            pen.setWidth(self.brush.size)
            pen.setColor(self.brush.color)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            
            painter.drawLine(self.last_point, event.pos())
            self.last_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def save_state(self):
        """Save current state for undo"""
        self.undo_stack.append(self.image.copy())
        self.redo_stack.clear()

    def undo(self):
        """Undo last action"""
        if self.undo_stack:
            self.redo_stack.append(self.image.copy())
            self.image = self.undo_stack.pop()
            self.update()

    def redo(self):
        """Redo last undone action"""
        if self.redo_stack:
            self.undo_stack.append(self.image.copy())
            self.image = self.redo_stack.pop()
            self.update()

    def clear(self):
        """Clear the canvas"""
        self.save_state()
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def resizeEvent(self, event):
        """Handle resize events"""
        if self.image.size() != self.size():
            new_image = QImage(self.size(), QImage.Format.Format_RGB32)
            new_image.fill(Qt.GlobalColor.white)
            painter = QPainter(new_image)
            painter.drawImage(0, 0, self.image)
            self.image = new_image
