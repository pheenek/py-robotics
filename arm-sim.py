import pygame
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Arm parameters (lengths of the two arm segments)
L1 = 10  # Length of first arm link
L2 = 10  # Length of second arm link

# Initialize pygame
pygame.init()

# Set up the plot
fig, ax = plt.subplots()
ax.set_xlim(-L1 - L2, L1 + L2)
ax.set_ylim(-L1 - L2, L1 + L2)
line, = ax.plot([], [], 'bo-', lw=2)  # Robot arm line
point, = ax.plot([], [], 'ro')  # End effector point

# Initial joystick (x, y) values
x_input = 0.0
y_input = 0.0

# Resolution for each key press
step_size = 0.01

# Inverse Kinematics for 2-DOF arm
def inverse_kinematics(x, y, L1, L2):
    # Solve for theta2 (second joint)
    cos_theta2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    if cos_theta2 < -1 or cos_theta2 > 1:  # Check for valid angles
        return None, None  # Invalid solution (out of reach)
    theta2 = math.acos(cos_theta2)
    
    # Solve for theta1 (first joint)
    k1 = L1 + L2 * math.cos(theta2)
    k2 = L2 * math.sin(theta2)
    theta1 = math.atan2(y, x) - math.atan2(k2, k1)
    
    # Convert radians to degrees
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)
    
    return theta1, theta2

# Function to update the arm's position
def update_frame(i):
    global x_input, y_input  # Use global variables for joystick input
    
    # Calculate the desired position (x, y) based on keyboard input
    x = x_input * (L1 + L2)
    y = y_input * (L1 + L2)
    
    # Calculate joint angles using inverse kinematics
    theta1, theta2 = inverse_kinematics(x, y, L1, L2)
    
    if theta1 is None or theta2 is None:
        # If the position is out of reach, keep the arm in the last valid position
        # return line, point
        return line

    # Calculate the position of the end effector
    x1 = L1 * math.cos(math.radians(theta1))
    y1 = L1 * math.sin(math.radians(theta1))
    x2 = x1 + L2 * math.cos(math.radians(theta1 + theta2))
    y2 = y1 + L2 * math.sin(math.radians(theta1 + theta2))

    # Update the line (robot arm)
    line.set_data([0, x1, x2], [0, y1, y2])
    # point.set_data(x2, y2)  # Update end effector position
    # return line, point
    return line,

# Main loop: Read key events and control arm
def handle_keyboard_input():
    global x_input, y_input
    
    # pygame.event.pump()
    for event in pygame.event.get():
        print(f"event: {event.type}")
        if event.type == pygame.QUIT:
            running = False
            print("quit")
        
        if event.type == pygame.KEYDOWN:
            print("key pressed")

    # Check for key events
    keys = pygame.key.get_pressed()
    # print("check keys")
    
    if keys[pygame.K_LEFT]:  # Move left (decrease x)
        x_input -= step_size
        print("left")
    if keys[pygame.K_RIGHT]:  # Move right (increase x)
        x_input += step_size
        print("right")
    if keys[pygame.K_UP]:  # Move up (increase y)
        y_input += step_size
        print("up")
    if keys[pygame.K_DOWN]:  # Move down (decrease y)
        y_input -= step_size
        print("down")
    
    # Clamp the values to prevent the arm from going out of bounds
    x_input = max(-1.0, min(1.0, x_input))
    y_input = max(-1.0, min(1.0, y_input))

# Animation function
def animate(i):
    handle_keyboard_input()  # Check for key inputs
    return update_frame(i)

# Animation setup
ani = FuncAnimation(fig, animate, frames=2000000, interval=50, blit=True)

# Show the plot
plt.show()

# Close pygame when done
pygame.quit()
