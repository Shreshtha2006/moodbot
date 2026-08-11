import random
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()


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


if "selected_mood_key" not in st.session_state:
    st.session_state.selected_mood_key = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "display_history" not in st.session_state:
    st.session_state.display_history = []


@st.cache_resource
def get_model():
    return ChatMistralAI(model="mistral-small-2506")


#Sidebar

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

#Dynamic Theme

num_floaters = 14
floaters_html = ""
for i in range(num_floaters):
    emoji = random.choice(theme["emojis"])
    left = random.randint(0, 100)
    duration = round(random.uniform(7, 15), 2)
    delay = round(random.uniform(0, 9), 2)
    size = random.randint(14, 26)
    floaters_html += (
        f'<div class="floater" style="left:{left}vw; font-size:{size}px; '
        f'animation-duration:{duration}s; animation-delay:{delay}s;">{emoji}</div>'
    )

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;800;900&family=Poppins:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stMarkdown, p, span, div {{
        font-family: 'Poppins', sans-serif;
    }}

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

    /* ---- FLOATER LAYER: forced BEHIND all real content ---- */
    div[data-testid="stAppViewContainer"] {{
        position: relative;
        z-index: 2;
    }}
    div[data-testid="stSidebar"] {{
        position: relative;
        z-index: 3;
    }}
    div[data-testid="stBottom"] {{
        position: relative;
        z-index: 5;
    }}
    .floater {{
        position: fixed;
        top: 100vh;
        opacity: 0.35;
        pointer-events: none;
        z-index: 0;
        animation-name: floatUp;
        animation-timing-function: ease-in;
        animation-iteration-count: infinite;
        filter: drop-shadow(0 0 4px {theme["accent"]});
    }}

    @keyframes floatUp {{
        0%   {{ transform: translateY(0) rotate(0deg); opacity: 0; }}
        10%  {{ opacity: 0.4; }}
        90%  {{ opacity: 0.4; }}
        100% {{ transform: translateY(-110vh) rotate(360deg); opacity: 0; }}
    }}

    .sticky-header {{
        position: sticky;
        top: 0;
        z-index: 999;
        padding: 16px 0 14px 0;
        margin: -1rem -1rem 14px -1rem;
        background: linear-gradient(160deg, {theme["bg_start"]}, {theme["bg_end"]});
        border-bottom: 2px solid {theme["primary"]}66;
        box-shadow: 0 4px 20px {theme["bg_start"]}, 0 0 20px {theme["primary"]}33;
    }}

    .neon-title {{
        font-family: 'Orbitron', sans-serif;
        text-align: center;
        font-size: 42px;
        font-weight: 900;
        letter-spacing: 2px;
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
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        letter-spacing: 0.5px;
        text-align: center;
        color: {theme["accent"]};
        font-size: 17px;
        margin-top: -6px;
        margin-bottom: 8px;
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
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-block;
        padding: 7px 20px;
        border-radius: 999px;
        border: 2px solid {theme["primary"]};
        color: {theme["primary"]};
        background: {theme["bg_start"]}cc;
        box-shadow: 0 0 12px {theme["primary"]};
        margin: 0 auto 4px auto;
        text-align: center;
    }}

    .badge-wrap {{
        text-align: center;
        position: relative;
        z-index: 6;
    }}

    /* ---- Chat input: stylish glassy pill with theme glow ---- */
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
        background: {theme["bg_end"]}f2 !important;
        backdrop-filter: blur(10px);
        border: 2px solid {theme["primary"]} !important;
        box-shadow:
            0 0 16px {theme["primary"]}aa,
            inset 0 0 12px {theme["primary"]}22 !important;
        border-radius: 20px !important;
        padding: 2px 6px;
    }}
    section[data-testid="stChatInput"] textarea {{
        background: transparent !important;
        color: {theme["accent"]} !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 15.5px !important;
        caret-color: {theme["primary"]} !important;
        border: none !important;
    }}
    section[data-testid="stChatInput"] textarea::placeholder {{
        color: {theme["accent"]}99 !important;
        font-style: italic;
    }}
    section[data-testid="stChatInput"] button {{
        background: {theme["primary"]}22 !important;
        border-radius: 50% !important;
        color: {theme["primary"]} !important;
        transition: 0.25s;
    }}
    section[data-testid="stChatInput"] button:hover {{
        background: {theme["primary"]} !important;
    }}
    section[data-testid="stChatInput"] svg {{
        fill: {theme["primary"]} !important;
    }}
    section[data-testid="stChatInput"] button:hover svg {{
        fill: #000 !important;
    }}

    /* ---- Chat message bubbles: glassmorphism, always above floaters, readable ---- */
    div[data-testid="stChatMessage"] {{
        position: relative;
        z-index: 4;
        background: {theme["bg_start"]}e6;
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid {theme["primary"]}88;
        border-radius: 18px;
        box-shadow: 0 0 14px {theme["secondary"]}77, 0 4px 18px rgba(0,0,0,0.45);
        padding: 10px 14px;
        margin-bottom: 10px;
    }}
    div[data-testid="stChatMessage"] p,
    div[data-testid="stChatMessage"] span,
    div[data-testid="stChatMessage"] div {{
        color: #f3f3f3 !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 15.5px !important;
        line-height: 1.55 !important;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {theme["bg_end"]}, {theme["bg_start"]});
        border-right: 2px solid {theme["primary"]};
        box-shadow: 4px 0 20px {theme["primary"]}44;
    }}

    div[data-baseweb="select"] > div {{
        border: 2px solid {theme["primary"]} !important;
        border-radius: 12px !important;
        box-shadow: 0 0 10px {theme["primary"]}77;
        font-family: 'Poppins', sans-serif !important;
    }}

    .stButton>button {{
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        border: 2px solid {theme["primary"]};
        color: {theme["primary"]};
        background: transparent;
        box-shadow: 0 0 10px {theme["primary"]}88;
        border-radius: 12px;
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

#Header

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


for role, content in st.session_state.display_history:
    avatar = theme["avatar"] if role == "assistant" else "🧑"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)


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
