import cv2
import numpy as np

# List of video paths
video_paths = [       # Option 2
    'Car Chase 1.mp4' ,
    'Car Chase 2.mp4' ,
    'Jet Dog Fight1.mp4'       # Option 3
]

# Create instruction screen
instruction_img = 135 * np.ones((400, 700, 3), dtype=np.uint8)

cv2.putText(instruction_img, "Press 1 for Station-1 tracking", (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
cv2.putText(instruction_img, "Press 2 for Station-2 tracking", (30, 150),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
cv2.putText(instruction_img, "Press 3 for Air footage tracking", (30, 200),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

cv2.imshow("Select Video", instruction_img)
key = cv2.waitKey(0)
cv2.destroyAllWindows()

# Select video based on key
if key == ord('1'):
    selected_video = video_paths[0]
elif key == ord('2'):
    selected_video = video_paths[1]
elif key == ord('3'):
    selected_video = video_paths[2]
else:
    print("Invalid key pressed. Exiting.")
    exit()

# Load selected video
cap = cv2.VideoCapture(selected_video)
if not cap.isOpened():
    print("Failed to open video.")
    exit()

# Initialize tracker
tracker = cv2.TrackerCSRT_create()

# Read the first frame
ret, frame = cap.read()
if not ret:
    print("Cannot read first frame.")
    cap.release()
    exit()

# Select object to track
bbox = cv2.selectROI("Select Object to Track", frame, False)

tracker.init(frame, bbox)

# Tracking loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    success, box = tracker.update(frame)

    if success:
        x, y, w, h = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, "Tracking", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Lost Track", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Object Tracking", frame)

    if cv2.waitKey(10) & 0xFF == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
