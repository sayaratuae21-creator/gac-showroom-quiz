import streamlit as st
import pandas as pd
import requests
import json
import random

# Set up page config
st.set_page_config(page_title="GAC RAK - Sales Product Competency Leaderboard", layout="wide")

# --- CUSTOM BACKGROUND IMAGE ---
BACKGROUND_IMAGE_URL = "https://images.unsplash.com/photo-1617788138017-80ad40651399?auto=format&fit=crop&w=1920&q=80"

st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("{BACKGROUND_IMAGE_URL}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 3rem 3rem !important;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0px 8px 32px rgba(0, 0, 0, 0.3);
        margin-top: 2rem;
        margin-bottom: 2rem;
        max-width: 1100px !important;
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.88) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- PERMANENT DATABASE CONFIG (JSONBin.io) ---
# Paste your credentials here:
BIN_ID = "6a55d6caf5f4af5e298c1651"
API_KEY = "$2a$10$vJelScEkNfMQ2fA5Au5OrOgFYlZNy8KCgCBsaStqMSQ1tb4t8zn1y"

def load_global_db():
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
    headers = {"X-Master-Key": API_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("record", {})
        return {}
    except:
        return {}

def update_lifetime_score(name, score_to_add, total_added):
    db = load_global_db()
    
    # Clean out placeholder test accounts if they exist
    if "test_user" in db:
        del db["test_user"]
        
    if name not in db:
        db[name] = {"correct": 0, "attempted": 0}
    
    db[name]["correct"] += score_to_add
    db[name]["attempted"] += total_added
    
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": API_KEY
    }
    try:
        requests.put(url, json=db, headers=headers)
    except:
        pass

