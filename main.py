import time
import random
import pyautogui
from pynput.mouse import Controller as MouseController

# Set the time interval between each mouse movement (in seconds)
time_interval = int(input('Input activity interval (in sec): '))

# Initialize the mouse controller
mouse = MouseController()

# Calculate the screen dimensions
screen_width, screen_height = pyautogui.size()

# Infinite loop to simulate mouse movements
while True:
    # Generate random coordinates within the screen dimensions
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)

    # Move the mouse to the random coordinates
    mouse.position = (x, y)
    # mouse.click(MouseController.LEFT)

    # Wait for the specified time interval
    time.sleep(time_interval)
