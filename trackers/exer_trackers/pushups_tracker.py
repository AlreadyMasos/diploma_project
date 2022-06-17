import cv2
import mediapipe as mp
from utils import counter_class

mp_pose = mp.solutions.pose


def track_pushups(filename):
    helper = counter_class.AngleCounter()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    counter_push = 0
    stage_push = None
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        cap = cv2.VideoCapture(filename)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                image.flags.writeable = False

                results = pose.process(image)

                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                try:
                    landmarks = results.pose_landmarks.landmark
                    # извлечение необходимых точек
                    knee_left = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

                    hip_left = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

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

                    angle_curls = helper.calculate_angle(shoulder_l,
                                                         hip_left,
                                                         knee_left)
                    # проверка условий для отжиманий
                    angle_wrist_r = helper.calculate_angle(shoulder_l, elbow_l, wrist_l)

                    angle_wrist_l = helper.calculate_angle(shoulder_r, elbow_r, wrist_r)
                    if (angle_wrist_l > 160 or angle_wrist_r > 160) and (angle_curls <= 180 and angle_curls >= 160):
                        stage_push = 'down'
                        startpoint_l = shoulder_l[0]

                    if (angle_wrist_l < 100 and stage_push == 'down' and shoulder_l[0] <= startpoint_l - 0.05 or
                        angle_wrist_r < 100 and stage_push == 'down') and (angle_curls <= 180 and angle_curls >= 160):
                        stage_push = 'up'
                        counter_push += 1

                except:
                    pass

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    return counter_push
