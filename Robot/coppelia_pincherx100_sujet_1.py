# -*- coding: utf-8 -*-
"""
Created on Tue May 30 15:46:29 2023
Test de la scene "pincherX_Simu"
    1) Lancer le simulateur
    2) Executer le programme Python

Le bras est dans la position initiale: [D1=0°, D2=0°, D3=0°, D4=0°] et pince Ouverte
Après 2[s] il passe dans le position : [D1=45°, D2=-10°, D3=0°, D4=45°] et pince Fermée

@author: et
"""

from ast import For
import sim
import math as math
import time
import sys
import pygame
import numpy as np


def connect(port):
    sim.simxFinish(-1)  # Ferme communication si active
    clientID = sim.simxStart('127.0.0.1',port,True,True,2000,5)
    if clientID == 0: print("Connecté au port",port)
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


## Angles de départ [D1=0°, D2=0°, D3=0°, D4=0°] et pince Ouverte
#
#   D2 b b D3 b b D4 b b O
#   b
#   b
#   b
#   D1
##
###position = [0, 0, 0, 0, 0]
#### Initialisation des positions
###for ID in range(4):
###    # Ecriture des angles consignes 
###    returnCode = sim.simxSetJointTargetPosition(clientID, D[ID], position[ID], sim.simx_opmode_blocking)
#### Ouverture de la pince
###returnCode = sim.simxSetJointTargetPosition(clientID, D5_G, 0, sim.simx_opmode_blocking)
###returnCode = sim.simxSetJointTargetPosition(clientID, D5_D, 0, sim.simx_opmode_blocking) 

###time.sleep(0.1)  # temporisation pour laisser le temps au simulateur pour faire les calculs et gérer l'affichage 
#### lecture de la position de la pince
###returnCode, positionPince = sim.simxGetObjectPosition(clientID, pinceRef, positionRef,sim.simx_opmode_blocking)
###print("pinceX=",positionPince[0], "pinceY=", positionPince[1], "pinceZ=", positionPince[2])   

###time.sleep(3)


#### Colors
###BLACK = (0, 0, 0)
###WHITE = (255, 255, 255)

#### This is a simple class that will help us print to the screen
#### It has nothing to do with the joysticks, just outputing the
#### information.
###class TextPrint:
###    def __init__(self):
###        self.reset()
###        self.font = pygame.font.Font(None, 30)

###    def print(self, screen, textString):
###        textBitmap = self.font.render(textString, True, WHITE)
###        screen.blit(textBitmap, [self.x, self.y])
###        self.y += self.line_height

###    def reset(self):
###        self.x = 10
###        self.y = 10
###        self.line_height = 30


###    def indent(self):
###        self.x += 20

###    def unindent(self):
###        self.x -= 20

pygame.init()

#### Set the width and height of the screen [width, height]
###size = [500, 1000]
###screen = pygame.display.set_mode(size)
###pygame.display.set_caption("Joystick Tester")
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

    #### Drawing code
    ###screen.fill(BLACK)
    ###textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    ###textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    ###textPrint.indent()

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

        ##textPrint.print(screen, "Joystick {}".format(i) )
        ##textPrint.indent()

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

    #q2 = 20
    #q3 = 50
    #q4 = -20

    #theta2 = 20
    #theta3 = 30
    #theta4 = -70

    ##Py = L2+L3+L4
    ##Pz = L1
    ##q4 = 0
    ##Pyp = Py - L4 * math.cos(q4)
    ##Pzp = Pz - L4 * math.sin(q4) - L1
    
    ##E = math.atan2(-Pzp/math.sqrt(Pyp**2 + Pzp**2),-Pyp/math.sqrt(Pyp**2 + Pzp**2))
    
    ##theta2p = E + math.acos (-(Pyp**2 + Pzp**2 + L2**2 - L3**2)/(2 * L2 * math.sqrt(Pyp**2 + Pzp**2)))
    ##theta2m = E  - 1 *math.acos (-(Pyp**2 + Pzp**2 + L2**2 - L3**2)/(2 * L2 * math.sqrt(Pyp**2 + Pzp**2)))
    
    ##theta3p = math.atan2((Pzp - L2 * math.sin(theta2p))/L3,(Pyp - L2 * math.cos(theta2p))/L3) - theta2p
    ##theta3m = math.atan2((Pzp - L2 * math.sin(theta2m))/L3,(Pyp - L2 * math.cos(theta2m))/L3) - theta2m
    
    ##theta4p = q4 - theta2p - theta3p
    ##theta4m = q4 - theta2m - theta3m

    ##D1 = 0
    ##D2 = -50
    ##D3 = 60
    ##D4 = -30

    ##alpha = 19.29

    ##D1_a = 0

    ##theta2m=math.degrees(theta2m)
    ##theta2p=math.degrees(theta2p)

    ##theta3m=math.degrees(theta3m)
    ##theta3p=math.degrees(theta3p)

    ###theta4m=math.degrees(theta4m)
    ###theta4p=math.degrees(theta4p)

    ##D2_am = theta2m + 270 + alpha
    ##D3_am = theta3m - 270 - alpha
    ##D4_am = theta4m

    ##D2_ap = theta2p + 270 + alpha
    ##D3_ap = theta3p - 270 - alpha
    ##D4_ap = theta4p
    ##print("theta2p = ", theta2p)
    ##print("theta3p = ", theta3p)
    ##print("theta4p = ", theta4p)
    ##print("theta2m = ", theta2m)
    ##print("theta3m = ", theta3m)
    ##print("theta4m = ", theta4m)
    
    ##print("D2_am = ",D2_am,"D3_am = ",D3_am,"D4_am = ",D4_am)
    ##print("D2_ap = ",D2_ap,"D3_ap = ",D3_ap,"D4_ap = ",D4_ap)

    ##q2cm = 90 + D2_am
    ##q2m = q2cm - 19.29
    ##q3m = D3_am + D2_am
    ##q4m = D4_am + q3m

    ##q2cp = 90 + D2_ap
    ##q2p = q2cp - 19.29
    ##q3p = D3_ap + D2_ap
    ##q4 = D4_am + q3p

    ##position = [math.radians(D1_a), math.radians(D2_am), math.radians(D3_am), math.radians(D4_am)] 
    
    ##for ID in range(4):
    ##    returnCode = sim.simxSetJointTargetPosition(clientID, D[ID], position[ID], sim.simx_opmode_blocking)

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

