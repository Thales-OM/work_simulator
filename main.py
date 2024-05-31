import time
import random
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Listener, KeyCode

# Set the time interval between each mouse movement (in seconds)
time_interval = int(input('Input activity interval (in sec): '))

# Initialize the mouse controller
mouse = MouseController()

# Calculate the screen dimensions
screen_width, screen_height = pyautogui.size()

# Variable to track if the program is running
running = True


# Keyboard input handler function
def on_press(key):
    global running

    # Check if Ctrl+E is pressed to terminate the program
    if key == KeyCode.from_combinations([('control'), ('e')]):
        running = False


# Start listening for keyboard inputs
listener = Listener(on_press=on_press)
listener.start()

# Infinite loop to simulate mouse movements
while running:
    # Generate random coordinates within the screen dimensions
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)

    # Move the mouse to the random coordinates
    mouse.position = (x, y)
    # mouse.click(MouseController.LEFT)

    # Wait for the specified time interval
    time.sleep(time_interval)

# Stop listening for keyboard inputs
listener.stop()
