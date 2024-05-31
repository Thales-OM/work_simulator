import sys
import time
import random
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Listener
import keyboard
import threading


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
    if keyboard.is_pressed('ctrl+e'):
        print('Exit sequence pressed - terminating process')
        running = False
        sys.exit()


# Start the keyboard listener thread (to work in parallel to main cycle)
listener = Listener(on_press=on_press)
listener_thread = threading.Thread(target=listener.start())

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