## Mise à jour des positions des servomoteurs en fonction des axes du joystick
#    d1 += joystick.get_axis(0) 
#    d2 += joystick.get_axis(1) 
#    d3 += joystick.get_axis(2) 
#    d4 += joystick.get_axis(3)

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

    #with open('positions.txt', 'a') as file:
    #    file.write("Positions de D[0] à D[3]:\n")

    #    # À l'intérieur de la boucle for
    #    for ID in range(4):
    #        returnCode = sim.simxSetJointTargetPosition(clientID, D[ID], position[ID], sim.simx_opmode_blocking)
    #        # Enregistrez la position dans le fichier
    #        file.write(f"D[{ID}]: {position[ID]}\n")

    
    #Cinematique directe
    #def positionC ():

    #    # Calcul de la position de la pince (Py,Px)
    #    Py = L2 * math.cos(math.radians(q2m)) + L3 * math.cos(math.radians(q3m)) + L4 * math.cos(math.radians(q4))
    #    Pz = L1 + L2 * math.sin(math.radians(q2m)) + L3 * math.sin(math.radians(q3m)) + L4 * math.sin(math.radians(q4))

    #    print("Py = ",Py,"Pz = ",Pz)

    # temporisation pour laisser le temps au simulateur pour faire les calculs et gérer l'affichage
    #time.sleep(0.1)   

    #Cinematique inverse
    #Py = 150
    #Pz = 250
    #q4 = math.pi/4

    #Py = 292
    #Pz = 89.45
    #q4 = 0
    #Pyp = Py - L4 * math.cos(q4)
    #Pzp = Pz - L4 * math.sin(q4) - L1
    
    #E = math.atan2(-Pzp/math.sqrt(Pyp**2 + Pzp**2),-Pyp/math.sqrt(Pyp**2 + Pzp**2))
    
    #theta2p = E + math.acos (-(Pyp**2 + Pzp**2 + L2**2 - L3**2)/(2 * L2 * math.sqrt(Pyp**2 + Pzp**2)))
    #theta2m = E  - 1 *math.acos (-(Pyp**2 + Pzp**2 + L2**2 - L3**2)/(2 * L2 * math.sqrt(Pyp**2 + Pzp**2)))
    
    #theta3p = math.atan2((Pzp - L2 * math.sin(theta2p))/L3,(Pyp - L2 * math.cos(theta2p))/L3) - theta2p
    #theta3m = math.atan2((Pzp - L2 * math.sin(theta2m))/L3,(Pyp - L2 * math.cos(theta2m))/L3) - theta2m
    
    #theta4p = q4 - theta2p - theta3p
    #theta4m = q4 - theta2m - theta3m
    
    #print("theta2p = ", theta2p*180/math.pi)
    #print("theta3p = ", theta3p*180/math.pi)
    #print("theta4p = ", theta4p*180/math.pi)
    #print("theta2m = ", theta2m*180/math.pi)
    #print("theta3m = ", theta3m*180/math.pi)
    #print("theta4m = ", theta4m*180/math.pi)
    #print("Pyp = ", Pyp)
    #print("Pzp = ", Pzp)
    

    # lecture de la position de la pince
    returnCode, positionPince = sim.simxGetObjectPosition(clientID, pinceRef, positionRef,sim.simx_opmode_blocking)
    print("pinceX=",positionPince[0], "pinceY=", positionPince[1], "pinceZ=", positionPince[2])
    
    ### Go ahead and update the screen with what we've drawn.
    ##pygame.display.flip()
     
    clock.tick(REFRESH_RATE)

    # Appel de la fonction positionC
    #positionC()

    # fermeture communication avec client
sim.simxFinish(-1)

