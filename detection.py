# import cv2
# import datetime

# cap = cv2.VideoCapture(0)
# cap.set(3, 1280)
# cap.set(4, 720)
# frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
# out = cv2.VideoWriter("output.avi", fourcc, 15.0, (1280, 720))

# # Variables for motion detection
# motion_timer = 0  # Timer to track duration without motion
# motion_detected = False  # Flag to indicate motion detection
# motion_timeout = 25  # Timeout duration (in frames) without motion to stop saving

# ret, frame1 = cap.read()
# ret, frame2 = cap.read()
# while cap.isOpened():
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     cv2.putText(frame2, timestamp, (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#     diff = cv2.absdiff(frame1, frame2)
#     gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
#     blur = cv2.GaussianBlur(gray, (5, 5), 0)
#     _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
#     dilated = cv2.dilate(thresh, None, iterations=3)
#     contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#     motion_detected = False  # Reset motion detection flag for each frame


#     for contour in contours:
#         if cv2.contourArea(contour) < 5000:
#             continue
#         motion_detected = True  # Set motion detection flag if contour area is significant
#         (x, y, w, h) = cv2.boundingRect(contour)
#         cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

#     if motion_detected:
#         motion_timer = 0  
#     else:
#         motion_timer += 1  

#     if motion_timer < motion_timeout:
#         image = cv2.resize(frame1, (1280, 720))
#         out.write(image)
#         cv2.imshow("feed", frame1)
    

#     frame1 = frame2
#     ret, frame2 = cap.read()

#     if cv2.waitKey(40) == 27:
#         break

# cv2.destroyAllWindows()
# cap.release()
# out.release()

import cv2
import datetime

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
out = cv2.VideoWriter("output.avi", fourcc, 15.0, (1280, 720))


motion_timer = 0  
motion_detected = False
motion_timeout = 150

ret, frame1 = cap.read()
ret, frame2 = cap.read()
while cap.isOpened():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame2, timestamp, (10, frame_height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False 

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        motion_detected = True  
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    if motion_detected:
        motion_timer = 0
    else:
        motion_timer += 1


    time_since_movement = motion_timer / 15  
    cv2.putText(frame1, f"Time since last movement: {time_since_movement:.2f} seconds", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    if motion_timer < motion_timeout:
        image = cv2.resize(frame1, (1280, 720))
        out.write(image)
        cv2.imshow("feed", frame1)
    else:
        # cv2.putText(frame1, f"NOT RECORDING: {time_since_movement:.2f} seconds", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
        cv2.putText(frame1, "NOT RECORDING", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imshow("feed", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

cv2.destroyAllWindows()
cap.release()
out.release()
