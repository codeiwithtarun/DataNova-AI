import streamlit as st


def render_sidebar():

    st.sidebar.title("DataNova AI")

    selected_option = st.sidebar.radio(
        "Navigation",
        [
            "Home",
            "Upload Dataset",
            "Data Cleaning",
            "Visualization",
            "EDA Analysis",
            "AI Suggestions",
            "Reports",
            "AI Chatbot"
        ]
    )

    return selected_option
