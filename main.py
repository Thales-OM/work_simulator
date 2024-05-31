import time
import random
import pyautogui

# Set the time interval between each mouse movement (in seconds)
time_interval = 10

# Calculate the screen dimensions
screen_width, screen_height = pyautogui.size()

# Infinite loop to simulate mouse movements
while True:
    # Generate random coordinates within the screen dimensions
    x = random.randint(0, screen_width)
    y = random.randint(0, screen_height)

    # Move the mouse to the random coordinates
    pyautogui.moveTo(x, y, duration=0.5)

    # Wait for the specified time interval
    time.sleep(time_interval)
