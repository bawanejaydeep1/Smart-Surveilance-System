import cv2
import datetime

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Define the codec for the color video
# color_fourcc = cv2.VideoWriter_fourcc(*'XVID')
# color_out = cv2.VideoWriter("output_color.avi", color_fourcc, 15.0, (1280, 720), isColor=True)

# Define the codec for the grayscale video
gray_fourcc = cv2.VideoWriter_fourcc(*'XVID')
gray_out = cv2.VideoWriter("output_gray.avi", gray_fourcc, 15.0, (1280, 720), isColor=False)

# Variables for motion detection and frame subsampling
motion_timer = 0  # Timer to track duration without motion
motion_detected = False  # Flag to indicate motion detection
motion_timeout = 150  # Timeout duration (in frames) without motion to stop saving
frame_count = 0  # Counter for frames processed
subsampling_rate = 5  # Capture every 5th frame

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

    motion_detected = False  # Reset motion detection flag for each frame

    for contour in contours:
        if cv2.contourArea(contour) < 5000:
            continue
        motion_detected = True  # Set motion detection flag if contour area is significant
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
        frame_count += 1
        if frame_count % subsampling_rate == 0:  # Check if current frame should be captured based on subsampling rate
            # color_out.write(frame1)  # Write color frame to color video file
            gray_frame = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
            gray_out.write(gray_frame)  # Write grayscale frame to grayscale video file
            cv2.imshow("feed", frame1)
    else:
        cv2.putText(frame1, "NOT RECORDING", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imshow("feed", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

# Release everything if job is finished
cap.release()
# color_out.release()
gray_out.release()
cv2.destroyAllWindows()
