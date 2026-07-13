import streamlit as st
import pandas as pd
import requests
import json

# Set up page config
st.set_page_config(page_title="GAC Showroom - Sales Product Knowledge Quiz", layout="wide")

# --- GLOBAL DATABASE CONFIG ---
# This creates a unique public bucket link to sync scores across different devices
DB_URL = "https://kvdb.io/MN87X9WvSgWj8U3n8v5X9f/gac_rak_quiz_scores"

def load_global_scores():
    try:
        response = requests.get(DB_URL)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def save_score_global(name, score_str):
    scores = load_global_scores()
    scores[name] = score_str
    try:
        requests.post(DB_URL, data=json.dumps(scores))
    except:
        pass

# --- CUSTOM SPEC DATA FROM YOUR EXCEL ---
GAC_DATA = {
    "EMPOW": {
        "variants": ["GE", "GL"],
        "facts": [
            "The EMPOW comes in both GE and GL trims, both featuring 18\" Aluminum Alloy Wheels with 225/45 tires.",
            "Both GE and GL trims feature Rain Sensing Wipers and Heated Side Mirrors."
        ]
    },
    "EMPOWR": {
        "variants": ["2T+8AT GE"],
        "facts": [
            "The high-performance EMPOWR comes equipped with a 2T engine paired with an 8AT gearbox.",
            "Unique styling items on the EMPOWR include a Car Spoiler and high-visibility Front Fixed Callipers."
        ]
    },
    "GS3 EMZOOM": {
        "variants": ["GB", "GS", "SPORT+"],
        "facts": [
            "The high-end SPORT+ variant is exclusively equipped with Automatic Headlights and Power Side Mirrors featuring Auto Folding + Heating.",
            "The GB and GS trims ride on 225/55R R18 Tires, whereas the SPORT+ has a distinct configuration."
        ]
    },
    "GS4 MAX": {
        "variants": ["GL+", "GL"],
        "facts": [
            "The premium GL+ variant stands out by offering optional R20 Tires with Wheels, whereas the standard GL does not.",
            "Both GL and GL+ feature Electric Hidden Door Handles and Rain Sensing Front Windshield Wipers."
        ]
    },
    "GS8": {
        "variants": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider"],
        "facts": [
            "The special 'Desert Raider' edition comes distinctively styled with a Black Edition Grille/Rims, Red GAC Front Logo, and Desert Raider side decals.",
            "The Desert Raider trim is uniquely optimized for adventure, boasting a Roof Rack set complete with a tent and ladder."
        ]
    },
    "HYPTEC HT": {
        "variants": ["Elite", "Ultra Gullwing Door"],
        "facts": [
            "The HYPTEC HT is powered by advanced Magazine Battery technology utilizing LFP chemistry.",
            "The Ultra Gullwing Door model features signature upward-opening rear doors, while both models feature 6.6 kW AC charging capability."
        ]
    },
    "M8": {
        "variants": ["GT", "GX"],
        "facts": [
            "The luxury M8 GX variant comes upgraded with Master Specific Wheel Rims and Adaptive Driving Beam headlights.",
            "Both GT and GX luxury trims feature Side Mirrors with Position Memory and an integrated Reverse Tilt function."
        ]
    }
}

