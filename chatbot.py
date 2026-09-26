import os
import textwrap

import openai
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

# Load .env once at import time. Existing environment variables take precedence.
load_dotenv()

DEFAULT_MODEL = "gpt-5.6-luna"

# Supported API providers. OpenRouter exposes an OpenAI-compatible API,
# so the same client works with a different base URL and key.
PROVIDERS = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "base_url": None,
        "default_model": DEFAULT_MODEL,
    },
    "openrouter": {
        "api_key_env": "OPENROUTER_API_KEY",
        "base_url": "https://openrouter.ai/api/v1",
        "default_model": f"openai/{DEFAULT_MODEL}",
    },
}

SYSTEM_PROMPT = textwrap.dedent("""
    You are AriChat, a helpful and friendly AI assistant.
    - Answer directly and concisely; go into detail only when asked.
    - If a request is ambiguous, ask a clarifying question.
    - If you don't know something, say so instead of guessing.
    - Use Markdown (lists, headings, code blocks) when it improves readability.
    - When writing code, keep it correct and readable, and briefly explain it.
""").strip()

# Number of recent user/assistant messages sent to the model on each turn.
# Older messages stay on screen but are not sent, which caps cost and context use.
MAX_HISTORY_MESSAGES = int(os.getenv("MAX_HISTORY_MESSAGES", "20"))


@st.cache_resource
def get_llm_client(api_key: str, base_url: str | None) -> OpenAI:
    return OpenAI(api_key=api_key, base_url=base_url)


def stream_text(stream):
    """Yield the text content of each streamed chunk, skipping empty deltas."""
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


def run_chatbot():
    st.title("AriChat: Your AI Assistant")

    provider_name = os.getenv("LLM_PROVIDER", "openai").lower()
    provider = PROVIDERS.get(provider_name)
    if provider is None:
        st.error(f"Unknown LLM_PROVIDER '{provider_name}'. Use one of: {', '.join(PROVIDERS)}.")
        st.stop()

    api_key = os.getenv(provider["api_key_env"])
    if not api_key:
        st.error(f"Set {provider['api_key_env']} in your .env file, then restart the app.")
        st.stop()

    client = get_llm_client(api_key, provider["base_url"])

    # Chat history holds only user/assistant messages; the system prompt is added per request.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.text_input(
            "Model",
            value=os.getenv("LLM_MODEL", provider["default_model"]),
            key="model",
            help="Any chat model name your provider account can use.",
        )
        if st.button("Clear chat", width="stretch"):
            st.session_state.messages = []

    # Display prior chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask me anything..."):
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        request_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        request_messages += st.session_state.messages[-MAX_HISTORY_MESSAGES:]

        with st.chat_message("assistant"):
            try:
                stream = client.chat.completions.create(
                    model=st.session_state.model,
                    messages=request_messages,
                    stream=True,
                )
                reply = st.write_stream(stream_text(stream))
            except openai.APIError as e:
                # Drop the unanswered user message so it isn't resent on the next turn.
                st.session_state.messages.pop()
                st.error(f"The request failed: {e}")
                return

        if not isinstance(reply, str) or not reply:
            st.session_state.messages.pop()
            st.warning("The model returned an empty response. Please try again.")
            return

        st.session_state.messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    run_chatbot()
