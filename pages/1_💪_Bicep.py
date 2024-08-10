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
st.title("BICEP CURLS")

# Read the video file
video_file = open('pages/Bicep.mp4', 'rb')
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

if st.button("Let's Start "):
    while(x>0):

        mp_drawing = mp.solutions.drawing_utils
        mp_pose = mp.solutions.pose


        def caluclate_angle(a, b, c):
            a = np.array(a)  # first
            b = np.array(b)  # secont
            c = np.array(c)  # third

            radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
            angle = np.abs(radians * 180.0 / np.pi)

            if angle > 180:
                angle = 360 - angle

            return angle


        bot = pyttsx3.init()
        bot.say(" hi  , I           am         ai         GYM       GUARDIAN")
        bot.say(" Current Exercise : Bicep curl")
        if(x ==3):
             bot.say(f" Remaining sets : 3")
        elif(x ==2):
             bot.say(f" Remaining sets : 2")
        elif(x ==1):
             bot.say(f" Remaining sets : 1")
        bot.runAndWait()

        cap = cv2.VideoCapture(0)

        # curl counter
        counter = 0
        flag = 0
        test = 0
        stage = None
        stat = None
        eror = "start"
        color = (0, 255, 0)
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
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                    Rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    Relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    Rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                    # CALculate angle
                    angle = caluclate_angle(shoulder, elbow, wrist)
                    Rangle = caluclate_angle(Rshoulder, Relbow, Rwrist)

                    # visulize angle
                    cv2.putText(image, f"{angle:.1f}",
                                tuple(np.multiply(elbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
                    cv2.putText(image, f"{Rangle:.1f}",
                                tuple(np.multiply(Relbow, [640, 480]).astype(int)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )

                    # Curl counter logic
                    if (angle > 150 and Rangle > 150):
                        stage = 'UP'

                    if (angle < 30 or Rangle < 30) and stage == "UP":
                        stage = "DOWN"

                        counter += 0.5

                    # instruction to print
                    if (angle > 150) or (Rangle > 150):
                        stat = "up"

                    if angle < 30 or Rangle < 30:
                        stat = "down"

                    # caluclatinf tume between reps
                    if (angle > 150 and Rangle < 30):
                        first_visit_time = time.time()

                    if (angle < 30 and Rangle > 150):
                        second_visit_time = time.time()

                        # priting hold and erors using time differrence
                    time_difference = second_visit_time - first_visit_time
                    if (np.abs(time_difference) < 3):
                        stat = "Hold"

                        flag = 0

                    else:
                        flag = 1
                        color = (0, 255, 0)
                        eror = "Going good"
                        test = counter

                    if (flag == 0 and (test + 1) < counter):
                        eror = "Too Fast"
                        color = (0, 0, 255)



                except:
                    pass

                # Reneder count box
                # setup status box
                cv2.rectangle(image, (5, 5), (275, 85), (245, 117, 16), -1)
                cv2.rectangle(image, (550, 5), (350, 85), color, -1)
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

                cv2.putText(image, "Faults", (400, 18),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
                cv2.putText(image, eror, (385, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 0, cv2.LINE_AA)

                # rendor detection
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 177, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                cv2.imshow('Mediapipe feed ', image)

                if (cv2.waitKey(10) & 0xFF == ord('q') )or (counter >= y) :
                        break

        cap.release()
        cv2.destroyAllWindows()
        x -= 1