import streamlit as st
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
st.title("Settings")



# For the first selectbox and button
initial_reps = 10  # Set initial value to 10

if "reps" not in st.session_state:
    st.session_state["reps"] = initial_reps

reps = st.selectbox(
    "Select the Reps",
    (2, 8, 10, 12, 14, 16, 18, 20),
    key="reps_selectbox",
    index=(2, 8, 10, 12, 14, 16, 18, 20).index(st.session_state["reps"])  # Set initial index based on the initial value
)

submit_reps = st.button("Submit Reps", key="submit_reps_button")

if submit_reps:
    st.session_state["reps"] = reps
    st.write("You have entered: ", reps)

# For the second selectbox and button
initial_sets = 3  # Set initial value to 3

if "sets" not in st.session_state:
    st.session_state["sets"] = initial_sets

sets = st.selectbox(
    "Select the Sets",
    (2, 3, 4),
    key="sets_selectbox",
    index=(2, 3, 4).index(st.session_state["sets"])  # Set initial index based on the initial value
)

submit_sets = st.button("Submit Sets", key="submit_sets_button")

if submit_sets:
    st.session_state["sets"] = sets
    st.write("You have entered: ", sets)
