# -*- coding: utf-8 -*-
#Ce code sert a manipuler le robot sur Coppelia avec les manettes 

from ast import For
import sim
import math as math
import time
import sys
import pygame
import numpy as np

# Fonction pour établir la connexion avec CoppeliaSim
def connect(port):
    sim.simxFinish(-1)  # Ferme communication si active
    clientID = sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID == 0: print("Connecte au port",port)
    else: 
        print("echec connection au port",port)
        sys.exit()
    return clientID


# Connection à CoppeliaSim
clientID = connect(19999)
# Handles des servomoteurs
D = [0, 0, 0, 0, 0]
returnCode,D[0] = sim.simxGetObjectHandle(clientID,'D1',sim.simx_opmode_blocking)
returnCode,D[1] = sim.simxGetObjectHandle(clientID,'D2',sim.simx_opmode_blocking)
returnCode,D[2] = sim.simxGetObjectHandle(clientID,'D3',sim.simx_opmode_blocking)
returnCode,D[3] = sim.simxGetObjectHandle(clientID,'D4',sim.simx_opmode_blocking)
# Handles des actionneurs de la pince - 2 déplacements linéaires
returnCode,D5_G = sim.simxGetObjectHandle(clientID,'D5_G',sim.simx_opmode_blocking)
returnCode,D5_D = sim.simxGetObjectHandle(clientID,'D5_D',sim.simx_opmode_blocking)
# Dummy position de référence
returnCode,positionRef = sim.simxGetObjectHandle(clientID,'positionRef',sim.simx_opmode_blocking)
# Dummy position de la pince
returnCode,pinceRef = sim.simxGetObjectHandle(clientID,'pinceRef',sim.simx_opmode_blocking)
# Objet et sensor
returnCode,Objet1 = sim.simxGetObjectHandle(clientID,'Objet1',sim.simx_opmode_blocking)
returnCode,ForceSensor = sim.simxGetObjectHandle(clientID,'ForceSensor',sim.simx_opmode_blocking)


pygame.init()

REFRESH_RATE = 5000

#### Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

#### Get ready to print
###textPrint = TextPrint()

# Game Loop
running = True

d1 = 45
d2 = -10
d3 = 0
d4 = 45

p1= 0.025
p2= -0.025

while running:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()
    
    # For each joystick:
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

        ### Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        ##textPrint.print(screen, "Joystick name: {}".format(name) )

        ### Usually axis run in pairs, up/down for one, and left/right for the other.
        axes = joystick.get_numaxes()
        ##textPrint.print(screen, "Number of axes: {}".format(axes) )
        ##textPrint.indent()

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

        ###textPrint.unindent()
        
    # Modification Angles [D1=45°, D2=-10°, D3=0°, D4=45°] et pince Fermée
    L1 = 89.45
    L2 = 105.95
    L3 = 100
    L4 = 86.05


    button4= joystick.get_button(4)
    button5= joystick.get_button(5)
    
    if (button4==1 and button5==0):
        # Fermeture de la pince
        returnCode = sim.simxSetJointTargetPosition(clientID, D5_G, 0.025, sim.simx_opmode_blocking)
        returnCode = sim.simxSetJointTargetPosition(clientID, D5_D, -0.025, sim.simx_opmode_blocking)
    elif (button4==0 and button5==1):
        ##Ouverture de la pince
        returnCode = sim.simxSetJointTargetPosition(clientID, D5_G, 0, sim.simx_opmode_blocking)
        returnCode = sim.simxSetJointTargetPosition(clientID, D5_D, 0, sim.simx_opmode_blocking) 


    # Envoi des nouvelles positions aux servomoteurs dans CoppeliaSim
    sim.simxSetJointTargetPosition(clientID, D[0], math.radians(d1), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[1], math.radians(d2), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[2], math.radians(d3), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[3], math.radians(d4), sim.simx_opmode_blocking)

    #Gestion de la saisie d'un objet par la pince
    close_button = joystick.get_button(4)
    open_button = joystick.get_button(5)
    if close_button : 
        returnCode = sim.simxSetObjectParent(clientID,Objet1,ForceSensor,True,sim.simx_opmode_blocking)
    if open_button:
        returnCode = sim.simxSetObjectParent(clientID,Objet1,-1,True,sim.simx_opmode_blocking)


    # lecture de la position de la pince
    returnCode, positionPince = sim.simxGetObjectPosition(clientID, pinceRef, positionRef,sim.simx_opmode_blocking)
    print("pinceX=",positionPince[0], "pinceY=", positionPince[1], "pinceZ=", positionPince[2])
     
    clock.tick(REFRESH_RATE)

    # fermeture communication avec client
sim.simxFinish(-1)






