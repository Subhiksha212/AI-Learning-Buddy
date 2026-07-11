import streamlit as st
import google.generativeai as genai

# -----------------------------
# Gemini Configuration
# -----------------------------
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Learning Buddy",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Learning Buddy")

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "saved_chats" not in st.session_state:
    st.session_state.saved_chats = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("💬 Chat History")

    if st.button("➕ New Chat"):

        # Save current chat before clearing
        if len(st.session_state.messages) > 0:

            first_question = "New Chat"

            for msg in st.session_state.messages:

                if msg["role"] == "user":

                    title_prompt = f"""
Generate a short chat title (maximum 5 words).

Conversation:
{msg["content"]}

Return ONLY the title.
"""

                    try:
                        title = model.generate_content(title_prompt)
                        first_question = title.text.strip()

                    except:
                        first_question = msg["content"][:30]

                    break

            # Avoid duplicate chats
            exists = False

            for chat in st.session_state.saved_chats:
                if chat["messages"] == st.session_state.messages:
                    exists = True
                    break

            if not exists:
                st.session_state.saved_chats.append(
                    {
                        "title": first_question,
                        "messages": st.session_state.messages.copy()
                    }
                )

        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if len(st.session_state.saved_chats) == 0:
        st.info("No previous chats")

    else:

        for i, chat in enumerate(reversed(st.session_state.saved_chats)):

            if st.button(chat["title"], key=f"chat_{i}"):

                st.session_state.messages = chat["messages"]
                st.rerun()

# -----------------------------
# Display Messages
# -----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat Input
# -----------------------------
prompt = st.chat_input("Ask me anything...")

if prompt:

    # User message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = model.generate_content(prompt)
            answer = response.text

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()
