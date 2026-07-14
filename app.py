import streamlit as st
import pandas as pd
import requests
import json
import random

# Set up page config
st.set_page_config(page_title="GAC RAK - Sales Product Competency Leaderboard", layout="wide")

# --- CUSTOM BACKGROUND IMAGE ---
# You can replace this link with ANY direct image link you want (e.g., from Imgur, Unsplash, or a GAC website)
BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1920&q=80"

# Inject custom CSS to set the background and style the text cards for readability
st.markdown(
    f"""
    <style>
    /* Background image for the entire app */
    [data-testid="stAppViewContainer"] {{
        background-image: url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    
    /* Make the top header area transparent */
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    
    /* Elegant frosted-glass card so the background car is beautifully visible */
    .block-container {{
        background-color: rgba(255, 255, 255, 0.4); /* High transparency */
        backdrop-filter: blur(10px); /* Frosted glass effect */
        -webkit-backdrop-filter: blur(10px);
        padding: 3rem 3rem !important;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.25); /* Shiny border */
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
        margin-bottom: 2rem;
        max-width: 1100px !important;
    }}
    
    /* Style the sidebar to match the glass style */
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.85) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- GLOBAL DATABASE CONFIG ---
DB_URL = "https://kvdb.io/MN87X9WvSgWj8U3n8v5X9f/gac_rak_showroom_cumulative_leaderboard"

def load_global_db():
    try:
        response = requests.get(DB_URL)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {}

def update_lifetime_score(name, score_to_add, total_added):
    db = load_global_db()
    if name not in db:
        db[name] = {"correct": 0, "attempted": 0}
    
    db[name]["correct"] += score_to_add
    db[name]["attempted"] += total_added
    
    try:
        requests.post(DB_URL, data=json.dumps(db))
    except:
        pass

# --- COMPREHENSIVE PRODUCT KNOWLEDGE POOL ---
MASTER_QUESTION_POOL = [
    {"question": "Which specific GAC GS8 variant features the 'Desert Raider Kit' including a roof rack set with tent and ladder?", "options": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider", "GL Trim"], "answer": "Desert Raider"},
    {"question": "Does the GAC GS8 Desert Raider variant feature a unique Red GAC Front Logo and black edition grille?", "options": ["Yes, exclusively", "No, it is standard on Hybrid", "No, it is only on ICE GX", "It is optional across all"], "answer": "Yes, exclusively"},
    {"question": "What type of advanced battery architecture chemistry is utilized standard inside the HYPTEC HT Elite?", "options": ["Magazine Battery - LFP", "Standard Lithium Ion", "Solid State Pack", "Nickel Manganese Cobalt"], "answer": "Magazine Battery - LFP"},
    {"question": "Which HYPTEC HT variant comes equipped with distinctive upward opening doors?", "options": ["Elite", "Ultra Gullwing Door", "Luxury+", "GT Edition"], "answer": "Ultra Gullwing Door"},
    {"question": "On the premium GAC M8, which variant upgrades to Master Specific Wheel Rims and Adaptive Driving Beam (ADB)?", "options": ["GT", "GX", "GL", "GB"], "answer": "GX"},
    {"question": "Do both the GT and GX luxury trims of the GAC M8 feature Side Mirrors with Position Memory & Reverse Tilt?", "options": ["Yes, both trims have it", "Only the GX has it", "Only the GT has it", "Neither trim has it"], "answer": "Yes, both trims have it"},
    {"question": "Which GS3 EMZOOM variant uniquely sports the full suite of Automatic Headlights and Power Folding + Heated Side Mirrors?", "options": ["GB", "GS", "SPORT+", "Comfort"], "answer": "SPORT+"},
    {"question": "What tire profile size is standard on the baseline GAC GS3 EMZOOM GB and GS versions?", "options": ["225/55R R18", "235/55 R20", "19-inch Alloy", "215/60 R17"], "answer": "225/55R R18"},
    {"question": "The aggressive GAC EMPOWR variant explicitly pairs its performance setup with what transmission setup?", "options": ["7-Speed DCT", "8-Speed Automatic (8AT)", "CVT", "6-Speed Manual"], "answer": "8-Speed Automatic (8AT)"},
    {"question": "Which visual aesthetic styling component is factory standard exclusively on the EMPOWR package?", "options": ["Car Spoiler & Front Fixed Calliper", "19\" Aluminum Wheels", "Hidden Door Handles", "Panoramic Sunroof"], "answer": "Car Spoiler & Front Fixed Calliper"},
    {"question": "What tire dimension configuration is standard across both EMPOW GE and GL sedan variants?", "options": ["225/45 Tires on 18\" Rims", "235/55 Tires on 20\" Rims", "215/50 Tires on 17\" Rims", "255/50 Tires on 20\" Rims"], "answer": "225/45 Tires on 18\" Rims"},
    {"question": "Which specification variant of the GS4 MAX features upgraded R20 Wheels and Tires?", "options": ["GL", "GL+", "GB", "Luxury+"], "answer": "GL+"},
    {"question": "Do both GL and GL+ variants of the GS4 MAX feature Electric Hidden Door Handles as standard exterior equipment?", "options": ["Yes, both trims", "Only GL+", "Only GL", "Neither trim handles hide"], "answer": "Yes, both trims"},
    {"question": "What configuration profile characterizes the standalone luxury variant layout of the electric AION V sheet?", "options": ["Luxury+", "Premium Comfort", "Executive AWD", "Standard Elite"], "answer": "Luxury+"}
]

# --- SESSION TRACKING FOR DYNAMIC RANDOMIZATION ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_quiz_set" not in st.session_state:
    st.session_state.current_quiz_set = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "session_correct" not in st.session_state:
    st.session_state.session_correct = 0

# --- HEADER UI ---
st.title("🚘 GAC Showroom Dynamic Training Engine")
st.subheader("Randomized assessments to master vehicle trims and features")
st.markdown("---")

# --- SIDEBAR LEADERBOARD ---
with st.sidebar:
    st.header("📋 Representative Log In")
    
    if not st.session_state.current_user:
        name = st.text_input("Enter your full name to start a new test round:")
        if st.button("Log In & Draw Fresh Quiz 🎲"):
            if name.strip():
                st.session_state.current_user = name.strip()
                st.session_state.current_quiz_set = random.sample(MASTER_QUESTION_POOL, min(5, len(MASTER_QUESTION_POOL)))
                st.session_state.quiz_submitted = False
                st.rerun()
            else:
                st.error("Please enter your name.")
    else:
        st.success(f"Active Session: **{st.session_state.current_user}**")
        if st.button("Draw Another New Quiz Set 🔄"):
            st.session_state.current_quiz_set = random.sample(MASTER_QUESTION_POOL, min(5, len(MASTER_QUESTION_POOL)))
            st.session_state.quiz_submitted = False
            st.rerun()
        if st.button("Switch Account / Log Out"):
            st.session_state.current_user = None
            st.session_state.current_quiz_set = []
            st.session_state.quiz_submitted = False
            st.rerun()
            
    st.markdown("---")
    st.header("🏆 Live Showroom Ranking")
    
    raw_db = load_global_db()
    if raw_db:
        leaderboard_rows = []
        for user, data in raw_db.items():
            correct = data.get("correct", 0)
            attempted = data.get("attempted", 0)
            accuracy = (correct / attempted * 100) if attempted > 0 else 0
            leaderboard_rows.append({
                "Sales Executive": user,
                "Cumulative Correct": correct,
                "Total Questions": attempted,
                "Accuracy": f"{accuracy:.1f}%"
            })
        
        df_leaderboard = pd.DataFrame(leaderboard_rows)
        df_leaderboard = df_leaderboard.sort_values(by="Cumulative Correct", ascending=False).reset_index(drop=True)
        df_leaderboard.index = df_leaderboard.index + 1
        st.table(df_leaderboard)
    else:
        st.info("No recorded stats on the scoreboard yet.")

# --- MAIN WINDOW DISPLAY ---
if not st.session_state.current_user:
    st.info("👋 **Welcome to the Product Knowledge Hub.** Enter your name in the sidebar menu. The app will generate a completely random selection of questions from the master vehicle variant specification sheet every single time you sign in.")
else:
    st.header(f"✏️ 5-Question Adaptive Quiz Round")
    st.caption("Every attempt updates your cumulative showroom record score dynamically.")
    
    if not st.session_state.quiz_submitted:
        with st.form("dynamic_quiz_form"):
            user_answers = {}
            for idx, q in enumerate(st.session_state.current_quiz_set):
                st.markdown(f"**Q{idx+1}: {q['question']}**")
                user_answers[idx] = st.radio("Select choice:", q['options'], key=f"dyn_q_{idx}")
                st.markdown("")
                
            submit_round = st.form_submit_button("Submit Answers")
            
            if submit_round:
                correct_count = 0
                for idx, q in enumerate(st.session_state.current_quiz_set):
                    if user_answers[idx] == q['answer']:
                        correct_count += 1
                
                update_lifetime_score(st.session_state.current_user, correct_count, len(st.session_state.current_quiz_set))
                st.session_state.session_correct = correct_count
                st.session_state.quiz_submitted = True
                st.rerun()
    else:
        st.balloons()
        st.success(f"🎯 **Round Complete!** You scored **{st.session_state.session_correct} / {len(st.session_state.current_quiz_set)}** on this random draw.")
        st.info("Your points have been added to your lifetime profile record. Check the live scoreboard on the left sidebar to see your current ranking position across the team!")
        if st.button("Start Another Quiz Immediately"):
            st.session_state.current_quiz_set = random.sample(MASTER_QUESTION_POOL, min(5, len(MASTER_QUESTION_POOL)))
            st.session_state.quiz_submitted = False
            st.rerun()    
