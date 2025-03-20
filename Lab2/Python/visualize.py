from vpython import *

scene = canvas()

# Create a 3D box to represent an object
box_object = box(color=color.red)

# Simulate gyroscope rotation
while True:
    rate(50)  # Control speed
    box_object.rotate(angle=0.01, axis=vector(1, 0, 0))  # Example rotation