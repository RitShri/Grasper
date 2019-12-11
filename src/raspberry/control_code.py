#Inspiration for this type of sensing and for the code came from https://gogul.dev/software/hand-gesture-recognition-p2
import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise
import serial
import time

background_image = None
BAUD = 9600 # Baud Rate
arduino = serial.Serial('/dev/ttyACM0', 9600) # Found with 'ls /dev/tty.*' [this changes each time the arduino is connected]
print("Serial Port is open: {}".format(arduino.is_open))
print("Baud Rate: {}".format(BAUD))

def run_avg(image, accumWeight):
    global background_image
    # initialize the background
    if background_image is None:
        background_image = image.copy().astype("float")
        return

    # compute weighted average, accumulate it and update the background
    cv2.accumulateWeighted(image, background_image, accumWeight)
    
def segment(image, threshold=20):
    global background_image
    # differnce of background and frame
    diff = cv2.absdiff(background_image.astype("uint8"), image)

    # threshold 
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # contour
    cnts, heir = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # return None, if no contours detected
    if len(cnts) == 0:
        return
    else:
        # based on contour area, get the maximum contour which is the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)
    
def count(thresholded, segmented):
    # convex hull
    chull = cv2.convexHull(segmented)

    # most extreme points
    extreme_top    = tuple(chull[chull[:, :, 1].argmin()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left   = tuple(chull[chull[:, :, 0].argmin()][0])
    extreme_right  = tuple(chull[chull[:, :, 0].argmax()][0])

    # center of the palm
    cX = int((extreme_left[0] + extreme_right[0]) / 2)
    cY = int((extreme_top[1] + extreme_bottom[1]) / 2)

    # maximum euclidean distance 
    distance = pairwise.euclidean_distances([(cX, cY)], Y=[extreme_left, extreme_right, extreme_top, extreme_bottom])[0]
    maximum_distance = distance[distance.argmax()]

    # radius of the circle 
    radius = int(0.8 * maximum_distance)

    # circumference of the circle
    circumference = (2 * np.pi * radius)

    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")
    
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    cnts, heir = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    count = 0

    for c in cnts:
        # compute the bounding box of the contour
        (x, y, w, h) = cv2.boundingRect(c)

        # increment the count of fingers only if -
        # 1. The contour region is not the wrist (bottom area)
        # 2. The number of points along the contour does not exceed
        #     25% of the circumference of the circular ROI
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count

class RobotHand():
    """
    RobotHand that plays Rock, Paper, Scissors
    """
    states = ("Rock", "Paper", "Scissors")

    def __init__(self):
        self.state = self.states[1]

    def state_transition(self, state):
        """
        Abstraction for an FSM to move from one state to another

        Args:
            state (str)
        """
        self.state = state

    def play_rock(self):
        """
        Activate servos that form Rock hand.
        """
        self.state_transition("Rock")
        print("Rock!")
        arduino.write(b"R")

    def play_paper(self):
        """
        Activate respective seros [list them here] to form paper hand.
        """
        self.state_transition("Paper")
        print("Paper!")
        arduino.write(b"P")

    def play_scissor(self):
        """
        Activate respecftive servos [list them here] to form the scissor hand.
        """
        self.state_transition("Scissor")
        print("Scissor!")
        arduino.write(b"S")

if __name__ == "__main__":
    # initialize accumulated weight
    accumWeight = 0.5

    # get the reference to the webcam
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize num of frames
    num_frames = 0

    # calibration indicator
    calibrated = False
    
    #when the hand is first seen
    frame_start = 0
    
    #how many frames the hand has to be the same
    hs = 150
    
    #array of if a hand was rock paper of scissors
    rps = [0,0,0]

    while(True):
        (grabbed, frame) = camera.read()

        frame = imutils.resize(frame, width=700)

        frame = cv2.flip(frame, 1)

        clone = frame.copy()

        (height, width) = frame.shape[:2]

        roi = frame[top:bottom, right:left]

        gray = cv2.cvtColor(roi, cv2.COLOR_background_imageR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        if num_frames < 30:
            run_avg(gray, accumWeight)
            if num_frames == 1:
                print("[STATUS] please wait! calibrating...")
            elif num_frames == 29:
                print("[STATUS] calibration successfull...")
        else:
            hand = segment(gray)
            
            if hand is not None:
                if frame_start == 0:
                    frame_start = num_frames
                if num_frames == frame_start + hs:
                    print(rps)
                    index = rps.index(max(rps))
                    h = RobotHand()
                    if index == 0:
                        print("see rock. will play paper")
                        h.play_paper()
                        time.sleep(5)
                    if index == 1:
                        print("see paper. will play scissor")
                        h.play_scissor()
                        time.sleep(5)
                    if index == 2:
                        print("see scissor. will play rock")
                        h.play_rock()
                        time.sleep(5)
                    rps = [0,0,0]
                    frame_start = num_frames
                    
                (thresholded, segmented) = hand

                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))

                fingers = count(thresholded, segmented)
    
                if fingers > 2:
                    rps[1] += 10
                elif fingers > 0:
                    rps[2] += 1
                else:
                    rps[0] += 1
                
                cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                
                cv2.imshow("Thesholded", thresholded)

        cv2.rectangle(clone, (left, top), (right, bottom), (0,255,0), 2)

        num_frames += 1

        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF

        if keypress == ord("q"):
            break

# free up memory
camera.release()
cv2.destroyAllWindows()