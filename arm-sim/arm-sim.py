import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Arm parameters (lengths of the two arm segments)
L1 = 10  # Length of first arm link
L2 = 10  # Length of second arm link

# Initialize pygame

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
    # TODO: Limit the angle to a maximum and minimum (avoid collisions and overstretching)
    # TODO: Limit the x and y input values so that they're strictly confined to a maximum and minimum (eliminate delays in motion when the stretch limit has been reached)
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
        return line,

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

def on_key_press(event):
    global x_input, y_input # Use global variables

    if (event.key == 'up'):
        y_input += step_size
    if (event.key == 'down'):
        y_input -= step_size
    if (event.key == 'left'):
        x_input -= step_size
    if (event.key == 'right'):
        x_input += step_size
    if (event.key == 'x'):
        pass

    # Clamp the values to prevent the arm from going out of bounds
    x_input = max(-1.0, min(1.0, x_input))
    y_input = max(-1.0, min(1.0, y_input))

    print(f"x: {x_input}, y: {y_input}")


# Animation function
def animate(i):
    # handle_keyboard_input()  # Check for key inputs
    return update_frame(i)

fig.canvas.mpl_connect('key_press_event', on_key_press)
# Animation setup
ani = FuncAnimation(fig, animate, frames=2000000, interval=50, blit=True)

# Show the plot
plt.show()
