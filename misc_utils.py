'''
Various miscellaneous functions.
They are:
  - calc_speed
  - timer
  - dialogue
  - help
'''
# Standard library modules
import time
import curses
import random

# Custom modules
import flow_control
from constants import INITSPEED, CONTROL_KEYS
from constants import UP, DOWN, LEFT, RIGHT


def calc_speed(length):
    return int(INITSPEED - (length / 5 + length) / 10 % 120)


def timer():
    start_time = time.time()
    yield 0
    while True:
        time_elapsed = time.time() - start_time
        start_time = time.time()
        yield time_elapsed * 1000


def dialogue(window, text, answer_map=None, border=0):
    '''
Shows a dialogue box to the user, and then returns True or False
The answer map is a dictionary,
where the keys are the menu options for the user.

and the values are what is returned when a given option is chosen.
The keys should be one letter strings,
but the values can be whatever you can put in a dictionary.

For example, in the default mapping ({'y':True, 'n':False}),
if the user presses 'y' True is returned

None is a wild-card. If None is used as a key,
then any free key will return the value.

The text passed should inform the user what options he has,
and it can be a multi-line string.
If it is, then each line will be cantered
    '''

    if answer_map is None:
        answer_map = {'y': True, 'n': False}
    text = text.split('\n')

    win_height, win_width = window.getmaxyx()
    win_start_y, win_start_x = window.getbegyx()

    width = int((win_width * 70) / 100)  # 70% of the window
    height = len(text) + 2  # 1 line of padding around the text.
    start_y = int(((win_height - height) / 2) + win_start_y)
    start_x = int(((win_width - width) / 2) + win_start_x)

    dialogue = curses.newwin(height, width, start_y, start_x)
    dialogue.border(*([border] * 8))

    for i, s in enumerate(text, 1):
        dialogue.addstr(i, 1, s.center(width - 2))
    dialogue.refresh()

    safe_map = answer_map.copy()
    for key in answer_map.keys():
        if key is None:
            del(safe_map[None])
    ord_keys = [ord(key) for key in safe_map.keys()]
    window.nodelay(0)
    c = -1
    while c not in ord_keys:
        # chr(c) will throw up an exception if the number isn't valid,
        # so were checking c against a list of the keys in ord() form
        c = dialogue.getch()
        if None in answer_map.keys() and c not in ord_keys:
            answer_map[chr(c)] = answer_map[None]
            ord_keys.append(c)
    window.nodelay(1)

    del dialogue
    window.touchwin()
    window.refresh()
    return answer_map[chr(c)]


def help(window):
    command_help = """
Commands

      %s           
Use %s + %s  or the
      %s           
arrow keys for movement

'p': Pause

'q': Quit

'?': This help text

--Press space--
                """ % (CONTROL_KEYS[UP], CONTROL_KEYS[LEFT],
                       CONTROL_KEYS[RIGHT], CONTROL_KEYS[DOWN])

    gameplay_help_1 = """
Gameplay

Run around and eat the apples.
As you eat, you'll grow longer,
but be careful! Running into yourself,
or going backwards means Game Over.

The higher your score, the faster
you'll go.

Every now and again though.
you'll get a bonus...

--Press space--
    """

    gameplay_help_2 = """
Bugs

Bugs are a delicious treat,
for which you'll get extra points!
If you see one, try and get to it
as quickly as possible.
There's a counter, and if it
reaches 0, the bug runs away.
But if you do catch it, then
the rest of the timer
will be added to your score!

That's it. I hope you have fun!

--Press space--
"""

    dialogue(window, command_help, {' ': None})
    dialogue(window, gameplay_help_1, {' ': None})
    dialogue(window, gameplay_help_2, {' ': None})
    flow_control.countdown(window)


def get_random_pos(win, exclude_list=(None,)):
    '''
Returns a random position in win, that is not in exclude_list
    '''
    while True:
        random_pos = [random.randrange(1, win.getmaxyx()[0] - 1),
                    random.randrange(1, win.getmaxyx()[1] - 1)]
        if random_pos in exclude_list:
            continue
        else:
            break
    return random_pos
