# Reddit C2 Serverless - Persistent Shell

## 📘 Description

This project implements a **serverless Command and Control (C2)** framework leveraging Reddit as a covert communication channel.

- **Serverless**: Operates without self-hosted infrastructure by using Reddit as the transport layer.
- **Obfuscated communications**: Commands and responses are XOR-encrypted and Base64-encoded.
- **Persistent shell**: Maintains command context across sessions.
- **Evasion techniques**:
  - Randomized `User-Agent` headers.
  - Random sleep intervals to bypass bot detection mechanisms.
  - Invisible separators to circumvent platform restrictions.

---

## 🧱 Architecture

- **Two Reddit accounts**:
  - **Controller**: Publishes encrypted commands.
  - **Agent**: Monitors the subreddit and posts encrypted responses.
- **Private subreddit**: Used as the covert communication channel.
- **Reddit applications**: API keys are used for authentication and interaction.

---

## 📂 Files

| File               | Description                                      |
|--------------------|--------------------------------------------------|
| `c2red.py`         | Agent script that runs a persistent shell        |
| `c2redlistener.py` | Controller script that sends commands and reads responses |

---

## 📦 Requirements

- **Python**: Version 3.7 or higher
- **Dependencies**:
  - `praw`
  - `base64` (built-in)
  - `random`, `re`, `subprocess`, `threading` (built-in)

### Installation

```bash
pip install praw
```

---

## ⚙️ Configuration

Edit the following credentials in both scripts before running:

```python
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'
```

Ensure the Reddit app is configured as a **script** type for proper authentication.

---

## 🚀 Usage

### 1. Start the Agent

```bash
python c2red.py
```

### 2. Start the Controller

```bash
python reddit_c2_shell.py
```

### 3. Send Commands

```bash
> whoami
> uname -a
```

The agent will execute these within a persistent shell and return the output via subreddit comments.

---

## ⚠️ Disclaimer

> This project is intended for **educational and research purposes only**.  
> It is **not designed for malicious use** and **does not implement advanced operational security**.  
> Use responsibly and within the bounds of the law.

---

## 📄 License

**© Secra Solutions S.L. 2025**  
All rights reserved.
