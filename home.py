import streamlit as st


st.set_page_config(
    page_title="AI Gym Guardian",
    page_icon="👋",
)
initial_reps = 12
if "reps" not in st.session_state:
    st.session_state["reps"] = initial_reps

initial_sets = 3
if "sets" not in st.session_state:
    st.session_state["sets"] = initial_sets


import base64
import streamlit as st
import plotly.express as px

df = px.data.iris()


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



with st.container():

    st.title('AI GYM GUARDIAN')
    st.caption('Your personal  :blue[Rep Counter] :sunglasses:')


    import hmac

    def check_password():
        """Returns `True` if the user had a correct password."""

        def login_form():
            """Form with widgets to collect user information"""
            with st.form("Credentials"):
                st.text_input("Username", key="username")
                st.text_input("Password", type="password", key="password")
                st.form_submit_button("Log in", on_click=password_entered)

        def password_entered():
            """Checks whether a password entered by the user is correct."""
            if st.session_state["username"] in st.secrets[
                "passwords"
            ] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["username"]],
            ):
                st.session_state["password_correct"] = True
                del st.session_state["password"]  # Don't store the username or password.
                del st.session_state["username"]
            else:
                st.session_state["password_correct"] = False

        # Return True if the username + password is validated.
        if st.session_state.get("password_correct", False):
            return True

        # Show inputs for username + password.
        login_form()
        if "password_correct" in st.session_state:
            st.error("😕 User not known or password incorrect")
        return False


    if not check_password():
        st.stop()
    st.subheader("WELCOME ")
    st.subheader("Choose your Exercise today")
    # streamlit_app.py


    # images start

    st.image('bicep.jpeg')


    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False



    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    # CSS for styling the button
    button_style = """
        <style>
        .centered-button {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 10vh;  /* Adjust height as needed */
        }
        #my-button {
            background-color: red;
            color: white;
            font-size: 24px;
            padding: 20px 40px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            cursor: pointer;
        }
        #my-button:hover {
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
        }
        </style>
        """

    # Inject the custom CSS
    st.markdown(button_style, unsafe_allow_html=True)

    # HTML wrapper for the button
    centered_button_html = """
        <div class="centered-button">
            <button id="my-button"> Bicep Curl</button>
        </div>
        """

    # Inject the HTML for the button
    st.markdown(centered_button_html, unsafe_allow_html=True)

    # JavaScript to trigger the Streamlit button click
    st.markdown("""
        <script>
        const button = document.getElementById('my-button');
        button.addEventListener('click', () => {
            window.location.href = window.location.href.split('?')[0] + "?button_clicked=true";
        });
        </script>
        """, unsafe_allow_html=True)


    st.divider()
    st.image('shoulder.jpg' )

    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False



    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    # CSS for styling the button
    button_style = """
        <style>
        .centered-button {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 10vh;  /* Adjust height as needed */
        }
        #my-button {
            background-color: red;
            color: white;
            font-size: 24px;
            padding: 20px 40px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            cursor: pointer;
        }
        #my-button:hover {
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
        }
        </style>
        """

    # Inject the custom CSS
    st.markdown(button_style, unsafe_allow_html=True)

    # HTML wrapper for the button
    centered_button_html = """
        <div class="centered-button">
            <button id="my-button">Shoulder Press</button>
        </div>
        """

    # Inject the HTML for the button
    st.markdown(centered_button_html, unsafe_allow_html=True)

    # JavaScript to trigger the Streamlit button click
    st.markdown("""
        <script>
        const button = document.getElementById('my-button');
        button.addEventListener('click', () => {
            window.location.href = window.location.href.split('?')[0] + "?button_clicked=true";
        });
        </script>
        """, unsafe_allow_html=True)

    # Check if the button was clicked


    st.image('squats.png' )

    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False



    # Initialize session state for button click
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    # CSS for styling the button
    button_style = """
        <style>
        .centered-button {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 10vh;  /* Adjust height as needed */
        }
        #my-button {
            background-color: red;
            color: white;
            font-size: 24px;
            padding: 20px 40px;
            border: none;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
            cursor: pointer;
        }
        #my-button:hover {
            box-shadow: 0 0 30px rgba(255, 0, 0, 0.8);
        }
        </style>
        """

    # Inject the custom CSS
    st.markdown(button_style, unsafe_allow_html=True)

    # HTML wrapper for the button
    centered_button_html = """
        <div class="centered-button">
            <button id="my-button">Squats</button>
        </div>
        """

    # Inject the HTML for the button
    st.markdown(centered_button_html, unsafe_allow_html=True)

    # JavaScript to trigger the Streamlit button click
    st.markdown("""
        <script>
        const button = document.getElementById('my-button');
        button.addEventListener('click', () => {
            window.location.href = window.location.href.split('?')[0] + "?button_clicked=true";
        });
        </script>
        """, unsafe_allow_html=True)

    # Check if the button was clicked





