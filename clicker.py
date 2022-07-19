import sys
from pynput.mouse import Listener, Controller, Button
from pynput import keyboard
import argparse
import time
import signal

parser = argparse.ArgumentParser()
parser.add_argument('-block', help='blocks cursor', action='store_true')
parser.add_argument('-delay', help='click delay', type=float, default=0, required=False)
parser.add_argument('-key', help='key to start and end autoclicker loop', default='ctrl', required=False)
parser.add_argument('-points', help='how many points do you want to select', default=1, type=int, required=False)

available_keys = ('alt', 'alt_gr', 'alt_l', 'alt_r', 'backspace', 'caps_lock', 'cmd', 'cmd_l', 'cmd_r',
                  'ctrl', 'ctrl_l', 'ctrl_r', 'delete', 'down', 'end', 'enter', 'esc', 'f1', 'home', 'insert',
                  'left', 'media_next', 'media_play_pause', 'media_previous', 'media_volume_mute', 'media_volume_up',
                  'menu', 'num_lock', 'page_down', 'page_up', 'pause', 'print_screen', 'right', 'scroll_lock', 'shift',
                  'shift_l', 'shift_r', 'space', 'tab', 'up')

args = parser.parse_args()

if args.block and args.points > 1:
    sys.exit('block and points(more than 1) options cannot be specified together')

try:
    available_keys.index(args.key)
except ValueError:
    print("error: you can't use this key", args.key)
    print('list of available keys:')
    print(available_keys)
    sys.exit()

args.key = 'Key.' + args.key
print(args.key)

Mouse = Controller()

start_position = None
mouse_last_key = None
keyboard_last_key = None

print(args.block)
print(args.delay)

point_list = []
point_counter = len(point_list) - 1


def on_move(x, y):
    if args.block and point_list[0] is not None:
        Mouse.position = start_position


def on_click(x, y, button, pressed):
    global mouse_last_key
    mouse_last_key = button


mouse_listener = Listener(on_move=on_move, on_click=on_click)

def on_press(key):
    global keyboard_last_key
    if keyboard_last_key is None:
        keyboard_last_key = key


def on_release(key):
    global keyboard_last_key
    keyboard_last_key = None


keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)
keyboard_listener.start()

for point in range(0, args.points):
    while True:
        if str(keyboard_last_key) == args.key:
            start_position = Mouse.position
            keyboard_last_key = None
            point_list.append(Mouse.position)
            break

print(point_list)
point_counter = len(point_list)
print(point_counter)
mouse_listener.start()


while True:

    try:
        time.sleep(args.delay)
    except KeyboardInterrupt:
        sys.exit('exit')


    if str(keyboard_last_key) == args.key:
        sys.exit('exit')

    if point_counter > 1:
        for x in point_list:
            Mouse.position = x
            Mouse.click(Button.left, 1)
    else:
        Mouse.click(Button.left, 1)