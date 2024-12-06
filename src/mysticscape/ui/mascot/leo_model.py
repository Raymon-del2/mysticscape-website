"""
Leo mascot model for Mystic Scape
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class LeoMascot:
    def __init__(self):
        self.rotation = 0
        self.create_model()
        
    def create_model(self):
        """Create Leo's geometry"""
        # Head sphere
        self.head_radius = 1.0
        
        # Mane details
        self.mane_segments = 16
        self.mane_layers = 3
        self.mane_color = (0.8, 0.6, 0.2, 1.0)  # Golden
        
        # Face details
        self.face_color = (0.9, 0.75, 0.5, 1.0)  # Light tan
        self.eye_color = (0.3, 0.6, 0.9, 1.0)    # Blue
        self.nose_color = (0.3, 0.2, 0.2, 1.0)   # Dark brown
        
    def draw_sphere(self, radius, slices, stacks):
        """Draw a sphere with given parameters"""
        quad = gluNewQuadric()
        gluSphere(quad, radius, slices, stacks)
        
    def draw_mane_segment(self, angle, layer):
        """Draw a single mane segment"""
        radius = self.head_radius * (1.2 + layer * 0.2)
        height = self.head_radius * 0.3
        
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(radius, 0, 0)
        glRotatef(90, 0, 1, 0)
        
        # Draw mane spike
        glBegin(GL_TRIANGLES)
        glVertex3f(0, height, 0)
        glVertex3f(-height/2, -height/2, 0)
        glVertex3f(height/2, -height/2, 0)
        glEnd()
        
        glPopMatrix()
        
    def draw_mane(self):
        """Draw Leo's mane"""
        glColor4f(*self.mane_color)
        
        for layer in range(self.mane_layers):
            for i in range(self.mane_segments):
                angle = (360.0 * i) / self.mane_segments
                self.draw_mane_segment(angle, layer)
                
    def draw_face(self):
        """Draw Leo's face features"""
        # Draw eyes
        glColor4f(*self.eye_color)
        glPushMatrix()
        glTranslatef(0.4, 0.3, 0.7)
        self.draw_sphere(0.15, 16, 16)
        glTranslatef(-0.8, 0, 0)
        self.draw_sphere(0.15, 16, 16)
        glPopMatrix()
        
        # Draw nose
        glColor4f(*self.nose_color)
        glPushMatrix()
        glTranslatef(0, 0, 0.9)
        self.draw_sphere(0.2, 16, 16)
        glPopMatrix()
        
    def render(self):
        """Render the Leo mascot"""
        glPushMatrix()
        
        # Apply rotation animation
        glRotatef(self.rotation, 0, 1, 0)
        
        # Draw head
        glColor4f(*self.face_color)
        self.draw_sphere(self.head_radius, 32, 32)
        
        # Draw mane
        self.draw_mane()
        
        # Draw face features
        self.draw_face()
        
        glPopMatrix()
        
    def update(self, dt):
        """Update mascot animation"""
        self.rotation += 45.0 * dt  # 45 degrees per second
        if self.rotation >= 360:
            self.rotation -= 360

class LeoMascotViewer:
    """OpenGL viewer for Leo mascot"""
    
    def __init__(self, width=400, height=400):
        self.width = width
        self.height = height
        self.leo = LeoMascot()
        self.setup_lighting()
        
    def setup_lighting(self):
        """Setup OpenGL lighting"""
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_DEPTH_TEST)
        
        # Light position and properties
        glLightfv(GL_LIGHT0, GL_POSITION, [5.0, 5.0, 5.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        
    def resize(self, width, height):
        """Handle window resize"""
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, width/height, 0.1, 100.0)
        
        glMatrixMode(GL_MODELVIEW)
        
    def render(self):
        """Render the scene"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        # Position camera
        gluLookAt(0, 0, 5,  # Camera position
                 0, 0, 0,   # Look at point
                 0, 1, 0)   # Up vector
        
        # Render Leo
        self.leo.render()
        
    def update(self, dt):
        """Update animation"""
        self.leo.update(dt)
