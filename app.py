import streamlit as st
import pandas as pd
import requests
import json
import random

# Set up page config
st.set_page_config(page_title=" GAC – Product Learning ", layout="wide")
# --- CUSTOM SIDEBAR & INPUT BOX STYLING ---
st.markdown(
    """
    <style>
    /* 1. Style the text input field in the sidebar (Make it highly visible light-gray) */
    [data-testid="stSidebar"] .stTextInput input {
        background-color: #EAECEF !important;     /* Distinct light gray background */
        color: #111111 !important;                /* Dark, highly readable text */
        border: 1.5px solid #A0AAB2 !important;   /* Solid border to define the box */
        border-radius: 6px !important;            /* Clean rounded corners */
        padding: 8px 12px !important;
    }
    
    /* Highlight the box with a GAC Blue outline when clicked/focused */
    [data-testid="stSidebar"] .stTextInput input:focus {
        border-color: #0F2942 !important;
        box-shadow: 0 0 0 0.2rem rgba(15, 41, 66, 0.2) !important;
        background-color: #EAECEF !important;
    }

    /* 2. Style the table headers in the sidebar ranking */
    [data-testid="stSidebar"] table th {
        background-color: #0F2942 !important;     /* Deep Premium GAC Blue header */
        color: #FFFFFF !important;                /* Bold white text */
        font-weight: bold !important;
        text-align: center !important;
    }
    
    /* Center align the rankings data inside the table cells */
    [data-testid="stSidebar"] table td {
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

# --- COMPREHENSIVE PRODUCT KNOWLEDGE POOL (100+ QUESTIONS) ---
import streamlit as st
import pandas as pd
import random
import copy

# ==========================================================
# 1. DYNAMIC EXCEL QUESTION GENERATOR
# ==========================================================
# This function automatically reads your uploaded "GIMINI SPECS.xlsx"
# and builds a comprehensive question pool for all vehicle models.
# ==========================================================
def load_questions_from_excel(filepath="GIMINI SPECS.xlsx"):
    generated_pool = []
    question_id_counter = 1
    
    # Helper to organize questions into your standard 8 categories
    def map_to_category(feature_name):
        f_lower = str(feature_name).lower()
        if any(k in f_lower for k in ["length", "width", "height", "wheelbase", "capacity", "weight", "tank", "cargo", "volume"]):
            return "Dimensions, Weight & Capacities"
        if any(k in f_lower for k in ["engine", "displacement", "torque", "power", "transmission", "speed", "fuel", "km/l"]):
            return "Engine, Drivetrain & Fuel Consumption"
        if any(k in f_lower for k in ["suspension", "wheel", "tire", "brake", "steering"]):
            return "Suspension, Steering, Brakes & Wheels"
        if any(k in f_lower for k in ["headlight", "lamp", "mirror", "exterior", "grille", "sunroof"]):
            return "Exterior Design, Lighting & Mirrors"
        if any(k in f_lower for k in ["seat", "leather", "interior", "steering wheel", "material"]):
            return "Interior Comfort, Seats & Materials"
        if any(k in f_lower for k in ["ac", "air condition", "climate", "filter", "pm2.5"]):
            return "AC, Climate Control & Cabin Comfort"
        if any(k in f_lower for k in ["screen", "display", "bluetooth", "apple", "carplay", "android", "speaker", "usb"]):
            return "Infotainment, Tech & Connectivity"
        return "Safety, Airbags & Driver Assistance (ADAS)"

    try:
        xls = pd.ExcelFile(filepath)
        for sheet in xls.sheet_names:
            df = pd.read_excel(filepath, sheet_name=sheet, skiprows=1)
            
            # Standardize columns: Col 0: Category Group, Col 1: Feature Name, Col 2+: Trims
            df.rename(columns={df.columns[0]: 'Category_Group', df.columns[1]: 'Feature'}, inplace=True)
            
            # Find the dynamic trim columns (e.g. GB (Entry), GS (Mid), GL (Top))
            trim_cols = [c for c in df.columns if c not in ['Category_Group', 'Feature'] and not str(c).startswith('Unnamed')]
            
            for _, row in df.iterrows():
                feature = row.get('Feature')
                if pd.isna(feature) or str(feature).strip() == "" or str(feature).startswith('MAIN TECHNICAL'):
                    continue
                
                # The question MUST ask about the feature name!
                feature_str = str(feature).strip()
                
                # Skip any rows where the feature name itself accidentally parsed as a symbol
                if feature_str in ['●', '○', '■', '-', '•']:
                    continue
                
                # Create a question for each trim level
                for trim in trim_cols:
                    val_check = row[trim]
                    raw_val = str(val_check).strip() if pd.notna(val_check) else ""
                    
                    # --- TRANSLATE VALUE (THE ANSWER) ---
                    if raw_val == "" or raw_val.lower() in ['nan', '-', 'no', 'n/a']:
                        correct_val = "Not Available"
                    elif raw_val in ['●', '•', 'yes', 'Yes']:
                        correct_val = "Standard"
                    else:
                        correct_val = raw_val  # e.g., "14.6-inch HD LCD Touch Screen" or "5 Passengers (Including Driver)"
                    
                    # Clean the feature name in the question to avoid repeating details
                    q_text = f"For the GAC {sheet.strip()} ({trim.strip()}), what is the specification for '{feature_str}'?"
                    category = map_to_category(feature_str)
                    
                    # Create logical wrong answers (distractors)
                    wrong_choices = set()
                    
                    if correct_val in ["Standard", "Not Available"]:
                        wrong_choices.add("Standard" if correct_val == "Not Available" else "Not Available")
                        wrong_choices.add("Optional Feature")
                        wrong_choices.add("Premium Package Only")
                    else:
                        # Grab other values from matching trims to act as realistic distractors
                        for tc in trim_cols:
                            sib_val = row[tc]
                            sib_raw = str(sib_val).strip() if pd.notna(sib_val) else ""
                            
                            if sib_raw.lower() not in ['nan', '', raw_val.lower()]:
                                if sib_raw in ['●', '•', 'yes', 'Yes']:
                                    wrong_choices.add("Standard")
                                elif sib_raw == "" or sib_raw.lower() in ['nan', '-', 'no', 'n/a']:
                                    wrong_choices.add("Not Available")
                                else:
                                    wrong_choices.add(sib_raw)
                        
                        # Add general technical decoys if we need more options
                        decoys = ["Not Available", "Standard", "Optional Feature", "N/A"]
                        for decoy in decoys:
                            if decoy.lower() != correct_val.lower():
                                wrong_choices.add(decoy)
                    
                    # Format final option choices (Limit to 4 total)
                    options = [correct_val] + list(wrong_choices)[:3]
                    
                    # Ensure symbols don't slip into the options
                    options = [o for o in options if o not in ['●', '•', '-', 'nan', 'NaN']]
                    
                    # Final security check to ensure we have exactly 4 choices
                    if len(options) < 4:
                        for opt in ["Standard", "Not Available", "Optional Feature", "Premium Package Only"]:
                            if opt not in options:
                                options.append(opt)
                            if len(options) == 4:
                                break
                    
                    random.shuffle(options)
                    
                    generated_pool.append({
                        "id": f"auto_{sheet.strip().lower().replace(' ', '_')}_{question_id_counter}",
                        "category": category,
                        "question": q_text,
                        "options": options,
                        "correct": correct_val
                    })
                    question_id_counter += 1
                    
    except Exception as e:
        return []

    return generated_pool
    # Load the dynamic pool into memory
MASTER_QUESTION_POOL = load_questions_from_excel()
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
