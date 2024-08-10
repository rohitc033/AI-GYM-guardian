import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
import time
import pyttsx3
import base64

def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


img = get_img_as_base64("img22.jpeg")


page_bg_img = f"""
<style>


[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");

width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-attachment: fixed;
  background-size: cover;
  background-position: center; 
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def caluclate_angle(a, b, c):
    a = np.array(a)  # first
    b = np.array(b)  # secont
    c = np.array(c)  # third

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180:
        angle = 360 - angle

    return angle


st.title("Squats")

# Read the video file
video_file = open('pages/squats.mp4', 'rb')
video_bytes = video_file.read()

# Get the video bytes and encode them in base64
import base64

video_base64 = base64.b64encode(video_bytes).decode('utf-8')

# Define the HTML to embed the video with autoplay and loop
video_html = f'''
    <video width="100%" height="auto" controls autoplay loop>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
'''

# Display the video in Streamlit using custom HTML
st.markdown(video_html, unsafe_allow_html=True)

st.divider()

st.subheader("Basic rules")

st.write(':blue[1] : Check out video for reference ')
st.write(':blue[2] : Follow up the instructions block that appears ')
st.write(':blue[3] : If Fault block becomes :red[red] color,slow down  ')
st.write(':blue[4] : If Error block becomes :red[red] color, follow it up  ')
st.write(':blue[5] : We will count reps for you   ')

st.divider()  # 👈 Another horizontal rule

st.write("Reps Count", st.session_state["reps"])
st.write("Sets Count", st.session_state["sets"])

st.divider()  # 👈 Another horizontal rule
y = st.session_state["reps"]
x = st.session_state["sets"]
wrong_reps_1 = 0
wrong_reps_2 = 0
wrong_reps_3 = 0
if st.button("Let's Start "):
    while (x > 0):

        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose
        bot = pyttsx3.init()
        bot.say(" hi  , I           am         ai         GYM       GUARDIAN")
        bot.say(" Current Exercise :  Squats")
        if (x == 3):
            bot.say(f" Remaining sets : 3")
        elif (x == 2):
            bot.say(f" Remaining sets : 2")
        elif (x == 1):
            bot.say(f" Remaining sets : 1")
        bot.runAndWait()

        cap = cv2.VideoCapture(0)

        # curl counter
        counter = 0
        flag = 0
        test = 0
        wrong_rep = 0
        temp = 0
        stage = None
        stat = None
        fault = None
        eror = "start"
        color = (0, 255, 0)
        color_for_fault = (0, 255, 0)
        # Variable to store the time of the first visit
        first_visit_time = None
        second_visit_time = None
        time_difference = None

        # setup mediapipe instance
        with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
            while cap.isOpened():
                ret, frame = cap.read()

                # recolor imgaes
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # make ddetectios
                results = pose.process(image)

                # recolor back to bgr
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # extract landmarks
                try:
                    landmarks = results.pose_landmarks.landmark

                    # get cordinates
                    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                    left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                    left_heel = [landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].x,
                                 landmarks[mp_pose.PoseLandmark.LEFT_HEEL.value].y]
                    left_index = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

                    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
                    right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
                    right_heel = [landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].x,
                                  landmarks[mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
                    right_index = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

                    # CALculate angle
                    left_leg = caluclate_angle(left_hip, left_knee, left_heel)
                    right_leg = caluclate_angle(right_hip, right_knee, right_heel)
                    left_ankle = caluclate_angle(left_knee, left_heel, left_index)
                    right_ankle = caluclate_angle(right_knee, right_heel, right_index)

                    # visulize angle
                    cv2.putText(image, f"{left_leg:.1f}",
                                tuple(np.multiply(left_knee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    cv2.putText(image, f"{right_leg :.1f}",
                                tuple(np.multiply(right_knee, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    cv2.putText(image, f"{left_ankle:.1f}",
                                tuple(np.multiply(left_heel, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    cv2.putText(image, f"{right_ankle:.1f}",
                                tuple(np.multiply(right_heel, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    # Curl counter logic
                    if left_leg < 90 and right_leg < 90:
                        stage = 'DOWN'

                    if left_leg > 170 and right_leg > 170 and stage == "DOWN":
                        stage = "UP"

                        counter += 1

                    # instruction to print
                    if left_leg < 90 and right_leg < 90:
                        stat = "up"

                    if left_leg > 170 and right_leg > 170:
                        stat = "down"

                    # caluclatinf tume between reps
                    if left_leg > 170 and right_leg > 170:
                        first_visit_time = time.time()

                    if left_leg < 90 and right_leg < 90:
                        second_visit_time = time.time()

                    # priting hold and erors using time differrence

                    time_difference = second_visit_time - first_visit_time

                    if (np.abs(time_difference) < 2):
                        flag = 0

                    else:
                        flag = 1
                        color = (0, 255, 0)
                        eror = "Going good"
                        test = counter

                    if (flag == 0 and (test + 1) < counter):
                        eror = "Too Fast"
                        color = (0, 0, 255)

                        # fault section4

                    if (left_leg < 90 and right_leg < 90) and (left_ankle < 80 and right_ankle < 80):
                        fault = "**Moving Knees forward**"
                        color_for_fault = (0, 0, 255)
                    else:
                        fault = "Good"
                        color_for_fault = (0, 255, 0)

                    # checking for wrong reps
                    if ((color == (0, 0, 255) or color_for_fault == (0, 0, 255)) and temp != counter):
                        wrong_rep += 0.5
                        temp = counter

                except:
                    pass

                # Reneder count box
                # setup status box
                cv2.rectangle(image, (5, 5), (275, 85), (245, 117, 16), -1)
                cv2.rectangle(image, (550, 5), (350, 85), color, -1)
                cv2.rectangle(image, (6000, 505), (350, 420), color_for_fault, -1)
                # rep data
                # redata
                cv2.putText(image, "Reps", (18, 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, str(counter), (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(image, "Instruction", (125, 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, stat, (145, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

                cv2.putText(image, "Speed", (400, 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, eror, (385, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 0, cv2.LINE_AA)

                cv2.putText(image, "Faults", (400, 420),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, fault, (385, 450),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 0, cv2.LINE_AA)

                # rendor detection
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 177, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                cv2.imshow('Mediapipe feed ', image)

                if (cv2.waitKey(10) & 0xFF == ord('q')) or counter >= y:
                    break




                if (x == 3):
                    wrong_reps_1 = wrong_rep
                elif (x == 2):
                    wrong_reps_2 = wrong_rep
                elif (x == 1):
                    wrong_reps_3 = wrong_rep
        cap.release()
        cv2.destroyAllWindows()

        x -= 1
        wrong_reps = wrong_rep


def is_strict_float(number):
    if isinstance(number, float):
        if number.is_integer():
            return False  # It's a float but equivalent to an integer
        return True
    return False

if is_strict_float(wrong_reps_1):
    wrong_rep_1 = wrong_reps_1 + 0.5
else:
    pass

if is_strict_float(wrong_reps_2):
    wrong_rep_2 = wrong_reps_2 + 0.5
else:
    pass

if is_strict_float(wrong_reps_1):
    wrong_rep_3 = wrong_reps_3 + 0.5
else:
    pass

st.write("Wrong Reps in set 1 ", wrong_reps_1)
st.write("Wrong Reps in set 2 ", wrong_reps_2)
st.write("Wrong Reps in set 3", wrong_reps_2)