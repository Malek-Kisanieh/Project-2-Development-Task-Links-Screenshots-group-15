#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.messaging import BluetoothMailboxClient, TextMailbox
from pybricks.media.ev3dev import Image, ImageFile
# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()

axis = Motor(Port.C)
touch = TouchSensor(Port.S1)
sensor = ColorSensor(Port.S2)
elbow = Motor(Port.B, Direction.COUNTERCLOCKWISE, [8, 40])
claw = Motor(Port.A)

# Write your program here.


########################Calibration######################
def calibrate(start_position, start_height):
    elbow.run_until_stalled(60,then=Stop.HOLD, duty_limit=50)
    elbow.reset_angle(120)
    
    claw.run_until_stalled(200,then=Stop.COAST, duty_limit=50)
    claw.reset_angle(0)
    claw.run_target(200,-90)

    while not touch.pressed():
        axis.run_until_stalled(60,then=Stop.HOLD, duty_limit=30)
    axis.reset_angle(0)
    axis.run_target(60, start_position)
    
    elbow.run_target(60, start_height)
    elbow.hold()
#########################################################

######################RGB Sensor#########################
def rgb_sensor():
    rgb_value = sensor.rgb()
    print(rgb_value)
    #Threshold
    blue_min = (1,5,22)
    blue_max = (3,10,46)

    green_min = (3,12,8)
    green_max = (5,21,15)

    red_min = (8,2,2)
    red_max = (20,4,1)

    yellow_min = (20,7,4)
    yellow_max = (33,29,13)

    if red_max >= rgb_value >= red_min:
        print("Red Found")
        ev3.speaker.say("Red Found")
        return "red"
    elif blue_max >= rgb_value >= blue_min:
        print("Blue Found")
        ev3.speaker.say("Blue Found")
        return "blue"
    elif green_max >= rgb_value >= green_min:
        print("Green Found")
        ev3.speaker.say("Green Found")
        return "green"
    elif yellow_max >= rgb_value >= yellow_min:
        print("Yellow Found")
        ev3.speaker.say("Yellow Found")
        return "yellow"
    else:
        print("None")
        ev3.speaker.say("Nothing Found")
        return "none"
#########################################################


########################Grab#############################
def grab():
    claw.run_until_stalled(300,then=Stop.HOLD, duty_limit=50)
    claw.hold()
    elbow.run_target(60, 55)
#########################################################

######################Restart############################
def restart(start_position, start_height):

    claw.run_until_stalled(200,then=Stop.COAST, duty_limit=50)
    claw.reset_angle(0)
    claw.run_target(200,-90)

    elbow.run_target(60, 120)

    while not touch.pressed():
        axis.run_until_stalled(60,then=Stop.HOLD, duty_limit=30)
    axis.reset_angle(0)
    axis.run_target(60,start_position)

    elbow.run_target(60, start_height)
#########################################################


############Menu################
def menu_position(speach):
    ev3.speaker.say(speach)
    button=[]
    while button == []:
        button = ev3.buttons.pressed()
    if Button.UP in button:
        position = -82
    elif Button.LEFT in button:
        position = -395
    elif Button.DOWN in button:
        position = -560
    elif Button.RIGHT in button:
        position = -640
    return position

def menu_color(speach):
    ev3.speaker.say(speach)
    ev3.screen.clear()
    ev3.screen.load_image("pybrick3.png")
    button=[]
    while button == []:
        button = ev3.buttons.pressed()
    if Button.UP in button:
        color = "blue"
    elif Button.RIGHT in button:
        color = "green"
    elif Button.DOWN in button:
        color = "red"
    elif Button.LEFT in button:
        color = "yellow"
    elif Button.CENTER in button:
        color = "all"
    return color

def menu_height(speach):
    ev3.speaker.say(speach)
    button=[]
    while button == []:
        button = ev3.buttons.pressed()
    if Button.UP in button:
        position = 120
    elif Button.LEFT in button:
        position = None
    elif Button.DOWN in button:
        position = 0
    elif Button.RIGHT in button:
        position = 35
    return position

def menu_main(speach):
    ev3.speaker.say(speach)
    ev3.screen.clear()
    ev3.screen.load_image("pybrick4.png")
    button=[]
    while button == []:
        button = ev3.buttons.pressed()
    if Button.RIGHT in button:
        answer = "yes"
    elif Button.LEFT in button:
        answer = "no"
    return answer
################################


###################Input####################
def parameters():
    ev3.screen.load_image("pybrick1.png")
    start_position = menu_position("Chose The pick up position")
    ev3.screen.clear()

    ev3.screen.load_image("pybrick5.png")
    height_position_p = menu_height("Chose the height for the pick up position")
    ev3.screen.clear()

    ev3.screen.load_image("pybrick2.png")
    end_position = menu_position("Chose the drop off position")
    color = menu_color("Chose the color for the drop off zone")
    ev3.screen.clear()

    ev3.screen.load_image("pybrick6.png")
    height_position_d = menu_height("Chose the height for the drop off position")

    d={color:end_position}
    d2={color:height_position_d}#watch
    taken_zones=1
    switch = True
    while taken_zones < 3 and switch:
        answer = menu_main("Would you like to select more dropp of zones?")
        if answer == "yes":
            ev3.screen.clear()
            ev3.screen.load_image("pybrick2.png")
            position_in_d = menu_position("Chose the drop off position")
            color_in_d = menu_color("Chose the color for the drop off zone")
            
            ev3.screen.clear()
            ev3.screen.load_image("pybrick6.png")
            height_position_d_ind = menu_height("Chose the height for the drop off position")

            d[color_in_d] = position_in_d
            d2[color_in_d] = height_position_d_ind
            taken_zones +=1
        elif answer == "no":
            switch = False
    return start_position,height_position_p,d,d2
############################################


##################Main######################
def main():
    start_position, start_height, d, d2 = parameters()
    ev3.screen.clear()
    calibrate(start_position,start_height)

    run=True
    while run:
        grab()
        color_brick=rgb_sensor()

        if color_brick not in d.keys():
            ev3.speaker.say("I dont have a drop off zone for that color")
        elif "all" in d.keys():
            all_colors_p = d.get("all")
            axis.run_target(60,all_colors_p)

        try:
           end_position = d.get(color_brick)
           end_height = d2.get(color_brick)
           axis.run_target(60,end_position)
           elbow.run_target(60, end_height)
        except:
            pass
        restart(start_position,start_height)   
main()
############################################
