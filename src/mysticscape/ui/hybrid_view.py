"""
Hybrid mode implementation combining 2D and 3D views
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QSplitter, QPushButton, QToolBar)
from PyQt6.QtCore import Qt
from mysticscape.tools.paint2d import Canvas2D
from mysticscape.tools.viewport3d import Viewport3D

class HybridView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialize the hybrid view UI"""
        layout = QVBoxLayout(self)
        
        # Create splitter for 2D/3D views
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create containers for each view
        self.view_2d = QWidget()
        self.view_3d = QWidget()
        
        # Setup 2D view
        layout_2d = QVBoxLayout(self.view_2d)
        self.canvas_2d = Canvas2D()
        self.toolbar_2d = self.create_2d_toolbar()
        layout_2d.addWidget(self.toolbar_2d)
        layout_2d.addWidget(self.canvas_2d)
        
        # Setup 3D view
        layout_3d = QVBoxLayout(self.view_3d)
        self.viewport_3d = Viewport3D()
        self.toolbar_3d = self.create_3d_toolbar()
        layout_3d.addWidget(self.toolbar_3d)
        layout_3d.addWidget(self.viewport_3d)
        
        # Add views to splitter
        self.splitter.addWidget(self.view_2d)
        self.splitter.addWidget(self.view_3d)
        
        # Set initial sizes
        self.splitter.setSizes([int(self.width() * 0.5)] * 2)
        
        layout.addWidget(self.splitter)
        
        # Add sync controls
        sync_layout = QHBoxLayout()
        self.sync_button = QPushButton("Sync Views")
        self.sync_button.clicked.connect(self.sync_views)
        sync_layout.addWidget(self.sync_button)
        layout.addLayout(sync_layout)

    def create_2d_toolbar(self):
        """Create toolbar for 2D view"""
        toolbar = QToolBar()
        toolbar.addAction("Brush")
        toolbar.addAction("Eraser")
        toolbar.addAction("Color")
        toolbar.addAction("Layers")
        return toolbar

    def create_3d_toolbar(self):
        """Create toolbar for 3D view"""
        toolbar = QToolBar()
        toolbar.addAction("Orbit")
        toolbar.addAction("Pan")
        toolbar.addAction("Zoom")
        toolbar.addAction("Focus")
        return toolbar

    def sync_views(self):
        """Synchronize 2D and 3D views"""
        # TODO: Implement view synchronization
        # This could include:
        # - Using 2D view as texture in 3D
        # - Matching camera angle with 2D perspective
        # - Syncing selection between views
        pass

    def set_2d_active(self):
        """Activate 2D tools and deactivate 3D"""
        self.canvas_2d.setFocus()
        self.toolbar_2d.setEnabled(True)
        self.toolbar_3d.setEnabled(False)

    def set_3d_active(self):
        """Activate 3D tools and deactivate 2D"""
        self.viewport_3d.setFocus()
        self.toolbar_2d.setEnabled(False)
        self.toolbar_3d.setEnabled(True)

    def split_vertical(self):
        """Switch to vertical split layout"""
        self.splitter.setOrientation(Qt.Orientation.Vertical)

    def split_horizontal(self):
        """Switch to horizontal split layout"""
        self.splitter.setOrientation(Qt.Orientation.Horizontal)

    def maximize_2d(self):
        """Maximize 2D view"""
        self.splitter.setSizes([self.width(), 0])

    def maximize_3d(self):
        """Maximize 3D view"""
        self.splitter.setSizes([0, self.width()])

    def balance_views(self):
        """Balance view sizes"""
        self.splitter.setSizes([int(self.width() * 0.5)] * 2)
