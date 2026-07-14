import streamlit as st
import random
import copy

# ==========================================
# 1. THE MASTER QUESTION POOL (Safe & Structured)
# ==========================================
# Every single question has a unique "id", a "category",
# a list of "options", and a "correct" answer string.
# ==========================================
MASTER_QUESTION_POOL = [
    # --- Dimensions, Weight & Capacities ---
    {
        "id": "dim_1", 
        "category": "Dimensions, Weight & Capacities", 
        "question": "What is the exact overall length of the GAC M8 in millimeters?",
        "options": ["5,212 mm", "5,089 mm", "4,975 mm", "5,156 mm"],
        "correct": "5,212 mm"
    },
    {
        "id": "dim_2", 
        "category": "Dimensions, Weight & Capacities", 
        "question": "What is the width of the GAC M8 excluding side mirrors?",
        "options": ["1,895 mm", "1,905 mm", "1,850 mm", "1,920 mm"],
        "correct": "1,895 mm"
    },
    {
        "id": "dim_3", 
        "category": "Dimensions, Weight & Capacities", 
        "question": "How much longer is the R-STYLE version of the GS3 EMZOOM compared to the standard model?",
        "options": ["25 mm", "50 mm", "10 mm", "No difference"],
        "correct": "50 mm"
    },
    {
        "id": "dim_4", 
        "category": "Dimensions, Weight & Capacities", 
        "question": "What is the fuel tank capacity of the GAC EMPOW in liters?",
        "options": ["47 Liters", "50 Liters", "55 Liters", "45 Liters"],
        "correct": "47 Liters"
    },
    {
        "id": "dim_5", 
        "category": "Dimensions, Weight & Capacities", 
        "question": "What is the cargo volume of the GAC GS3 EMZOOM with the second-row seats upright?",
        "options": ["341 Liters", "390 Liters", "420 Liters", "280 Liters"],
        "correct": "341 Liters"
    },

    # --- Engine, Drivetrain & Fuel Consumption ---
    {
        "id": "eng_1", 
        "category": "Engine, Drivetrain & Fuel Consumption", 
        "question": "How much peak torque (Nm) does the GAC EMPOW 1.5T engine produce?",
        "options": ["270 Nm", "250 Nm", "300 Nm", "220 Nm"],
        "correct": "270 Nm"
    },
    {
        "id": "eng_2", 
        "category": "Engine, Drivetrain & Fuel Consumption", 
        "question": "Who is the manufacturer of the 8-speed automatic transmission in the GAC GS8?",
        "options": ["Aisin", "ZF", "Getrag", "In-house GAC"],
        "correct": "Aisin"
    },
    {
        "id": "eng_3", 
        "category": "Engine, Drivetrain & Fuel Consumption", 
        "question": "What is the official fuel economy rating (KM/L) of the GAC GS3 EMZOOM?",
        "options": ["18.3 KM/L", "16.1 KM/L", "15.5 KM/L", "19.0 KM/L"],
        "correct": "18.3 KM/L"
    },

    # --- Suspension, Steering, Brakes & Wheels ---
    {
        "id": "sus_1", 
        "category": "Suspension, Steering, Brakes & Wheels", 
        "question": "What type of rear suspension does the GAC EMPOW utilize?",
        "options": ["Multi-link Independent", "Torsion Beam", "Double Wishbone", "MacPherson Strut"],
        "correct": "Multi-link Independent"
    },
    {
        "id": "sus_2", 
        "category": "Suspension, Steering, Brakes & Wheels", 
        "question": "What is the standard wheel size on the GAC EMPOW GL?",
        "options": ["18-inch", "17-inch", "16-inch", "19-inch"],
        "correct": "18-inch"
    },

    # --- Exterior Design, Lighting & Mirrors ---
    {
        "id": "ext_1", 
        "category": "Exterior Design, Lighting & Mirrors", 
        "question": "What is the design inspiration behind the GAC M8's front face?",
        "options": ["Awakening Lion", "Flying Dynamics", "Mecha Style", "Diamond Cut"],
        "correct": "Awakening Lion"
    },
    {
        "id": "ext_2", 
        "category": "Exterior Design, Lighting & Mirrors", 
        "question": "Do the side mirrors on the GAC GS8 feature auto-folding when locking?",
        "options": ["Yes, Standard", "No, manual only", "Only on GX trim", "Optional package"],
        "correct": "Yes, Standard"
    },

    # --- Interior Comfort, Seats & Materials ---
    {
        "id": "int_1", 
        "category": "Interior Comfort, Seats & Materials", 
        "question": "How many ways can the driver's seat be power-adjusted in the GAC GS8?",
        "options": ["8-way", "6-way", "10-way", "12-way"],
        "correct": "8-way"
    },
    {
        "id": "int_2", 
        "category": "Interior Comfort, Seats & Materials", 
        "question": "Does the GAC M8 feature second-row massage options?",
        "options": ["Yes, with multiple programs", "No, heating only", "Only on Special Request", "Only ventilation"],
        "correct": "Yes, with multiple programs"
    },

    # --- AC, Climate Control & Cabin Comfort ---
    {
        "id": "ac_1", 
        "category": "AC, Climate Control & Cabin Comfort", 
        "question": "Does GAC use PM2.5 air filters in their air conditioning systems?",
        "options": ["Yes, across all models", "Only on GAC M8", "No", "Optional extra"],
        "correct": "Yes, across all models"
    },

    # --- Infotainment, Tech & Connectivity ---
    {
        "id": "inf_1", 
        "category": "Infotainment, Tech & Connectivity", 
        "question": "What is the size of the HD LCD central touchscreen display in the GAC GS8?",
        "options": ["14.6-inch", "10.1-inch", "12.3-inch", "15.6-inch"],
        "correct": "14.6-inch"
    },

    # --- Safety, Airbags & Driver Assistance (ADAS) ---
    {
        "id": "saf_1", 
        "category": "Safety, Airbags & Driver Assistance (ADAS)", 
        "question": "Does the GAC GS8 feature driver's knee airbags?",
        "options": ["Yes, standard on GCC specs", "No", "Only on 4WD variants", "Optional"],
        "correct": "Yes, standard on GCC specs"
    }
]

