# VisionCube: A Rubik's Cube Solver

VisionCube is a program that helps users solve a Rubik's cube by scanning all sides of the cube and producing a solution algorithm for it.

![alt text](img/visioncube.png)

<br>

## How it works

---

### Cube Face Detection

In order to get an accurate boundary as to where the current cube face lies within the frame, I utilised a mix of thresholding and countouring. Thresholding allowed me to get rid isolate the cube from it's surroundings (given its dark edges) which immensely helped with detecting clean contours. And finally, by getting the location of the largest contour detected, I would be sure that it's the one that holds the cube's whole face. Indicated by green bounding box on the UI.

### Color Extraction
