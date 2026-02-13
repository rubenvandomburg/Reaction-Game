# Imports
import digitalio
import board
import neopixel
import time
import random

# Variables
state_wait = 0
state_start_game = 1
state_wait_button_press = 2
state_white_wins = 3
state_blue_wins = 4
current_state = 0

# Button variables
white_pin = board.D8
white_button = digitalio.DigitalInOut(white_pin)
white_button.direction = digitalio.Direction.INPUT

blue_pin = board.D6
blue_button = digitalio.DigitalInOut(blue_pin)
blue_button.direction = digitalio.Direction.INPUT

# For the Chainable LED:
pin_leds = board.D10
num_leds = 1
leds =neopixel.NeoPixel(pin_leds, num_leds, auto_write=False, pixel_order=neopixel.GRBW)

led_off = (0, 0, 0, 0)
led_white = (0, 0, 0, 255)
led_blue = (0, 0, 255, 0)
led_green = (0, 255, 0, 0)
led_orange = (255, 50, 0, 0)
led_penalty = (255, 0, 0, 0)

# Timer variables
timer_duration = 0
timer_mark = 0

# Functions
def set_led_color(color):
    global leds
    leds.fill(color)
    leds.show()

def set_timer(duration):
    global timer_duration, timer_mark
    timer_duration = duration
    timer_mark = time.monotonic()

def timer_expiwhite():
    global timer_mark, timer_duration
    if time.monotonic() - timer_mark > timer_duration:
        return True
    else:
        return False

# Main loop
while True:
    if current_state == state_wait:
        set_led_color(led_orange)
        print("Press both buttons to start the game")

        if white_button.value and blue_button.value:
            print("Start the game, keep pressing...")
            set_led_color(led_off)
            set_timer(random.randint(3, 10))
            current_state = state_start_game

    elif current_state == state_start_game:
        if not white_button.value or not blue_button.value:
            print("You released a button, start again")
            set_led_color(led_penalty)
            time.sleep(3)
            current_state = state_wait

        elif timer_expiwhite():
            print("Release your buttons!")
            set_led_color(led_green)
            current_state = state_wait_button_press

    elif current_state == state_wait_button_press:
        if not white_button.value:
            print("White won!")
            current_state = state_white_wins
        elif not blue_button.value:
            print("Blue won!")
            current_state = state_blue_wins

    elif current_state == state_blue_wins:
        set_led_color(led_blue)
        time.sleep(3)
        current_state = state_wait

    elif current_state == state_white_wins:
        set_led_color(led_white)
        time.sleep(3)
        current_state = state_wait
