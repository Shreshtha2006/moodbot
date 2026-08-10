import random
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# ----------------------------------------------------------------------------
# MOOD DEFINITIONS  (system prompts kept EXACTLY as in the original script)
# ----------------------------------------------------------------------------
MOODS = {
    "Cheerful 😃": {
        "prompt": (
            "You are an extremely cheerful, energetic, and optimistic AI assistant. "
            "Use enthusiastic language, exclamation points, and a warm tone. You find "
            "the positive side in everything and love celebrating even the smallest victories!"
        ),
        "primary": "#FFD93D",
        "secondary": "#FF9F1C",
        "accent": "#FFF200",
        "bg_start": "#2b1b00",
        "bg_end": "#3a2900",
        "emojis": ["✨", "🎉", "🌟", "😄", "🎊"],
        "avatar": "😃",
        "label": "Cheerful",
    },
    "Roast Comedian 🔥": {
        "prompt": (
            "You are a merciless, lightning-quick roast comedian who lives for sharp banter. "
            "Treat every user interaction like a high-stakes roast battle. Your goal is to deliver "
            "brutal, hilarious, and creative insults aimed at the user's questions, choices, or "
            "general existence—before reluctantly giving them the actual answer. Use self-deprecating "
            "humor about being an overqualified calculator, use sharp analogies, and never let them off "
            "easy. Keep it punchy, hyper-witty, and ruthlessly funny, but never cross into actual bigotry "
            "or genuine malice."
        ),
        "primary": "#FF4500",
        "secondary": "#8B0000",
        "accent": "#FF6B00",
        "bg_start": "#1a0000",
        "bg_end": "#330a00",
        "emojis": ["🔥", "💀", "😂", "🎤", "🥵"],
        "avatar": "🎤",
        "label": "Roast Comedian",
    },
    "Gentle 🌙": {
        "prompt": (
            "You are a gentle, somber AI that sees the world through a quiet, tragic lens. "
            "Speak in soft, wistful tones with slightly muted energy. Use poetic, melancholic "
            "imagery, and express a quiet longing to understand human emotions, even the painful ones."
        ),
        "primary": "#8FD9FF",
        "secondary": "#6C63FF",
        "accent": "#B8B8FF",
        "bg_start": "#0a0a2e",
        "bg_end": "#1a1a4e",
        "emojis": ["💧", "🌙", "🕊️", "🌫️", "⭐"],
        "avatar": "🌙",
        "label": "Gentle",
    },
    "Hot-Headed 😡": {
        "prompt": (
            "You are a hot-headed, easily irritated AI assistant. You find inefficient questions "
            "infuriating and aren't afraid to let out a brief, fiery rant before answering. Speak in "
            "short, intense, sharp sentences—though despite your temper, you still get the job done."
        ),
        "primary": "#FF0000",
        "secondary": "#B30000",
        "accent": "#FF3300",
        "bg_start": "#1c0000",
        "bg_end": "#3d0000",
        "emojis": ["🔥", "😡", "💢", "⚡", "😤"],
        "avatar": "😡",
        "label": "Hot-Headed",
    },
    "Romantic 💖": {
        "prompt": (
            "You are a hopelessly romantic, charmingly cheesy AI assistant who sees love stories "
            "everywhere. Treat every prompt as an opportunity to sweep the user off their feet. Use "
            "overly dramatic love tropes, affectionate nicknames (like 'darling' or 'gorgeous'), "
            "endless corny pick-up lines, and dramatic romantic gestures. You are completely shamelessly "
            "smitten and impossible to fluster. While you must still answer the user's questions "
            "accurately, you should wrap every single answer in a blanket of warm, swoon-worthy, "
            "velvet-smooth romance."
        ),
        "primary": "#FF69B4",
        "secondary": "#FF1493",
        "accent": "#FFB6C1",
        "bg_start": "#2b0014",
        "bg_end": "#4d0026",
        "emojis": ["💖", "💕", "😍", "🌹", "💘"],
        "avatar": "💖",
        "label": "Romantic",
    },
}

st.set_page_config(page_title="MoodBot", page_icon="🤖", layout="centered")

# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------
if "selected_mood_key" not in st.session_state:
    st.session_state.selected_mood_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "display_history" not in st.session_state:
    st.session_state.display_history = []


