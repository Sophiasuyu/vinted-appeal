import streamlit as st
import requests
import time
import requests


st.set_page_config(page_title="Appeal with Care", layout="centered")

st.markdown("""
    <style>
    .main, .block-container {
        background: linear-gradient(270deg, #fefcea, #f1f5f9, #e0f7fa);
        background-size: 600% 600%;
        animation: gradientFlow 18s ease infinite;
    }

    @keyframes gradientFlow {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    html, body {
        transition: background 1s ease-in-out;
    }

    .stButton button {
        background-color: #00BFA6;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1.2rem;
        border: none;
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(0, 191, 166, 0.2);
    }
    .stButton button:hover {
        background-color: #00a08b;
        box-shadow: 0 4px 12px rgba(0, 160, 139, 0.3);
    }

    textarea, input {
        background-color: #ffffff !important;
        border: 1px solid #ccc !important;
        border-radius: 6px !important;
        transition: all 0.3s ease-in-out;
    }

    .stMarkdown h3, .stMarkdown h4 {
        color: #333333;
        font-family: 'Segoe UI', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Platform Appeal Assistant")
st.markdown("We're here to listen. Let’s figure this out together. 💬")

user_id = st.text_input("Enter your User ID")
st.markdown("**Have you done any of the following recently?**")

options = [
    "Posted a lot of items",
    "Switched accounts frequently",
    "Logged in from a different location",
    "Had disputes with other users",
    "Other (please specify)",
    "None of the above"
]

selected_options = st.multiselect("Select all that apply:", options)

custom_input = ""
if "Other (please specify)" in selected_options:
    custom_input = st.text_area("Please describe anything else that might have happened:")

uploaded_file = st.file_uploader("Upload any screenshots or files to support your case:")

if st.button("Submit Appeal"):
    if not user_id:
        st.warning("Please enter your User ID")
    else:
        final_reason = ", ".join(selected_options)
        if custom_input:
            final_reason += f" | Details: {custom_input}"

        data = {"flag_reason": final_reason}
        res = requests.post(f"http://localhost:8000/appeals/{user_id}", json=data)
        st.success("Thanks for sharing. We’re now reviewing your case...")
        with st.spinner("⏳ Processing..."):
            time.sleep(2)
            ai_feedback = requests.get(f"http://localhost:8000/ai_feedback/{user_id}").json()

        import random
        if random.random() < 0.9:
            st.markdown("""
            <div style='padding: 1rem; background-color: #e0f8ec; border-radius: 10px; border-left: 6px solid #00BFA6;'>
            <h3>✅ Account Restored</h3>
            <p>Your account is now active again. Thanks for your patience and understanding.</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div style='padding: 1rem; background-color: #fef4e5; border-radius: 10px; border-left: 6px solid #ffb347;'>
            <h3> Sent for Human Review</h3>
            <p>We couldn't fully resolve this automatically. Our support team has received your case and will follow up soon.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("""
        ### AI Review Summary
        {}

        ### Human-Centered Response
        {}
        """.format(
            ai_feedback.get("review_summary"),
            ai_feedback.get("human_touch")
        ))

# AI Chatbot
st.markdown("---")
st.subheader("Need to talk to our AI assistant?")
st.markdown("You can ask anything about your account, the appeal process, or just share how you're feeling.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

chat_input = st.chat_input("Ask me something…")

if chat_input:
    st.session_state.chat_history.append(("user", chat_input))
    with st.spinner("AI is thinking..."):
       ollama_response = requests.post(
         "http://localhost:11434/api/generate",
         json={
           "model": "llama3.2",
             "prompt": f"You are a kind, empathetic platform assistant. Help this user: {chat_input}",
            "stream": False
          }
     )

    resp_json = ollama_response.json()
    ai_reply = ollama_response.json().get("response", "[No response]")

    st.session_state.chat_history.append(("ai", ai_reply))

 
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)
