#importing OpenCV,time and Pandas library
import cv2 , time , pandas
#importing datetime class from datetime library
from datetime import datetime

#assigning our static_back to None
static_back = None

#list when any moving object appear
motion_list = [ None , None ]
#time of movement
time = []
#initializing DataFrame, one column is start time and other column is end time
df = pandas.DataFrame(columns = ["Start" , "End"])
#capturing video
video = cv2.VideoCapture(0)
#infinite while loop to treat stack of image as video
while True:
    #reading frame(image) from video
    check , frame = video.read()
    #initializing motion=0(no motion)
    motion = 0
    # converting color image to gray_scale image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #converting gray scale image to GaussianBlur so that change can be find easily
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    #in first iteration we assign the value of static_back to our first frame
    if static_back is None:
        static_back = gray
        continue
    #difference between static background and current frame(which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back, gray)
    #if change in between static background and
    #current frame is greater than 30 it will show white color(255)
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    #finding contour of moving object
    (_,cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1

        (x,y,w,h) = cv2.boundingRect(contour)
        #making green rectangle arround the moving object
        cv2.rectangle(frame, (x, y), (x+w,y+h), (0, 255, 0), 3)
    #appending status of motion
    motion_list.append(motion)

    motion_list = motion_list[-2:]
    #appending Start time of motion
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time.append(datetime.now())
    #appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time.append(datetime.now())
    #displaying image in gray_scale
    cv2.imshow("Gray Frame", gray)
    #displaying the difference in currentframe to
    # the staticframe(very first_frame)
    cv2.imshow("Difference Frame", diff_frame)
    #diplaying the black and white image in which if
    #intencity difference greater than 30 it will appear white
    cv2.imshow("Threshold Frame", thresh_frame)
    #displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)
    #if q entered whole process will stop
    if key == ord('q'):
        #if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break
#appending time of motion in DataFrame
for i in range(0, len(time), 2):
    df = df.append({"Start":time[i], "End":time[i+1]}, ignore_index=True)
#creating a csv file in which time of movements will be saved
df.to_csv("Time_of_movements.csv")

video.release()
#destroying all the windows
cv2.destroyAllWindows()
