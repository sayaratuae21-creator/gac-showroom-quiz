import streamlit as st
import pandas as pd
import requests
import json
import random
import re
import copy

# Set up page config
import streamlit as st

# -----------------------------------------------------------
# REDESIGNED OPENING PAGE (KEEPING ORIGINAL TEXT & STRUCTURE)
# -----------------------------------------------------------

# Vibrant Title & Subtitle
st.markdown("""
    <div style="padding: 10px 0px 5px 0px;">
        <h1 style="color: #0F172A; font-weight: 800; font-size: 2.3rem; margin-bottom: 0px;">
            🚙 GAC Showroom Dynamic Training Engine
        </h1>
        <p style="color: #2563EB; font-weight: 600; font-size: 1.15rem; margin-top: 5px;">
            Randomized assessments to master vehicle trims and features
        </p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# Styled Banner Box (Original Content with Color & Border)
st.markdown("""
    <div style="
        background: linear-gradient(90deg, #EFF6FF 0%, #F0F9FF 100%);
        border-left: 5px solid #2563EB;
        border-radius: 8px;
        padding: 16px 20px;
        margin-top: 10px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.04);
    ">
        <p style="color: #1E3A8A; font-size: 1.05rem; font-weight: 500; margin: 0; line-height: 1.5;">
            👋 <strong style="color: #1D4ED8;">Welcome to the Product Knowledge Hub.</strong> 
            Enter your name in the sidebar menu. The app will fetch questions from the live database that you have never completed before.
        </p>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# MAIN LANDING PAGE HEADER
# -----------------------------------------------------------
st.markdown('<p class="main-header">GAC Motor | Product Knowledge Hub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Automotive Sales Excellence & Specification Training Engine</p>', unsafe_allow_html=True)
st.divider()

# Logged Out / Initial Welcome State
if "logged_in_user" not in st.session_state or not st.session_state["logged_in_user"]:
    
    # Quick Executive Overview Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Lineup Vehicles", value="7 Models")
    with col2:
        st.metric(label="Question Modules", value="Specs & Features")
    with col3:
        st.metric(label="Training Mode", value="Dynamic / Adaptive")

    st.markdown("---")

    # Instructions Card
    st.markdown("""
        <div class="welcome-card">
            <h4 style="margin-top:0; color:#0F172A;">Welcome Sales Executive</h4>
            <p style="color:#334155; margin-bottom:10px;">
                This portal tests real-time product knowledge, vehicle specifications, trim levels, and standard vs. optional features across the GAC lineup.
            </p>
            <ol style="color:#475569; margin-left: -15px;">
                <li>Enter your registered name in the <b>Sidebar Menu</b> on the left.</li>
                <li>Click <b>"Start Assessment Round"</b> to generate a dynamic question set.</li>
                <li>Track your cumulative accuracy on the live showroom leaderboard.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

    st.info("👈 Please enter your details in the sidebar to initiate your evaluation session.")
    
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
    th {{
        color: #111111 !important;
        font-weight: bold !important;
        text-align: center !important;
        font-size: 1rem !important;
    }}
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
BIN_ID = "6a55d6caf5f4af5e298c1651"
API_KEY = "$2a$10$vJelScEkNfMQ2fA5Au5OrOgFYlZNy8KCgCBsaStqMSQ1tb4t8zn1y"

# ==========================================================
# 1. DYNAMIC EXCEL QUESTION GENERATOR
# ==========================================================
def load_questions_from_excel(filepath="GIMINI SPECS.xlsx"):
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

    def generate_close_digits_decoys(feature_name, original_text):
        """Creates realistic numeric variations or smart domain-specific decoys without silly string repetitions."""
        fname_lower = feature_name.lower()
        
        if "suspension" in fname_lower:
            all_suspensions = ["MacPherson Strut", "Multi-Link", "Torsion Beam", "Double Wishbone"]
            return [s for s in all_suspensions if s.lower() not in original_text.lower()][:3]

        if "drivetrain" in fname_lower or "drive type" in fname_lower or "drive mode" in fname_lower:
            all_types = ["FWD", "RWD", "AWD", "4WD"]
            return [t for t in all_types if t.lower() not in original_text.lower()][:3]

        numbers = re.findall(r'\d+\.\d+|\d+', original_text)
        if not numbers:
            # NO MORE "Standard Standard" / "Premium Standard" fallbacks
            return []
            
        decoys = set()
        attempts = 0
        while len(decoys) < 3 and attempts < 40:
            attempts += 1
            altered_text = original_text
            for num_str in numbers:
                if '.' in num_str:
                    val = float(num_str)
                    offset = random.choice([0.1, 0.2, 0.3, -0.1, -0.2, -0.3])
                    new_val = round(max(0.5, val + offset), 1)
                    altered_text = altered_text.replace(num_str, str(new_val), 1)
                else:
                    val = int(num_str)
                    if val > 2000:
                        delta = random.choice([50, 100, 150, -50, -100, -150])
                    elif val > 500:
                        delta = random.choice([20, 30, 50, -20, -30, -50])
                    elif val > 100:
                        delta = random.choice([10, 15, 20, -10, -15, -20])
                    else:
                        delta = random.choice([2, 5, 8, -2, -5, -8])
                    
                    new_val = max(0, val + delta)
                    altered_text = altered_text.replace(num_str, str(new_val), 1)
            
            if altered_text != original_text and altered_text not in decoys:
                decoys.add(altered_text)
                
        return list(decoys)

    try:
        xls = pd.ExcelFile(filepath)
        global_spec_database = {}
        feature_to_model_value_map = {}
        parsed_sheets = []
        all_model_trim_identities = []

        # PHASE 1: Parse Sheets and Map Cross-Model Features
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
                if feat_key not in feature_to_model_value_map:
                    feature_to_model_value_map[feat_key] = {}
                    
                for trim in trim_cols:
                    val = row[trim]
                    model_trim_name = f"GAC {sheet.strip()} ({trim.strip()})"
                    if model_trim_name not in all_model_trim_identities:
                        all_model_trim_identities.append(model_trim_name)
                        
                    if pd.notna(val):
                        val_str = str(val).strip()
                        if val_str not in ['-', '', 'nan', 'NaN', 'Not Available', 'Not available', 'n/a', 'N/A']:
                            global_spec_database[current_section][feat_key].add(val_str)
                            feature_to_model_value_map[feat_key][model_trim_name] = get_base_specification(val_str)

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
                
                # Check for standard binary/feature toggle
                is_binary_feature = all(
                    v in ['●', '○', '■', '-', '•', 'yes', 'no', 'standard', 'equipped', 'not available', 'n/a', ''] 
                    for v in all_trim_values
                )
                
                for trim in trim_cols:
                    val_check = row[trim]
                    raw_val = str(val_check).strip() if pd.notna(val_check) else ""
                    
                    if raw_val in ['-', '', 'nan', 'NaN', 'Not Available', 'Not available', 'n/a', 'N/A']:
                        continue
                        
                    clean_trim = trim.strip()
                    model_label = f"{sheet_name.strip()} ({clean_trim})" if clean_trim else f"{sheet_name.strip()}"
                    current_model_trim = f"GAC {model_label}"
                    
                    # -----------------------------------------------------------
                    # TYPE A: CLEAN YES/NO BINARY INTERFACES
                    # -----------------------------------------------------------
                    if is_binary_feature:
                        has_feature = raw_val.lower() in ['●', '•', 'yes', 'standard', 'equipped']
                        
                        if random.random() > 0.5:
                            q_text = f"Does the {current_model_trim} come equipped with {feature_str} as a standard feature?"
                        else:
                            q_text = f"Is {feature_str} included as a standard feature on the {current_model_trim}?"
                        
                        correct_val = "Yes" if has_feature else "No"
                        
                        pool_binary_yes_no.append({
                            "id": f"auto_binary_{question_id_counter}",
                            "category": current_section,
                            "question": q_text,
                            "options": ["Yes", "No"],
                            "correct": correct_val,
                            "answer": correct_val
                        })
                        question_id_counter += 1
                        continue
                    
                    # -----------------------------------------------------------
                    # -----------------------------------------------------------
                    # CATEGORY FILTERS & SMART PHRASING
                    # -----------------------------------------------------------
                    clean_spec = get_base_specification(raw_val)
                    
                    # 1. Shared specs (Never Model Hunt)
                    shared_non_unique_specs = ['drivetrain', 'drive type', 'drive mode', 'seating', 'seat', 'doors', 'cylinders', 'fuel tank', 'valves']
                    is_shared_spec = any(s in feat_key for s in shared_non_unique_specs)

                    # 2. Performance / Measurement metrics (Phrased as "offers / features a X of Y")
                    performance_keywords = [
                        'torque', 'power', 'horsepower', 'displacement', 'speed', 'acceleration', 
                        'fuel consumption', 'weight', 'trunk', 'boot', 'cargo', 'clearance', 'volume', 'capacity'
                    ]
                    is_performance = any(kw in feat_key for kw in performance_keywords) and not is_shared_spec

                    has_brand_or_detail = any(
                        brand in raw_val.lower() 
                        for brand in ['continental', 'brembo', 'bosch', 'harman', 'alpine', 'piston', 'michelin', 'dunlop']
                    )

                    # 3. Handle Suspension Phrasing (Front vs Rear)
                    display_feature_name = feature_str
                    if 'suspension' in feat_key:
                        if 'front' in current_section.lower() and 'front' not in feat_key:
                            display_feature_name = f"Front {feature_str}"
                        elif 'rear' in current_section.lower() and 'rear' not in feat_key:
                            display_feature_name = f"Rear {feature_str}"
                    
                    # -----------------------------------------------------------
                    # TYPE B: INVERTED MODEL HUNT
                    # -----------------------------------------------------------
                    if (random.random() > 0.3 or has_brand_or_detail or is_performance) and not is_shared_spec:
                        if is_performance:
                            q_text = f"Which GAC model offers a {display_feature_name} of '{clean_spec}'?"
                        else:
                            q_text = f"Which GAC model is equipped with '{clean_spec}' for its {display_feature_name}?"
                        
                        correct_ans = current_model_trim
                        model_decoys = []
                        for m_identity in all_model_trim_identities:
                            if m_identity == current_model_trim:
                                continue
                            decoy_val = feature_to_model_value_map.get(feat_key, {}).get(m_identity, "")
                            if decoy_val.lower() == clean_spec.lower():
                                continue # Prevent duplicate correct answers
                            model_decoys.append(m_identity)
                            
                        if len(model_decoys) >= 3:
                            chosen_decoys = random.sample(model_decoys, 3)
                            options = [correct_ans] + chosen_decoys
                            random.shuffle(options)
                            
                            pool_technical_specs.append({
                                "id": f"auto_model_hunt_{question_id_counter}",
                                "category": current_section,
                                "question": q_text,
                                "options": options,
                                "correct": correct_ans,
                                "answer": correct_ans
                            })
                            question_id_counter += 1
                            continue

                    # -----------------------------------------------------------
                    # TYPE C: DIRECT SPECIFICATION DETAILS
                    # -----------------------------------------------------------
                    q_text = f"What is the '{display_feature_name}' for the {current_model_trim}?"
                    correct_base = clean_spec
                    correct_digits = extract_only_digits(correct_base)
                    correct_has_digits = any(c.isdigit() for c in correct_base)
                    
                    seen_texts = {correct_base.lower()}
                    seen_digits = {correct_digits} if correct_digits else set()
                    
                    raw_wrongs = set()
                    if current_section in global_spec_database and feat_key in global_spec_database[current_section]:
                        for val_v in global_spec_database[current_section][feat_key]:
                            if val_v.lower() not in ['-', '', 'nan', 'not available', 'n/a', 'standard', 'equipped']:
                                raw_wrongs.add(val_v)
                            
                    selected_wrongs = []
                    for rw in raw_wrongs:
                        w_base = get_base_specification(rw)
                        w_dig = extract_only_digits(w_base)
                        
                        if w_base == "" or w_base.lower() in seen_texts or (w_dig and w_dig in seen_digits):
                            continue
                        if correct_has_digits != any(c.isdigit() for c in w_base):
                            continue  
                        
                        correct_words = set(re.findall(r'\w{4,}', correct_base.lower()))
                        decoy_words = set(re.findall(r'\w{4,}', w_base.lower()))
                        if correct_words.intersection(decoy_words):
                            continue
                            
                        seen_texts.add(w_base.lower())
                        if w_dig:
                            seen_digits.add(w_dig)
                        selected_wrongs.append(w_base)
                    
                    final_wrongs = selected_wrongs[:3]
                    
                    if len(final_wrongs) < 3:
                        numeric_decoys = generate_close_digits_decoys(display_feature_name, correct_base)
                        for d_item in numeric_decoys:
                            if d_item.lower() not in seen_texts and len(final_wrongs) < 3:
                                final_wrongs.append(d_item)
                    
                    if len(final_wrongs) < 3:
                        continue

                    options = [correct_base] + final_wrongs[:3]
                    random.shuffle(options)
                    
                    pool_technical_specs.append({
                        "id": f"auto_spec_{question_id_counter}",
                        "category": current_section,
                        "question": q_text,
                        "options": options,
                        "correct": correct_base,
                        "answer": correct_base
                    })
                    question_id_counter += 1
                    
                    continue # Skip Type C if Model Hunt succeeds

                    # -----------------------------------------------------------
                    # TYPE C: DIRECT SPECIFICATION DETAILS (FOR SHARED/GENERIC METRICS)
                    # -----------------------------------------------------------
                    q_text = f"What is the '{feature_str}' for the {current_model_trim}?"
                    correct_base = clean_spec
                    correct_digits = extract_only_digits(correct_base)
                    correct_has_digits = any(c.isdigit() for c in correct_base)
                    
                    seen_texts = {correct_base.lower()}
                    seen_digits = {correct_digits} if correct_digits else set()
                    
                    raw_wrongs = set()
                    if current_section in global_spec_database and feat_key in global_spec_database[current_section]:
                        for val_v in global_spec_database[current_section][feat_key]:
                            if val_v.lower() not in ['-', '', 'nan', 'not available', 'n/a', 'standard', 'equipped']:
                                raw_wrongs.add(val_v)
                            
                    selected_wrongs = []
                    for rw in raw_wrongs:
                        w_base = get_base_specification(rw)
                        w_dig = extract_only_digits(w_base)
                        
                        if w_base == "" or w_base.lower() in seen_texts or (w_dig and w_dig in seen_digits):
                            continue
                        if correct_has_digits != any(c.isdigit() for c in w_base):
                            continue  
                        
                        correct_words = set(re.findall(r'\w{4,}', correct_base.lower()))
                        decoy_words = set(re.findall(r'\w{4,}', w_base.lower()))
                        if correct_words.intersection(decoy_words):
                            continue
                            
                        seen_texts.add(w_base.lower())
                        if w_dig:
                            seen_digits.add(w_dig)
                        selected_wrongs.append(w_base)
                    
                    final_wrongs = selected_wrongs[:3]
                    
                    # Fill missing options using domain decoys
                    if len(final_wrongs) < 3:
                        numeric_decoys = generate_close_digits_decoys(feature_str, correct_base)
                        for d_item in numeric_decoys:
                            if d_item.lower() not in seen_texts and len(final_wrongs) < 3:
                                final_wrongs.append(d_item)
                    
                    if len(final_wrongs) < 3:
                        continue

                    options = [correct_base] + final_wrongs[:3]
                    random.shuffle(options)
                    
                    pool_technical_specs.append({
                        "id": f"auto_spec_{question_id_counter}",
                        "category": current_section,
                        "question": q_text,
                        "options": options,
                        "correct": correct_base,
                        "answer": correct_base
                    })
                    question_id_counter += 1
                    
                    # TYPE C: SPEC VALUE DETAILS (STRICT NO-NONSENSE DECOYS)
                    q_text = f"What is the '{feature_str}' for the {current_model_trim}?"
                    correct_base = clean_spec
                    correct_digits = extract_only_digits(correct_base)
                    correct_has_digits = any(c.isdigit() for c in correct_base)
                    
                    seen_texts = {correct_base.lower()}
                    seen_digits = {correct_digits} if correct_digits else set()
                    
                    raw_wrongs = set()
                    if current_section in global_spec_database and feat_key in global_spec_database[current_section]:
                        for val_v in global_spec_database[current_section][feat_key]:
                            if val_v.lower() not in ['-', '', 'nan', 'not available', 'n/a', 'standard', 'equipped']:
                                raw_wrongs.add(val_v)
                            
                    selected_wrongs = []
                    for rw in raw_wrongs:
                        w_base = get_base_specification(rw)
                        w_dig = extract_only_digits(w_base)
                        
                        if w_base == "" or w_base.lower() in seen_texts or (w_dig and w_dig in seen_digits):
                            continue
                        if correct_has_digits != any(c.isdigit() for c in w_base):
                            continue  
                        
                        correct_words = set(re.findall(r'\w{4,}', correct_base.lower()))
                        decoy_words = set(re.findall(r'\w{4,}', w_base.lower()))
                        if correct_words.intersection(decoy_words):
                            continue
                            
                        seen_texts.add(w_base.lower())
                        if w_dig:
                            seen_digits.add(w_dig)
                        selected_wrongs.append(w_base)
                    
                    final_wrongs = selected_wrongs[:3]
                    
                    # Fill missing options using clean domain decoys only if numbers/categories exist
                    if len(final_wrongs) < 3:
                        numeric_decoys = generate_close_digits_decoys(feature_str, correct_base)
                        for d_item in numeric_decoys:
                            if d_item.lower() not in seen_texts and len(final_wrongs) < 3:
                                final_wrongs.append(d_item)
                    
                    # DISCARD LOW-VALUE QUESTIONS THAT CANNOT GENERATE 3 VALID WRONG ANSWERS
                    if len(final_wrongs) < 3:
                        continue

                    options = [correct_base] + final_wrongs[:3]
                    random.shuffle(options)
                    
                    pool_technical_specs.append({
                        "id": f"auto_spec_{question_id_counter}",
                        "category": current_section,
                        "question": q_text,
                        "options": options,
                        "correct": correct_base,
                        "answer": correct_base
                    })
                    question_id_counter += 1

        # PHASE 3: BALANCE MIXER (40% Yes/No, 60% Technical Specs)
        TOTAL_QUIZ_SIZE = 10 
        target_binary_count = int(TOTAL_QUIZ_SIZE * (2 / 5)) 
        target_tech_count = TOTAL_QUIZ_SIZE - target_binary_count 

        random.shuffle(pool_binary_yes_no)
        random.shuffle(pool_technical_specs)

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
    
    available_pool = [q for q in MASTER_QUESTION_POOL if q["id"] not in seen_ids]
    
    if len(available_pool) < 5:
        available_pool = list(MASTER_QUESTION_POOL)
        if username in db:
            db[username]["seen_ids"] = []
            requests.put(f"https://api.jsonbin.io/v3/b/{BIN_ID}", json=db, headers={"Content-Type": "application/json", "X-Master-Key": API_KEY})
            
    random.shuffle(available_pool)
    round_questions = []
    
    for _ in range(min(5, len(available_pool))):
        original_q = available_pool.pop(0)
        q_copy = dict(original_q)
        
        shuffled_options = list(q_copy["options"])
        random.shuffle(shuffled_options)
        q_copy["options"] = shuffled_options
        
        round_questions.append(q_copy)
        
    st.session_state.current_quiz_set = round_questions
    st.session_state.quiz_submitted = False
    st.session_state.saved_answers = {}
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
            
            if "current_quiz_set" in st.session_state and st.session_state.current_quiz_set:
                for idx, q in enumerate(st.session_state.current_quiz_set):
                    st.markdown(f"**Q{idx+1}: {q['question']}**")
                    
                    user_answers[idx] = st.radio(
                        "Select choice:", 
                        options=q['options'], 
                        index=None, 
                        key=f"radio_{idx}"
                    )
                    st.markdown("")
            else:
                st.info("🔄 Loading quiz pool... Please refresh or start a new quiz session.")
                
            submit_round = st.form_submit_button("Submit Answers")
            
            if submit_round:
                if None in user_answers.values() or len(user_answers) < len(st.session_state.current_quiz_set):
                    st.error("⚠️ Please answer all questions on the screen before submitting!")
                else:
                    correct_count = 0
                    completed_ids = []
                    
                    st.session_state.saved_answers = {idx: user_answers.get(idx, None) for idx in range(len(st.session_state.current_quiz_set))}
                    
                    for idx, q in enumerate(st.session_state.current_quiz_set):
                        completed_ids.append(q["id"])
                        if user_answers.get(idx, None) == q['answer']:
                            correct_count += 1
                    
                    update_db_on_submission(st.session_state.current_user, correct_count, len(st.session_state.current_quiz_set), completed_ids)
                    st.session_state.session_correct = correct_count
                    st.session_state.quiz_submitted = True
                    st.rerun()
                    
    # CASE 2: RESULTS SUBMITTED
    else:
        st.balloons()
        st.success(f"🎯 **Round Complete!** You scored **{st.session_state.session_correct} / {len(st.session_state.current_quiz_set)}** on this random draw.")
        st.markdown("### 🔍 Answer Review & Instant Training Feedback:")
        
        for idx, q in enumerate(st.session_state.current_quiz_set):
            user_ans = st.session_state.saved_answers.get(idx, "No Answer Given")
            correct_ans = q['answer']
            is_correct = (user_ans == correct_ans)
            
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            if is_correct:
                st.success(f"🟢 **Correct!** You selected: **{user_ans}**")
            else:
                st.error(f"🔴 **Incorrect.** You selected: **{user_ans}**  \n👉 **Correct Answer:** **{correct_ans}**")
            st.markdown("---")
            
        st.info("Your results are saved directly to your cloud history. You will never see these 5 questions again in this cycle!")
