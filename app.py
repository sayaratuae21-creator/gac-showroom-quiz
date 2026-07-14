import streamlit as st
import pandas as pd
import requests
import json
import random

# Set up page config
st.set_page_config(page_title="GAC RAK - Sales Product Competency Leaderboard", layout="wide")

# --- CUSTOM BACKGROUND IMAGE ---
BACKGROUND_IMAGE_URL = "https://i.postimg.cc/g0Nw6495/GS3.png"

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
    
    /* --- TABLE CUSTOMIZATION FOR CONTRAST & CENTERING --- */
    /* Force table header text to be dark, bold, and perfectly centered */
    th {{
        color: #111111 !important;
        font-weight: bold !important;
        text-align: center !important;
        font-size: 1rem !important;
    }}
    /* Force all table cells (including numbers) to center-align and have better contrast */
    td {{
        color: #222222 !important;
        text-align: center !important;
        font-weight: 500 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# --- PERMANENT DATABASE CONFIG (JSONBin.io) ---
# Paste your credentials here:
BIN_ID = "6a55d6caf5f4af5e298c1651"
API_KEY = "$2a$10$vJelScEkNfMQ2fA5Au5OrOgFYlZNy8KCgCBsaStqMSQ1tb4t8zn1y"

# --- COMPREHENSIVE PRODUCT KNOWLEDGE POOL ---
# We added a unique "id" to each question so we can track exactly which ones the user has completed.
MASTER_QUESTION_POOL = [
    # AION V
    {"id": "aion_v_1", "question": "What is the premium trim level name listed on the electric GAC AION V specification sheet?", "options": ["Luxury+", "Elite", "Comfort", "Executive"], "answer": "Luxury+"},
    {"id": "aion_v_2", "question": "Does the GAC AION V Luxury+ feature a Panoramic Sunroof with an Electric Sunshade?", "options": ["Yes, standard", "No, it is optional", "No sunroof is available", "Only standard sunroof without shade"], "answer": "Yes, standard"},
    {"id": "aion_v_3", "question": "The GAC AION V Luxury+ comes standard with which alloy wheel size setup?", "options": ["19\" Aluminum Alloy Wheels", "18\" Steel Wheels", "20\" Black Sport Rims", "17\" Multi-spoke Wheels"], "answer": "19\" Aluminum Alloy Wheels"},
    {"id": "aion_v_4", "question": "Does the GAC AION V Luxury+ feature a power tailgate?", "options": ["Yes, standard with height memory", "No, manual tailgate only", "Optional upgrade only", "No tailgate is present"], "answer": "Yes, standard with height memory"},
    
    # EMPOW
    {"id": "empow_1", "question": "On the GAC EMPOW, which variant is equipped standard with a 15W Wireless Charger?", "options": ["GL Only", "GE Only", "Both GE and GL", "Neither variant"], "answer": "GL Only"},
    {"id": "empow_2", "question": "Which EMPOW trim features a Power Sunroof (with Anti-Pinch) and Power Windows standard?", "options": ["GE Only", "GL Only", "Both GE and GL", "Neither variant"], "answer": "GE Only"},
    {"id": "empow_3", "question": "What tire dimension configuration is standard across both EMPOW GE and GL sedan variants?", "options": ["225/45 R18", "235/55 R20", "215/50 R17", "255/50 R20"], "answer": "225/45 R18"},
    {"id": "empow_4", "question": "Does the GAC EMPOW GE trim feature standard Rear Parking Sensors?", "options": ["Yes, standard", "No, front sensors only", "No sensors are available", "Optional add-on only"], "answer": "Yes, standard"},

    # EMPOWR
    {"id": "empowr_1", "question": "The high-performance EMPOWR variant explicitly pairs its performance setup with what transmission setup?", "options": ["8-Speed Automatic (8AT)", "7-Speed DCT", "CVT", "6-Speed Manual"], "answer": "8-Speed Automatic (8AT)"},
    {"id": "empowr_2", "question": "Which visual aesthetic styling component is factory standard exclusively on the EMPOWR package?", "options": ["Car Spoiler & Front Fixed Calliper", "19\" Aluminum Wheels", "Hidden Door Handles", "Panoramic Sunroof"], "answer": "Car Spoiler & Front Fixed Calliper"},
    {"id": "empowr_3", "question": "What is the standard engine type utilized inside the high-performance GAC EMPOWR variant?", "options": ["2.0T", "1.5T", "2.0L Hybrid", "1.5L Eco"], "answer": "2.0T"},

    # GS3 EMZOOM
    {"id": "gs3_1", "question": "In the GAC GS3 EMZOOM, which variant does NOT come standard with 225/55R R18 Tires?", "options": ["SPORT+", "GB", "GS", "All variants have them"], "answer": "SPORT+"},
    {"id": "gs3_2", "question": "Which GS3 EMZOOM trim level includes Power Side Mirrors with Auto Folding + Heating alongside Automatic Headlights?", "options": ["SPORT+", "GB", "GS", "Comfort"], "answer": "SPORT+"},
    {"id": "gs3_3", "question": "In the GS3 EMZOOM, which trim does NOT come standard with a Temporary Spare Tire?", "options": ["GS and SPORT+", "GB Only", "All trims have it", "None of the trims have it"], "answer": "GS and SPORT+"},
    {"id": "gs3_4", "question": "Which GS3 EMZOOM variant uniquely sports a rear bumper diffuser, orange trim accents, and active exhaust valves?", "options": ["SPORT+", "GB", "GS", "GL"], "answer": "SPORT+"},
    {"id": "gs3_5", "question": "Do both the GS3 EMZOOM GB and GS trims come equipped with standard Electric Hidden Door Handles?", "options": ["Yes, both GB and GS have them", "Only the GS has them", "Only the GB has them", "Neither trim has them"], "answer": "Yes, both GB and GS have them"},
    {"id": "gs3_6", "question": "What is the high-performance package tire size equipped on the GS3 EMZOOM SPORT+?", "options": ["225/45 R19", "225/55 R18", "215/60 R17", "235/50 R19"], "answer": "225/45 R19"},

    # GS4 MAX
    {"id": "gs4_1", "question": "Which specification variant of the GAC GS4 MAX features upgraded R20 Wheels and Tires?", "options": ["GL+", "GL", "GB", "Luxury+"], "answer": "GL+"},
    {"id": "gs4_2", "question": "Do both GL and GL+ variants of the GAC GS4 MAX feature Electric Hidden Door Handles as standard exterior equipment?", "options": ["Yes, both trims", "Only GL+", "Only GL", "Neither trim has them"], "answer": "Yes, both trims"},
    {"id": "gs4_3", "question": "What active safety and driving assist system is standard across both GS4 MAX GL and GL+ variants?", "options": ["Adaptive Cruise Control & Lane Keep Assist", "Rear parking sensors only", "No active driver assistance", "Basic cruise control only"], "answer": "Adaptive Cruise Control & Lane Keep Assist"},
    {"id": "gs4_4", "question": "Does the GAC GS4 MAX GL+ feature a panoramic glass roof?", "options": ["Yes, with electric sunshade", "No, regular metal roof", "No, fixed glass roof without shade", "Optional on GL+ only"], "answer": "Yes, with electric sunshade"},

    # GS8
    {"id": "gs8_1", "question": "Which specific GAC GS8 variant features the 'Desert Raider Kit' including a roof rack set with tent and ladder?", "options": ["Desert Raider", "Hybrid GX AWD", "ICE GX AWD", "GL Trim"], "answer": "Desert Raider"},
    {"id": "gs8_2", "question": "Does the GAC GS8 Desert Raider variant feature a unique Red GAC Front Logo and black edition grille?", "options": ["Yes, exclusively", "No, it is standard on Hybrid", "No, it is only on ICE GX", "It is optional across all"], "answer": "Yes, exclusively"},
    {"id": "gs8_3", "question": "Which GS8 variant uniquely features eCall (emergency call system) and Audio, Video, Navigation & Telematics (AVNT)?", "options": ["Desert Raider", "Hybrid GX AWD", "ICE GX AWD", "All variants"], "answer": "Desert Raider"},
    {"id": "gs8_4", "question": "What size tires are standard across the entire GAC GS8 variant lineup (Hybrid GX, ICE GX, and Desert Raider)?", "options": ["255/50 R20", "235/55 R18", "225/45 R19", "265/45 R21"], "answer": "255/50 R20"},
    {"id": "gs8_5", "question": "Which GS8 trim is optimized for maximum fuel efficiency using an advanced dual-motor petrol-electric hybrid setup?", "options": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider", "All variants use hybrids"], "answer": "Hybrid GX AWD"},
    {"id": "gs8_6", "question": "Does the GAC GS8 Desert Raider include exclusive side body decals?", "options": ["Yes, standard", "No, it is a dealer option", "No side decals are on any trim", "Only on the Hybrid model"], "answer": "Yes, standard"},

    # HYPTEC HT
    {"id": "ht_1", "question": "What type of advanced battery architecture chemistry is standard inside the HYPTEC HT Elite?", "options": ["Magazine Battery - LFP", "Standard Lithium Ion", "Solid State Pack", "Nickel Manganese Cobalt"], "answer": "Magazine Battery - LFP"},
    {"id": "ht_2", "question": "Which HYPTEC HT variant comes equipped with distinctive upward opening rear doors?", "options": ["Ultra Gullwing Door", "Elite", "Luxury+", "GT Edition"], "answer": "Ultra Gullwing Door"},
    {"id": "ht_3", "question": "Which HYPTEC HT variant features standard Four-Door Electric Unlock Release but lacks the Gullwing operation?", "options": ["Elite", "Ultra Gullwing Door", "Both variants", "Neither variant"], "answer": "Elite"},
    {"id": "ht_4", "question": "What is the standard AC charging capacity rate for both the HYPTEC HT Elite and Ultra variants?", "options": ["6.6 kW", "11 kW", "22 kW", "3.6 kW"], "answer": "6.6 kW"},
    {"id": "ht_5", "question": "Does the HYPTEC HT Ultra Gullwing Door variant feature an upgraded passenger calf rest and executive table?", "options": ["Yes, standard executive features", "No, standard seats only", "Optional add-on package", "Available only on the Elite"], "answer": "Yes, standard executive features"},

    # M8
    {"id": "m8_1", "question": "On the premium GAC M8, which variant upgrades to Master Specific Wheel Rims?", "options": ["GX", "GT", "GL", "GB"], "answer": "GX"},
    {"id": "m8_2", "question": "Which M8 variant features standard LED Headlights with Height Automatic Adjustment and Adaptive Driving Beam (ADB)?", "options": ["GX", "GT", "Both GT and GX", "Neither variant"], "answer": "GX"},
    {"id": "m8_3", "question": "Do both the GT and GX luxury trims of the GAC M8 feature Side Mirrors with Position Memory & Reverse Tilt?", "options": ["Yes, both trims have it", "Only the GX has it", "Only the GT has it", "Neither trim has it"], "answer": "Yes, both trims have it"},
    {"id": "m8_4", "question": "Which active and passive safety features are standard on both GT and GX trims of the GAC M8?", "options": ["Electronic Stability Program (ESP)", "Rear view camera only", "No electronic stability control", "Basic ABS only"], "answer": "Electronic Stability Program (ESP)"},
    {"id": "m8_5", "question": "Does the GAC M8 GX variant feature a heated/ventilated steering wheel and premium rear seat massagers?", "options": ["Yes, standard on GX", "Only standard on GT", "Neither trim has massagers", "Optional dealer upgrade"], "answer": "Yes, standard on GX"}
]

# --- DATABASE LOAD / SAVE FUNCTIONS ---
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

def update_db_on_submission(name, score_to_add, total_added, completed_q_ids):
    db = load_global_db()
    
    if "test_user" in db:
        del db["test_user"]
        
    if name not in db:
        db[name] = {"correct": 0, "attempted": 0, "seen_ids": []}
    
    db[name]["correct"] += score_to_add
    db[name]["attempted"] += total_added
    
    # Track which questions they have answered permanently
    if "seen_ids" not in db[name]:
        db[name]["seen_ids"] = []
    
    db[name]["seen_ids"] = list(set(db[name]["seen_ids"] + completed_q_ids))
    
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Master-Key": API_KEY
    }
    try:
        requests.put(url, json=db, headers=headers)
    except:
        pass

# --- SESSION INITIALIZATION ---
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "current_quiz_set" not in st.session_state:
    st.session_state.current_quiz_set = []
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "session_correct" not in st.session_state:
    st.session_state.session_correct = 0
if "saved_answers" not in st.session_state:
    st.session_state.saved_answers = {}
if "user_unseen_deck" not in st.session_state:
    st.session_state.user_unseen_deck = []

def generate_user_round(username):
    """Draws 5 unique questions that the user has NEVER seen, with shuffled answers."""
    db = load_global_db()
    user_record = db.get(username, {})
    seen_ids = user_record.get("seen_ids", [])
    
    # Filter out questions this user has already answered in past sessions
    available_pool = [q for q in MASTER_QUESTION_POOL if q["id"] not in seen_ids]
    
    # If the user has already answered all questions in the pool, reset their deck so they can practice again!
    if len(available_pool) < 5:
        available_pool = list(MASTER_QUESTION_POOL)
        # Clear database tracking list to start fresh
        if username in db:
            db[username]["seen_ids"] = []
            requests.put(f"https://api.jsonbin.io/v3/b/{BIN_ID}", json=db, headers={"Content-Type": "application/json", "X-Master-Key": API_KEY})
            
    random.shuffle(available_pool)
    round_questions = []
    
    for _ in range(min(5, len(available_pool))):
        original_q = available_pool.pop(0)
        q_copy = dict(original_q)
        
        # Randomly shuffle option choices so correct answer is NOT always choice #1
        shuffled_options = list(q_copy["options"])
        random.shuffle(shuffled_options)
        q_copy["options"] = shuffled_options
        
        round_questions.append(q_copy)
        
    st.session_state.current_quiz_set = round_questions
    st.session_state.quiz_submitted = False
    st.session_state.saved_answers = {}
    
    # Calculate how many questions are left in their personal database pool
    st.session_state.user_unseen_deck = [q for q in MASTER_QUESTION_POOL if q["id"] not in seen_ids]

# --- HEADER UI ---
st.title("🚘 GAC Showroom Dynamic Training Engine")
st.subheader("Randomized assessments to master vehicle trims and features")
st.markdown("---")

# --- SIDEBAR LEADERBOARD & LOGIN ---
with st.sidebar:
    st.header("📋 Representative Log In")
    
    if not st.session_state.current_user:
        name = st.text_input("Enter your full name to start a new test round:")
        if st.button("Log In & Draw Fresh Quiz 🎲"):
            if name.strip():
                st.session_state.current_user = name.strip()
                generate_user_round(st.session_state.current_user)
                st.rerun()
            else:
                st.error("Please enter your name.")
    else:
        st.success(f"Active Session: **{st.session_state.current_user}**")
        
        # Accurately show how many unique questions they have left to practice
        total_qs = len(MASTER_QUESTION_POOL)
        remaining = len(st.session_state.user_unseen_deck)
        st.caption(f"📦 Unique Questions remaining in your database: **{remaining} / {total_qs}**")
        
        if st.button("Draw Another New Quiz Set 🔄"):
            generate_user_round(st.session_state.current_user)
            st.rerun()
            
        if st.button("Switch Account / Log Out"):
            st.session_state.current_user = None
            st.session_state.current_quiz_set = []
            st.session_state.quiz_submitted = False
            st.session_state.saved_answers = {}
            st.session_state.user_unseen_deck = []
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
    st.info("👋 **Welcome to the Product Knowledge Hub.** Enter your name in the sidebar menu. The app will fetch questions from the live database that you have never completed before.")
else:
    st.header(f"✏️ 5-Question Adaptive Quiz Round")
    st.caption("Each question is pulled from your persistent history to ensure no duplicate repeats!")
    
    # CASE 1: QUIZ IN PROGRESS
    if not st.session_state.quiz_submitted:
        if len(st.session_state.current_quiz_set) == 0:
            st.warning("All available questions have been successfully completed! Generating a fresh training deck...")
            generate_user_round(st.session_state.current_user)
            st.rerun()
            
        with st.form("dynamic_quiz_form"):
            user_answers = {}
            for idx, q in enumerate(st.session_state.current_quiz_set):
                st.markdown(f"**Q{idx+1}: {q['question']}**")
                user_answers[idx] = st.radio("Select choice:", q['options'], key=f"dyn_q_{idx}")
                st.markdown("")
                
            submit_round = st.form_submit_button("Submit Answers")
            
            if submit_round:
                correct_count = 0
                completed_ids = []
                st.session_state.saved_answers = {idx: user_answers[idx] for idx in range(len(st.session_state.current_quiz_set))}
                
                for idx, q in enumerate(st.session_state.current_quiz_set):
                    completed_ids.append(q["id"])
                    if user_answers[idx] == q['answer']:
                        correct_count += 1
                
                # Permanently update the score and save these seen questions to the DB
                update_db_on_submission(st.session_state.current_user, correct_count, len(st.session_state.current_quiz_set), completed_ids)
                st.session_state.session_correct = correct_count
                st.session_state.quiz_submitted = True
                st.rerun()
                
    # CASE 2: RESULTS SUBMITTED (SHOW CORRECTIONS)
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
            
        st.info("Your results are saved directly to your cloud history. You will never see these 5 questions again in this cycle!")
        if st.button("Start Another Quiz Immediately"):
            generate_user_round(st.session_state.current_user)
            st.rerun()
