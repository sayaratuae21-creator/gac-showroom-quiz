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
    # Two separate pools to guarantee a strict 2/5 (40%) Yes/No question ratio
    pool_binary_yes_no = []
    pool_technical_specs = []
    
    question_id_counter = 1
    
    def normalize_header(header_str):
        return str(header_str).strip().upper()

    def get_base_specification(val_str):
        if not val_str:
            return ""
        base = re.sub(r'\s*[\(\[].*?[\)\]]', '', str(val_str))
        base = base.split('\n')[0].split('/')[0].strip()
        return base

    def extract_only_digits(val_str):
        return "".join(re.findall(r'\d+', str(val_str)))

    try:
        xls = pd.ExcelFile(filepath)
        
        global_spec_database = {}
        feature_availability_map = {}
        parsed_sheets = []
        all_model_trim_identities = []

        # PHASE 1: Build cross-model references
        for sheet in xls.sheet_names:
            df_raw = pd.read_excel(filepath, sheet_name=sheet, header=None)
            
            header_row_idx = 0
            for idx, row in df_raw.iterrows():
                row_vals = [str(v).strip().lower() for v in row.values if pd.notna(v)]
                if len([v for v in row_vals if v != ""]) <= 1:
                    continue
                if any('feature' in r or 'specification' in r for r in row_vals):
                    header_row_idx = idx
                    break
            
            df = pd.read_excel(filepath, sheet_name=sheet, skiprows=header_row_idx)
            feat_col = next((c for c in df.columns if 'feature' in str(c).lower() or 'specification' in str(c).lower()), df.columns[0])
            trim_cols = [c for c in df.columns if c != feat_col and not str(c).startswith('Unnamed')]
            
            parsed_sheets.append({
                "sheet_name": sheet.strip(),
                "df": df,
                "feat_col": feat_col,
                "trim_cols": trim_cols
            })
            
            current_section = "GENERAL"
            
            for _, row in df.iterrows():
                feature_raw = row.get(feat_col)
                if pd.isna(feature_raw):
                    continue
                
                feature_str = str(feature_raw).strip()
                if feature_str == "" or any(keyword in feature_str.upper() for keyword in ['MAIN TECHNICAL', 'SPECIFICATION']):
                    continue
                
                trim_values = [row[t] for t in trim_cols if pd.notna(row[t])]
                if len(trim_values) == 0:
                    current_section = normalize_header(feature_str)
                    continue
                
                if current_section not in global_spec_database:
                    global_spec_database[current_section] = {}
                
                feat_key = feature_str.lower()
                if feat_key not in global_spec_database[current_section]:
                    global_spec_database[current_section][feat_key] = set()
                if feat_key not in feature_availability_map:
                    feature_availability_map[feat_key] = []
                    
                for trim in trim_cols:
                    val = row[trim]
                    model_trim_name = f"GAC {sheet.strip()} ({trim.strip()})"
                    if model_trim_name not in all_model_trim_identities:
                        all_model_trim_identities.append(model_trim_name)
                        
                    if pd.notna(val):
                        val_str = str(val).strip()
                        if val_str not in ['-', '', 'nan', 'NaN', 'Not Available']:
                            global_spec_database[current_section][feat_key].add(val_str)
                            if val_str.lower() in ['●', '•', 'yes', 'standard'] or len(val_str) > 2:
                                feature_availability_map[feat_key].append(model_trim_name)

        # PHASE 2: Generate sorted question categorizations
        for p in parsed_sheets:
            sheet_name = p["sheet_name"]
            df = p["df"]
            feat_col = p["feat_col"]
            trim_cols = p["trim_cols"]
            
            current_section = "GENERAL"
            
            for _, row in df.iterrows():
                feature_raw = row.get(feat_col)
                if pd.isna(feature_raw):
                    continue
                
                feature_str = str(feature_raw).strip()
                if feature_str == "" or any(keyword in feature_str.upper() for keyword in ['MAIN TECHNICAL', 'SPECIFICATION']):
                    continue
                
                trim_values = [row[t] for t in trim_cols if pd.notna(row[t])]
                if len(trim_values) == 0:
                    current_section = normalize_header(feature_str)
                    continue
                
                feat_key = feature_str.lower()
                all_trim_values = [str(row[t]).strip().lower() for t in trim_cols if pd.notna(row[t])]
                is_binary_feature = all(v in ['●', '○', '■', '-', '•', 'yes', 'no', 'standard', 'not available', 'n/a', ''] for v in all_trim_values)
                
                for trim in trim_cols:
                    val_check = row[trim]
                    raw_val = str(val_check).strip() if pd.notna(val_check) else ""
                    current_model_trim = f"GAC {sheet_name} ({trim.strip()})"
                    
                    # TYPE A: YES/NO BINARY INTERFACES (Mapped to separate collection)
                    if is_binary_feature:
                        correct_val = "Yes" if raw_val.lower() in ['●', '•', 'yes', 'standard'] else "No"
                        q_text = f"Is the '{feature_str}' feature available as standard on the {current_model_trim}?"
                        
                        pool_binary_yes_no.append({
                            "id": f"auto_binary_{question_id_counter}",
                            "category": current_section,
                            "question": q_text,
                            "options": ["Yes", "No"],
                            "correct": correct_val,
                            "answer": correct_val  # Added to prevent KeyError on submission
                        })
                        question_id_counter += 1
                        continue
                    
                    # TYPE B: INVERTED MODEL HUNT 
                    if raw_val not in ['-', '', 'nan', 'NaN'] and random.random() > 0.5:
                        clean_spec = get_base_specification(raw_val)
                        q_text = f"Which GAC model and variant features the following specification: '{clean_spec}' under '{feature_str}'?"
                        correct_ans = current_model_trim
                        
                        model_decoys = [m for m in all_model_trim_identities if m != correct_ans]
                        strict_decoys = [m for m in model_decoys if m not in feature_availability_map.get(feat_key, [])]
                        
                        chosen_decoys = random.sample(strict_decoys, 3) if len(strict_decoys) >= 3 else random.sample(model_decoys, 3)
                        options = [correct_ans] + chosen_decoys
                        random.shuffle(options)
                        
                        pool_technical_specs.append({
                            "id": f"auto_model_hunt_{question_id_counter}",
                            "category": current_section,
                            "question": q_text,
                            "options": options,
                            "correct": correct_ans,
                            "answer": correct_ans  # Added to prevent KeyError on submission
                        })
                        question_id_counter += 1
                        continue

                    # TYPE C: SPEC VALUE DETAILS
                    correct_val = raw_val if (raw_val != "" and raw_val.lower() not in ['nan', '-', 'no', 'n/a']) else "Not Available"
                    q_text = f"What is the '{feature_str}' for the {current_model_trim}?"
                    
                    correct_base = get_base_specification(correct_val)
                    correct_digits = extract_only_digits(correct_base)
                    correct_has_digits = any(c.isdigit() for c in correct_base)
                    
                    seen_texts = {correct_base.lower()}
                    seen_digits = {correct_digits} if correct_digits else set()
                    
                    raw_wrongs = set()
                    if current_section in global_spec_database and feat_key in global_spec_database[current_section]:
                        for val_v in global_spec_database[current_section][feat_key]:
                            raw_wrongs.add(val_v)
                            
                    selected_wrongs = []
                    for rw in raw_wrongs:
                        w_base = get_base_specification(rw)
                        w_dig = extract_only_digits(w_base)
                        if w_base == "" or w_base.lower() in seen_texts or (w_dig and w_dig in seen_digits):
                            continue
                        if correct_has_digits != any(c.isdigit() for c in w_base):
                            continue  
                            
                        seen_texts.add(w_base.lower())
                        if w_dig:
                            seen_digits.add(w_dig)
                        selected_wrongs.append(w_base)
                    
                    final_wrongs = selected_wrongs[:3]
                    while len(final_wrongs) < 3:
                        final_wrongs.append("Not Available" if "not available" not in seen_texts else f"Alternative Option {len(final_wrongs)+1}")
                    
                    options = [correct_base] + final_wrongs[:3]
                    random.shuffle(options)
                    
                    pool_technical_specs.append({
                        "id": f"auto_spec_{question_id_counter}",
                        "category": current_section,
                        "question": q_text,
                        "options": options,
                        "correct": correct_base,
                        "answer": correct_base  # Added to prevent KeyError on submission
                    })
                    question_id_counter += 1

        # ------------------------------------------------------------------
        # PHASE 3: STRICT 2/5 (40%) YES/NO BALANCE MIXER
        # ------------------------------------------------------------------
        # Total number of questions your app shows per test session (Adjust if your test length is different)
        TOTAL_QUIZ_SIZE = 10 
        target_binary_count = int(TOTAL_QUIZ_SIZE * (2 / 5)) # Exactly 4
        target_tech_count = TOTAL_QUIZ_SIZE - target_binary_count # Exactly 6

        random.shuffle(pool_binary_yes_no)
        random.shuffle(pool_technical_specs)

        # Slice precisely to match the percentage constraints
        final_pool = (
            pool_binary_yes_no[:target_binary_count] + 
            pool_technical_specs[:target_tech_count]
        )
        random.shuffle(final_pool)
        return final_pool

    except Exception as e:
        return []
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
                user_choice = st.radio(
    "Select choice:", 
    options=q['options'], 
    index=None, 
    key=f"radio_{idx}"
)
                st.markdown("")
                
            submit_round = st.form_submit_button("Submit Answers")
            
            if submit_round:
                correct_count = 0
                completed_ids = []
                st.session_state.saved_answers = {idx: user_answers.get(idx, None) for idx in range(len(st.session_state.quiz_questions))}
                
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
        # In your "Submit Answers" section:
if st.button("Submit Answers"):
    # Check if any questions were left empty
    if None in user_answers:
        st.warning("⚠️ Please answer all questions before submitting!")
    else:
        # Your existing scoring loop runs perfectly here...
        score = 0
        # Check if quiz_questions actually exists in session state first
if "quiz_questions" in st.session_state and st.session_state.quiz_questions:
    for idx, q in enumerate(st.session_state.quiz_questions):
        # ... your existing code inside the loop goes here ...
else:
    st.info("🔄 Loading quiz pool... Please refresh or start a new quiz session.")
            if user_answers[idx] == q['answer']:
                score += 1
