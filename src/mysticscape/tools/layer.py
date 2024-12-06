"""
Layer management system for 2D workspace
"""

from PyQt6.QtGui import QImage, QPainter, QColor
from PyQt6.QtCore import Qt
from dataclasses import dataclass
from typing import Optional
import uuid

@dataclass
class LayerProperties:
    opacity: float = 1.0
    visible: bool = True
    locked: bool = False
    blend_mode: str = "normal"

class Layer:
    def __init__(self, width: int, height: int, name: Optional[str] = None):
        self.id = str(uuid.uuid4())
        self.name = name or f"Layer {self.id[:8]}"
        self.image = QImage(width, height, QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.transparent)
        self.properties = LayerProperties()
        self.thumbnail = None
        self.update_thumbnail()

    def resize(self, width: int, height: int):
        """Resize the layer"""
        new_image = QImage(width, height, QImage.Format.Format_ARGB32)
        new_image.fill(Qt.GlobalColor.transparent)
        painter = QPainter(new_image)
        painter.drawImage(0, 0, self.image)
        painter.end()
        self.image = new_image
        self.update_thumbnail()

    def update_thumbnail(self, size: int = 64):
        """Update layer thumbnail"""
        self.thumbnail = self.image.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio)

    def clear(self):
        """Clear the layer"""
        self.image.fill(Qt.GlobalColor.transparent)
        self.update_thumbnail()

    def merge_down(self, bottom_layer: 'Layer') -> 'Layer':
        """Merge with the layer below"""
        merged = Layer(self.image.width(), self.image.height())
        painter = QPainter(merged.image)
        
        # Draw bottom layer
        if bottom_layer.properties.visible:
            painter.setOpacity(bottom_layer.properties.opacity)
            painter.drawImage(0, 0, bottom_layer.image)
        
        # Draw this layer
        if self.properties.visible:
            painter.setOpacity(self.properties.opacity)
            painter.drawImage(0, 0, self.image)
        
        painter.end()
        merged.update_thumbnail()
        return merged

class LayerStack:
    def __init__(self):
        self.layers = []
        self.active_layer_index = -1

    def add_layer(self, layer: Layer) -> int:
        """Add a new layer and return its index"""
        self.layers.append(layer)
        if self.active_layer_index == -1:
            self.active_layer_index = 0
        return len(self.layers) - 1

    def remove_layer(self, index: int):
        """Remove layer at specified index"""
        if 0 <= index < len(self.layers):
            self.layers.pop(index)
            if self.active_layer_index >= len(self.layers):
                self.active_layer_index = len(self.layers) - 1

    def move_layer(self, from_index: int, to_index: int):
        """Move layer from one position to another"""
        if 0 <= from_index < len(self.layers) and 0 <= to_index < len(self.layers):
            layer = self.layers.pop(from_index)
            self.layers.insert(to_index, layer)

    def merge_visible(self) -> Layer:
        """Merge all visible layers"""
        if not self.layers:
            return None

        merged = Layer(self.layers[0].image.width(), self.layers[0].image.height())
        painter = QPainter(merged.image)

        for layer in self.layers:
            if layer.properties.visible:
                painter.setOpacity(layer.properties.opacity)
                painter.drawImage(0, 0, layer.image)

        painter.end()
        merged.update_thumbnail()
        return merged

    def get_active_layer(self) -> Optional[Layer]:
        """Get the currently active layer"""
        if 0 <= self.active_layer_index < len(self.layers):
            return self.layers[self.active_layer_index]
        return None

    def set_active_layer(self, index: int):
        """Set the active layer"""
        if 0 <= index < len(self.layers):
            self.active_layer_index = index

    def duplicate_layer(self, index: int) -> int:
        """Duplicate a layer and return new index"""
        if 0 <= index < len(self.layers):
            layer = self.layers[index]
            new_layer = Layer(layer.image.width(), layer.image.height())
            painter = QPainter(new_layer.image)
            painter.drawImage(0, 0, layer.image)
            painter.end()
            new_layer.properties = LayerProperties(**layer.properties.__dict__)
            new_layer.name = f"Copy of {layer.name}"
            return self.add_layer(new_layer)
        return -1
