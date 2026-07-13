import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Set up page config (must be called before other Streamlit UI code)
st.set_page_config(page_title="GAC Showroom - Sales Product Knowledge Quiz", layout="wide")

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

# --- MANUAL QUIZ QUESTIONS (seeded examples with explanations) ---
MANUAL_QUIZ = [
    {
        "question": "Which specific GAC GS8 variant comes factory-equipped with a roof rack set, tent, ladder, and custom side decals?",
        "options": ["Hybrid GX AWD", "ICE GX AWD", "Desert Raider", "GL Link"],
        "answer": "Desert Raider",
        "explanation": "The 'Desert Raider' edition is the adventure-focused trim and is described as including a roof rack set with a tent and ladder and Desert Raider side decals."
    },
    {
        "question": "What battery technology type is standard across the HYPTEC HT Elite and Ultra variants?",
        "options": ["Standard Ternary Lithium", "Magazine Battery - LFP", "Solid-State Cell", "Sodium-Ion pack"],
        "answer": "Magazine Battery - LFP",
        "explanation": "HYPTEC HT uses Magazine Battery technology utilizing LFP chemistry per the spec data."
    },
    {
        "question": "Which variant of the new GS4 MAX features the distinct upgrade of optional R20 Tires and Wheels?",
        "options": ["GL", "GL+", "GB", "GS SPORT+"],
        "answer": "GL+",
        "explanation": "The GS4 MAX GL+ is the premium variant and offers optional R20 Tires with Wheels."
    },
    {
        "question": "The high-performance EMPOWR variant pairs its 2.0T engine with which transmission configuration?",
        "options": ["7-Speed DCT", "CVT", "8-Speed Automatic (8AT)", "6-Speed Manual"],
        "answer": "8-Speed Automatic (8AT)",
        "explanation": "EMPOWR high-performance version is specified as 2T + 8AT (8-Speed Automatic)."
    },
    {
        "question": "On the GAC M8, which trim level upgrades to Master Specific Wheel Rims and Adaptive Driving Beam (ADB) headlights?",
        "options": ["GT", "GL", "GX", "Comfort"],
        "answer": "GX",
        "explanation": "The M8 GX variant is the luxury variant that upgrades to Master Specific Wheel Rims and ADB headlights."
    },
    {
        "question": "Which GS3 EMZOOM trim level includes Power Side Mirrors with Auto Folding + Heating alongside Automatic Headlights?",
        "options": ["GB", "GS", "SPORT+", "Standard"],
        "answer": "SPORT+",
        "explanation": "SPORT+ is the high-end GS3 EMZOOM variant and includes Automatic Headlights and Power Side Mirrors with Auto Folding + Heating."
    },
    {
        "question": "What wheel and tire dimension profile is shared across the EMPOW GE and GL sedan variants?",
        "options": ["17\" / 215/50 Tires", "18\" / 225/45 Tires", "19\" / 235/40 Tires", "16\" / 205/55 Tires"],
        "answer": "18\" / 225/45 Tires",
        "explanation": "The EMPOW GE and GL trims are listed with 18\" Aluminum Alloy Wheels and 225/45 tires."
    }
]

# --- QUESTION GENERATOR FROM GAC_DATA ---
def generate_questions_from_gac(gac_data, existing_questions, target=10, seed=42):
    """
    Generate additional questions based on GAC_DATA facts until reaching 'target' total questions.
    Strategy:
      - For each model, create a 'Which model is described by: <fact snippet>?' question using a random fact.
      - Options are the model names (one correct + 3 random other model names).
    """
    rand = random.Random(seed)
    questions = existing_questions.copy()
    model_names = list(gac_data.keys())

    # Helper to pick distractor models (names)
    def pick_distractors(correct_model, n=3):
        distractors = [m for m in model_names if m != correct_model]
        return rand.sample(distractors, k=min(n, len(distractors)))

    # Prevent duplicates by question text
    existing_q_texts = {q['question'] for q in questions}

    # Iterate models and add generated questions
    i = 0
    while len(questions) < target and i < len(model_names):
        model = model_names[i % len(model_names)]
        facts = gac_data[model].get("facts", [])
        if not facts:
            i += 1
            continue
        fact = rand.choice(facts)
        # Shorten fact for the prompt if very long
        prompt_fact = fact if len(fact) <= 220 else fact[:217] + "..."
        qtext = f"Which GAC model is described by: \"{prompt_fact}\""
        if qtext in existing_q_texts:
            i += 1
            continue

        opts = [model] + pick_distractors(model, 3)
        rand.shuffle(opts)
        question = {
            "question": qtext,
            "options": opts,
            "answer": model,
            "explanation": f"This fact refers to the {model}: {fact}"
        }
        questions.append(question)
        existing_q_texts.add(qtext)
        i += 1

    # If still short (very small GAC_DATA), create variant-questions as fallback
    i = 0
    while len(questions) < target and i < len(model_names):
        model = model_names[i % len(model_names)]
        variants = gac_data[model].get("variants", [])
        if variants:
            variant = variants[0]
            qtext = f"Which model includes the variant '{variant}'?"
            if qtext not in existing_q_texts:
                opts = [model] + pick_distractors(model, 3)
                random.shuffle(opts)
                question = {
                    "question": qtext,
                    "options": opts,
                    "answer": model,
                    "explanation": f"The variant '{variant}' is listed under {model}."
                }
                questions.append(question)
                existing_q_texts.add(qtext)
        i += 1

    return questions[:target]

