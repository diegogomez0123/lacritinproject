# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import cv2
class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, c):
        self.shape = "unidentified"
        self.peri = cv2.arcLength(c, True)
        self.approx = cv2.approxPolyDP(c, 0.04 * self.peri, True)
    
        if len(self.approx) == 4:
            shape = "square"
        elif len(self.approx) == 3:
            shape = "triangle"
        elif len(self.approx) >= 5:
            shape = "somethingelse"
        else:
            shape = "circle"
            

