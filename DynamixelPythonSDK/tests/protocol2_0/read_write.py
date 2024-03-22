#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# Copyright 2017 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

# Author: Ryu Woon Jung (Leon)

#
# *********     Read and Write Example      *********
#
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#

import os
from ast import For
import math as math
import time
import sys
import pygame
import numpy as np


if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                      = 1                 # Dynamixel ID : 1
BAUDRATE                    = 1000000            # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM5'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE_1  = 1023                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE_1  = 3073              # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_MINIMUM_POSITION_VALUE_2  = 2048                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE_2  = 2730
DXL_MINIMUM_POSITION_VALUE_3  = 1764                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE_3  = 3073
DXL_MINIMUM_POSITION_VALUE_4  = 1023                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE_4  = 3073
DXL_MINIMUM_POSITION_VALUE_5  = 1594                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE_5  = 2503

DXL_MINIMUM_POSITION_VALUE  = [1023, 2048, 1764, 1023, 1594]               # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE = [3073, 2730, 3073, 3073, 2503]


DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0
dxl_goal_position = [DXL_MINIMUM_POSITION_VALUE_1, DXL_MAXIMUM_POSITION_VALUE_1]         # Goal position


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

p1= 0.025
p2= -0.025

d1 = 45
d2 = -10
d3 = 0
d4 = 45

while True:
    pygame.init()

    # Initialize the joysticks
    pygame.joystick.init()

    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    #print(f"Nombre de joysticks connectés : {joystick_count}")

    print("Press any key to continue! (or press ESC to quit!)")
    if getch() == chr(0x1b):
        break

    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        buttons = joystick.get_numbuttons()

        print("Before Update - d5 :", p1, p2)
        for i in range( buttons ):
            button = joystick.get_button( i )

            if i == 4:
                p1 -= 0.02*button
            elif i == 6:
                p1 += 0.02*button
            elif i == 5:
                p2 += 0.02*button
            elif i == 7:
                p2 -= 0.02*button

        print("After Update - d5 :", p1, p2)
        print("______________________")

        ###textPrint.print(screen, "Joystick {}".format(i) )
        ###textPrint.indent()

        #### Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        ###textPrint.print(screen, "Joystick name: {}".format(name) )

        #### Usually axis run in pairs, up/down for one, and left/right for the other.
        axes = joystick.get_numaxes()
        ###textPrint.print(screen, "Number of axes: {}".format(axes) )
        ###textPrint.indent()

        print("Before Update - d1:", d1, "d2:", d2, "d3:", d3, "d4:", d4)
        for i in range( axes ):
            axis = joystick.get_axis( i )
            ###textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )

            if i == 0:
                d1 += axis
            elif i == 1:
                d2 += axis
            elif i == 2:
                d3 += axis
            elif i == 3:
                d4 += axis

        print("After Update - d1:", d1, "d2:", d2, "d3:", d3, "d4:", d4)
        print("______________________")


    # Write goal position
    for i in range(4):

        button4= joystick.get_button(4)
        button5= joystick.get_button(5)

        #Gestion de la saisie d'un objet par la pince
        close_button = joystick.get_button(4)
        open_button = joystick.get_button(5)

        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, i, ADDR_PRO_GOAL_POSITION, DXL_MINIMUM_POSITION_VALUE[i])
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

    while 1:
        # Read present position
        dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_PRESENT_POSITION)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, dxl_goal_position[index], dxl_present_position))

        if not abs(dxl_goal_position[index] - dxl_present_position) > DXL_MOVING_STATUS_THRESHOLD:
            break

    #index = index + 1
    
    #if index == dxl_goal_position.len():
    #    index = 0
    if index == 0:
        index = 1
    else:
        index = 0


# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
