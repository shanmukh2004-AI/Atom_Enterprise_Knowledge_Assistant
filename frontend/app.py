import streamlit as st
import requests
import time
BACKEND_URL = "http://127.0.0.1:8000"

# =========================
# API HELPER FUNCTION
# =========================
def api_post(endpoint, payload):
    try:
        response = requests.post(
            f"{BACKEND_URL}/{endpoint}",
            json=payload,
            timeout=60
        )
        if response.status_code == 200:

            return response.json()
        return {
            "error": "Server error occurred."
        }
    except requests.exceptions.Timeout:
        return {
            "error": "Server timeout. Try again."
        }
    except requests.exceptions.ConnectionError:
        return {
            "error": "Backend server is not running."
        }
    except Exception:
        return {
            "error": "Something went wrong."
        }

st.set_page_config(page_title="Atom AI", layout="wide")
# =========================
# SESSION STATE
# =========================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}
if "current_chat" not in st.session_state:
    st.session_state.current_chat = None
if "edit_index" not in st.session_state:
    st.session_state.edit_index = None
# =========================
# SIDEBAR UPLOAD
# =========================
with st.sidebar:
    st.title("📂 Upload Knowledge Base")
    uploaded_files = st.file_uploader(
    "Upload files",
    type=["txt", "md", "json", "html", "csv"],
    accept_multiple_files=True
    )
    st.divider()
    if st.button("➕ New Chat"):
        chat_id = f"chat_{len(st.session_state.chat_history) + 1}"
        st.session_state.chat_history[chat_id] = []
        st.session_state.current_chat = chat_id
    st.subheader("💬 Chats")
    for chat_id, messages in list(st.session_state.chat_history.items()):
        # DEFAULT TITLE
        title = "New Chat"
        # FIRST USER MESSAGE TITLE
        for msg in messages:
            if msg["role"] == "user":
                title = msg["content"][:30]
                break
        col1, col2 = st.columns([4, 1])
        # OPEN CHAT
        with col1:
            if st.button(title, key=f"open_{chat_id}"):
                st.session_state.current_chat = chat_id
        # DELETE CHAT
        with col2:
            if st.button("🗑", key=f"delete_{chat_id}"):
                del st.session_state.chat_history[chat_id]
                # HANDLE EMPTY CHAT CASE
                if st.session_state.chat_history:
                    st.session_state.current_chat = list(
                        st.session_state.chat_history.keys()
                    )[0]
                else:
                    st.session_state.current_chat = None
                st.rerun()
    if uploaded_files:
        
        for uploaded_file in uploaded_files:

            # file_text = uploaded_file.read().decode("utf-8")
            try:

                file_text = uploaded_file.read().decode("utf-8")

            except Exception:

                st.error(f"{uploaded_file.name} is not supported")
                continue

            result = api_post(
                "upload",
                {
                    "file_name": uploaded_file.name,
                    "file_content": file_text
                }
            )

            if "error" not in result:

                st.success(f"{uploaded_file.name} uploaded!")

            else:

                st.error(result["error"])
if st.session_state.current_chat is None:
    chat_id = "chat_1"
    st.session_state.chat_history[chat_id] = []
    st.session_state.current_chat = chat_id
st.title("🤖 Atom AI")

current_messages = st.session_state.chat_history[
    st.session_state.current_chat
]

for i, message in enumerate(current_messages):
    with st.chat_message(message["role"]):
        # =========================
        # NORMAL MESSAGE
        # =========================
        if st.session_state.edit_index != i:
            st.markdown(message["content"])
        # =========================
        # EDIT MODE
        # =========================
        else:
            new_query = st.text_input(
                "Rewrite Query",
                value=message["content"],
                key=f"rewrite_input_{i}"
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Save", key=f"save_{i}"):
                    # UPDATE QUERY
                    current_messages[i]["content"] = new_query
                    # REMOVE OLD ASSISTANT RESPONSE
                    if i + 1 < len(current_messages):
                        if current_messages[i + 1]["role"] == "assistant":
                            current_messages.pop(i + 1)
                    # GENERATE NEW RESPONSE
                    result = api_post(
                        "chat",
                        {
                            "query": new_query,
                            "history": current_messages[:i]
                        }
                    )

                    new_answer = result.get(
                        "answer",
                        result.get("error", "No response")
                    )
                    current_messages.insert(
                        i + 1,
                        {
                            "role": "assistant",
                            "content": new_answer
                        }
                    )
                    st.session_state.edit_index = None
                    st.rerun()
            with col2:
                if st.button("❌ Cancel", key=f"cancel_{i}"):
                    st.session_state.edit_index = None
                    st.rerun()
        # =========================
        # REWRITE BUTTON
        # =========================
        if message["role"] == "user":
            if st.button("✏ Rewrite", key=f"edit_{i}"):
                st.session_state.edit_index = i
                st.rerun()
# =========================
# USER INPUT
# =========================
prompt = st.chat_input("Ask anything...")
if prompt:
    # -------------------------
    # SAVE USER MESSAGE
    # -------------------------
    current_messages.append({
        "role": "user",
        "content": prompt
    })
    # -------------------------
    # SHOW USER MESSAGE
    # -------------------------
   # SHOW USER MESSAGE
    with st.chat_message("user"):
        st.markdown(prompt)
        # REWRITE BUTTON
        latest_index = len(current_messages) - 1
        if st.button("✏ Rewrite", key=f"edit_{latest_index}"):
            st.session_state.edit_index = latest_index
            st.rerun()
    # -------------------------
    # API CALL
    # -------------------------
    result = api_post(
        "chat",
        {
            "query": prompt,
            "history": current_messages[-6:]
        }
    )

    answer = result.get(
        "answer",
        result.get("error", "No response")
    )
    # SAVE ASSISTANT MESSAGE
    current_messages.append({
        "role": "assistant",
        "content": answer
    })
    # -------------------------
    # STREAMING EFFECT
    # -------------------------
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for char in answer:
            full_response += char
            time.sleep(0.005)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
