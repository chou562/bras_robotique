
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel PRO 54-200, and an USB2DYNAMIXEL.
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
# Be sure that Dynamixel PRO properties are already set as %% ID : 1 / Baudnum : 1 (Baudrate : 57600)
#Tache 4 : enregistre et rejoue les mouvements 

import os
import pygame
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time

pygame.init()

REFRESH_RATE = 5000
with open('C:/Users/cc105536/Documents/Positions.txt', 'w') as fichier:
    fichier.write("Positions :")

def degretoE(D):
    E=((D/180)+1)*2048
    return E

def valmax(angle,Anglemax,Anglemin):
    """
    angle, Saturation = valmax(angle,Anglemax,Anglemin)
    entree:
    angle :  Valeur a tester ()
    Anglemax : Valeur max de angle
    Anglemin: valeur min de angle
    sortie:

    """
    Saturation = False
    if (angle > Anglemax):
        angle = round(Anglemax)
        saturation = True
    if (angle < Anglemin):
        angle = round(Anglemin)
        Saturation = True
    return angle, Saturation


# Initialize the joysticks
pygame.joystick.init()

import msvcrt
def getch():
    return msvcrt.getch().decode()


joystickGaucheX = pygame.joystick.Joystick(0).get_axis(0)
joystickGaucheY = pygame.joystick.Joystick(0).get_axis(1)
joystickDroitX= pygame.joystick.Joystick(0).get_axis(3)
joystickDroitY= pygame.joystick.Joystick(0).get_axis(2)

Angle=100


# Control table address
ADDR_PRO_TORQUE_ENABLE      = 64               # Control table address is different in Dynamixel model
ADDR_PRO_GOAL_POSITION      = 116
ADDR_PRO_PRESENT_POSITION   = 132

# Protocol version
PROTOCOL_VERSION            = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID1                      = 1                # Dynamixel ID : 1
DXL_ID2                      = 2
DXL_ID3                      = 3
DXL_ID4                      = 4
DXL_ID5                      = 5
BAUDRATE                    = 1000000            # Dynamixel default baudrate : 57600
DEVICENAME                  = 'COM5'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque

DXL1_MINIMUM_POSITION_VALUE  = 2050     # Dynamixel will rotate between this value
pos1=DXL1_MINIMUM_POSITION_VALUE
DXL1_MAXIMUM_POSITION_VALUE  = 3073     # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)

DXL2_MINIMUM_POSITION_VALUE  = 2048     # Dynamixel will rotate between this value
pos2=DXL2_MINIMUM_POSITION_VALUE
DXL2_MAXIMUM_POSITION_VALUE  = 2408

DXL3_MINIMUM_POSITION_VALUE  = 1900     # Dynamixel will rotate between this value
pos3=DXL3_MINIMUM_POSITION_VALUE
DXL3_MAXIMUM_POSITION_VALUE  = 3073

DXL4_MINIMUM_POSITION_VALUE  = 2070     # Dynamixel will rotate between this value
pos4=DXL4_MINIMUM_POSITION_VALUE
DXL4_MAXIMUM_POSITION_VALUE  = 3073

DXL5_MINIMUM_POSITION_VALUE  = 1592     # Dynamixel will rotate between this value
pos5=DXL5_MINIMUM_POSITION_VALUE
DXL5_MAXIMUM_POSITION_VALUE  = 2503

DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0

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
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID4, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID5, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

joystick = pygame.joystick.Joystick(0)
joystick.init()


if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")


run = True

record = False
replay = False
positions_file_path = 'C:/Users/cc105536/Documents/Positions.txt'

record_interval = 1  # Enregistrez une position tous les 10 cycles

while run:
    # Gérer les événements pygame
    pygame.event.pump()

    # Lire l'état des boutons 5 et 6 du joystick
    button5= joystick.get_button(4)
    button6= joystick.get_button(5)

    if joystick.get_button(0):  # Bouton pour commencer l'enregistrement
        record = True

        # Désactivation du couple des moteurs Dynamixel
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID4, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID5, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)

        print ("record mode")

        # Ouverture du fichier en mode écriture
        with open(positions_file_path, 'w') as file:  # Ouvrir le fichier en mode écriture
            file.write("Enregistrement des positions\n")

    if joystick.get_button(1) and record:  # Bouton pour arrêter l'enregistrement
        record = False

        # Activation du couple des moteurs Dynamixel
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID4, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID5, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

    if joystick.get_button(2):  # Bouton pour commencer la lecture
        replay = True

        # Activation du couple des moteurs Dynamixel
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID4, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID5, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)

        print ("replay mode")
        with open(positions_file_path, 'r') as file:  # Ouvrir le fichier en mode lecture
            recorded_positions = [line.strip() for line in file.readlines() if line.strip() and not line.startswith("Enregistrement")]

    if record:
        # Lire les positions actuelles et les enregistrer dans le fichier
        current_positions = [packetHandler.read4ByteTxRx(portHandler, i, ADDR_PRO_PRESENT_POSITION)[0] for i in range(1, 6)]
        with open(positions_file_path, 'a') as file:
            # Convertit les positions actuelles (liste d'entiers) en une chaîne de caractères séparée par des virgules
            file.write(','.join(map(str, current_positions)) + '\n')

     # Rejouer les positions enregistrées si la variable replay est vraie et des positions sont enregistrées
    if replay and recorded_positions:
        current_positions = list(map(int, recorded_positions.pop(0).split(',')))
        for i in range(1, 6):
            packetHandler.write4ByteTxRx(portHandler, i, ADDR_PRO_GOAL_POSITION, current_positions[i-1])
        if not recorded_positions:  # Liste vide, fin de la lecture
            replay = False


# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID1, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID2, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID3, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID4, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID5, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()




