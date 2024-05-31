import yaml
import os
import keyboard

# Config file with at least default configuration filled is required
CONFIG_REL_PATH = 'config.yaml'
CONFIG_ABS_PATH = os.path.join(os.path.dirname(__file__), CONFIG_REL_PATH)


def is_valid_key(key_name):
    try:
        keyboard.add_hotkey(key_name, lambda: None)
        return True
    except:
        return False
    finally:
        keyboard.clear_hotkey(key_name)


def read_config(config_path, mode='default'):
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)

    try:
        current_config = config[mode]
    except KeyError as ke:
        raise KeyError(f'Config file must contain selected configuration name ("{mode}") as a top-level key.\n{ke}')

    interval_type = current_config['interval_type']
    if interval_type == 'set':
        interval_size = int(current_config['interval_size'])
        assert interval_size > 0, 'Interval size must be positive int'
    elif interval_type == 'random':
        interval_lower = int(current_config['interval_lower'])
        interval_upper = int(current_config['interval_upper'])
        assert 0 < interval_lower <= interval_upper, 'Random interval bounds must satisfy: 0 < lower <= upper'
    else:
        raise ValueError('Invalid interval_type, must be one of: set, random')

    mouse = current_config['mouse']
    for attr in ('movement', 'left_click', 'right_click'):
        assert isinstance(mouse[attr], bool), f'Mouse attribute {attr} must be type bool'

    keyboard_keys = current_config['keyboard']['keys']
    for key in keyboard_keys:
        assert is_valid_key(key), f'Invalid key name provided for keyboard inputs: "{key}"'

    return current_config


def construct_config():
    current_config = {}

    # Repeat interval type and bounds
    while True:
        try:
            interval_type = input('Enter interval_type: ')
            current_config['interval_type'] = interval_type
            if interval_type == 'set':
                while True:
                    try:
                        interval_size = int(input('Enter interval_size (sec): '))
                        assert interval_size > 0, 'Interval size must be positive int'
                    except AssertionError as ae:
                        continue
                    current_config['interval_size'] = interval_size
                    break
            elif interval_type == 'random':
                while True:
                    try:
                        interval_lower = int(input('Enter interval_lower bound: '))
                        interval_upper = int(input('Enter interval_upper bound: '))
                        assert 0 < interval_lower <= interval_upper, 'Random interval bounds must satisfy: 0 < lower <= upper'
                    except AssertionError as ae:
                        continue
                    current_config['interval_lower'] = interval_lower
                    current_config['interval_upper'] = interval_upper
                    break
            else:
                raise ValueError('Invalid interval_type, must be one of: set, random')
        except ValueError as ve:
            continue
        break

    # Mouse inputs
    while True:
        try:
            mouse_attrs = {}
            for attr in ('movement', 'left_click', 'right_click'):
                mouse_attrs[attr] = input(f'Enter mouse {attr} value: ')
                if mouse_attrs[attr] == 'True':
                    mouse_attrs[attr] = True
                elif mouse_attrs[attr] == 'False':
                    mouse_attrs[attr] = False
                else:
                    raise ValueError(f'Mouse attribute {attr} must be bool (True, False)')
        except ValueError as ve:
            continue
        current_config['mouse'] = mouse_attrs
        break

    # Keyboard inputs
    while True:
        try:
            keys_str = input('Enter space-separated list of keys names/combinations(+): ')
            keys = keys_str.split(' ')
            keys = [key for key in keys if key != '']
            for key in keys:
                assert is_valid_key(key), f'Invalid key name: "{key}"'
        except AssertionError as ae:
            continue
        current_config['keyboard'] = {'keys': keys}
        break

    return current_config
