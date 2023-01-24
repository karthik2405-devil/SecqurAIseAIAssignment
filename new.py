
import cv2
import datetime
import numpy as np
# Define the minimum and maximum radius of the balls to detect

def get_quadrant(x, y, cx, cy):
    """
    Helper function to determine in which quadrant of the frame the center of the ball is located.
    """
    if x < cx and y < cy:
        return "top-left"
    elif x > cx and y < cy:
        return "top-right"
    elif x < cx and y > cy:
        return "bottom-left"
    else:
        return "bottom-right"


min_radius = 5
max_radius = 50

# Create a VideoCapture object to read the video
cap = cv2.VideoCapture("video.mp4")

# Open a new file to write the timestamps, quadrants and coordinates of the balls
file = open("2.txt", "w")

while True:
    # Read the next frame from the video
    ret, frame = cap.read()

    # Check if the video has ended
    if not ret:
        break
    frame=cv2.resize(frame,(600,400))
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a Gaussian blur to the frame
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use the HoughCircles function to detect circles in the frame
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=min_radius, maxRadius=max_radius)

    # Check if any circles were detected
    if circles is not None:
        # Convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")

        # Get the current timestamp
        timestamp = str(datetime.datetime.now())

        # Write the timestamp to the file
        file.write("Timestamp: " + timestamp + "\n")

        # Iterate over the circles
        for (x, y, r) in circles:
            # Draw a circle around the ball
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            
            # Write the coordinates and quadrant of the ball to the file
            file.write("Ball: x: " + str(x) + " y: " + str(y) + " quadrant:" + get_quadrant(x, y, frame.shape[1]//2, frame.shape[0]//2)+"\n")
    
    # Show the frame
    cv2.imshow("Frame", frame)

    # Check if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture object
cap.release()

# Close the file
file.close()

# Close all the windows
cv2.destroyAllWindows()

