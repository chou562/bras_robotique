import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import pygame
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time

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

import msvcrt
def getch():
    return msvcrt.getch().decode()

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

# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

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

def capture_video():
    # Start video capture
    cap = cv2.VideoCapture(0)

    while True:
        # Read a frame

        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define color ranges for detection
        red_lower = np.array([0, 120, 70])
        red_upper = np.array([10, 255, 255])
        green_lower = np.array([40, 40, 40])
        green_upper = np.array([70, 255, 255])
        blue_lower = np.array([110,50,50])
        blue_upper = np.array([130,255,255])

        # Create masks for colors
        red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
        green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)
        blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper) 

        # Filtering to remove small noise
        red_mask = cv2.erode(red_mask, None, iterations=2)
        red_mask = cv2.dilate(red_mask, None, iterations=2)
        green_mask = cv2.erode(green_mask, None, iterations=2)
        green_mask = cv2.dilate(green_mask, None, iterations=2)
        blue_mask = cv2.erode(blue_mask, None, iterations=2)
        blue_mask = cv2.dilate(blue_mask, None, iterations=2)

        # Find contours for detected objects
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        blue_contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in red_contours:
            process_contour(contour, 'Red', frame)
            area = cv2.contourArea(contour)
            if area > 500:
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    print(f"Red Object Position: {cX}, {cY}")  # Print the position
                    cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)
                    cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)  # Optional: to visualize the center

        for contour in green_contours:
            process_contour(contour, 'Green', frame)
            #area = cv2.contourArea(contour)
            #if area > 500:
            #    M = cv2.moments(contour)
            #    if M["m00"] != 0:
            #        cX = int(M["m10"] / M["m00"])
            #        cY = int(M["m01"] / M["m00"])
            #        print(f"Green Object Position: {cX}, {cY}")  # Print the position
            #        cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            #        cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)  # Optional: to visualize the center

        for contour in blue_contours:
            process_contour(contour, 'Blue', frame)

        # Display the result
        cv2.imshow('Frame', frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

    def apply_filtering(mask):
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask

def process_contour(contour, color, frame):
    area = cv2.contourArea(contour)
    if area > 500:
        if color == 'Red':
            cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)
            # Ajouter la logique pour l'objet rouge
        elif color == 'Green':
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            # Ajouter la logique pour l'objet vert
        elif color == 'Blue':
            cv2.drawContours(frame, [contour], -1, (255, 0, 0), 3)
             # Ajouter la logique pour l'objet bleu

if __name__ == "__main__":
    capture_video()



