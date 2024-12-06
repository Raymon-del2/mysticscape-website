"""
Main window implementation for Mystic Scape
"""

from PyQt6.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget, 
                           QVBoxLayout, QToolBar, QStatusBar, QDockWidget,
                           QPushButton, QMessageBox, QStackedWidget, QColorDialog,
                           QSpinBox, QComboBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QColor
from datetime import datetime, timedelta

from mysticscape.tools.paint2d import Canvas2D
from mysticscape.tools.viewport3d import Viewport3D
from mysticscape.tools.layer import Layer, LayerStack
from mysticscape.tools.navigation3d import Navigation3D, NavigationMode
from mysticscape.ui.hybrid_view import HybridView
from mysticscape.core.engine import WorkspaceMode

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mystic Scape")
        self.trial_end_date = None
        self.current_mode = WorkspaceMode.MODE_3D
        self.layer_stack = LayerStack()
        self.navigation = Navigation3D()
        self.setup_ui()
        self.show_splash_screen()
        self.check_license()

    def setup_ui(self):
        """Initialize the main window UI"""
        self.setMinimumSize(1200, 800)
        self.setGeometry(100, 100, 1200, 800)

        # Create central stacked widget
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Create workspaces
        self.canvas_2d = Canvas2D()
        self.viewport_3d = Viewport3D()
        self.hybrid_view = HybridView()
        
        # Add workspaces to stack
        self.stack.addWidget(self.viewport_3d)  # Index 0
        self.stack.addWidget(self.canvas_2d)    # Index 1
        self.stack.addWidget(self.hybrid_view)  # Index 2

        self.setup_toolbar()
        self.setup_status_bar()
        self.setup_dock_widgets()

    def setup_toolbar(self):
        """Setup the main toolbar"""
        # Main toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Mode switching
        self.action_3d = QAction("3D Mode", self)
        self.action_2d = QAction("2D Mode", self)
        self.action_hybrid = QAction("Hybrid Mode", self)
        toolbar.addActions([self.action_3d, self.action_2d, self.action_hybrid])
        toolbar.addSeparator()

        # 2D tools
        self.setup_2d_tools(toolbar)
        toolbar.addSeparator()

        # 3D tools
        self.setup_3d_tools(toolbar)
        toolbar.addSeparator()

        # Layer tools
        self.setup_layer_tools(toolbar)

        # Connect actions
        self.connect_actions()

    def setup_2d_tools(self, toolbar):
        """Setup 2D editing tools"""
        self.action_brush = QAction("Brush", self)
        self.action_eraser = QAction("Eraser", self)
        self.action_color = QAction("Color", self)
        self.action_clear = QAction("Clear", self)
        
        # Brush size control
        self.brush_size = QSpinBox()
        self.brush_size.setRange(1, 100)
        self.brush_size.setValue(5)
        
        toolbar.addAction(self.action_brush)
        toolbar.addAction(self.action_eraser)
        toolbar.addAction(self.action_color)
        toolbar.addAction(self.action_clear)
        toolbar.addWidget(self.brush_size)

    def setup_3d_tools(self, toolbar):
        """Setup 3D navigation tools"""
        self.nav_mode = QComboBox()
        self.nav_mode.addItems([mode.value for mode in NavigationMode])
        
        self.camera_preset = QComboBox()
        self.camera_preset.addItems(["Perspective", "Front", "Top", "Right"])
        
        toolbar.addWidget(QLabel("Navigation:"))
        toolbar.addWidget(self.nav_mode)
        toolbar.addWidget(QLabel("Camera:"))
        toolbar.addWidget(self.camera_preset)

    def setup_layer_tools(self, toolbar):
        """Setup layer management tools"""
        self.action_new_layer = QAction("New Layer", self)
        self.action_delete_layer = QAction("Delete Layer", self)
        self.action_merge_layers = QAction("Merge Layers", self)
        
        toolbar.addAction(self.action_new_layer)
        toolbar.addAction(self.action_delete_layer)
        toolbar.addAction(self.action_merge_layers)

    def setup_status_bar(self):
        """Setup enhanced status bar"""
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        # Add permanent widgets
        self.mode_label = QLabel()
        self.coords_label = QLabel()
        self.license_label = QLabel()
        
        self.statusBar.addPermanentWidget(self.mode_label)
        self.statusBar.addPermanentWidget(self.coords_label)
        self.statusBar.addPermanentWidget(self.license_label)

    def setup_dock_widgets(self):
        """Setup enhanced dock widgets"""
        # Tools dock
        self.tools_dock = QDockWidget("Tools", self)
        self.tools_dock.setAllowedAreas(Qt.DockWidgetArea.LeftDockWidgetArea | 
                                      Qt.DockWidgetArea.RightDockWidgetArea)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.tools_dock)

        # Layers dock
        self.layers_dock = QDockWidget("Layers", self)
        self.layers_list = QListWidget()
        self.layers_dock.setWidget(self.layers_list)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.layers_dock)

        # Properties dock
        self.props_dock = QDockWidget("Properties", self)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.props_dock)

    def connect_actions(self):
        """Connect all action signals"""
        # Mode switching
        self.action_3d.triggered.connect(lambda: self.switch_mode(WorkspaceMode.MODE_3D))
        self.action_2d.triggered.connect(lambda: self.switch_mode(WorkspaceMode.MODE_2D))
        self.action_hybrid.triggered.connect(lambda: self.switch_mode(WorkspaceMode.MODE_HYBRID))
        
        # 2D tools
        self.action_brush.triggered.connect(self.activate_brush)
        self.action_eraser.triggered.connect(self.activate_eraser)
        self.action_color.triggered.connect(self.choose_color)
        self.action_clear.triggered.connect(self.clear_canvas)
        self.brush_size.valueChanged.connect(self.update_brush_size)
        
        # 3D navigation
        self.nav_mode.currentTextChanged.connect(self.change_navigation_mode)
        self.camera_preset.currentTextChanged.connect(self.change_camera_preset)
        
        # Layer management
        self.action_new_layer.triggered.connect(self.add_new_layer)
        self.action_delete_layer.triggered.connect(self.delete_active_layer)
        self.action_merge_layers.triggered.connect(self.merge_selected_layers)
        self.layers_list.itemClicked.connect(self.change_active_layer)

    def switch_mode(self, mode):
        """Enhanced mode switching"""
        self.current_mode = mode
        if mode == WorkspaceMode.MODE_3D:
            self.stack.setCurrentIndex(0)
            self.mode_label.setText("3D Mode")
            self.update_3d_tools_visibility(True)
            self.update_2d_tools_visibility(False)
        elif mode == WorkspaceMode.MODE_2D:
            self.stack.setCurrentIndex(1)
            self.mode_label.setText("2D Mode")
            self.update_3d_tools_visibility(False)
            self.update_2d_tools_visibility(True)
        else:  # Hybrid mode
            self.stack.setCurrentIndex(2)
            self.mode_label.setText("Hybrid Mode")
            self.update_3d_tools_visibility(True)
            self.update_2d_tools_visibility(True)

    def update_2d_tools_visibility(self, visible):
        """Update 2D tool visibility"""
        self.action_brush.setVisible(visible)
        self.action_eraser.setVisible(visible)
        self.action_color.setVisible(visible)
        self.action_clear.setVisible(visible)
        self.brush_size.setVisible(visible)

    def update_3d_tools_visibility(self, visible):
        """Update 3D tool visibility"""
        self.nav_mode.setVisible(visible)
        self.camera_preset.setVisible(visible)

    # Layer management methods
    def add_new_layer(self):
        """Add a new layer"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            layer = Layer(self.canvas_2d.width(), self.canvas_2d.height())
            index = self.layer_stack.add_layer(layer)
            self.update_layer_list()
            self.layer_stack.set_active_layer(index)

    def delete_active_layer(self):
        """Delete the active layer"""
        if self.layer_stack.active_layer_index >= 0:
            self.layer_stack.remove_layer(self.layer_stack.active_layer_index)
            self.update_layer_list()

    def merge_selected_layers(self):
        """Merge selected layers"""
        selected_items = self.layers_list.selectedItems()
        if len(selected_items) > 1:
            indices = [self.layers_list.row(item) for item in selected_items]
            # Implement layer merging logic here
            self.update_layer_list()

    def update_layer_list(self):
        """Update the layer list widget"""
        self.layers_list.clear()
        for layer in reversed(self.layer_stack.layers):
            item = QListWidgetItem(layer.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked if layer.properties.visible 
                             else Qt.CheckState.Unchecked)
            self.layers_list.addItem(item)

    def change_active_layer(self, item):
        """Change the active layer"""
        index = self.layers_list.row(item)
        self.layer_stack.set_active_layer(len(self.layer_stack.layers) - 1 - index)

    # Navigation methods
    def change_navigation_mode(self, mode_name):
        """Change 3D navigation mode"""
        self.navigation.set_mode(NavigationMode(mode_name))

    def change_camera_preset(self, preset_name):
        """Change camera to preset view"""
        self.navigation.set_camera_preset(preset_name)
        self.viewport_3d.update()

    # Tool methods
    def activate_brush(self):
        """Activate brush tool"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            self.canvas_2d.brush.configure(size=self.brush_size.value(), 
                                         color=QColor(0, 0, 0))

    def activate_eraser(self):
        """Activate eraser tool"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            self.canvas_2d.brush.configure(size=self.brush_size.value(), 
                                         color=QColor(255, 255, 255))

    def update_brush_size(self, size):
        """Update brush size"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            self.canvas_2d.brush.configure(size=size)

    def choose_color(self):
        """Open color picker"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            color = QColorDialog.getColor()
            if color.isValid():
                self.canvas_2d.brush.configure(color=color)

    def clear_canvas(self):
        """Clear the current workspace"""
        if self.current_mode in [WorkspaceMode.MODE_2D, WorkspaceMode.MODE_HYBRID]:
            active_layer = self.layer_stack.get_active_layer()
            if active_layer:
                active_layer.clear()
                self.canvas_2d.update()

    # License and trial methods
    def show_splash_screen(self):
        """Display the splash screen"""
        splash = QMessageBox()
        splash.setWindowTitle("Welcome")
        splash.setText("Developed by Lucid Realms Studios")
        splash.setStandardButtons(QMessageBox.StandardButton.Ok)
        splash.exec()

    def check_license(self):
        """Check license status and trial period"""
        if self.is_special_user():
            self.license_label.setText("Pro License")
            return

        if not self.trial_end_date:
            self.start_trial()

        timer = QTimer(self)
        timer.timeout.connect(self.check_trial_status)
        timer.start(3600000)  # Check every hour

    def is_special_user(self):
        """Check if user has special access"""
        # TODO: Implement actual user checking
        return False

    def start_trial(self):
        """Start the trial period"""
        self.trial_end_date = datetime.now() + timedelta(days=14)
        self.license_label.setText(f"Trial Version - {14} days remaining")

    def check_trial_status(self):
        """Check remaining trial period"""
        if datetime.now() > self.trial_end_date:
            self.show_trial_expired()
        else:
            days_left = (self.trial_end_date - datetime.now()).days
            self.license_label.setText(f"Trial Version - {days_left} days remaining")