QUIZ_BANK = [
    {
        "question": "Which specific GAC GS8 variant comes factory-equipped with a roof rack set, tent, ladder, and custom side decals?",
        "options": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider", "GL Link"],
        "answer": "Desert Raider"
    },
    {
        "question": "What battery technology type is standard across the HYPTEC HT Elite and Ultra variants?",
        "options": ["Standard Ternary Lithium", "Magazine Battery - LFP", "Solid-State Cell", "Sodium-Ion pack"],
        "answer": "Magazine Battery - LFP"
    },
    {
        "question": "Which variant of the new GS4 MAX features the distinct upgrade of optional R20 Tires and Wheels?",
        "options": ["GL", "GL+", "GB", "GS SPORT+"],
        "answer": "GL+"
    },
    {
        "question": "The high-performance EMPOWR variant pairs its 2.0T engine with which transmission configuration?",
        "options": ["7-Speed DCT", "CVT", "8-Speed Automatic (8AT)", "6-Speed Manual"],
        "answer": "8-Speed Automatic (8AT)"
    },
    {
        "question": "On the GAC M8, which trim level upgrades to Master Specific Wheel Rims and Adaptive Driving Beam (ADB) headlights?",
        "options": ["GT", "GL", "GX", "Comfort"],
        "answer": "GX"
    },
    {
        "question": "Which GS3 EMZOOM trim level includes Power Side Mirrors with Auto Folding + Heating alongside Automatic Headlights?",
        "options": ["GB", "GS", "SPORT+", "Standard"],
        "answer": "SPORT+"
    },
    {
        "question": "What wheel and tire dimension profile is shared across the EMPOW GE and GL sedan variants?",
        "options": ["17\" / 215/50 Tires", "18\" / 225/45 Tires", "19\" / 235/40 Tires", "16\" / 205/55 Tires"],
        "answer": "18\" / 225/45 Tires"
    }
]

# --- STATE MANAGEMENT ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

# Load live database scores
global_scores = load_global_scores()

# --- UI HEADER ---
st.title("🚘 GAC Showroom Product Knowledge Center")
st.subheader("Test your team's knowledge on current models & trim variants")
st.markdown("---")

# --- SIDEBAR: LEADERBOARD & REGISTRATION ---
with st.sidebar:
    st.header("📋 Representative Sign-In")
    
    if not st.session_state.current_user:
        name = st.text_input("Enter your full name:")
        if st.button("Register & Start"):
            if name.strip():
                st.session_state.current_user = name.strip()
                if name.strip() not in global_scores:
                    save_score_global(name.strip(), "Not Attempted")
                st.rerun()
            else:
                st.error("Please enter a valid name.")
    else:
        st.success(f"Logged in as: **{st.session_state.current_user}**")
        if st.button("Refresh Scoreboard 🔄"):
            st.rerun()
        if st.button("Log Out / New User"):
            st.session_state.current_user = None
            st.session_state.quiz_submitted = False
            st.rerun()
            
    st.markdown("---")
    st.header("🏆 Live Showroom Scoreboard")
    
    # Reload latest entries for display
    latest_scores = load_global_scores()
    if latest_scores:
        leaderboard_data = [{"Sales Executive": k, "Score / Status": v} for k, v in latest_scores.items()]
        st.table(pd.DataFrame(leaderboard_data))
    else:
        st.info("No participants registered yet.")

# --- MAIN PAGE: CONTENT & QUIZ ---
if not st.session_state.current_user:
    st.info("👋 Welcome! Please register your name in the sidebar panel to access the active training deck and variant quiz.")
    
    st.header("📚 Model Variant Quick Reference")
    cols = st.columns(3)
    for i, (model, data) in enumerate(GAC_DATA.items()):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### **GAC {model}**")
                st.caption(f"Trims: {', '.join(data['variants'])}")
                for fact in data['facts']:
                    st.markdown(f"• {fact}")
else:
    st.header(f"✏️ Variant Knowledge Assessment")
    st.write("Answer the questions below based on the current product catalogs. Good luck!")
    
    with st.form("quiz_form"):
        user_answers = {}
        for idx, q in enumerate(QUIZ_BANK):
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            user_answers[idx] = st.radio("Select the correct answer:", q['options'], key=f"q_{idx}")
            st.markdown("")
            
        submit_button = st.form_submit_button("Submit Assessment")
        
        if submit_button:
            correct_count = 0
            for idx, q in enumerate(QUIZ_BANK):
                if user_answers[idx] == q['answer']:
                    correct_count += 1
            
            final_score_str = f"{correct_count} / {len(QUIZ_BANK)}"
            save_score_global(st.session_state.current_user, final_score_str)
            st.session_state.quiz_submitted = True
            st.rerun()

    if st.session_state.quiz_submitted:
        st.balloons()
        latest_scores = load_global_scores()
        user_score_str = latest_scores.get(st.session_state.current_user, "0 / 0")
        st.success(f"🎉 Assessment completed! Your score **({user_score_str})** has been uploaded directly to the manager scoreboard.")
