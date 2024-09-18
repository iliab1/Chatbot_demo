import streamlit as st

# Set page configuration
st.set_page_config(page_title="Company Landing Page", layout="centered")

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .css-1aumxhk {padding-top: 2rem;} /* Adjust top padding */
    .css-1d391kg {padding-bottom: 2rem;} /* Adjust bottom padding */
    </style>
    """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Display company logo
#st.image("static/logo-placeholder.png", width=300)

# Set the title of the landing page with a larger font size
st.markdown("<h1 style='text-align: center; font-size: 2.5rem; color: #4A90E2;'>Welcome to the AI Chatbot Demo</h1>", unsafe_allow_html=True)

# Add a brief description or call-to-action with a subtle style
st.markdown("""
<div style="text-align: center; font-size: 1.2rem; color: #FFF;">
    Proceed to chat with documents or use advanced agents to explore thier AI capabilities.
</div>
""", unsafe_allow_html=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Add buttons with custom styles to enhance appearance
col1, col2 = st.columns(2, gap="large")

with col1:
    if st.button("Chat with Documents", use_container_width=True):
        st.switch_page("pages/1_Chat_with_Documents.py")

with col2:
    if st.button("Chat with Agent", use_container_width=True):
        st.switch_page("pages/2_Chat_with_Agent.py")

# Add a subtle footer or contact info (optional)
st.markdown("""
<hr style="border-top: 1px solid #eee; margin-top: 3rem; margin-bottom: 1rem;">
<div style="text-align: center; font-size: 0.9rem; color: #FFF;">
    © 2024 Ilia Bukin. All rights reserved.
</div>
""", unsafe_allow_html=True)
