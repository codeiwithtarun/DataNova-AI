import streamlit as st

from src.auth.database import (
    create_user,
    login_user
)

st.title("Authentication")

option = st.selectbox(
    "Choose Option",
    ["Login", "Signup"]
)

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

if option == "Signup":

    if st.button("Signup"):

        success = create_user(
            email,
            password
        )

        if success:

            st.success(
                "Account Created Successfully"
            )

        else:

            st.error(
                "Email Already Exists"
            )

else:

    if st.button("Login"):

        user = login_user(
            email,
            password
        )

        if user:

            st.session_state.logged_in = True

            st.success(
                "Login Successful"
            )

        else:

            st.error(
                "Invalid Email or Password"
            )