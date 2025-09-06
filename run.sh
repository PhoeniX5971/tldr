#!/bin/bash

cleanup() {
	echo "Stopping servers..."
	kill $PID1 $PID2
	exit
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

source ~/code/ai/tldr/.venv/bin/activate
uvicorn backend.main:app --reload --port 8000 &
PID1=$!

python ~/code/ai/tldr/agents/discord_summarizer/bot.py &
PID2=$!

wait $PID1 $PID2
