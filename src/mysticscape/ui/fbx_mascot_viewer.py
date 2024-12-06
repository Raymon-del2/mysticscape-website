"""
FBX Mascot viewer for Mystic Scape
"""
import os
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import trimesh

class FBXMascotViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh = None
        self.rotation = 0
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # 60 FPS
        
    def load_mascot(self):
        """Load the Leo.fbx mascot"""
        try:
            mascot_path = Path(__file__).parent / "resources" / "mascot" / "Leo.fbx"
            print(f"Loading mascot from: {mascot_path}")
            
            self.mesh = trimesh.load(str(mascot_path))
            
            # Center and normalize size
            self.mesh.vertices -= self.mesh.center_mass
            scale = 2.0 / self.mesh.scale
            self.mesh.vertices *= scale
            
            print("Successfully loaded Leo mascot!")
            self.update()
            return True
        except Exception as e:
            print(f"Failed to load mascot: {e}")
            return False
    
    def initializeGL(self):
        """Initialize OpenGL"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set light
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        
        # Load the mascot
        self.load_mascot()
        
    def resizeGL(self, w, h):
        """Handle resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100.0)
        
    def paintGL(self):
        """Render the mascot"""
        if not self.mesh:
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Position and rotate
        glTranslatef(0, 0, -5)
        glRotatef(self.rotation, 0, 1, 0)
        
        # Draw mesh
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_TRIANGLES)
        for face in self.mesh.faces:
            for vertex_id in face:
                glVertex3fv(self.mesh.vertices[vertex_id])
        glEnd()
        
    def animate(self):
        """Rotate the mascot"""
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
        self.update()
