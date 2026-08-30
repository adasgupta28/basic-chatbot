# AriChat

A beginner-friendly, interactive **Python chatbot** that runs directly in your terminal. This project demonstrates basic rule-based or NLP-based logic to process user input and return predefined responses. The UI code is mostly from Streamlit documentation. 

## 🚀 Features

* **Interactive CLI:** Run a continuous chat loop inside your terminal.
* **Predefined Responses:** Quickly replies to basic commands, greetings, and common questions.
* **Easy Extension:** Simple codebase designed to let you plug in your own logic or external APIs easily.


## 📂 Project Structure

```text
simple-python-chatbot/
├── chatbot.py          # Main executable script containing chatbot logic
├── pyproject.toml      # Project configuration file
└── README.md           # Project documentation
```

## 🛠️ Prerequisites

* **Python 3.13** installed on your system. You can check your version by running:
  ```bash
  python --version
  ```

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

   # On Windows Powershell:
   irm https://astral.sh/uv/install.ps1 | iex
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

## 💻 Usage

Run the main application script from your terminal:

```bash
uv run python -m streamlit run chatbot.py
```

### Example Interaction

```text
Chatbot: Hello! I am a simple chatbot. Type 'bye' to exit.
You: Hi
Chatbot: Hi there! How can I help you today?
You: What is your name?
Chatbot: I am a very simple chatbot built in Python.
You: bye
Chatbot: Goodbye! Have a great day.
```