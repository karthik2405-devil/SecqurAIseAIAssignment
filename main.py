#considering the color of the ball
import cv2
import numpy as np
import time

# Read the input video
cap = cv2.VideoCapture("Video.mp4")

# Initialize variables to store the coordinates
top_left = (float('inf'), float('inf'))
top_right = (float('-inf'), float('inf'))
bottom_left = (float('inf'), float('-inf'))
bottom_right = (float('-inf'), float('-inf'))

# Define the range of colors for the ball in the HSV color space
lower_color = np.array([0,50,6])
upper_color = np.array([180,255,255])

# Set up the alternative detector
# for example using `cv2.HoughCircles`

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and resize the frame
    frame = cv2.flip(frame, flipCode=-1)
    frame = cv2.resize(frame, (500,500))

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Threshold the frame to only select the ball color
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Use the alternative detector to find the center of the ball
   # Use the alternative detector to find the center of the ball
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)
    if circles is not None:
        # Ball detected
        print("Ball detected")
        circles = np.round(circles[0, :]).astype("int")

        # Draw a circle around the center of the ball
        for (x, y, r) in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)

        # Find the top-left, top-right, bottom-left, and bottom-right coordinates of the ball
        for (x, y, r) in circles:
            if x <= top_left[0] and y <= top_left[1]:
                top_left = (x, y)
            if x >= top_right[0] and y <= top_right[1]:
                top_right = (x, y)
            if x <= bottom_left[0] and y >= bottom_left[1]:
                bottom_left = (x, y)
            if x >= bottom_right[0] and y >= bottom_right[1]:
                bottom_right = (x, y)
        print("Top Left: ", top_left)
        print("Top Right: ", top_right)
        print("Bottom Left: ", bottom_left)
        print("Bottom Right: ", bottom_right)
        
        # Determine in which quadrant the ball is located
        if x < frame.shape[1]/2 and y < frame.shape[0]/2:
            quadrant = "top-left"
        elif x >= frame.shape[1]/2 and y < frame.shape[0]/2:
            quadrant = "top-right"
        elif x < frame.shape[1]/2 and y >= frame.shape[0]/2:
            quadrant = "bottom-left"
        else:
            quadrant = "bottom-right"
        print("Ball is in: ", quadrant)
        
        # Get the current timestamp
        timestamp = time.time()
        print("Timestamp: ", timestamp)
        
        # Write the timestamp and quadrant to a file
        with open("1.txt", "a") as f:
            f.write(str(timestamp) + ": Ball entered the " + quadrant + " quadrant\n")
    # else:
    #     print("Ball not detected")

    # Display the frame
    cv2.imshow('window', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

# Release the video capture and destroy the windows
cap.release()
cv2.destroyAllWindows()

