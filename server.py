import shelve
import streamlit as st
from vertexai import agent_engines

st.set_page_config(page_title="ADK Chatbot", page_icon="💬", layout="centered")

USER_AVATAR = "👤"
BOT_AVATAR = "🤖"
DEFAULT_WELCOME_MESSAGE = "¡Hola! Soy tu asistente de IA. ¿En qué puedo ayudarte hoy?"

try:
    adk_app = agent_engines.get(st.secrets["DEPLOY_NAME"])
except Exception as e:
    st.error(f"Error al cargar el agente IA. Asegúrate de que DEPLOY_NAME esté configurado correctamente. Detalles: {e}")
    st.stop()


adk_session_id = "streamlit_user_session"
adk_session = adk_app.create_session(user_id=adk_session_id)


def load_chat_history():
    """Loads chat messages from the 'chat_history' shelve file."""
    with shelve.open("chat_history") as db:
        return db.get("messages", [])

def save_chat_history(messages):
    """Saves chat messages to the 'chat_history' shelve file."""
    with shelve.open("chat_history") as db:
        db["messages"] = messages


st.title("🤖 Chat con Agente IA")

if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "assistant", "content": DEFAULT_WELCOME_MESSAGE})
        save_chat_history(st.session_state.messages)

with st.sidebar:
    st.header("Opciones de Chat")
    if st.button("✨ Iniciar Nuevo Chat", type="primary"):
        st.session_state.messages = [{"role": "assistant", "content": DEFAULT_WELCOME_MESSAGE}]
        save_chat_history(st.session_state.messages)

    if st.button("🗑️ Eliminar Historial Completo"):
        st.session_state.messages = [{"role": "assistant", "content": DEFAULT_WELCOME_MESSAGE}]
        save_chat_history(st.session_state.messages)

    st.markdown("---")
    st.info("Desarrollado con Vertex AI Agent Development Kit (ADK)")

for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""
        try:
            with st.spinner("Pensando..."):
                for event in adk_app.stream_query(
                        user_id=adk_session_id,
                        session_id=adk_session.get("id"),
                        message=prompt,
                ):
                    if event.get("content") and event.get("content").get("parts"):
                        part_text = event.get("content").get("parts")[0].get("text")
                        if part_text:
                            full_response += part_text
                            message_placeholder.markdown(full_response + "▌") # Add a blinking cursor effect
            message_placeholder.markdown(full_response) # Display final response
        except Exception as e:
            error_message = f"Ocurrió un error al procesar tu solicitud. Por favor, intenta de nuevo. Detalles: {e}"
            message_placeholder.error(error_message)
            full_response = error_message

    st.session_state.messages.append({"role": "assistant", "content": full_response})

save_chat_history(st.session_state.messages)