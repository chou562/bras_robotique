import cv2
import numpy as np
import matplotlib.pyplot as plt

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

        # Create masks for colors
        red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)
        green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

        # Filtering to remove small noise
        red_mask = cv2.erode(red_mask, None, iterations=2)
        red_mask = cv2.dilate(red_mask, None, iterations=2)
        green_mask = cv2.erode(green_mask, None, iterations=2)
        green_mask = cv2.dilate(green_mask, None, iterations=2)

        # Find contours for detected objects
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Process each contour
        for contour in red_contours + green_contours:
            area = cv2.contourArea(contour)
            if area > 500:  # Filter out small objects
                # Draw contour and decide on action based on color
                color = 'Red' if contour in red_contours else 'Green'
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                # TODO: Add your robotic arm control logic here

        # Display the result
        cv2.imshow('Frame', frame)

        # Break the loop with 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_video()
