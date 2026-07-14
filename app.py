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
    # --- Dimensions, Weight & Capacities ---
    {"id": "dim_1", "category": "Dimensions, Weight & Capacities", "question": "What is the exact overall length of the GAC M8 in millimeters?"},
    {"id": "dim_2", "category": "Dimensions, Weight & Capacities", "question": "What is the width of the GAC M8 including/excluding mirrors?"},
    {"id": "dim_3", "category": "Dimensions, Weight & Capacities", "question": "How tall is the GAC M8, and how does this height impact parking access?"},
    {"id": "dim_4", "category": "Dimensions, Weight & Capacities", "question": "What is the precise wheelbase of the GAC M8, and what does it mean for second-row legroom?"},
    {"id": "dim_5", "category": "Dimensions, Weight & Capacities", "question": "What are the length, width, and height dimensions of the GAC EMPOW GL?"},
    {"id": "dim_6", "category": "Dimensions, Weight & Capacities", "question": "How does the wheelbase of the GAC EMPOW compare to the GAC GS3 EMZOOM?"},
    {"id": "dim_7", "category": "Dimensions, Weight & Capacities", "question": "What is the length of the standard version of the GS3 EMZOOM?"},
    {"id": "dim_8", "category": "Dimensions, Weight & Capacities", "question": "How much longer is the R-STYLE version of the GS3 EMZOOM compared to the standard model?"},
    {"id": "dim_9", "category": "Dimensions, Weight & Capacities", "question": "What are the official exterior dimensions (L x W x H) of the GS3 EMZOOM?"},
    {"id": "dim_10", "category": "Dimensions, Weight & Capacities", "question": "What is the overall length of the flagship GAC GS8?"},
    {"id": "dim_11", "category": "Dimensions, Weight & Capacities", "question": "What is the exact width of the GAC GS8?"},
    {"id": "dim_12", "category": "Dimensions, Weight & Capacities", "question": "What is the height of the GAC GS8, and does it include the roof rails?"},
    {"id": "dim_13", "category": "Dimensions, Weight & Capacities", "question": "What is the wheelbase of the GAC GS8?"},
    {"id": "dim_14", "category": "Dimensions, Weight & Capacities", "question": "How does the wheelbase of the GS8 compare to the GAC M8 MPV?"},
    {"id": "dim_15", "category": "Dimensions, Weight & Capacities", "question": "What is the minimum ground clearance of the GAC GS8 under full load?"},
    {"id": "dim_16", "category": "Dimensions, Weight & Capacities", "question": "What is the front and rear track width of the GAC EMPOW?"},
    {"id": "dim_17", "category": "Dimensions, Weight & Capacities", "question": "What is the ramp angle and approach angle for the GAC GS8 4WD?"},
    {"id": "dim_18", "category": "Dimensions, Weight & Capacities", "question": "What is the departure angle of the GAC GS8?"},
    {"id": "dim_19", "category": "Dimensions, Weight & Capacities", "question": "How does the ground clearance of the GS3 EMZOOM compare to a standard hatchback?"},
    {"id": "dim_20", "category": "Dimensions, Weight & Capacities", "question": "What is the minimum turning radius of the GAC M8?"},
    {"id": "dim_21", "category": "Dimensions, Weight & Capacities", "question": "What is the curb weight of the GAC EMPOW GL in kilograms?"},
    {"id": "dim_22", "category": "Dimensions, Weight & Capacities", "question": "What is the gross vehicle weight rating (GVWR) of the GAC GS8?"},
    {"id": "dim_23", "category": "Dimensions, Weight & Capacities", "question": "What is the curb weight of the GAC GS3 EMZOOM GB trim?"},
    {"id": "dim_24", "category": "Dimensions, Weight & Capacities", "question": "How much heavier is the GS8 AWD compared to the GS8 2WD variant?"},
    {"id": "dim_25", "category": "Dimensions, Weight & Capacities", "question": "What is the maximum payload capacity of the GAC M8 MPV?"},
    {"id": "dim_26", "category": "Dimensions, Weight & Capacities", "question": "What is the curb weight of the GAC M8?"},
    {"id": "dim_27", "category": "Dimensions, Weight & Capacities", "question": "What is the fuel tank capacity of the GAC EMPOW (in liters)?"},
    {"id": "dim_28", "category": "Dimensions, Weight & Capacities", "question": "How many liters of fuel can the GAC GS8 tank hold?"},
    {"id": "dim_29", "category": "Dimensions, Weight & Capacities", "question": "What is the fuel tank capacity of the GS3 EMZOOM?"},
    {"id": "dim_30", "category": "Dimensions, Weight & Capacities", "question": "What is the cargo volume of the GAC GS3 EMZOOM with the second-row seats upright?"},
    {"id": "dim_31", "category": "Dimensions, Weight & Capacities", "question": "What is the maximum cargo volume of the GS3 EMZOOM when second-row seats are folded flat?"},
    {"id": "dim_32", "category": "Dimensions, Weight & Capacities", "question": "What is the trunk depth of the GAC M8 when the third-row seats are folded down?"},
    {"id": "dim_33", "category": "Dimensions, Weight & Capacities", "question": "How many liters of cargo space are available behind the third row of the GAC GS8?"},
    {"id": "dim_34", "category": "Dimensions, Weight & Capacities", "question": "Can the GAC M8 accommodate golf bags in the back with all three rows in use?"},
    {"id": "dim_35", "category": "Dimensions, Weight & Capacities", "question": "What is the maximum towing capacity of the GAC GS8?"},

    # --- Engine, Drivetrain & Fuel Consumption ---
    {"id": "eng_1", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the displacement and engine type of the GAC EMPOW GL?"},
    {"id": "eng_2", "category": "Engine, Drivetrain & Fuel Consumption", "question": "How much horsepower does the GAC EMPOW 1.5L turbo engine produce?"},
    {"id": "eng_3", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the peak torque output (in Nm) of the GAC EMPOW, and at what RPM range is it achieved?"},
    {"id": "eng_4", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What engine powers the GAC GS8, and what is its official displacement?"},
    {"id": "eng_5", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the maximum horsepower output of the GAC GS8 2.0T engine?"},
    {"id": "eng_6", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the peak torque output of the GAC GS8?"},
    {"id": "eng_7", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What are the performance specs of the GS3 EMZOOM’s 1.5TG engine (HP and Torque)?"},
    {"id": "eng_8", "category": "Engine, Drivetrain & Fuel Consumption", "question": "At what RPM range does the GS3 EMZOOM reach its maximum torque of 270 Nm?"},
    {"id": "eng_9", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the engine output (power and torque) of the flagship GAC M8?"},
    {"id": "eng_10", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the thermal efficiency percentage of GAC's 1.5TG engine used in the GS3 EMZOOM?"},
    {"id": "eng_11", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What type of gearbox is fitted to the GAC EMPOW?"},
    {"id": "eng_12", "category": "Engine, Drivetrain & Fuel Consumption", "question": "How many forward speeds does the GAC EMPOW transmission have?"},
    {"id": "eng_13", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What transmission is paired with the GAC GS8’s 2.0TGDI engine?"},
    {"id": "eng_14", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Who is the manufacturer of the 8-speed automatic transmission in the GAC GS8?"},
    {"id": "eng_15", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What type of transmission is used in the GS3 EMZOOM?"},
    {"id": "eng_16", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What does \"WDCT\" stand for in the GS3 EMZOOM's transmission specifications?"},
    {"id": "eng_17", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Is the GAC EMPOW front-wheel drive (FWD) or rear-wheel drive (RWD)?"},
    {"id": "eng_18", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Does the GS3 EMZOOM come with an All-Wheel Drive (AWD) option?"},
    {"id": "eng_19", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What are the key differences between the GS8 2WD and 4WD drivetrain systems?"},
    {"id": "eng_20", "category": "Engine, Drivetrain & Fuel Consumption", "question": "How does the AWD system in the GS8 distribute torque between the front and rear axles?"},
    {"id": "eng_21", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Does the GAC M8 utilize a front-wheel-drive or rear-wheel-drive layout?"},
    {"id": "eng_22", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the official fuel economy rating (KM/L) of the GAC GS3 EMZOOM?"},
    {"id": "eng_23", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the fuel economy rating of the GAC EMKOO Hybrid?"},
    {"id": "eng_24", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the 0 to 100 km/h acceleration time of the GS3 EMZOOM?"},
    {"id": "eng_25", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the 0 to 100 km/h acceleration of the GAC EMPOW?"},
    {"id": "eng_26", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What fuel grade (octane rating) is recommended for the GAC GS8?"},
    {"id": "eng_27", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Does the GAC M8 have an eco-driving mode to optimize fuel consumption?"},
    {"id": "eng_28", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What are the official fuel consumption figures for the GAC GS8 in city vs. highway driving?"},
    {"id": "eng_29", "category": "Engine, Drivetrain & Fuel Consumption", "question": "How does the GPMA platform contribute to the performance and efficiency of GAC vehicles?"},
    {"id": "eng_30", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What driving modes are available on the GAC GS8 4WD?"},
    {"id": "eng_31", "category": "Engine, Drivetrain & Fuel Consumption", "question": "How does \"Sport+\" or \"Track\" mode change the instrument cluster and exhaust note in the EMPOW?"},
    {"id": "eng_32", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Does the GS3 EMZOOM offer selectable driving modes, and if so, what are they?"},
    {"id": "eng_33", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is GAC's \"MegaWave Power\" technology?"},
    {"id": "eng_34", "category": "Engine, Drivetrain & Fuel Consumption", "question": "What is the function of the \"AVDC Shadow Driver\" system in the GAC GS8?"},
    {"id": "eng_35", "category": "Engine, Drivetrain & Fuel Consumption", "question": "Does the GAC M8 utilize a mild-hybrid system or is it purely petrol-powered in the standard GCC spec?"},

    # --- Suspension, Steering, Brakes & Wheels ---
    {"id": "sus_1", "category": "Suspension, Steering, Brakes & Wheels", "question": "What type of front suspension is used on the GAC EMPOW?"},
    {"id": "sus_2", "category": "Suspension, Steering, Brakes & Wheels", "question": "What type of rear suspension does the GAC EMPOW utilize?"},
    {"id": "sus_3", "category": "Suspension, Steering, Brakes & Wheels", "question": "Describe the front suspension setup of the GAC GS8."},
    {"id": "sus_4", "category": "Suspension, Steering, Brakes & Wheels", "question": "Describe the rear suspension setup of the GAC GS8."},
    {"id": "sus_5", "category": "Suspension, Steering, Brakes & Wheels", "question": "What type of rear suspension is configured on the GS3 EMZOOM?"},
    {"id": "sus_6", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the suspension setup of the GAC M8?"},
    {"id": "sus_7", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the \"Megastar Chassis,\" and which models feature it?"},
    {"id": "sus_8", "category": "Suspension, Steering, Brakes & Wheels", "question": "What does the Electromagnetic Suspension (SDC) on the GAC M8 do?"},
    {"id": "sus_9", "category": "Suspension, Steering, Brakes & Wheels", "question": "How does the GAC GS8's Megastar chassis balance ride comfort with high-speed handling?"},
    {"id": "sus_10", "category": "Suspension, Steering, Brakes & Wheels", "question": "What type of power steering system is standard across GAC models (e.g., EPS)?"},
    {"id": "sus_11", "category": "Suspension, Steering, Brakes & Wheels", "question": "Is the steering wheel column manually adjustable or power-adjustable on the GAC GS8 GT?"},
    {"id": "sus_12", "category": "Suspension, Steering, Brakes & Wheels", "question": "Does the GAC EMPOW feature speed-sensitive power steering?"},
    {"id": "sus_13", "category": "Suspension, Steering, Brakes & Wheels", "question": "Can you adjust the steering feel/weight (e.g., Comfort, Sport, Light) on GAC vehicles?"},
    {"id": "sus_14", "category": "Suspension, Steering, Brakes & Wheels", "question": "How many turns lock-to-lock does the GAC M8 steering wheel require?"},
    {"id": "sus_15", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the front brake disc type on the GAC EMPOW GL (e.g., ventilated)?"},
    {"id": "sus_16", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the rear brake disc type on the GAC EMPOW GL?"},
    {"id": "sus_17", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the 100-0 km/h braking distance of the GAC GS3 EMZOOM?"},
    {"id": "sus_18", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the braking setup (front and rear) for the GAC GS8?"},
    {"id": "sus_19", "category": "Suspension, Steering, Brakes & Wheels", "question": "Does the GAC GS8 feature Hydraulic Brake Assist (HBA)?"},
    {"id": "sus_20", "category": "Suspension, Steering, Brakes & Wheels", "question": "What are the key benefits of the Electronic Parking Brake (EPB) with Auto-Hold in GAC cars?"},
    {"id": "sus_21", "category": "Suspension, Steering, Brakes & Wheels", "question": "Does the brake system in GAC cars feature a Brake Override System (BOS)?"},
    {"id": "sus_22", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the standard wheel size on the GAC EMPOW GL?"},
    {"id": "sus_23", "category": "Suspension, Steering, Brakes & Wheels", "question": "What are the exact tire specifications (width/aspect ratio/rim diameter) of the GAC EMPOW GL?"},
    {"id": "sus_24", "category": "Suspension, Steering, Brakes & Wheels", "question": "What wheel size options are available for the GAC GS8 (e.g., GL vs. GX)?"},
    {"id": "sus_25", "category": "Suspension, Steering, Brakes & Wheels", "question": "What are the tire dimensions for the GAC GS3 EMZOOM GB trim?"},
    {"id": "sus_26", "category": "Suspension, Steering, Brakes & Wheels", "question": "What wheel design/finish is offered on the GS3 EMZOOM R-Style?"},
    {"id": "sus_27", "category": "Suspension, Steering, Brakes & Wheels", "question": "What is the \"Star Floating Wheel Hub\" on the GAC M8?"},
    {"id": "sus_28", "category": "Suspension, Steering, Brakes & Wheels", "question": "Do GAC vehicles come with a temporary spare wheel or a full-size spare?"},
    {"id": "sus_29", "category": "Suspension, Steering, Brakes & Wheels", "question": "Where is the spare tire located on the GAC GS8?"},
    {"id": "sus_30", "category": "Suspension, Steering, Brakes & Wheels", "question": "Are GAC alloy wheels fitted with anti-theft wheel bolts?"},

    # --- Exterior Design, Lighting & Mirrors ---
    {"id": "ext_1", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the design inspiration behind the GAC M8's \"Awakening Lion\" front face?"},
    {"id": "ext_2", "category": "Exterior Design, Lighting & Mirrors", "question": "How many chrome-plated vertical trim strips are on the front of the GAC M8?"},
    {"id": "ext_3", "category": "Exterior Design, Lighting & Mirrors", "question": "What styling package is applied specifically to the GAC GS3 EMZOOM R-Style?"},
    {"id": "ext_4", "category": "Exterior Design, Lighting & Mirrors", "question": "What unique exhaust layout does the GS3 EMZOOM R-Style feature?"},
    {"id": "ext_5", "category": "Exterior Design, Lighting & Mirrors", "question": "Describe the \"Rhythmic Groove\" design on the GAC EMKOO front grille."},
    {"id": "ext_6", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the aerodynamic benefit of the mecha-style spoiler on GAC SUVs?"},
    {"id": "ext_7", "category": "Exterior Design, Lighting & Mirrors", "question": "Do GAC vehicles feature hidden or flush-fitting door handles?"},
    {"id": "ext_8", "category": "Exterior Design, Lighting & Mirrors", "question": "How do the electric hidden door handles on the GS3 EMZOOM operate when you approach the car?"},
    {"id": "ext_9", "category": "Exterior Design, Lighting & Mirrors", "question": "What type of headlight technology is standard on the GAC EMPOW (e.g., LED or Halogen)?"},
    {"id": "ext_10", "category": "Exterior Design, Lighting & Mirrors", "question": "How many LED bulbs are embedded in the Daytime Running Lights (DRLs) of the GS3 EMZOOM?"},
    {"id": "ext_11", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the design name of the rear taillights on the GAC GS3 EMZOOM?"},
    {"id": "ext_12", "category": "Exterior Design, Lighting & Mirrors", "question": "How many LED bulbs make up the 3D effect \"Glowing Dart\" taillights on the GS3 EMZOOM?"},
    {"id": "ext_13", "category": "Exterior Design, Lighting & Mirrors", "question": "Do GAC vehicles offer \"Follow Me Home\" delay-off headlights?"},
    {"id": "ext_14", "category": "Exterior Design, Lighting & Mirrors", "question": "What are the \"Awakening Eye\" headlamps on the GAC M8, and how do they function?"},
    {"id": "ext_15", "category": "Exterior Design, Lighting & Mirrors", "question": "What are the \"Light Saber\" styled taillights on the GAC EMKOO?"},
    {"id": "ext_16", "category": "Exterior Design, Lighting & Mirrors", "question": "Does the GAC GS8 offer an Adaptive Driving Beam (ADB) headlight system?"},
    {"id": "ext_17", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the \"Welcome Headlamps\" feature on the GAC GS8?"},
    {"id": "ext_18", "category": "Exterior Design, Lighting & Mirrors", "question": "Are the fog lights (front and rear) standard LED units across all GAC trims?"},
    {"id": "ext_19", "category": "Exterior Design, Lighting & Mirrors", "question": "Are the exterior side mirrors on the GAC EMPOW GL power-adjustable and heated?"},
    {"id": "ext_20", "category": "Exterior Design, Lighting & Mirrors", "question": "Do GAC side mirrors automatically fold when locking the vehicle?"},
    {"id": "ext_21", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the \"Reversing Auto Flip\" function on the GAC GS8 side mirrors?"},
    {"id": "ext_22", "category": "Exterior Design, Lighting & Mirrors", "question": "Do GAC side mirrors feature integrated LED turn signal indicators?"},
    {"id": "ext_23", "category": "Exterior Design, Lighting & Mirrors", "question": "Is the rear window defogger standard on GAC SUVs?"},
    {"id": "ext_24", "category": "Exterior Design, Lighting & Mirrors", "question": "Do GAC models feature acoustic/double-glazed glass for improved cabin quietness?"},
    {"id": "ext_25", "category": "Exterior Design, Lighting & Mirrors", "question": "Which GAC models/trims feature factory-tinted rear privacy glass?"},
    {"id": "ext_26", "category": "Exterior Design, Lighting & Mirrors", "question": "Is the inside rearview mirror auto-dimming on the GAC GS8?"},
    {"id": "ext_27", "category": "Exterior Design, Lighting & Mirrors", "question": "Does the GAC EMPOW feature a standard sunroof or a panoramic sunroof?"},
    {"id": "ext_28", "category": "Exterior Design, Lighting & Mirrors", "question": "Describe the panoramic sunroof on the GAC GS3 EMZOOM (is it openable)?"},
    {"id": "ext_29", "category": "Exterior Design, Lighting & Mirrors", "question": "Does the GAC GS8 have a panoramic sunroof with an electric sunshade?"},
    {"id": "ext_30", "category": "Exterior Design, Lighting & Mirrors", "question": "Which GAC models feature an electric power tailgate?"},
    {"id": "ext_31", "category": "Exterior Design, Lighting & Mirrors", "question": "Does the GAC GS8 tailgate have a height memory function?"},
    {"id": "ext_32", "category": "Exterior Design, Lighting & Mirrors", "question": "What is the \"Sensor-Activated\" power tailgate on the GAC M8 and how does it work?"},
    {"id": "ext_33", "category": "Exterior Design, Lighting & Mirrors", "question": "Is there a physical button inside the cabin to open the tailgate on GAC SUVs?"},
    {"id": "ext_34", "category": "Exterior Design, Lighting & Mirrors", "question": "Are roof rails standard on all GAC SUV trims?"},
    {"id": "ext_35", "category": "Exterior Design, Lighting & Mirrors", "question": "What type of antenna is fitted on GAC vehicles (e.g., shark fin)?"},

    # --- Interior Comfort, Seats & Materials ---
    {"id": "int_1", "category": "Interior Comfort, Seats & Materials", "question": "What seat upholstery material is used in the GAC EMPOW GL (leather, fabric, or combination)?"},
    {"id": "int_2", "category": "Interior Comfort, Seats & Materials", "question": "Are fabric seats available on any GAC GS8 entry-level trims?"},
    {"id": "int_3", "category": "Interior Comfort, Seats & Materials", "question": "Describe the diamond-stitching pattern available in the GAC GS8 interior."},
    {"id": "int_4", "category": "Interior Comfort, Seats & Materials", "question": "What seat upholstery material is used in the GS3 EMZOOM GB trim?"},
    {"id": "int_5", "category": "Interior Comfort, Seats & Materials", "question": "What interior color schemes are available for the GAC GS8?"},
    {"id": "int_6", "category": "Interior Comfort, Seats & Materials", "question": "What is the steering wheel material on the GAC EMPOW GL?"},
    {"id": "int_7", "category": "Interior Comfort, Seats & Materials", "question": "Does the GAC GS8 feature a leather-wrapped steering wheel?"},
    {"id": "int_8", "category": "Interior Comfort, Seats & Materials", "question": "How many ways can the driver’s seat be power-adjusted in the GAC GS8?"},
    {"id": "int_9", "category": "Interior Comfort, Seats & Materials", "question": "Does the GAC EMPOW feature electric seat adjustments for the driver?"},
    {"id": "int_10", "category": "Interior Comfort, Seats & Materials", "question": "Is the front passenger seat power-adjustable or manual in the GAC GS8 GT/GX trims?"},
    {"id": "int_11", "category": "Interior Comfort, Seats & Materials", "question": "How many ways can you adjust the front passenger seat in the GS3 EMZOOM?"},
    {"id": "int_12", "category": "Interior Comfort, Seats & Materials", "question": "Does the driver’s seat in the GAC GS8 feature lumbar support adjustment?"},
    {"id": "int_13", "category": "Interior Comfort, Seats & Materials", "question": "Does the driver’s seat in the GAC GS8 have a memory function?"},
    {"id": "int_14", "category": "Interior Comfort, Seats & Materials", "question": "What is the \"Boss Key\" on the front passenger seat of the GAC GS8, and what is its purpose?"},
    {"id": "int_15", "category": "Interior Comfort, Seats & Materials", "question": "Is the front passenger seat height-adjustable in the GAC EMPOW?"},
    {"id": "int_16", "category": "Interior Comfort, Seats & Materials", "question": "Are the front-row seats ventilated in the GAC EMPOW GL?"},
    {"id": "int_17", "category": "Interior Comfort, Seats & Materials", "question": "Does the GAC GS8 offer heated and ventilated front-row seats?"},
    {"id": "int_18", "category": "Interior Comfort, Seats & Materials", "question": "What massage function is available on GAC seats, and which models feature it?"},
    {"id": "int_19", "category": "Interior Comfort, Seats & Materials", "question": "How many massage points and programs are built into the second-row seats of the GAC M8?"},
    {"id": "int_20", "category": "Interior Comfort, Seats & Materials", "question": "Do GAC vehicles feature ventilated glove boxes or center armrest boxes?"},
    {"id": "int_21", "category": "Interior Comfort, Seats & Materials", "question": "Describe the \"First-Class\" captain chairs in the second row of the GAC M8."},
    {"id": "int_22", "category": "Interior Comfort, Seats & Materials", "question": "What is the sliding range (in mm) of the second-row seats in the GAC M8?"},
    {"id": "int_23", "category": "Interior Comfort, Seats & Materials", "question": "Do the second-row seats in the GAC M8 feature power leg rests?"},
    {"id": "int_24", "category": "Interior Comfort, Seats & Materials", "question": "What is the \"Easy Entry\" function for the second-row seats in the GAC GS8?"},
    {"id": "int_25", "category": "Interior Comfort, Seats & Materials", "question": "Are the second-row seats in the GAC GS8 power-foldable?"},
    {"id": "int_26", "category": "Interior Comfort, Seats & Materials", "question": "Can the third-row seats in the GAC GS8 fold completely flat to extend the trunk floor?"},
    {"id": "int_27", "category": "Interior Comfort, Seats & Materials", "question": "How do you split-fold the second-row seats in the GS3 EMZOOM (e.g., 60:40)?"},
    {"id": "int_28", "category": "Interior Comfort, Seats & Materials", "question": "Does the second row of the GS3 EMZOOM feature a center armrest with cup holders?"},
    {"id": "int_29", "category": "Interior Comfort, Seats & Materials", "question": "What is the step-in height of the first pedal for easy entry/exit in the GAC M8?"},
    {"id": "int_30", "category": "Interior Comfort, Seats & Materials", "question": "How long is the second-row entry grab handle in the GAC M8?"},

    # --- AC, Climate Control & Cabin Comfort ---
    {"id": "ac_1", "category": "AC, Climate Control & Cabin Comfort", "question": "Is the air conditioning system in the GAC EMPOW manual or automatic?"},
    {"id": "ac_2", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC EMPOW feature dual-zone automatic climate control?"},
    {"id": "ac_3", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC GS8 feature a tri-zone automatic climate control system?"},
    {"id": "ac_4", "category": "AC, Climate Control & Cabin Comfort", "question": "Can rear-seat passengers control their own AC temperature and fan speed in the GAC GS8?"},
    {"id": "ac_5", "category": "AC, Climate Control & Cabin Comfort", "question": "How is the AC controlled in the GAC M8 for all three rows?"},
    {"id": "ac_6", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC EMPOW feature rear air conditioning vents?"},
    {"id": "ac_7", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC GS3 EMZOOM come equipped with rear AC ducts?"},
    {"id": "ac_8", "category": "AC, Climate Control & Cabin Comfort", "question": "Where are the rear AC vents positioned in the GAC M8 (roof-mounted or console-mounted)?"},
    {"id": "ac_9", "category": "AC, Climate Control & Cabin Comfort", "question": "What are the \"Rolling Vent\" AC outlets in the GAC EMKOO?"},
    {"id": "ac_10", "category": "AC, Climate Control & Cabin Comfort", "question": "What is the \"Air Quality System (AQS)\" in GAC vehicles?"},
    {"id": "ac_11", "category": "AC, Climate Control & Cabin Comfort", "question": "Does GAC use PM2.5 air filters in their air conditioning systems?"},
    {"id": "ac_12", "category": "AC, Climate Control & Cabin Comfort", "question": "Is there an active cabin fragrance system available in high-spec GAC models?"},
    {"id": "ac_13", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC EMPOW GL feature customizable ambient cabin lighting?"},
    {"id": "ac_14", "category": "AC, Climate Control & Cabin Comfort", "question": "How many colors are available in the GAC GS8's intelligent ambient lighting system?"},
    {"id": "ac_15", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the ambient lighting sync with the music rhythm in GAC cars?"},
    {"id": "ac_16", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC GS3 EMZOOM feature ambient lighting?"},
    {"id": "ac_17", "category": "AC, Climate Control & Cabin Comfort", "question": "Are there heated and cooled cup holders in the GAC M8?"},
    {"id": "ac_18", "category": "AC, Climate Control & Cabin Comfort", "question": "Is the glove compartment in the GAC GS8 flocked inside?"},
    {"id": "ac_19", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the GAC M8 feature integrated foldable trays/tables for second-row passengers?"},
    {"id": "ac_20", "category": "AC, Climate Control & Cabin Comfort", "question": "What is the size of the vanity mirror in the sun visors, and is it illuminated?"},
    {"id": "ac_21", "category": "AC, Climate Control & Cabin Comfort", "question": "Does the driver's side feature a sunglasses holder overhead?"},
    {"id": "ac_22", "category": "AC, Climate Control & Cabin Comfort", "question": "Are there dedicated LED reading lights for second and third-row passengers?"},
    {"id": "ac_23", "category": "AC, Climate Control & Cabin Comfort", "question": "Is there a 12V power outlet inside the trunk of GAC SUVs?"},
    {"id": "ac_24", "category": "AC, Climate Control & Cabin Comfort", "question": "How many USB charging ports are distributed throughout the cabin of the GAC M8?"},
    {"id": "ac_25", "category": "AC, Climate Control & Cabin Comfort", "question": "What is the maximum power output of the wireless phone charger in the GS3 EMZOOM?"},

    # --- Infotainment, Tech & Connectivity ---
    {"id": "inf_1", "category": "Infotainment, Tech & Connectivity", "question": "What is the screen size of the central touch display in the GAC EMPOW GL?"},
    {"id": "inf_2", "category": "Infotainment, Tech & Connectivity", "question": "What is the size of the digital instrument cluster in the GAC EMPOW GL?"},
    {"id": "inf_3", "category": "Infotainment, Tech & Connectivity", "question": "What is the size of the HD LCD central touchscreen display in the GAC GS8?"},
    {"id": "inf_4", "category": "Infotainment, Tech & Connectivity", "question": "What is the size of the digital instrument cluster in the GAC GS8?"},
    {"id": "inf_5", "category": "Infotainment, Tech & Connectivity", "question": "What are the screen sizes for the central control and instrument cluster in the GAC M8?"},
    {"id": "inf_6", "category": "Infotainment, Tech & Connectivity", "question": "What processor chip (e.g., Qualcomm Snapdragon) powers the infotainment system in GAC mid-to-high trims?"},
    {"id": "inf_7", "category": "Infotainment, Tech & Connectivity", "question": "Does GAC feature a Head-Up Display (HUD), and which model offers a 30-inch AR-HUD?"},
    {"id": "inf_8", "category": "Infotainment, Tech & Connectivity", "question": "Does the GAC EMPOW support Apple CarPlay?"},
    {"id": "inf_9", "category": "Infotainment, Tech & Connectivity", "question": "Does the GAC EMPOW support Android Auto?"},
    {"id": "inf_10", "category": "Infotainment, Tech & Connectivity", "question": "How does \"Phone Mirroring\" work in the GAC GS3 EMZOOM?"},
    {"id": "inf_11", "category": "Infotainment, Tech & Connectivity", "question": "Does GAC support wireless Apple CarPlay?"},
    {"id": "inf_12", "category": "Infotainment, Tech & Connectivity", "question": "Is Bluetooth hands-free phone connectivity standard across all GAC trims?"},
    {"id": "inf_13", "category": "Infotainment, Tech & Connectivity", "question": "Is there a wireless phone charger available in the GAC EMPOW GL?"},
    {"id": "inf_14", "category": "Infotainment, Tech & Connectivity", "question": "How many speakers are fitted in the GAC EMPOW GL?"},
    {"id": "inf_15", "category": "Infotainment, Tech & Connectivity", "question": "How many speakers does the GAC GS3 EMZOOM GB trim have?"},
    {"id": "inf_16", "category": "Infotainment, Tech & Connectivity", "question": "What premium sound system brand is featured in high-end GAC GS8 trims?"},
    {"id": "inf_17", "category": "Infotainment, Tech & Connectivity", "question": "How many speakers does the Alpine Sound System have in the GAC GS8?"},
    {"id": "inf_18", "category": "Infotainment, Tech & Connectivity", "question": "Does GAC feature Speed-Based Volume Adjustment in its audio system?"},
    {"id": "inf_19", "category": "Infotainment, Tech & Connectivity", "question": "How many speakers are in the audio system of the GAC M8?"},
    {"id": "inf_20", "category": "Infotainment, Tech & Connectivity", "question": "Can you adjust the audio balance/equalizer manually through the GAC center screen?"},

    # --- Safety, Airbags & Driver Assistance (ADAS) ---
    {"id": "saf_1", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "How many airbags are equipped in the GAC EMPOW GL, and where are they located?"},
    {"id": "saf_2", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does the GAC GS8 feature driver’s knee airbags?"},
    {"id": "saf_3", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "How many airbags does the GAC GS8 offer in total?"},
    {"id": "saf_4", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "How many safety airbags does the GAC GS3 EMZOOM GB trim have?"},
    {"id": "saf_5", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "How many airbags are standard on the flagship GAC M8?"},
    {"id": "saf_6", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Are there side curtain airbags that protect all three rows in GAC 7-seater vehicles?"},
    {"id": "saf_7", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Is the Anti-Lock Braking System (ABS) with Electronic Brakeforce Distribution (EBD) standard on all GAC models?"},
    {"id": "saf_8", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is the Electronic Stability Program (ESP) standard on GAC vehicles?"},
    {"id": "saf_9", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is Hill-start Hold Control (HHC) and does GAC offer it?"},
    {"id": "saf_10", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does GAC feature Hill Descent Control (HDC) for steep off-road slopes?"},
    {"id": "saf_11", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is the role of Traction Control in GAC vehicles?"},
    {"id": "saf_12", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does the GAC EMPOW GL have a reverse parking camera?"},
    {"id": "saf_13", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What type of parking camera system does the GAC GS3 EMZOOM GL feature?"},
    {"id": "saf_14", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does the GAC GS8 feature a 360-degree HD Surround Vision Parking System?"},
    {"id": "saf_15", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does the GAC GS8 support Fusion Automatic Parking Assist (FAPA)?"},
    {"id": "saf_16", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is the \"Digital Video Recorder (DVR)\" or built-in dashcam featured in GAC SUVs?"},
    {"id": "saf_17", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Are front and rear parking sensors standard on the GAC GS8?"},
    {"id": "saf_18", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What level of autonomous driving assistance (e.g., L2) does the GAC M8 offer?"},
    {"id": "saf_19", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is Adaptive Cruise Control (ACC) and which GAC vehicles offer it?"},
    {"id": "saf_20", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does GAC offer Lane Departure Warning (LDW) and Lane Keep Assist (LKA)?"},
    {"id": "saf_21", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Explain how Forward Collision Warning (FCW) and Autonomous Emergency Braking (AEB) work on GAC models."},
    {"id": "saf_22", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is Traffic Jam Assist (TJA) and Integrated Cruise Assist (ICA) on the GAC GS8?"},
    {"id": "saf_23", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is Blind Spot Detection (BSD) and Lane Change Assist (LCA)?"},
    {"id": "saf_24", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does GAC feature Rear Cross Traffic Alert (RCTA) and Rear Collision Warning (RCW)?"},
    {"id": "saf_25", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is the Door Open Warning (DOW) safety feature?"},
    {"id": "saf_26", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does GAC feature Traffic Sign Recognition (TSR) with Intelligent Speed Limit Control?"},
    {"id": "saf_27", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is Emergency Lane Keeping Assist (ELKA)?"},
    {"id": "saf_28", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "What is the \"In-car monitoring system (IMR)\" on the GAC GS8?"},
    {"id": "saf_29", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Are ISOFIX child safety seat anchors standard in the second row of all GAC vehicles?"},
    {"id": "saf_30", "category": "Safety, Airbags & Driver Assistance (ADAS)", "question": "Does GAC feature a Tire Pressure Monitoring System (TPMS) with real-time pressure and temperature displays?"}
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