# ==========================================
# 2. SESSION STATE INITIALIZATION
# ==========================================
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "seen_ids" not in st.session_state:
    st.session_state.seen_ids = []
if "current_quiz" not in st.session_state:
    st.session_state.current_quiz = []
if "user_answers" not in st.session_state:
    st.session_state.user_answers = {}
if "score" not in st.session_state:
    st.session_state.score = None

# ==========================================
# 3. ROBUST QUIZ GENERATION ENGINE
# ==========================================
def generate_user_round(username):
    st.session_state.current_user = username
    seen_ids = st.session_state.seen_ids
    
    # 🛡️ DEFENSIVE GUARD 1: Filter out any faulty questions missing ID, Options or correct keys
    valid_pool = [
        q for q in MASTER_QUESTION_POOL 
        if isinstance(q, dict) 
        and "id" in q 
        and "options" in q 
        and "correct" in q
    ]
    
    if not valid_pool:
        st.error("Error: The Question Pool has no valid question dictionaries defined!")
        return

    # Filter out questions that have already been seen in this session
    available_pool = [q for q in valid_pool if q["id"] not in seen_ids]
    
    # Fallback if all questions have been seen: Reset seen history
    if len(available_pool) < 5:
        st.session_state.seen_ids = []
        available_pool = valid_pool
    
    # Randomly select 5 unique questions from our available pool
    num_to_draw = min(len(available_pool), 5)
    selected_questions = random.sample(available_pool, num_to_draw)
    
    quiz_round = []
    for q in selected_questions:
        q_copy = copy.deepcopy(q)
        
        # 🛡️ DEFENSIVE GUARD 2: Safely handle options shuffling
        options_list = q_copy.get("options", [])
        if isinstance(options_list, list) and len(options_list) > 0:
            shuffled_options = list(options_list)
            random.shuffle(shuffled_options)
            q_copy["shuffled_options"] = shuffled_options
        else:
            # Emergency fallback if a question somehow has empty options
            q_copy["shuffled_options"] = ["No Options Provided"]
            q_copy["correct"] = "No Options Provided"
            
        quiz_round.append(q_copy)
        st.session_state.seen_ids.append(q_copy["id"])
        
    st.session_state.current_quiz = quiz_round
    st.session_state.user_answers = {}
    st.session_state.score = None

# ==========================================
# 4. USER INTERFACE (STREAMLIT APPS)
# ==========================================
st.title("🚙 GAC Showroom Dynamic Training Engine")
st.write("Randomized assessments to master vehicle trims and features")
st.markdown("---")

# Sidebar for Representative Registration / Login
with st.sidebar:
    st.subheader("📋 Representative Log In")
    username_input = st.text_input("Enter your full name to start a new test round:", key="username_box")
    
    if st.button("Log In & Draw Fresh Quiz 🗳️"):
        if username_input.strip() != "":
            generate_user_round(username_input.strip())
            st.success(f"Active Session: {username_input.strip()}")
        else:
            st.error("Please enter a valid name to proceed.")

# Main Display Panel
if st.session_state.current_user and st.session_state.current_quiz:
    st.subheader(f"Representative: **{st.session_state.current_user}**")
    
    # Render Dynamic Assessment Form
    with st.form(key="quiz_form"):
        for index, q in enumerate(st.session_state.current_quiz):
            st.markdown(f"### Q{index + 1}. *{q.get('category', 'General Knowledge')}*")
            st.write(q.get("question", "Question placeholder text?"))
            
            # Use shuffled options safely
            options = q.get("shuffled_options", ["True", "False"])
            
            # Track user response via a radio input group
            st.session_state.user_answers[q["id"]] = st.radio(
                "Select the correct spec option:",
                options,
                key=f"q_radio_{q['id']}"
            )
            st.markdown("---")
            
        submit_button = st.form_submit_button(label="Submit Assessment")
        
    # Evaluate Submission on Click
    if submit_button:
        correct_count = 0
        total_questions = len(st.session_state.current_quiz)
        
        st.subheader("Results Breakdown")
        for q in st.session_state.current_quiz:
            user_ans = st.session_state.user_answers.get(q["id"])
            correct_ans = q.get("correct")
            
            if user_ans == correct_ans:
                correct_count += 1
                st.success(f"🟢 **Q: {q.get('question')}**\n\nYour Answer: `{user_ans}` (Correct!)")
            else:
                st.error(f"🔴 **Q: {q.get('question')}**\n\nYour Answer: `{user_ans}`\n\nCorrect Spec: `{correct_ans}`")
                
        # Final Score Calculation
        score_pct = (correct_count / total_questions) * 100 if total_questions > 0 else 0
        st.session_state.score = score_pct
        
        if score_pct >= 80:
            st.balloons()
            st.success(f"🏆 Great job! You scored **{score_pct:.0f}%** ({correct_count}/{total_questions})")
        else:
            st.warning(f"💡 Practice makes perfect. You scored **{score_pct:.0f}%** ({correct_count}/{total_questions}). Study the specs and try again!")
else:
    st.info("Please enter your name in the sidebar and click **'Log In & Draw Fresh Quiz'** to begin.")
