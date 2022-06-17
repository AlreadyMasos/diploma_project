import cv2
import mediapipe as mp
from utils import counter_class

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

 
helper = counter_class.AngleCounter
counter = 0
stage = None
stage_knee = None


def squat_track(filename):
    helper = counter_class.AngleCounter()
    mp_pose = mp.solutions.pose
    counter_sq = 0
    stage_knee = None
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

                    ankle_left = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

                    knee_right = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

                    hip_right = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

                    ankle_right = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

                    # проверка условий для приседаний
                    angle_knee_left = helper.calculate_angle(hip_left,
                                                             knee_left,
                                                             ankle_left)

                    angle_knee_right = helper.calculate_angle(hip_right,
                                                              knee_right,
                                                              ankle_right)

                    if angle_knee_left > 160 and angle_knee_right > 160:
                        stage_knee = 'down'
                        starter = hip_left[1]
                    if (angle_knee_left <= 130 and angle_knee_right <= 130
                            and stage_knee == 'down' and hip_left[1] >= starter + 0.1):
                        stage_knee = 'up'
                        counter_sq += 1

                except:
                    pass

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    return counter_sq