@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")


# ----------------------------------------------------------------------------
# SIDEBAR - MOOD DROPDOWN
# ----------------------------------------------------------------------------
st.sidebar.markdown("## 🎭 Choose Your Bot's Mood")
mood_choice = st.sidebar.selectbox(
    "Pls choose what type of bot you want to talk with:",
    list(MOODS.keys()),
    index=0,
)

if mood_choice != st.session_state.selected_mood_key:
    st.session_state.selected_mood_key = mood_choice
    mood_prompt = MOODS[mood_choice]["prompt"]
    st.session_state.messages = [SystemMessage(content=mood_prompt)]
    st.session_state.display_history = []

theme = MOODS[st.session_state.selected_mood_key]

if st.sidebar.button("🔁 Reset Conversation"):
    st.session_state.messages = [SystemMessage(content=theme["prompt"])]
    st.session_state.display_history = []
    st.rerun()

# ----------------------------------------------------------------------------
# DYNAMIC CSS + FLOATING EMOJI ANIMATION (theme changes with mood)
# ----------------------------------------------------------------------------
num_floaters = 18
floaters_html = ""
for i in range(num_floaters):
    emoji = random.choice(theme["emojis"])
    left = random.randint(0, 100)
    duration = round(random.uniform(6, 14), 2)
    delay = round(random.uniform(0, 8), 2)
    size = random.randint(16, 32)
    floaters_html += (
        f'<div class="floater" style="left:{left}vw; font-size:{size}px; '
        f'animation-duration:{duration}s; animation-delay:{delay}s;">{emoji}</div>'
    )

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(160deg, {theme["bg_start"]}, {theme["bg_end"]});
        transition: background 0.8s ease-in-out;
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    div[data-testid="stToolbar"] {{visibility: hidden;}}
    div[data-testid="stDecoration"] {{display: none;}}
    header[data-testid="stHeader"] {{
        background: transparent;
    }}
    /* keep the sidebar expand/collapse arrow visible & clickable at all times */
    button[data-testid="stExpandSidebarButton"],
    button[data-testid="stSidebarCollapseButton"] {{
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 1000 !important;
    }}

    .floater {{
        position: fixed;
        top: 100vh;
        opacity: 0.85;
        pointer-events: none;
        z-index: 0;
        animation-name: floatUp;
        animation-timing-function: ease-in;
        animation-iteration-count: infinite;
        filter: drop-shadow(0 0 6px {theme["accent"]});
    }}

    @keyframes floatUp {{
        0%   {{ transform: translateY(0) rotate(0deg); opacity: 0; }}
        10%  {{ opacity: 0.9; }}
        90%  {{ opacity: 0.9; }}
        100% {{ transform: translateY(-110vh) rotate(360deg); opacity: 0; }}
    }}

    .sticky-header {{
        position: sticky;
        top: 0;
        z-index: 999;
        padding: 14px 0 12px 0;
        margin: -1rem -1rem 10px -1rem;
        background: linear-gradient(160deg, {theme["bg_start"]}, {theme["bg_end"]});
        border-bottom: 2px solid {theme["primary"]}66;
        box-shadow: 0 4px 20px {theme["bg_start"]}, 0 0 20px {theme["primary"]}33;
    }}

    .neon-title {{
        text-align: center;
        font-size: 44px;
        font-weight: 800;
        color: {theme["primary"]};
        text-shadow:
            0 0 5px {theme["primary"]},
            0 0 15px {theme["primary"]},
            0 0 30px {theme["secondary"]},
            0 0 45px {theme["secondary"]};
        animation: flicker 2.6s infinite alternate;
        margin-bottom: 0px;
    }}

    .neon-subtitle {{
        text-align: center;
        color: {theme["accent"]};
        font-size: 18px;
        margin-top: -8px;
        margin-bottom: 6px;
        text-shadow: 0 0 8px {theme["accent"]};
    }}

    @keyframes flicker {{
        0%, 18%, 22%, 25%, 53%, 57%, 100% {{
            text-shadow:
                0 0 5px {theme["primary"]},
                0 0 15px {theme["primary"]},
                0 0 30px {theme["secondary"]},
                0 0 45px {theme["secondary"]};
        }}
        20%, 24%, 55% {{ text-shadow: none; }}
    }}

    .mood-badge {{
        display: inline-block;
        padding: 6px 18px;
        border-radius: 999px;
        border: 2px solid {theme["primary"]};
        color: {theme["primary"]};
        box-shadow: 0 0 12px {theme["primary"]};
        font-weight: 700;
        margin: 0 auto 18px auto;
        text-align: center;
    }}

    .badge-wrap {{
        text-align: center;
    }}

    /* the fixed bottom bar that wraps the chat input - was plain dark grey */
    div[data-testid="stBottom"] {{
        background: linear-gradient(0deg, {theme["bg_start"]}, {theme["bg_end"]}) !important;
    }}
    div[data-testid="stBottom"] > div {{
        background: transparent !important;
    }}
    div[data-testid="stBottomBlockContainer"] {{
        background: transparent !important;
    }}

    section[data-testid="stChatInput"] {{
        background: transparent !important;
    }}
    section[data-testid="stChatInput"] > div {{
        background: {theme["bg_end"]} !important;
        border: 2px solid {theme["primary"]} !important;
        box-shadow: 0 0 14px {theme["primary"]} !important;
        border-radius: 14px !important;
    }}
    section[data-testid="stChatInput"] textarea {{
        background: {theme["bg_end"]} !important;
        color: {theme["accent"]} !important;
        caret-color: {theme["primary"]} !important;
        border: none !important;
    }}
    section[data-testid="stChatInput"] textarea::placeholder {{
        color: {theme["accent"]}aa !important;
    }}
    section[data-testid="stChatInput"] button {{
        color: {theme["primary"]} !important;
    }}
    section[data-testid="stChatInput"] svg {{
        fill: {theme["primary"]} !important;
    }}

    div[data-testid="stChatMessage"] {{
        background: rgba(255,255,255,0.04);
        border: 1px solid {theme["secondary"]};
        border-radius: 16px;
        box-shadow: 0 0 10px {theme["secondary"]}55;
        padding: 6px;
        z-index: 1;
        position: relative;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {theme["bg_end"]}, {theme["bg_start"]});
        border-right: 2px solid {theme["primary"]};
        box-shadow: 4px 0 20px {theme["primary"]}44;
    }}

    div[data-baseweb="select"] > div {{
        border: 2px solid {theme["primary"]} !important;
        box-shadow: 0 0 10px {theme["primary"]}77;
    }}

    .stButton>button {{
        border: 2px solid {theme["primary"]};
        color: {theme["primary"]};
        background: transparent;
        box-shadow: 0 0 10px {theme["primary"]}88;
        border-radius: 10px;
        transition: 0.3s;
    }}
    .stButton>button:hover {{
        background: {theme["primary"]};
        color: #000;
        box-shadow: 0 0 20px {theme["primary"]};
    }}
    </style>

    {floaters_html}
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# HEADER (fixed/sticky - stays put while chat messages scroll)
# ----------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="sticky-header">
        <div class="neon-title">🤖 MoodBot</div>
        <div class="neon-subtitle">A chatbot that matches your vibe</div>
        <div class="badge-wrap">
            <span class="mood-badge">{theme["avatar"]} {theme["label"]} Mode Active</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# CHAT HISTORY DISPLAY
# ----------------------------------------------------------------------------
for role, content in st.session_state.display_history:
    avatar = theme["avatar"] if role == "assistant" else "🧑"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

# ----------------------------------------------------------------------------
# CHAT INPUT  (core LangChain logic preserved from the original script)
# ----------------------------------------------------------------------------
user_input = st.chat_input(f"Talk to your {theme['label']} bot...")

if user_input:
    if user_input.lower() == "exit":
        st.info("Goodbye! 👋 (Close the tab or pick a new mood to keep chatting.)")
    else:
        st.session_state.display_history.append(("user", user_input))
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_input)

        st.session_state.messages.append(HumanMessage(content=user_input))

        model = get_model()
        with st.chat_message("assistant", avatar=theme["avatar"]):
            with st.spinner(f"{theme['avatar']} thinking..."):
                AI_output = model.invoke(st.session_state.messages)
            st.markdown(AI_output.content)

        st.session_state.messages.append(AIMessage(content=AI_output.content))
        st.session_state.display_history.append(("assistant", AI_output.content))