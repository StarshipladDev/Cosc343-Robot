#Defines python enviroment
#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B, OUTPUT_C
from ev3dev2.sensor.lego import UltrasonicSensor
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import TouchSensor
from time import *

# Output b and C are Movetank
m = MoveTank(OUTPUT_B, OUTPUT_C)
sound = Sound()
btn = Button()
colors = 0
cl = ColorSensor()
degree = 10
cl.mode = 'COL-REFLECT'
ts1 = TouchSensor('in1')  # left
ts2 = TouchSensor('in2')  # right
us = UltrasonicSensor()


def start():
    m.on_for_rotations(left_speed=20, right_speed=20, rotations=1, brake=True, block=True)
    findFrontTile(17)
    m.on_for_rotations(left_speed=20, right_speed=-20, rotations=0.45, brake=True, block=True)
    return

def tryMove(BLACK, blackCount, direction, degree):
    if blackCount == 15:
        m.on_for_rotations(left_speed=40, right_speed=-40, rotations=0.4, brake=True, block=True)  # turn 90 degrees to the right
        m.on_for_rotations(left_speed=50, right_speed=50, rotations=10, brake=True, block=True)  # drive forward and hope for in range for scanning

        sonarSearch(255)
        return

    findFrontTile(BLACK)
    checkSides(BLACK)
    searchBlackTile(BLACK, blackCount, direction, degree)

def findFrontTile(black):
    m.on(left_speed=20, right_speed=20)
    a = cl.reflected_light_intensity

    if a > black:
        m.on_for_rotations(left_speed=-15, right_speed=-15, rotations=0.2, brake=True, block=True)
        return

    findFrontTile(black)

def checkSides(BLACK):
    # check left side for not black and readjust
    m.on_for_degrees(left_speed=15, right_speed=-15, degrees=90, brake=True, block=True)
    m.on_for_rotations(left_speed=15, right_speed=15, rotations=0.1, brake=True, block=True)
    right = cl.reflected_light_intensity
    m.on_for_rotations(left_speed=-15, right_speed=-15, rotations=0.1, brake=True, block=True)
    m.on_for_degrees(left_speed=-15, right_speed=15, degrees=90, brake=True, block=True)

    # if left not black move to the right
    if right > BLACK:
        m.on_for_rotations(left_speed=0, right_speed=-20, rotations=0.5, brake=True, block=True)
        m.on_for_rotations(left_speed=-40, right_speed=0, rotations=0.5, brake=True, block=True)
        m.on_for_rotations(left_speed=20, right_speed=20, rotations=0.5, brake=True, block=True)
        return

    # check right side for not black and readjust
    m.on_for_degrees(left_speed=-15, right_speed=15, degrees=90, brake=True, block=True)
    m.on_for_rotations(left_speed=15, right_speed=15, rotations=0.1, brake=True, block=True)
    left = cl.reflected_light_intensity
    m.on_for_rotations(left_speed=-15, right_speed=-15, rotations=0.1, brake=True, block=True)
    m.on_for_degrees(left_speed=15, right_speed=-15, degrees=90, brake=True, block=True)

    # if right not black move to the left
    if left > BLACK:
        m.on_for_rotations(left_speed=-20, right_speed=0, rotations=0.5, brake=True, block=True)
        m.on_for_rotations(left_speed=0, right_speed=-40, rotations=0.5, brake=True, block=True)
        m.on_for_rotations(left_speed=20, right_speed=20, rotations=0.5, brake=True, block=True)
        return

def searchBlackTile(BLACK, blackCount, direction, degree):
    m.on_for_rotations(20, 20, 1, True, True)
    colour = cl.reflected_light_intensity

    if colour < BLACK:
        blackCount += 1
        degree = 10
        sound.beep()
        tryMove(BLACK, blackCount, direction, degree)
    else:
        m.on_for_rotations(-20, -20, 1, True, True)
        if direction == 'right':
            m.on_for_degrees(left_speed=30, right_speed=-30, degrees=degree, brake=True, block=True)
            degree = degree + 10
            searchBlackTile(BLACK, blackCount, 'left', degree)
        if direction == 'left':
            m.on_for_degrees(left_speed=-30, right_speed=30, degrees=degree, brake=True, block=True)
            degree = degree + 10
            searchBlackTile(BLACK, blackCount, 'right', degree)


def sonarSearch(distance):
    m.on_for_rotations(left_speed=-40, right_speed=40, rotations=0.4, brake=True, block=True)  # turn 45' to left

    # scan in 8 pieces to find closest object
    for test in range(8):
        m.on_for_rotations(left_speed=20, right_speed=-20, rotations=0.1, brake=True, block=True)  # turn right 10'
        scan = us.distance_centimeters

        if (scan < distance):
            distance = scan
            closest = test
            back = (7 - closest) * 0.1  # value to turn back by

    if (distance < 255):
        m.on_for_rotations(left_speed=-20, right_speed=20, rotations=back, brake=True, block=True)  # turn back to face closest because found target
        m.on_for_rotations(left_speed=50, right_speed=50, rotations=3, brake=True, block=False)  # move closer to target

        while (m.is_running):
            if ts1.value() > 0 and ts2.value() > 0:
                m.stop()

                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)  # back away from bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)  # push bottle

                sound.speak("Wohoo")
            elif ts1.value() > 0:
                m.stop()

                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)  # back away from bottle
                m.on_for_rotations(left_speed=-30, right_speed=30, rotations=0.1, brake=True, block=True)  # turn slightly more towards bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)  # push bottle

                sound.speak("Wohoo")
                return

            elif ts2.value() > 0:
                m.stop()

                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)  # back away from bottle
                m.on_for_rotations(left_speed=30, right_speed=-30, rotations=0.1, brake=True, block=True)  # turn slightly towards bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)  # push bottle

                sound.speak("Wohoo")
                return

        sonarSearch(255)

    elif (distance > 254):
        m.on_for_rotations(left_speed=-20, right_speed=20, rotations=0.4, brake=True, block=True)  # turn back to face front because found nothing
        m.on_for_rotations(left_speed=50, right_speed=50, rotations=3, brake=True, block=False)  # move closer to target

        while (m.is_running):

            if ts1.value() > 0 and ts2.value() > 0:
                m.stop()

                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)  # back away from bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)  # push bottle

                sound.speak("Wohoo")
            elif ts1.value() > 0:
                m.stop()

                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)  # back away from bottle
                m.on_for_rotations(left_speed=-30, right_speed=30, rotations=0.1, brake=True, block=True)  # turn slightly more towards bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)  # push bottle

                sound.speak("Wohoo")
                return

            elif ts2.value() > 0:
                m.stop()
                m.on_for_rotations(left_speed=-50, right_speed=-50, rotations=1, brake=True, block=True)
                m.on_for_rotations(left_speed=30, right_speed=-30, rotations=0.1, brake=True, block=True)  # turn slightly towards bottle
                m.on_for_rotations(left_speed=100, right_speed=100, rotations=5, brake=True, block=True)

                sound.speak("Wohoo")
                return
        sonarSearch(255)


sound.beep()
start()
tryMove(17, 1, 'left', 10)