# --- BUILD THE FULL QUIZ (auto-generate up to target total) ---
TARGET_QUESTIONS = 10  # change this to any other total you want
BASE_QUIZ = MANUAL_QUIZ.copy()
QUIZ_BANK = generate_questions_from_gac(GAC_DATA, BASE_QUIZ, target=TARGET_QUESTIONS, seed=12345)

# --- STATE MANAGEMENT ---
if "registered_users" not in st.session_state:
    st.session_state.registered_users = {}
if "user_history" not in st.session_state:
    st.session_state.user_history = {}
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "last_results" not in st.session_state:
    # store per-question result list for last submission
    st.session_state.last_results = []

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
            if name and name.strip():
                user = name.strip()
                st.session_state.current_user = user
                if user not in st.session_state.registered_users:
                    st.session_state.registered_users[user] = "Not Attempted"
                    st.session_state.user_history[user] = []
                st.rerun()
            else:
                st.error("Please enter a valid name.")
    else:
        st.success(f"Logged in as: **{st.session_state.current_user}**")
        if st.button("Log Out / Change User"):
            st.session_state.current_user = None
            st.session_state.quiz_submitted = False
            st.session_state.score = 0
            st.session_state.last_results = []
            st.rerun()

    st.markdown("---")
    st.header("🏆 Live main Showroom Scoreboard")
    if st.session_state.registered_users:
        rows = []
        for user, status in st.session_state.registered_users.items():
            last_ts = ""
            history = st.session_state.user_history.get(user, [])
            if history:
                last_ts = history[-1]["timestamp"]
            rows.append({"Sales Executive": user, "Score / Status": status, "Last Attempt": last_ts})
        st.table(pd.DataFrame(rows))
    else:
        st.info("No participants registered yet.")

# --- MAIN PAGE: CONTENT & QUIZ ---
if not st.session_state.current_user:
    st.info("👋 Welcome! Please register your name in the sidebar panel to access the active training deck and variant quiz.")

    st.header("📚 Model Variant Quick Reference")
    cols = st.columns(3)
    for i, (model, data) in enumerate(GAC_DATA.items()):
        with cols[i % 3]:
            with st.container():
                st.markdown(f"### **GAC {model}**")
                st.caption(f"Trims: {', '.join(data['variants'])}")
                for fact in data["facts"]:
                    st.markdown(f"• {fact}")
else:
    st.header(f"✏️ Variant Knowledge Assessment ({len(QUIZ_BANK)} q)")
    st.write("Answer the questions below based on the current product catalogs. Good luck!")

    # Build Quiz Form
    with st.form("quiz_form"):
        user_answers = {}
        # Shuffle options per question deterministically per user+question so UI is varied but stable per session
        for idx, q in enumerate(QUIZ_BANK):
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            options = q["options"].copy()
            random.Random(f"{st.session_state.current_user}-{idx}").shuffle(options)
            user_answers[idx] = st.radio(f"Choose an answer for Q{idx+1}:", options, key=f"q_{idx}")
            st.markdown("")

        submit_button = st.form_submit_button("Submit Assessment")

        if submit_button:
            correct_count = 0
            results = []
            for idx, q in enumerate(QUIZ_BANK):
                selected = user_answers.get(idx)
                correct = q["answer"]
                is_correct = selected == correct
                if is_correct:
                    correct_count += 1
                results.append({
                    "index": idx,
                    "question": q["question"],
                    "selected": selected,
                    "correct": correct,
                    "is_correct": is_correct,
                    "explanation": q.get("explanation", "")
                })

            total = len(QUIZ_BANK)
            final_score_str = f"{correct_count} / {total}"
            st.session_state.registered_users[st.session_state.current_user] = final_score_str
            st.session_state.score = correct_count
            st.session_state.quiz_submitted = True
            st.session_state.last_results = results

            # Append to user history with timestamp
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {"score": correct_count, "total": total, "pct": round((correct_count / total) * 100, 1), "timestamp": ts}
            st.session_state.user_history.setdefault(st.session_state.current_user, []).append(record)

            st.rerun()

    # After submission: show summary and per-question feedback
    if st.session_state.quiz_submitted:
        st.balloons()
        pct = (st.session_state.score / len(QUIZ_BANK)) * 100
        if pct >= 80:
            st.success(f"🎉 Fantastic Job! You scored {st.session_state.score} out of {len(QUIZ_BANK)} ({pct:.0f}%).")
        else:
            st.warning(f"👍 Good effort! You scored {st.session_state.score} out of {len(QUIZ_BANK)} ({pct:.0f}%).")

        st.markdown("---")
        st.subheader("Question-by-question feedback")

        # Render each question with feedback and explanation
        for res in st.session_state.last_results:
            qidx = res["index"]
            st.markdown(f"**Q{qidx+1}: {res['question']}**")
            if res["is_correct"]:
                st.success(f"Your answer: **{res['selected']}** — Correct ✅")
            else:
                st.error(f"Your answer: **{res['selected']}** — Incorrect ❌")
                st.info(f"Correct answer: **{res['correct']}**")
            if res["explanation"]:
                st.markdown(f"**Explanation:** {res['explanation']}")
            st.markdown("")

        # Allow retake: clear per-question keys so radios reset
        if st.button("Retake Quiz"):
            for idx in range(len(QUIZ_BANK)):
                key = f"q_{idx}"
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.quiz_submitted = False
            st.session_state.score = 0
            st.session_state.last_results = []
            st.rerun()

    # show recent attempts for the current user
    history = st.session_state.user_history.get(st.session_state.current_user, [])
    if history:
        st.markdown("---")
        st.subheader("Your recent attempts")
        hist_df = pd.DataFrame(history[::-1])  # latest first
        st.table(hist_df)
