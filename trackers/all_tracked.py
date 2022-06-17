import cv2
import numpy as np 
import mediapipe as mp
import time
from utils import counter_class

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

 
helper = counter_class.AngleCounter
counter = 0
pushup_counter = 0
squats_counter = 0
curls_counter = 0
stage = None
pTime = 0
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        try:
            landmarks = results.pose_landmarks.landmark
            knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                         landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                           landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            shoulder_l = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

            elbow_l = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            wrist_l = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            shoulder_r = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            elbow_r = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            wrist_r = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # проверка условий для приседаний
            angle_knee_left = helper.calculate_angle(hip_left,
                                                     knee_left,
                                                     ankle_left)

            angle_knee_right = helper.calculate_angle(hip_right,
                                                      knee_right,
                                                      ankle_right)
            angle_wrist_r = helper.calculate_angle(shoulder_l, elbow_l, wrist_l)

            angle_wrist_l = helper.calculate_angle(shoulder_r, elbow_r, wrist_r)

            angle_curls = helper.calculate_angle(shoulder_l, hip_left, knee_left)

            if (angle_wrist_l > 160 or angle_wrist_r > 160) and (angle_curls <= 180 and angle_curls >= 160):
                stage_push = 'down'
                startpoint_l = shoulder_l[0]

            if (angle_wrist_l < 100 and stage_push == 'down' and shoulder_l[0] <= startpoint_l - 0.05 or
                    angle_wrist_r < 100 and stage_push == 'down') and (angle_curls <= 180 and angle_curls >= 160):
                stage_push = 'up'
                pushup_counter += 1
            cv2.putText(image, str(round(angle_wrist_l)),
                           tuple(np.multiply(elbow_l, [640, 480]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 10), 2, cv2.LINE_AA
                                )
            
            cv2.putText(image, str(round(angle_knee_left)),
                           tuple(np.multiply(knee_left, [640, 480]).astype(int)),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 10), 2, cv2.LINE_AA
                                )

            cv2.putText(image, str(round(angle_curls)),
                        tuple(np.multiply(hip_left, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA
                        )

            #cv2.putText(image, str(round(angle_knee_right)),
                           #tuple(np.multiply(knee_right, [640, 480]).astype(int)),
                           #cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 10), 2, cv2.LINE_AA
                           #     )
            if angle_curls > 120:
                stage_curls = 'down'
            if angle_curls < 115:
                stage_curls = 'up'
                curls_counter += 1
            if angle_knee_left > 160 and angle_knee_right > 160:
                stage_knee = 'down'
                starter = hip_left[1]
            if (angle_knee_left <= 130 and angle_knee_right <= 130
                    and stage_knee == 'down' and hip_left[1] >= starter + 0.1):
                stage_knee = 'up'
                squats_counter += 1
        except:
            pass
        
        # отображение кол-ва повторений
        cv2.putText(image, 'reps', (15,12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1, cv2.LINE_AA)

        cv2.putText(image, str(squats_counter) + ' squats', 
                    (10,100), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)
        
        cv2.putText(image, str(pushup_counter) + ' pushups', 
                    (10,150),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 2, cv2.LINE_AA)

        """cv2.putText(image, str(curls_counter) + ' curls',
                    (10, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)"""
        
        # отображение текущий стадии скручивания
        mp_drawing.draw_landmarks(image, results.pose_landmarks, 
                                mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(220,117,65),thickness=2,circle_radius=2),
                                mp_drawing.DrawingSpec(color=(220,60,120),thickness=2,circle_radius=2))

        cv2.imshow('DIPLOMA', image)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

print(counter)