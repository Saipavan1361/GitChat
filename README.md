# 💬 GitChat

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-ff4b4b?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

GitChat is a lightweight GitHub-powered chat app that allows two users to exchange messages by syncing through their **private GitHub repositories**.

Built using [Streamlit](https://streamlit.io) and [GitPython](https://github.com/gitpython-developers/GitPython), it creates a Git-backed text chat where every conversation is version-controlled — and totally owned by you.

---

## Features

- Private GitHub repo–based messaging
- Message history saved per person (`chats/<partner>.txt`)
- Persistent config using local `config.json`
- Auto-refresh every 3 seconds during chats
- Supports chat with multiple users
- Easily expandable and beginner-friendly

---

## Tech Stack

- Python 3.9+
- [Streamlit](https://streamlit.io/)
- [GitPython](https://github.com/gitpython-developers/GitPython)
- GitHub (for chat storage)
- Local JSON file for storing user info

---

## Installation

### 1.Clone the repository

```bash
git clone https://github.com/Saipavan1361/GitChat.git
cd gitchat
```

### 2.Install required Python packages
```bash
pip install -r requirements.txt
```

### 3.Running App Locally
```bash
streamlit run app.py
```

###SECURITY NOTICE 
This app uses GitHub Personal Access Tokens.Tokens are saved locally in plain text(config.json). DO NOT commit or upload it anywhere public

(if you want to have some security with json file try to add in .gitignore file)

Made with 💡 by @Saipavan1361
Want to contribute? Fork the repo or open an issue! 

## License
This project is licensed under the [MIT License](LICENSE)
