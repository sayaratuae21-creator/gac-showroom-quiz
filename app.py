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
import re
import random
import pandas as pd

def load_questions_from_excel(filepath="GIMINI SPECS.xlsx"):
    generated_pool = []
    question_id_counter = 1
    
    # ----------------- TIGHT SEMANTIC SUB-GROUPS & TOUGH DECOYS -----------------
    # This prevents cross-contamination (e.g., seat ventilation showing up under seat trim)
    SEMANTIC_GROUPS = {
        "anti_theft": {
            "keywords": ["theft", "immobilizer", "alarm", "security", "burglar"],
            "decoys": ["Engine Immobilizer + Anti-Theft Alarm", "Engine Immobilizer", "Perimeter Alarm System", "Ultrasonic Intrusion Sensor", "Anti-Theft Security Alarm"]
        },
        "seat_trim": {
            "keywords": ["seat trim", "seat material", "upholstery", "seat fabric", "trim material"],
            "decoys": ["Premium Nappa Leather", "High-Quality PVC Leather", "Fabric / Cloth Seats", "Synthetic Leather & Suede Combo", "Alcantara Trimmed Seats", "Genuine Leather Trim"]
        },
        "seat_adjustment": {
            "keywords": ["adjust", "recline", "fold", "ventilation", "heating", "massage", "electric seat", "power seat", "lumbar"],
            "decoys": ["6-way Power Adjustable Driver Seat", "Manual 4-way Passenger Seat", "Front Row Seat Ventilation & Heating", "Electric Folding & Electric Recline", "Driver Seat Memory Function"]
        },
        "airbags": {
            "keywords": ["airbag", "curtain", "shield"],
            "decoys": ["Dual Front Airbags", "6 Airbags (Front, Side & Curtain)", "7 Airbags (with Driver Knee Airbag)", "8 Airbags Shield System"]
        },
        "wheel_tire": {
            "keywords": ["wheel", "tire", "alloy", "rim"],
            "decoys": ["18-inch Alloy Wheels", "19-inch Alloy Wheels", "20-inch Sporty Alloy Wheels", "21-inch Multi-Spoke Wheels"]
        },
        "audio_system": {
            "keywords": ["speaker", "sound", "audio", "dts", "dolby"],
            "decoys": ["6 Speakers High-Performance Sound", "8 Speakers Premium Audio", "11 Speakers with Subwoofer", "22-Speaker Dolby Atmos Surround"]
        },
        "ac_climate": {
            "keywords": ["ac ", "air condition", "climate", "filter", "pm2.5", "zone"],
            "decoys": ["Dual-Zone Automatic Climate Control", "Single-Zone Manual AC with Rear Vents", "Three-Zone Climate Control", "Automatic AC with PM2.5 Air Filter"]
        },
        "drivetrain_power": {
            "keywords": ["engine", "displacement", "torque", "power", "hp", "rpm", "output", "kw"],
            "decoys": ["1.5L Turbocharged (TGDI)", "2.0L Turbocharged (TG)", "177 hp / 5500 rpm", "248 hp / 5250 rpm", "265 hp / 5500 rpm"]
        },
        "transmission": {
            "keywords": ["transmission", "gearbox", "speed", "dct", "at", "cvt"],
            "decoys": ["7-Speed Wet DCT", "AISIN 8-Speed AT", "Electronically Controlled CVT (E-CVT)", "Single-Speed Reducer"]
        }
    }

    # Helper function to find which semantic subcategory a feature belongs to
    def get_semantic_subgroup(feature_name):
        f_lower = str(feature_name).lower()
        for group_name, config in SEMANTIC_GROUPS.items():
            if any(keyword in f_lower for keyword in config["keywords"]):
                return group_name
        return None

    # Helper function to strip parenthetical info, newlines, and retrieve base specification text
    def get_base_specification(val_str):
        if not val_str:
            return ""
        base = re.sub(r'\s*[\(\[].*?[\)\]]', '', str(val_str))
        base = base.split('\n')[0].split('/')[0].strip()
        return base

    def extract_only_digits(val_str):
        return "".join(re.findall(r'\d+', str(val_str)))

    def map_to_category(feature_name):
        f_lower = str(feature_name).lower()
        if any(k in f_lower for k in ["length", "width", "height", "wheelbase", "capacity", "weight", "tank", "cargo", "volume"]):
            return "Dimensions, Weight & Capacities"
        if any(k in f_lower for k in ["engine", "displacement", "torque", "power", "transmission", "speed", "fuel", "km/l", "hp", "rpm", "output", "kw"]):
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
        
        # Phase 1: Build a global pool of real values for every single feature across all sheets (models)
        global_feature_values = {}  
        global_category_values = {}  
        global_semantic_values = {g: set() for g in SEMANTIC_GROUPS.keys()}
        parsed_sheets = []
        
        for sheet in xls.sheet_names:
            df_raw = pd.read_excel(filepath, sheet_name=sheet, header=None)
            
            header_row_idx = 0
            for idx, row in df_raw.iterrows():
                row_vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
                non_empty_count = sum(1 for v in row_vals if v != "")
                if non_empty_count <= 1:
                    continue
                if any('feature' in r or 'specification' in r for r in row_vals):
                    header_row_idx = idx
                    break
            
            df = pd.read_excel(filepath, sheet_name=sheet, skiprows=header_row_idx)
            
            feat_col = None
            for col in df.columns:
                if 'feature' in str(col).lower() or 'specification' in str(col).lower():
                    feat_col = col
                    break
            if not feat_col:
                feat_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
                
            cat_col = df.columns[0]
            trim_cols = [c for c in df.columns if c != feat_col and c != cat_col and not str(c).startswith('Unnamed')]
            
            parsed_sheets.append({
                "sheet_name": sheet,
                "df": df,
                "feat_col": feat_col,
                "trim_cols": trim_cols
            })
            
            # Map values globally
            for _, row in df.iterrows():
                feature = row.get(feat_col)
                if pd.isna(feature) or str(feature).strip() == "" or str(feature).startswith('MAIN TECHNICAL'):
                    continue
                
                feat_name = str(feature).strip()
                feat_key = feat_name.lower()
                cat_name = map_to_category(feat_name)
                subgroup = get_semantic_subgroup(feat_name)
                
                if feat_key not in global_feature_values:
                    global_feature_values[feat_key] = set()
                if cat_name not in global_category_values:
                    global_category_values[cat_name] = set()
                    
                for trim in trim_cols:
                    val = row[trim]
                    if pd.notna(val):
                        val_str = str(val).strip()
                        if val_str not in ['●', '○', '■', '-', '•', 'nan', 'NaN', '']:
                            global_feature_values[feat_key].add(val_str)
                            global_category_values[cat_name].add(val_str)
                            if subgroup:
                                global_semantic_values[subgroup].add(val_str)

        # Phase 2: Generate highly competitive questions using global pools
        for p in parsed_sheets:
            sheet_name = p["sheet_name"]
            df = p["df"]
            feat_col = p["feat_col"]
            trim_cols = p["trim_cols"]
            
            for _, row in df.iterrows():
                feature = row.get(feat_col)
                if pd.isna(feature) or str(feature).strip() == "" or str(feature).startswith('MAIN TECHNICAL'):
                    continue
                
                feature_str = str(feature).strip()
                feat_key = feature_str.lower()
                category = map_to_category(feature_str)
                subgroup = get_semantic_subgroup(feature_str)
                
                # Check if it is a Yes/No (Binary) feature
                all_trim_values = [str(row[t]).strip().lower() for t in trim_cols if pd.notna(row[t])]
                is_binary_feature = all(v in ['●', '○', '■', '-', '•', 'yes', 'no', 'standard', 'not available', 'n/a', ''] for v in all_trim_values)
                
                for trim in trim_cols:
                    val_check = row[trim]
                    raw_val = str(val_check).strip() if pd.notna(val_check) else ""
                    
                    if is_binary_feature:
                        if raw_val in ['●', '•', 'yes', 'Yes', 'Standard']:
                            correct_val = "Yes, Standard"
                        else:
                            correct_val = "Not Available"
                            
                        q_text = f"Is the '{feature_str}' feature available as standard on the GAC {sheet_name.strip()} ({trim.strip()})?"
                        options = ["Yes, Standard", "Not Available", "Optional Feature", "Available in Premium Packages Only"]
                        
                    else:
                        # Technical Specification value!
                        correct_val = raw_val if (raw_val != "" and raw_val.lower() not in ['nan', '-', 'no', 'n/a']) else "Not Available"
                        q_text = f"What is the '{feature_str}' for the GAC {sheet_name.strip()} ({trim.strip()})?"
                        
                        # Set up the Deduplication and Format Matching system
                        correct_base = get_base_specification(correct_val)
                        correct_digits = extract_only_digits(correct_base)
                        correct_has_digits = any(c.isdigit() for c in correct_base)
                        
                        seen_simplified_texts = {correct_base.lower()}
                        seen_digit_sequences = {correct_digits} if correct_digits else set()
                        
                        raw_wrong_choices = set()
                        
                        # STEP 1: Strict Semantic Subgroup Isolation
                        # If the feature has a tight semantic subgroup, ONLY pull wrong choices from that subgroup!
                        if subgroup:
                            # Pull from other models with the same semantic subgroup
                            for g_val in global_semantic_values[subgroup]:
                                raw_wrong_choices.add(g_val)
                            # Pull from the hand-crafted semantic decoy database
                            for db_decoy in SEMANTIC_GROUPS[subgroup]["decoys"]:
                                raw_wrong_choices.add(db_decoy)
                        else:
                            # General feature fallback if no precise subgroup matches
                            if feat_key in global_feature_values:
                                for g_val in global_feature_values[feat_key]:
                                    raw_wrong_choices.add(g_val)
                            
                            # Standard category fallback
                            if len(raw_wrong_choices) < 5 and category in global_category_values:
                                for cat_val in global_category_values[category]:
                                    raw_wrong_choices.add(cat_val)

                        # Clean, deduplicate, and enforce format-matching
                        selected_wrongs = []
                        for raw_w in raw_wrong_choices:
                            w_base = get_base_specification(raw_w)
                            w_digits = extract_only_digits(w_base)
                            
                            if w_base == "" or w_base.lower() in seen_simplified_texts:
                                continue
                            if w_digits and w_digits in seen_digit_sequences:
                                continue
                                
                            # Format matching check
                            w_has_digits = any(c.isdigit() for c in w_base)
                            if correct_has_digits != w_has_digits:
                                continue  
                                
                            # Substring overlap checker
                            overlapping = False
                            for seen in seen_simplified_texts:
                                if w_base.lower() in seen or seen in w_base.lower():
                                    overlapping = True
                                    break
                            if overlapping:
                                continue
                                
                            seen_simplified_texts.add(w_base.lower())
                            if w_digits:
                                seen_digit_sequences.add(w_digits)
                            selected_wrongs.append(w_base)
                        
                        # Select top 3 cleanest distractors
                        final_wrongs = selected_wrongs[:3]
                        
                        # Ensure "Not Available" acts as a fallback decoy if appropriate (and format matches)
                        if len(final_wrongs) < 3 and correct_base != "Not Available" and "not available" not in seen_simplified_texts:
                            if not correct_has_digits: 
                                final_wrongs.append("Not Available")
                            
                        # Combine clean correct answer with clean wrong answers
                        options = [correct_base] + final_wrongs
                        
                        # Ultimate fallback to keep options count at exactly 4
                        while len(options) < 4:
                            options.append(f"Alternative Spec {len(options)}")
                    
                    # Shuffle options
                    random.shuffle(options)
                    
                    generated_pool.append({
                        "id": f"auto_{sheet_name.strip().lower().replace(' ', '_')}_{question_id_counter}",
                        "category": category,
                        "question": q_text,
                        "options": options,
                        "correct": correct_base if not is_binary_feature else correct_val
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
