# TLDR Discord Summarizer Bot

This project is a Discord bot that summarizes messages in a channel using a Gemini LLM via a FastAPI backend. It fetches all messages after a specified message ID and produces a concise summary including usernames.

---

## Setup

1. **Clone the repository**:

```bash
git clone https://github.com/PhoeniX5971/tldr.git
cd tldr
```

2. **Create a virtual environment and activate it**:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux / macOS
# .venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

> [!Note]
> I recommend python 3.10+

3. **Copy the example environment file**:

```bash
cp .env.example .env
```

4. **Fill in your credentials** in `.env`:

```
GOOGLE_API_KEY=YOUR_GEMINI_TOKEN
TOKEN=YOUR_DISCORD_BOT_TOKEN
PREFIX=YOUR_DISCORD_BOT_PREFIX
INVITE_LINK=YOUR_BOT_INVITE_LINK
```

5. **Edit `config.py`** if your FastAPI summarizer server is running on a different IP/port:

```python
SUMMARY_SERVER = "http://127.0.0.1:8000/summarize"
```

---

## Running the Bot

### On Linux

Use the `run.sh` file in the project root.

### Else

1. **Start the FastAPI backend**:

```bash
uvicorn backend.main:app --reload --port 8000
```

2. **Start the Discord bot**:

```bash
python agents/discord_summarizer/bot.py
```

> You can stop the bot by terminating the `run.sh` (ctrl+c in the terminal).

---

## Usage

- Copy the **message ID** of the message you want to summarize everything after.
- In Discord, run:

```
.summarize 123456789012345678
```

- The bot will fetch all messages after that ID (default up to 100), include usernames, send them to the FastAPI backend, and reply with a TL;DR summary.

**Notes**:

- Make sure the bot has the `Read Message History` intent enabled.
- You can adjust the `limit` in the command to fetch more than 100 messages.
- Only `.env.example` should be committed; keep your real `.env` private.

---

## Project Structure

```
tldr/
├── agents/discord_summarizer/   # Bot code and cogs
├── ai/                           # LLM graph and prompts
├── backend/                      # FastAPI server
├── config.py                     # FastAPI server link
├── .env.example                  # Example environment variables
├── README.md
├── requirements.txt
├── run.sh
└── stop.sh
```

---

This setup allows you to quickly run the bot and summarize messages by simply copying the message ID and using the `.summarize` command.
