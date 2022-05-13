from library import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

# create capture object
cap = cv2.VideoCapture(0)
existance_of_body = False # bool variable that detect state of body existance

while cap.isOpened():
    # read frame from capture object
    _, frame = cap.read()
    try:

        # convert the frame to RGB format
        RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # process the RGB frame to get the result
        results = pose.process(RGB)
        mp_drawing.draw_landmarks(
        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        # show the final output

        #qr code reader
        for barcode in decode(frame):
            text = barcode.data.decode('utf-8')
            polygon_Points = np.array([barcode.polygon], np.int32)
            polygon_Points=polygon_Points.reshape(-1,1,2)
            rect_Points= barcode.rect
            cv2.polylines(frame,[polygon_Points],True,(255,255, 0), 5)
            cv2.putText(frame, text, (rect_Points[0],rect_Points[1]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,255, 0), 2)
        #end of qr code detection

        #detect if the body detected or not
        if str(results.pose_landmarks)=="None":
            existance_of_body=False
        else:
            existance_of_body=True
        #end of check existance of the body

        cv2.imshow('Output', frame)
    except:
        break
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()