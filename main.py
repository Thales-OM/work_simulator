import sys
import time
import random
import itertools
import pyautogui
from pynput.mouse import Controller as MouseController
from pynput.keyboard import Listener
import keyboard
import threading
from initialize import read_config, construct_config, CONFIG_ABS_PATH


def on_press(key, event):
    """
    Keyboard input handler function
    :param key:
    :param event:
    :return:
    """
    # Check if Ctrl+E is pressed to terminate the program
    if keyboard.is_pressed('ctrl+e'):
        print('Exit sequence pressed - terminating process')
        event.clear()

        # faster exit than using Event
        # Event left for fail-safe/if needed to remove sys.exit() in the future
        sys.exit()


def get_interval_size(config):
    """
    Returns the duration (in sec) of sleep based on config
    :param config:
    :return:
    """
    if config['interval_type'] == 'set':
        return config['interval_size']
    elif config['interval_type'] == 'random':
        return random.randint(config['interval_lower'], config['interval_upper'])
    else:
        raise ValueError('Invalid interval_type. Expected: set, random')


def run_activity(config: dict):
    # Create an infinite iterator over the keys
    # If none were provided - always return None
    keys = config['keyboard']['keys']
    key_iter = itertools.cycle(keys) if keys else itertools.cycle(tuple([None]))

    # Initialize the mouse controller
    mouse = MouseController()

    # Calculate the screen dimensions
    screen_width, screen_height = pyautogui.size()

    # Event to track if the program should be running
    running_event = threading.Event()
    running_event.set()

    # Start the keyboard listener thread (to work in parallel to main cycle)
    listener = Listener(on_press=lambda key: on_press(key=key, event=running_event))
    listener_thread = threading.Thread(target=listener.start())

    # Infinite loop to simulate mouse movements
    while running_event.is_set():
        time_interval = get_interval_size(config)

        # Mouse movements
        if config['mouse']['movement']:
            # Generate random coordinates within the screen dimensions
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)

            # Move the mouse to the random coordinates
            mouse.position = (x, y)

        if config['mouse']['left_click']:
            mouse.click(MouseController.LEFT)

        if config['mouse']['right_click']:
            mouse.click(MouseController.RIGHT)

        # Keyboard presses
        if keys:  # check to prevent unnecessary iteration
            next_key = next(key_iter)
            keyboard.press(next_key)
            keyboard.release(next_key)

        # Wait for the specified time interval
        time.sleep(time_interval)

    # Stop listening for keyboard inputs
    listener.stop()


if __name__ == '__main__':
    # Seed random generation
    random.seed(0)

    mode = input('Enter configuration to be loaded from config (empty - manual setting, "default" is always '
                 'available): ')
    if mode:
        config = read_config(config_path=CONFIG_ABS_PATH, mode=mode)
    else:
        config = construct_config()

    run_activity(config=config)
