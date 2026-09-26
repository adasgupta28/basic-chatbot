# AriChat

A beginner-friendly **AI chatbot** with a web chat interface built on [Streamlit](https://streamlit.io/) and powered by the [OpenAI API](https://platform.openai.com/docs) (or any model on [OpenRouter](https://openrouter.ai/)). You type messages in your browser and the app sends the recent conversation to the model and streams back its reply. The UI follows the pattern from Streamlit's [conversational app tutorial](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps).

## 🚀 Features

* **Browser-based chat UI:** Uses Streamlit's `st.chat_message` and `st.chat_input` components.
* **Streaming responses:** Replies appear word by word as the model generates them.
* **OpenAI or OpenRouter:** Switch providers with one environment variable.
* **Model picker:** Change the model from the sidebar without editing code.
* **Conversation memory:** The chat history is kept in `st.session_state`. The model sees the most recent messages (20 by default) to keep cost and context use bounded.
* **Clear chat:** Start a fresh conversation from the sidebar.
* **Friendly errors:** A missing API key, failed request or empty reply shows a message in the app instead of a stack trace.
* **Markdown rendering:** Code blocks, lists and headings display correctly.

## 📂 Project Structure

```text
basic-chatbot/
├── chatbot.py          # Streamlit app: UI, chat history and LLM API calls
├── pyproject.toml      # Project metadata and dependencies
├── uv.lock             # Locked dependency versions (managed by uv)
├── .env.example        # Template for API keys and optional settings
└── README.md           # Project documentation
```

## 🛠️ Prerequisites

* **Python 3.13 or newer.** Check your version with:
  ```bash
  python --version
  ```
* **[uv](https://docs.astral.sh/uv/)** for installing dependencies and running the app (installation steps below).
* **An API key** for one of:
  * **OpenAI:** create one at <https://platform.openai.com/api-keys>
  * **OpenRouter:** create one at <https://openrouter.ai/keys>

  API usage is billed by the provider per token.

## ⚙️ Installation

1. **Clone the repository** (or download the source code files):
   ```bash
   git clone https://github.com/adasgupta28/basic-chatbot.git
   cd basic-chatbot
   ```

2. **Install uv (if not installed)**:
   ```bash
   # On macOS/Linux:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # On Windows PowerShell:
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```
   This creates a `.venv` folder and installs `streamlit`, `openai` and `python-dotenv`.

## 🔑 Configuration

The app reads its settings from a `.env` file in the project root.

1. Copy the example file:
   ```bash
   # macOS/Linux
   cp .env.example .env

   # Windows PowerShell
   Copy-Item .env.example .env
   ```

2. Open `.env` and set the key for your provider:
   ```env
   LLM_PROVIDER="openai"
   OPENAI_API_KEY="sk-..."
   ```

### Settings

| Variable | Required | Default | Description |
|---|---|---|---|
| `LLM_PROVIDER` | No | `openai` | `openai` or `openrouter`. |
| `OPENAI_API_KEY` | When provider is `openai` | – | Your OpenAI API key. |
| `OPENROUTER_API_KEY` | When provider is `openrouter` | – | Your OpenRouter API key. |
| `LLM_MODEL` | No | `gpt-5.6-luna` (OpenAI) or `openai/gpt-5.6-luna` (OpenRouter) | Model shown in the sidebar when the app starts. OpenRouter model names include a vendor prefix; see the [OpenRouter model list](https://openrouter.ai/models). |
| `MAX_HISTORY_MESSAGES` | No | `20` | Number of recent user/assistant messages sent to the model each turn. Older messages stay on screen but aren't sent. |

`.env` is listed in `.gitignore`, so your key is not committed. Never commit a real key.

Settings are read when the app starts. Existing environment variables take priority over `.env`. **Restart the app after editing `.env`.**

### Changing the system prompt

The assistant's tone and rules come from the `SYSTEM_PROMPT` string near the top of [chatbot.py](chatbot.py). Edit it and save. Streamlit detects the change and offers to rerun the app.

## 💻 Usage

Start the app:

```bash
uv run streamlit run chatbot.py
```

Streamlit prints a local URL (usually <http://localhost:8501>) and opens it in your browser.

* Type a message in the input box at the bottom of the page and press **Enter**.
* Use the **Model** box in the sidebar to switch models for the rest of the session.
* Click **Clear chat** in the sidebar to start a new conversation.

To stop the app, press **Ctrl+C** in the terminal.

### Example interaction

```text
You:       Hi! What can you do?
Assistant: Hi! I can answer questions, explain concepts, help you write or debug
           code, summarize text, and brainstorm ideas. What would you like to do?
You:       Write a Python one-liner to reverse a string.
Assistant: text[::-1]
           This uses slice notation with a step of -1 to walk the string backwards.
```

Replies come from the model, so the exact wording will differ each time.

## 🧯 Troubleshooting

| Message in the app | Likely cause and fix |
|---|---|
| `Set OPENAI_API_KEY in your .env file…` (or `OPENROUTER_API_KEY`) | The key for the selected provider is missing. Follow the [Configuration](#-configuration) steps, then restart the app. |
| `Unknown LLM_PROVIDER…` | `LLM_PROVIDER` has a typo. Use `openai` or `openrouter`. |
| `The request failed: … 401` / authentication error | The API key is wrong or has been revoked. Create a new key, update `.env` and restart. |
| `The request failed: … 404` / model not found | Your account can't use that model, or the name is wrong. Change it in the sidebar. |
| `The request failed: … 429` / rate limit | You've hit a rate limit or run out of credits. Check usage and billing on your provider's dashboard. |
| `The model returned an empty response` | The model sent no text. Try again or try a different model. |

When a request fails, your message is removed from the history so it isn't sent twice. Type it again to retry.

## 📚 How it works

1. On startup, `load_dotenv()` loads `.env`, and the app picks the provider's API key and base URL from `PROVIDERS`.
2. `get_llm_client()` creates an `OpenAI` client. OpenRouter is OpenAI-compatible, so the same client works with a different `base_url`. `@st.cache_resource` reuses one client for each key/URL pair.
3. The chat history in `st.session_state.messages` holds only user and assistant messages. Streamlit reruns the whole script on every interaction, so each run redraws them.
4. When you send a message, the app builds the request from the system prompt plus the last `MAX_HISTORY_MESSAGES` messages and calls `client.chat.completions.create(..., stream=True)`.
5. `st.write_stream()` shows the reply as it arrives and returns the full text, which is appended to the history for the next turn.
