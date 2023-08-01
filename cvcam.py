import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def cvcapture():
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Your function that runs inside the OpenCV loop
        #frame = do_something(frame)
        
        cv2.imshow('opencv', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


