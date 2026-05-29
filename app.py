import streamlit as st
import math
import re

def calculate_entropy(password):
    charset = 0
    if re.search(r"[a-z]", password): charset += 26
    if re.search(r"[A-Z]", password): charset += 26
    if re.search(r"[0-9]", password): charset += 10
    if re.search(r"[^a-zA-Z0-9]", password): charset += 32
    if charset == 0: return 0
    return round(len(password) * math.log2(charset), 2)

def get_strength_label(entropy):
    if entropy < 40: return "WEAK"
    elif entropy < 60: return "MODERATE"
    elif entropy < 80: return "STRONG"
    else: return "VERY STRONG"

def estimate_crack_time(entropy):
    if entropy < 28: return "Instantly"
    elif entropy < 36: return "Few minutes"
    elif entropy < 60: return "Few years"
    else: return "Millions of years"

def improve_password(password):
    suggestions = []
    if len(password) < 12: suggestions.append("Use at least 12 characters")
    if not re.search(r"[A-Z]", password): suggestions.append("Add uppercase letters")
    if not re.search(r"[a-z]", password): suggestions.append("Add lowercase letters")
    if not re.search(r"[0-9]", password): suggestions.append("Add numbers")
    if not re.search(r"[^a-zA-Z0-9]", password): suggestions.append("Add special symbols")
    return suggestions

st.title("AI Password Strength & Crack Predictor")
password = st.text_input("Enter Password", type="password")

if password:
    entropy = calculate_entropy(password)
    strength = get_strength_label(entropy)
    crack_time = estimate_crack_time(entropy)

    st.subheader("Results")
    st.write(f"Strength: **{strength}**")
    st.write(f"Entropy Score: **{entropy}**")
    st.write(f"Estimated Crack Difficulty: **{crack_time}**")

    suggestions = improve_password(password)
    if suggestions:
        st.subheader("Suggestions to Improve")
        for s in suggestions:
            st.write("- " + s)
    else:
        st.success("Excellent password!")
