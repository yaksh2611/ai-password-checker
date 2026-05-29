import streamlit as st
import math
import re

st.set_page_config(page_title="Password Strength Checker", page_icon="🔐", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
        background-color: #0f0f13;
        color: #f0f0f0;
    }

    .stApp {
        background: linear-gradient(135deg, #0f0f13 0%, #1a1a2e 100%);
    }

    h1 {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, #a78bfa, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem !important;
    }

    .subtitle {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    .stTextInput > div > div > input {
        background-color: #1e1e2e !important;
        border: 1.5px solid #2e2e4e !important;
        border-radius: 12px !important;
        color: #f0f0f0 !important;
        font-size: 1.1rem !important;
        padding: 0.75rem 1rem !important;
        font-family: 'Space Grotesk', monospace !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(167,139,250,0.15) !important;
    }

    .metric-card {
        background: #1e1e2e;
        border: 1px solid #2e2e4e;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-label {
        font-size: 0.78rem;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.3rem;
    }

    .metric-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #f0f0f0;
    }

    .strength-bar-container {
        background: #2e2e4e;
        border-radius: 99px;
        height: 8px;
        margin-top: 0.5rem;
        overflow: hidden;
    }

    .strength-bar {
        height: 8px;
        border-radius: 99px;
        transition: width 0.5s ease;
    }

    .badge {
        display: inline-block;
        padding: 0.25rem 0.85rem;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
    }

    .suggestion-item {
        background: #1e1e2e;
        border-left: 3px solid #a78bfa;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.92rem;
        color: #c4b5fd;
    }

    .success-box {
        background: linear-gradient(135deg, #064e3b, #065f46);
        border: 1px solid #10b981;
        border-radius: 16px;
        padding: 1.2rem 1.5rem;
        color: #6ee7b7;
        font-weight: 600;
        font-size: 1rem;
        text-align: center;
    }

    .stButton > button {
        display: none;
    }

    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)


def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    if charset == 0: return 0
    return round(len(password) * math.log2(charset), 2)

def get_strength(entropy):
    if entropy < 40: return "WEAK", "#ef4444", 25
    elif entropy < 60: return "MODERATE", "#f59e0b", 50
    elif entropy < 80: return "STRONG", "#3b82f6", 75
    else: return "VERY STRONG", "#10b981", 100

def estimate_crack_time(entropy):
    if entropy < 28: return "⚡ Instantly"
    elif entropy < 36: return "⏱ Few minutes"
    elif entropy < 60: return "📅 Few years"
    else: return "♾ Millions of years"

def improve_password(password):
    suggestions = []
    if len(password) < 12: suggestions.append("Use at least 12 characters")
    if not re.search(r"[A-Z]", password): suggestions.append("Add uppercase letters (A-Z)")
    if not re.search(r"[a-z]", password): suggestions.append("Add lowercase letters (a-z)")
    if not re.search(r"[0-9]", password): suggestions.append("Add numbers (0-9)")
    if not re.search(r"[^a-zA-Z0-9]", password): suggestions.append("Add special symbols (!@#$...)")
    return suggestions


st.markdown("<h1>🔐 Password Strength</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Check how strong your password really is</p>', unsafe_allow_html=True)

password = st.text_input("", placeholder="Enter your password...", type="password")

if password:
    entropy = calculate_entropy(password)
    label, color, bar_width = get_strength(entropy)
    crack_time = estimate_crack_time(entropy)
    suggestions = improve_password(password)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Strength</div>
            <div class="metric-value" style="color:{color}">{label}</div>
            <div class="strength-bar-container">
                <div class="strength-bar" style="width:{bar_width}%; background:{color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Entropy Score</div>
            <div class="metric-value">{entropy} <span style="font-size:0.85rem;color:#6b7280">bits</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Estimated Crack Time</div>
        <div class="metric-value">{crack_time}</div>
    </div>
    """, unsafe_allow_html=True)

    if suggestions:
        st.markdown("<br><b style='color:#a78bfa'>💡 Suggestions to Improve</b>", unsafe_allow_html=True)
        for s in suggestions:
            st.markdown(f'<div class="suggestion-item">→ {s}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="success-box">
            ✅ Excellent password! You're well protected.
        </div>
        """, unsafe_allow_html=True)