# --- COMPREHENSIVE PRODUCT KNOWLEDGE POOL ---
MASTER_QUESTION_POOL = [
    # AION V
    {"question": "What is the premium trim level name listed on the electric GAC AION V specification sheet?", "options": ["Luxury+", "Elite", "Comfort", "Executive"], "answer": "Luxury+"},
    {"question": "Does the GAC AION V Luxury+ feature a Panoramic Sunroof with an Electric Sunshade?", "options": ["Yes, standard", "No, it is optional", "No sunroof is available", "Only standard sunroof without shade"], "answer": "Yes, standard"},
    {"question": "The GAC AION V Luxury+ comes standard with which alloy wheel size setup?", "options": ["19\" Aluminum Alloy Wheels", "18\" Steel Wheels", "20\" Black Sport Rims", "17\" Multi-spoke Wheels"], "answer": "19\" Aluminum Alloy Wheels"},
    {"question": "Does the GAC AION V Luxury+ feature a power tailgate?", "options": ["Yes, standard with height memory", "No, manual tailgate only", "Optional upgrade only", "No tailgate is present"], "answer": "Yes, standard with height memory"},
    
    # EMPOW
    {"question": "On the GAC EMPOW, which variant is equipped standard with a 15W Wireless Charger?", "options": ["GL Only", "GE Only", "Both GE and GL", "Neither variant"], "answer": "GL Only"},
    {"question": "Which EMPOW trim features a Power Sunroof (with Anti-Pinch) and Power Windows standard?", "options": ["GE Only", "GL Only", "Both GE and GL", "Neither variant"], "answer": "GE Only"},
    {"question": "What tire dimension configuration is standard across both EMPOW GE and GL sedan variants?", "options": ["225/45 R18", "235/55 R20", "215/50 R17", "255/50 R20"], "answer": "225/45 R18"},
    {"question": "Does the GAC EMPOW GE trim feature standard Rear Parking Sensors?", "options": ["Yes, standard", "No, front sensors only", "No sensors are available", "Optional add-on only"], "answer": "Yes, standard"},

    # EMPOWR
    {"question": "The high-performance EMPOWR variant explicitly pairs its performance setup with what transmission setup?", "options": ["8-Speed Automatic (8AT)", "7-Speed DCT", "CVT", "6-Speed Manual"], "answer": "8-Speed Automatic (8AT)"},
    {"question": "Which visual aesthetic styling component is factory standard exclusively on the EMPOWR package?", "options": ["Car Spoiler & Front Fixed Calliper", "19\" Aluminum Wheels", "Hidden Door Handles", "Panoramic Sunroof"], "answer": "Car Spoiler & Front Fixed Calliper"},
    {"question": "What is the standard engine type utilized inside the high-performance GAC EMPOWR variant?", "options": ["2.0T", "1.5T", "2.0L Hybrid", "1.5L Eco"], "answer": "2.0T"},

    # GS3 EMZOOM
    {"question": "In the GAC GS3 EMZOOM, which variant does NOT come standard with 225/55R R18 Tires?", "options": ["SPORT+", "GB", "GS", "All variants have them"], "answer": "SPORT+"},
    {"question": "Which GS3 EMZOOM trim level includes Power Side Mirrors with Auto Folding + Heating alongside Automatic Headlights?", "options": ["SPORT+", "GB", "GS", "Comfort"], "answer": "SPORT+"},
    {"question": "In the GS3 EMZOOM, which trim does NOT come standard with a Temporary Spare Tire?", "options": ["GS and SPORT+", "GB Only", "All trims have it", "None of the trims have it"], "answer": "GS and SPORT+"},
    {"question": "Which GS3 EMZOOM variant uniquely sports a rear bumper diffuser, orange trim accents, and active exhaust valves?", "options": ["SPORT+", "GB", "GS", "GL"], "answer": "SPORT+"},
    {"question": "Do both the GS3 EMZOOM GB and GS trims come equipped with standard Electric Hidden Door Handles?", "options": ["Yes, both GB and GS have them", "Only the GS has them", "Only the GB has them", "Neither trim has them"], "answer": "Yes, both GB and GS have them"},
    {"question": "What is the high-performance package tire size equipped on the GS3 EMZOOM SPORT+?", "options": ["225/45 R19", "225/55 R18", "215/60 R17", "235/50 R19"], "answer": "225/45 R19"},

    # GS4 MAX
    {"question": "Which specification variant of the GAC GS4 MAX features upgraded R20 Wheels and Tires?", "options": ["GL+", "GL", "GB", "Luxury+"], "answer": "GL+"},
    {"question": "Do both GL and GL+ variants of the GAC GS4 MAX feature Electric Hidden Door Handles as standard exterior equipment?", "options": ["Yes, both trims", "Only GL+", "Only GL", "Neither trim has them"], "answer": "Yes, both trims"},
    {"question": "What active safety and driving assist system is standard across both GS4 MAX GL and GL+ variants?", "options": ["Adaptive Cruise Control & Lane Keep Assist", "Rear parking sensors only", "No active driver assistance", "Basic cruise control only"], "answer": "Adaptive Cruise Control & Lane Keep Assist"},
    {"question": "Does the GAC GS4 MAX GL+ feature a panoramic glass roof?", "options": ["Yes, with electric sunshade", "No, regular metal roof", "No, fixed glass roof without shade", "Optional on GL+ only"], "answer": "Yes, with electric sunshade"},

    # GS8
    {"question": "Which specific GAC GS8 variant features the 'Desert Raider Kit' including a roof rack set with tent and ladder?", "options": ["Desert Raider", "Hybrid GX AWD", "ICE GX AWD", "GL Trim"], "answer": "Desert Raider"},
    {"question": "Does the GAC GS8 Desert Raider variant feature a unique Red GAC Front Logo and black edition grille?", "options": ["Yes, exclusively", "No, it is standard on Hybrid", "No, it is only on ICE GX", "It is optional across all"], "answer": "Yes, exclusively"},
    {"question": "Which GS8 variant uniquely features eCall (emergency call system) and Audio, Video, Navigation & Telematics (AVNT)?", "options": ["Desert Raider", "Hybrid GX AWD", "ICE GX AWD", "All variants"], "answer": "Desert Raider"},
    {"question": "What size tires are standard across the entire GAC GS8 variant lineup (Hybrid GX, ICE GX, and Desert Raider)?", "options": ["255/50 R20", "235/55 R18", "225/45 R19", "265/45 R21"], "answer": "255/50 R20"},
    {"question": "Which GS8 trim is optimized for maximum fuel efficiency using an advanced dual-motor petrol-electric hybrid setup?", "options": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider", "All variants use hybrids"], "answer": "Hybrid GX AWD"},
    {"question": "Does the GAC GS8 Desert Raider include exclusive side body decals?", "options": ["Yes, standard", "No, it is a dealer option", "No side decals are on any trim", "Only on the Hybrid model"], "answer": "Yes, standard"},

    # HYPTEC HT
    {"question": "What type of advanced battery architecture chemistry is standard inside the HYPTEC HT Elite?", "options": ["Magazine Battery - LFP", "Standard Lithium Ion", "Solid State Pack", "Nickel Manganese Cobalt"], "answer": "Magazine Battery - LFP"},
    {"question": "Which HYPTEC HT variant comes equipped with distinctive upward opening rear doors?", "options": ["Ultra Gullwing Door", "Elite", "Luxury+", "GT Edition"], "answer": "Ultra Gullwing Door"},
    {"question": "Which HYPTEC HT variant features standard Four-Door Electric Unlock Release but lacks the Gullwing operation?", "options": ["Elite", "Ultra Gullwing Door", "Both variants", "Neither variant"], "answer": "Elite"},
    {"question": "What is the standard AC charging capacity rate for both the HYPTEC HT Elite and Ultra variants?", "options": ["6.6 kW", "11 kW", "22 kW", "3.6 kW"], "answer": "6.6 kW"},
    {"question": "Does the HYPTEC HT Ultra Gullwing Door variant feature an upgraded passenger calf rest and executive table?", "options": ["Yes, standard executive features", "No, standard seats only", "Optional add-on package", "Available only on the Elite"], "answer": "Yes, standard executive features"},

    # M8
    {"question": "On the premium GAC M8, which variant upgrades to Master Specific Wheel Rims?", "options": ["GX", "GT", "GL", "GB"], "answer": "GX"},
    {"question": "Which M8 variant features standard LED Headlights with Height Automatic Adjustment and Adaptive Driving Beam (ADB)?", "options": ["GX", "GT", "Both GT and GX", "Neither variant"], "answer": "GX"},
    {"question": "Do both the GT and GX luxury trims of the GAC M8 feature Side Mirrors with Position Memory & Reverse Tilt?", "options": ["Yes, both trims have it", "Only the GX has it", "Only the GT has it", "Neither trim has it"], "answer": "Yes, both trims have it"},
    {"question": "Which active and passive safety features are standard on both GT and GX trims of the GAC M8?", "options": ["Electronic Stability Program (ESP)", "Rear view camera only", "No electronic stability control", "Basic ABS only"], "answer": "Electronic Stability Program (ESP)"},
    {"question": "Does the GAC M8 GX variant feature a heated/ventilated steering wheel and premium rear seat massagers?", "options": ["Yes, standard on GX", "Only standard on GT", "Neither trim has massagers", "Optional dealer upgrade"], "answer": "Yes, standard on GX"}
]

# --- SESSION TRACKING (NO-REPEAT DECK SYSTEM) ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "unanswered_deck" not in st.session_state:
    st.session_state.unanswered_deck = []
if "current_quiz_set" not in st.session_state:
    st.session_state.current_quiz_set = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "session_correct" not in st.session_state:
    st.session_state.session_correct = 0
if "saved_answers" not in st.session_state:
    st.session_state.saved_answers = {}

def draw_new_quiz_round():
    if len(st.session_state.unanswered_deck) < 5:
        st.session_state.unanswered_deck = list(MASTER_QUESTION_POOL)
        random.shuffle(st.session_state.unanswered_deck)
    
    round_questions = []
    for _ in range(5):
        if st.session_state.unanswered_deck:
            round_questions.append(st.session_state.unanswered_deck.pop(0))
            
    st.session_state.current_quiz_set = round_questions
    st.session_state.quiz_submitted = False
    st.session_state.saved_answers = {}

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
                st.session_state.unanswered_deck = list(MASTER_QUESTION_POOL)
                random.shuffle(st.session_state.unanswered_deck)
                draw_new_quiz_round()
                st.rerun()
            else:
                st.error("Please enter your name.")
    else:
        st.success(f"Active Session: **{st.session_state.current_user}**")
        st.caption(f"📦 Unique Questions remaining in your training deck: **{len(st.session_state.unanswered_deck)}**")
        
        if st.button("Draw Another New Quiz Set 🔄"):
            draw_new_quiz_round()
            st.rerun()
            
        if st.button("Switch Account / Log Out"):
            st.session_state.current_user = None
            st.session_state.current_quiz_set = []
            st.session_state.unanswered_deck = []
            st.session_state.quiz_submitted = False
            st.session_state.saved_answers = {}
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
        # Filter out placeholder records if present
        df_leaderboard = df_leaderboard[df_leaderboard["Sales Executive"] != "test_user"]
        
        if not df_leaderboard.empty:
            df_leaderboard = df_leaderboard.sort_values(by="Cumulative Correct", ascending=False).reset_index(drop=True)
            df_leaderboard.index = df_leaderboard.index + 1
            st.table(df_leaderboard)
        else:
            st.info("No recorded stats on the scoreboard yet.")
    else:
        st.info("No recorded stats on the scoreboard yet.")

# --- MAIN WINDOW DISPLAY ---
if not st.session_state.current_user:
    st.info("👋 **Welcome to the Product Knowledge Hub.** Enter your name in the sidebar menu. The app will generate a completely random selection of questions from the master vehicle variant specification sheet every single time you sign in.")
else:
    st.header(f"✏️ 5-Question Adaptive Quiz Round")
    st.caption("Every attempt updates your cumulative showroom record score dynamically. Each question is pulled from a non-repeating deck.")
    
    # CASE 1: QUIZ IN PROGRESS
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
                # Save their selected answers to display in feedback
                st.session_state.saved_answers = {idx: user_answers[idx] for idx in range(len(st.session_state.current_quiz_set))}
                
                for idx, q in enumerate(st.session_state.current_quiz_set):
                    if user_answers[idx] == q['answer']:
                        correct_count += 1
                
                update_lifetime_score(st.session_state.current_user, correct_count, len(st.session_state.current_quiz_set))
                st.session_state.session_correct = correct_count
                st.session_state.quiz_submitted = True
                st.rerun()
                
    # CASE 2: RESULTS SUBMITTED (SHOW CORRECTIONS IN RED/GREEN)
    else:
        st.balloons()
        st.success(f"🎯 **Round Complete!** You scored **{st.session_state.session_correct} / {len(st.session_state.current_quiz_set)}** on this random draw.")
        st.markdown("### 🔍 Answer Review & Instant Training Feedback:")
        
        for idx, q in enumerate(st.session_state.current_quiz_set):
            user_ans = st.session_state.saved_answers.get(idx)
            correct_ans = q['answer']
            is_correct = (user_ans == correct_ans)
            
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            
            if is_correct:
                st.success(f"🟢 **Correct!** You selected: **{user_ans}**")
            else:
                st.error(f"🔴 **Incorrect.** You selected: **{user_ans}**  \n👉 **Correct Answer:** **{correct_ans}**")
            st.markdown("---")
            
        st.info("Your points have been added to your lifetime profile record. Check the live scoreboard on the left sidebar to see your current ranking position!")
        if st.button("Start Another Quiz Immediately"):
            draw_new_quiz_round()
            st.rerun()
