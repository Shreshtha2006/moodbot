# 🤖 MoodBot

A mood-based AI chatbot built with **Streamlit** and **LangChain (Mistral AI)**. Pick a personality from the dropdown — Cheerful, Roast Comedian, Gentle, Hot-Headed, or Romantic — and chat with a bot that responds entirely in that vibe. The UI theme, colors, and floating emoji animations change dynamically to match the selected mood.

## 🚀 Live Demo

Try it here: **https://moodbot-ktmkscoe38etiemeyh5cs6.streamlit.app**

## ✨ Features

- 5 selectable bot personalities via a sidebar dropdown
- Neon-themed UI that recolors based on the chosen mood
- Animated floating emojis (hearts, fire, sparkles, etc.) matching the mood
- Sticky header that stays fixed while chat messages scroll
- Powered by Mistral AI through LangChain for the actual chat responses

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework built with Claude
- [LangChain](https://www.langchain.com/) + [Mistral AI](https://mistral.ai/) — LLM backend
- Python 3

## 📂 Project Structure

```
├── MoodBot.py               # Main deployed app (UI + LLM logic combined)
├── streamlitUI.py            # UI-only reference version (no LLM calls)
├── llm_integration.py        # LLM logic-only reference version (original terminal script)
├── requirements.txt          # Python dependencies
└── .gitignore                 # Excludes .env and other local files
```

> `MoodBot.py` is the file actually deployed on Streamlit Cloud. The other two files are split out for readability — one shows the UI code, the other shows the core chatbot logic.

