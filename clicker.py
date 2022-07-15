import sys
from pynput.mouse import Listener, Controller, Button
from pynput import keyboard
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument('-block', help='blocks cursor', action='store_true')
parser.add_argument('-delay', help='click delay', type=float, default=0, required=False)
parser.add_argument('-key', help='key to start and end autoclicker loop', default=keyboard.Key.ctrl_l, required=False)

args = parser.parse_args()

args.key = 'Key.' + args.key
print(args.key)

Mouse = Controller()

start_position = None
mouse_last_key = None
keyboard_last_key = None

print(args.block)
print(args.delay)


# MOUSE
def on_move(x, y):
    if args.block and start_position is not None:
        Mouse.position = start_position


def on_click(x, y, button, pressed):
    global mouse_last_key
    mouse_last_key = button


mouse_listener = Listener(on_move=on_move, on_click=on_click)
mouse_listener.start()


def on_press(key):
    global keyboard_last_key
    keyboard_last_key = key


def on_release(key):
    global keyboard_last_key
    keyboard_last_key = None


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

while True:
    if str(keyboard_last_key) == args.key:
        start_position = Mouse.position
        keyboard_last_key = None
        break

while True:
    time.sleep(args.delay)

    if str(keyboard_last_key) == args.key:
        sys.exit('exit')

    Mouse.click(Button.left, 1)
