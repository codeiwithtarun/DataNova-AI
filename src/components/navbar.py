import streamlit as st


def render_navbar():
    """
    Render the top navbar section.
    """

    st.markdown(
        """
        <h1 style='text-align: center;'>
             DataNova AI
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align: center; font-size:18px;'>
            Professional AI-Powered Data Cleaning Tool
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
