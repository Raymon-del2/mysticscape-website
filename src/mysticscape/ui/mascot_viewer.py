"""
FBX Mascot viewer for Mystic Scape splash screen
"""

import os
from pathlib import Path
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import trimesh

class MascotViewer(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh = None
        self.rotation = 0
        
        # Setup animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS
        
        # Load the mascot
        self.load_mascot()
        
    def load_mascot(self):
        """Load Leo.fbx model"""
        try:
            # Get path to Leo.fbx
            mascot_path = Path(__file__).parent / "resources" / "mascot" / "Leo.fbx"
            print(f"Loading mascot from: {mascot_path}")
            
            # Load the mesh using trimesh
            self.mesh = trimesh.load(str(mascot_path))
            
            # Center and scale the mesh
            self.mesh.vertices -= self.mesh.center_mass
            scale = 2.0 / self.mesh.scale
            self.mesh.vertices *= scale
            
            print("Successfully loaded Leo mascot!")
            return True
        except Exception as e:
            print(f"Failed to load mascot: {e}")
            return False
            
    def initializeGL(self):
        """Initialize OpenGL with proper lighting"""
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        
        # Set light properties
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        
        # Set material properties
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        
        # Set background color to match splash screen
        glClearColor(0.137, 0.137, 0.137, 1.0)
        
    def resizeGL(self, w, h):
        """Handle window resize"""
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w/h, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        
    def paintGL(self):
        """Render the mascot"""
        if not self.mesh:
            return
            
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Position camera
        glTranslatef(0, 0, -5)
        
        # Apply rotation
        glRotatef(self.rotation, 0, 1, 0)
        
        # Render mesh
        glColor3f(1.0, 1.0, 1.0)  # White base color for lighting
        glBegin(GL_TRIANGLES)
        
        # Draw each face with proper normals
        for face in self.mesh.faces:
            vertices = self.mesh.vertices[face]
            # Calculate face normal
            normal = np.cross(vertices[1] - vertices[0], 
                            vertices[2] - vertices[0])
            normal = normal / np.linalg.norm(normal)
            
            # Set normal and draw vertices
            glNormal3fv(normal)
            for vertex in vertices:
                glVertex3fv(vertex)
                
        glEnd()
        
    def animate(self):
        """Update rotation animation"""
        self.rotation += 1
        if self.rotation >= 360:
            self.rotation = 0
        self.update()
