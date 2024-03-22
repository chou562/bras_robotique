# -*- coding: utf-8 -*-
#Ce code sert a modifier les angles des servomoteurs en fonction de ce qu'on lui met dans les d

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

# Initialisation de Pygame
pygame.init()


# Taux de rafraîchissement
REFRESH_RATE = 5000

# Utilisé pour gérer la fréquence de rafraîchissement de l'écran
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()

# Game Loop
running = True

# Initialiser les angles des servomoteurs
d1 = 0
d2 = 0
d3 = 0
d4 = 0

# Paramètres de déplacement de la pince
p1= 0.025
p2= -0.025

print("hello")

while running:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Envoi des nouvelles positions aux servomoteurs dans CoppeliaSim
    sim.simxSetJointTargetPosition(clientID, D[0], math.radians(d1), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[1], math.radians(d2), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[2], math.radians(d3), sim.simx_opmode_blocking)
    sim.simxSetJointTargetPosition(clientID, D[3], math.radians(d4), sim.simx_opmode_blocking)
     
    # Attendre pour maintenir le taux de rafraîchissement
    clock.tick(REFRESH_RATE)

    # Afficher les valeurs des handles
    print(D)

    # fermeture communication avec client
sim.simxFinish(-1)