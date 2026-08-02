st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
import streamlit as st
import math
import uuid
from datetime import datetime, timedelta
from foods import FOOD_DATABASE
# --- MOBILE DESIGN CONFIGURATION ---
st.markdown("""
    <style>
    /* 1. Hide the desktop header menu and footer padding */
    header, footer, [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    
    /* 2. Remove giant empty desktop padding on the sides */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    
    /* 3. Make all input fields and buttons bigger for human thumbs */
    div.stButton > button:first-child {
        width: 100% !important;
        height: 50px !important;
        font-size: 18px !important;
        font-weight: bold !important;
        border-radius: 12px !important;
        background-color: #FF4B4B !important; /* Changes button to a friendly active color */
        color: white !important;
    }
    
    /* 4. Make text boxes and numbers inputs easier to tap */
    input {
        font-size: 16px !important; /* Prevents iOS/Android from forcing an awkward zoom */
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Metabolic Digestion Calculator",
    page_icon="🍴",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- CLEAN MINIMALISM CUSTOM CSS FOR MOBILE-OPTIMIZED LAYOUT ---
st.markdown("""
<style>
/* Global Clean Minimalism Theme */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #FEF7FF;
    color: #1D1B20;
}

/* Mobile-friendly container spacing */
.block-container {
    padding-top: 1.5rem;
    padding-bottom: 5rem;
    padding-left: 1rem;
    padding-right: 1rem;
    max-width: 640px;
}

/* Distinct Visual Card Containers */
div[data-testid="stVerticalBlock"] > div[style*="border"], 
.metabolic-card {
    background: #FFFFFF;
    border: 1px solid rgba(202, 196, 208, 0.4);
    border-radius: 24px;
    padding: 1.25rem;
    box-shadow: 0 4px 16px rgba(103, 80, 164, 0.05);
    margin-bottom: 1rem;
}

/* Header Styling */
.metabolic-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 0.5rem;
    margin-bottom: 1rem;
}
.header-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #1D1B20;
    letter-spacing: -0.02em;
    margin: 0;
}
.header-subtitle {
    font-size: 0.8rem;
    color: #49454F;
    margin: 0;
}

/* Thumb-friendly Full-Width Buttons */
div.stButton > button {
    width: 100% !important;
    min-height: 54px !important;
    border-radius: 16px !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    padding: 0.75rem 1.25rem !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    border: none !important;
    box-shadow: 0 2px 8px rgba(103, 80, 164, 0.15) !important;
    transition: all 0.15s ease !important;
}

/* Primary purple button accent */
div.stButton > button[kind="primary"] {
    background-color: #6750A4 !important;
    color: #FFFFFF !important;
}
div.stButton > button[kind="primary"]:hover {
    background-color: #584193 !important;
}

/* Secondary outline button style */
div.stButton > button[kind="secondary"] {
    background-color: #F3EDF7 !important;
    color: #6750A4 !important;
    border: 1px solid rgba(103, 80, 164, 0.3) !important;
}

/* Danger button for clear batch */
.danger-btn > div.stButton > button {
    background-color: #E53935 !important;
    color: #FFFFFF !important;
}

/* Badge tags */
.metabolic-badge {
    background-color: #E8DEF8;
    color: #21005D;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    display: inline-block;
}

/* Card title & subtitle layout */
.card-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
}
.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1D1B20;
    margin: 0;
}
.card-subtitle {
    font-size: 0.8rem;
    color: #49454F;
    margin: 0;
}

/* Hero Biological Clearance Time Box */
.clearance-hero {
    background: linear-gradient(135deg, #E8DEF8 0%, #F3EDF7 100%);
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.clearance-time {
    font-size: 2.8rem;
    font-weight: 800;
    color: #21005D;
    margin: 0.25rem 0;
}

/* Warning alert box (Combined Enemy) */
.alert-enemy {
    background-color: #F2B8B5;
    color: #601410;
    border: 1px solid #B3261E;
    border-radius: 16px;
    padding: 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.75rem 0;
}
/* Success alert box */
.alert-success {
    background-color: #D7F5E4;
    color: #0F5132;
    border: 1px solid #198754;
    border-radius: 16px;
    padding: 1rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 0.75rem 0;
}

/* Ensure inputs stack vertically on mobile */
@media (max-width: 768px) {
    div[data-testid="column"] {
        width: 100% !important;
        flex: 1 1 100% !important;
    }
    .stTextInput, .stNumberInput, .stSelectbox, .stSlider {
        width: 100% !important;
    }
}

/* Sticky Watermark Bottom Right */
.sticky-watermark {
    position: fixed;
    bottom: 16px;
    right: 16px;
    background-color: rgba(255, 255, 255, 0.94);
    border: 1px solid rgba(202, 196, 208, 0.6);
    border-radius: 10px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 600;
    color: #1D1B20;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    z-index: 9999;
    backdrop-filter: blur(4px);
}
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if "logged_meal" not in st.session_state:
    st.session_state["logged_meal"] = []
if "custom_foods" not in st.session_state:
    st.session_state["custom_foods"] = {}
if "servings" not in st.session_state:
    st.session_state["servings"] = 1
if "meal_hour" not in st.session_state:
    st.session_state["meal_hour"] = 18
if "meal_minute" not in st.session_state:
    st.session_state["meal_minute"] = 0
if "bmi_weight" not in st.session_state:
    st.session_state["bmi_weight"] = 74.0
if "bmi_height" not in st.session_state:
    st.session_state["bmi_height"] = 176.0

# Merge built-in food database with any user-injected supermarket packets
combined_db = {**FOOD_DATABASE, **st.session_state["custom_foods"]}

# --- HELPER FUNCTIONS ---
def get_portion_rule(food_name):
    """Smart portion decoder returning unit label and default weight in grams."""
    lower = food_name.lower()
    if any(w in lower for w in ["slice", "crumpet", "bun", "croissant", "wrap", "muffin"]):
        w = 40 if "sourdough" in lower else 35
        return ("slices/pieces", w)
    elif "egg" in lower:
        return ("eggs", 50)
    elif "sausage" in lower:
        return ("sausages", 60)
    elif any(w in lower for w in ["tbsp", "tallow", "oil", "butter", "honey", "syrup"]):
        return ("tablespoons", 15)
    elif any(w in lower for w in ["black pudding", "haggis"]):
        return ("standard slices", 50)
    elif any(w in lower for w in ["steak", "breast", "thigh", "fillet", "chop", "kippers"]):
        return ("whole cuts/pieces", 150)
    elif any(w in lower for w in ["potato", "tomato", "mushroom", "onion"]):
        return ("whole items", 80)
    elif any(w in lower for w in ["milk", "broth", "stock", "water"]):
        return ("cups/mugs", 250)
    elif any(w in lower for w in ["beans", "oats", "rice", "pasta", "lentils", "chickpeas"]):
        return ("hearty handfuls / scoops", 75)
    else:
        return ("servings", 100)

def determine_packet_properties(name):
    lower = name.lower()
    wheat_val = 1 if any(x in lower for x in ["bread", "flour", "sourdough", "pasta", "spaghetti", "orzo", "crumpet", "biscuit", "cracker", "pastry", "rye", "barley"]) else 0
    if any(x in lower for x in ["broth", "stock", "coffee", "tea", "water", "juice", "milk"]):
        base_mins = 45 if "coconut milk" in lower else 15
    elif any(x in lower for x in ["yogurt", "yoghourt", "mousse", "fraiche", "creme", "cheese"]):
        base_mins = 120 if any(y in lower for y in ["cheddar", "colby", "parmesan", "feta", "halloumi", "goats", "blue"]) else 45
    elif any(x in lower for x in ["cracker", "biscuit", "oatcake", "nib"]):
        base_mins = 60
    elif any(x in lower for x in ["bread", "flour", "sourdough", "pasta", "spaghetti", "orzo", "rice", "oats", "porridge", "rye", "barley"]):
        base_mins = 90
    else:
        base_mins = 120
    return base_mins, wheat_val

# --- TOP MOBILE HEADER ---
st.markdown("""
<div class="metabolic-header">
    <div>
        <h1 class="header-title">🍴 Metabolic Calc</h1>
        <p class="header-subtitle">Biological structure & stomach clearance speeds</p>
    </div>
    <div style="width: 40px; height: 40px; border-radius: 50%; background: #E8DEF8; display: flex; align-items: center; justify-content: center; font-size: 18px;">
        👤
    </div>
</div>
""", unsafe_allow_html=True)

# --- CARD 1: INGREDIENT REGISTRATION CARD ---
with st.container():
    st.markdown("""
    <div class="card-header-row">
        <div>
            <h2 class="card-title">Log Batch Ingredients</h2>
            <p class="card-subtitle">Search and scale portions for your recipe</p>
        </div>
        <span class="metabolic-badge">Batch Registry</span>
    </div>
    """, unsafe_allow_html=True)
    
    food_names = sorted(list(combined_db.keys()))
    selected_food = st.selectbox(
        "Select Ingredient:",
        options=food_names,
        key="food_select",
        help="Type to search e.g. Sourdough, Eggs, Butter..."
    )
    
    unit_label, default_weight = get_portion_rule(selected_food)
    
    st.markdown(f"**Smart Portion Decoder:** Default `{default_weight}g` per `{unit_label}`")
    
    item_count = st.slider(
        f"How many {unit_label} added to batch?",
        min_value=1,
        max_value=12,
        value=2,
        step=1,
        key="portion_slider"
    )
    
    total_grams = item_count * default_weight
    st.caption(f"Calculated Total Batch Weight: **{total_grams}g**")
    
    if st.button("➕ Add to Recipe Batch", key="add_to_batch", type="primary"):
        fat_100g, prot_100g, base_mins, is_wheat = combined_db[selected_food]
        total_fat = (fat_100g / 100.0) * total_grams
        total_prot = (prot_100g / 100.0) * total_grams
        clean_name = selected_food.split(" - ")[-1] if " - " in selected_food else selected_food
        
        st.session_state["logged_meal"].append({
            "id": str(uuid.uuid4())[:8],
            "display": f"{item_count} {unit_label} of {clean_name}",
            "base_name": selected_food,
            "weight_g": total_grams,
            "fat_g": total_fat,
            "prot_g": total_prot,
            "base_mins": base_mins,
            "is_wheat": is_wheat
        })
        st.success(f"Added {item_count} {unit_label} of {clean_name} to batch!")
        st.rerun()

# --- CARD 2: CURRENT RECIPE BATCH REGISTRY ---
with st.container():
    st.markdown("""
    <div class="card-header-row">
        <div>
            <h2 class="card-title">Current Recipe Batch</h2>
            <p class="card-subtitle">Total fats, proteins & wheat structure</p>
        </div>
        <span class="metabolic-badge">{} Items</span>
    </div>
    """.format(len(st.session_state["logged_meal"])), unsafe_allow_html=True)
    
    if not st.session_state["logged_meal"]:
        st.info("Your recipe batch is empty. Log ingredients above to calculate digestion.")
    else:
        for idx, item in enumerate(st.session_state["logged_meal"]):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**• {item['display']}**")
                st.caption(f"{int(item['weight_g'])}g | Fat: **{int(item['fat_g'])}g** | Protein: **{int(item['prot_g'])}g**")
            with col2:
                if st.button("🗑️", key=f"del_{item['id']}", help="Remove item"):
                    st.session_state["logged_meal"].pop(idx)
                    st.rerun()
        
        batch_fat = sum(item["fat_g"] for item in st.session_state["logged_meal"])
        batch_prot = sum(item["prot_g"] for item in st.session_state["logged_meal"])
        wheat_present = any(item["is_wheat"] for item in st.session_state["logged_meal"])
        
        st.markdown("---")
        st.markdown(f"**Batch Total:** Fat `{batch_fat:.1f}g` | Protein `{batch_prot:.1f}g` | Wheat: `{'PRESENT ⚠️' if wheat_present else 'FREE ✅'}`")
        
        st.markdown('<div class="danger-btn">', unsafe_allow_html=True)
        if st.button("🗑️ Clear Entire Batch", key="clear_batch", type="secondary"):
            st.session_state["logged_meal"] = []
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# --- CARD 3: SERVINGS & TIMING ---
with st.container():
    st.markdown("""
    <div class="card-header-row">
        <div>
            <h2 class="card-title">Servings & Timing</h2>
            <p class="card-subtitle">Portions per batch and consumption time</p>
        </div>
        <span class="metabolic-badge">Portions</span>
    </div>
    """, unsafe_allow_html=True)
    
    servings = st.number_input(
        "How many portions does this batch make?",
        min_value=1,
        max_value=20,
        value=st.session_state["servings"],
        step=1,
        key="servings_input"
    )
    st.session_state["servings"] = servings
    
    col_hr, col_min = st.columns(2)
    with col_hr:
        meal_hour = st.selectbox(
            "Eating Hour (24h clock):",
            options=list(range(0, 24)),
            index=st.session_state["meal_hour"],
            key="meal_hr_select"
        )
        st.session_state["meal_hour"] = meal_hour
    with col_min:
        meal_min = st.selectbox(
            "Minute:",
            options=[0, 15, 30, 45],
            index=[0, 15, 30, 45].index(st.session_state["meal_minute"]) if st.session_state["meal_minute"] in [0, 15, 30, 45] else 0,
            key="meal_min_select"
        )
        st.session_state["meal_minute"] = meal_min

    # Expanders for Supermarket Packet Injector & Biological Grain Rules
    with st.expander("🛒 Supermarket Packet Injector (Add Custom Food)"):
        st.markdown("Add custom products from Tesco, Morrisons, or Aldi:")
        custom_name = st.text_input("Product Name & Brand", placeholder="e.g. Tesco Black Pudding Slices")
        c_fat = st.number_input("Fat per 100g (g)", min_value=0.0, max_value=100.0, value=15.0, step=0.5)
        c_prot = st.number_input("Protein per 100g (g)", min_value=0.0, max_value=100.0, value=12.0, step=0.5)
        if st.button("💾 Save Custom Product", key="save_packet"):
            if custom_name.strip():
                base_mins, is_w = determine_packet_properties(custom_name)
                st.session_state["custom_foods"][custom_name.strip()] = (c_fat, c_prot, base_mins, is_w)
                st.success(f"Saved '{custom_name}'! It is now selectable in the dropdown.")
                st.rerun()
            else:
                st.error("Please enter a product name.")

    with st.expander("ℹ️ The Biological Grain Rules (Stomach Clearance)"):
        st.markdown("""
        **💧 Water-Soluble Bases (Oats, Rice, Potatoes)**
        - Pure oats contain avenin, dissolving cleanly into water-based stomach juices without trapping fats.
        - Gastric acid and bile break down surrounding fats at normal biological speeds.

        **🍞 Elastic Gluten Sponges (Wheat Bread, Toast, Pasta, Barley)**
        - True gluten (gliadin/secalin) forms an elastic sponge structure.
        - If cooking fats are present, they soak into the grain sponge, cloaking food from stomach acid and triggering a **+30% digestion time penalty**.
        """)

# --- CARD 4: BMI & PERSONAL PLATE ANALYSIS ---
with st.container():
    st.markdown("""
    <div class="card-header-row">
        <div>
            <h2 class="card-title">Personal Plate Analysis</h2>
            <p class="card-subtitle">1 of {} servings calculated + BMI correlation</p>
        </div>
        <span class="metabolic-badge">Personal Stats</span>
    </div>
    """.format(servings), unsafe_allow_html=True)
    
    batch_fat = sum(item["fat_g"] for item in st.session_state["logged_meal"])
    batch_prot = sum(item["prot_g"] for item in st.session_state["logged_meal"])
    personal_fat = batch_fat / max(1, servings)
    personal_prot = batch_prot / max(1, servings)
    
    col_f, col_p = st.columns(2)
    with col_f:
        st.metric("FAT ON PLATE", f"{personal_fat:.1f}g")
    with col_p:
        st.metric("PROTEIN ON PLATE", f"{personal_prot:.1f}g")
    
    st.markdown("---")
    st.markdown("#### **Metabolic BMI Index**")
    
    bmi_w = st.slider("Weight (kg)", 40.0, 150.0, st.session_state["bmi_weight"], 0.5, key="bmi_weight_slider")
    bmi_h = st.slider("Height (cm)", 140.0, 210.0, st.session_state["bmi_height"], 0.5, key="bmi_height_slider")
    st.session_state["bmi_weight"] = bmi_w
    st.session_state["bmi_height"] = bmi_h
    
    height_m = max(0.5, bmi_h / 100.0)
    bmi_val = bmi_w / (height_m * height_m)
    
    if bmi_val < 18.5:
        bmi_cat = "Underweight"
        bmi_tip = "Low glycogen reserve: ensure sufficient water-soluble oats or potatoes for steady energy."
    elif bmi_val < 25.0:
        bmi_cat = "Normal weight"
        bmi_tip = "Optimal biological clearance zone: standard gastric emptying speeds apply."
    elif bmi_val < 30.0:
        bmi_cat = "Overweight"
        bmi_tip = "Moderately elevated lipid transit: avoid combining heavy cooking fats with wheat gluten sponges."
    else:
        bmi_cat = "Obesity Zone"
        bmi_tip = "High gastric retention risk: prioritize water-soluble bases and keep individual fat servings below 15g."
        
    st.markdown(f"**BMI Score:** `{bmi_val:.1f}` ({bmi_cat})")
    st.caption(f"💡 {bmi_tip}")

# --- CARD 5: BIOLOGICAL TIMELINE & CLEARANCE RESULTS ---
with st.container():
    st.markdown("""
    <div class="card-header-row">
        <div>
            <h2 class="card-title">Your Biological Timeline</h2>
            <p class="card-subtitle">Stomach clearance forecast & structural checks</p>
        </div>
        <span class="metabolic-badge">Clearance Forecast</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state["logged_meal"]:
        auto_baseline = 15
    else:
        auto_baseline = max(item["base_mins"] for item in st.session_state["logged_meal"])
        
    fat_penalty = int((personal_fat / 5.0) * 15.0)
    prot_penalty = int((personal_prot / 10.0) * 15.0)
    subtotal_mins = auto_baseline + fat_penalty + prot_penalty
    
    wheat_present = any(item["is_wheat"] for item in st.session_state["logged_meal"])
    combined_enemy = wheat_present and personal_fat >= 10.0 and auto_baseline >= 60
    
    total_mins = int(subtotal_mins * 1.3) if combined_enemy else subtotal_mins
    dig_hours = total_mins // 60
    dig_rem_mins = total_mins % 60
    
    # Calculate finish clock time
    start_time = datetime.now().replace(hour=meal_hour, minute=meal_min, second=0, microsecond=0)
    clear_time = start_time + timedelta(minutes=total_mins)
    clear_time_str = clear_time.strftime("%I:%M %p").lstrip("0")
    
    st.markdown(f"""
    <div class="clearance-hero">
        <div style="font-size: 0.8rem; font-weight: 700; color: #6750A4; text-transform: uppercase; letter-spacing: 0.08em;">Individual Portion Breakdown Time</div>
        <div class="clearance-time">{dig_hours}h {dig_rem_mins}m</div>
        <div style="font-size: 0.85rem; color: #49454F;">{total_mins} total biological digestion minutes</div>
    </div>
    """, unsafe_allow_html=True)
    
    if combined_enemy:
        st.markdown("""
        <div class="alert-enemy">
            ⚠️ <strong>COMBINED ENEMY TRIGGERED</strong><br>
            Calculated plate fat has saturated porous wheat layers. (+30% digestion penalty applied)
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state["logged_meal"]:
        st.markdown("""
        <div class="alert-success">
            ✅ <strong>Clean Structural Layering</strong><br>
            Food elements clear efficiently without stomach clogs.
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown(f"#### **Clearance Clock Time**")
    st.markdown(f"If consumed at **{start_time.strftime('%I:%M %p').lstrip('0')}**, your stomach clears completely by:")
    st.markdown(f"### 👉 **{clear_time_str}**")
    
    target_time = start_time.replace(hour=22, minute=0)
    if clear_time <= target_time and clear_time.day == start_time.day:
        st.success("🔥 METABOLIC SUCCESS: Window stays wide open before 10:00 PM!")
    else:
        st.error("❌ NOTICE: Digestion runs past 10:00 PM tonight.")

# --- STICKY WATERMARK BOTTOM RIGHT ---
st.markdown("""
<div class="sticky-watermark">
    👤 Matthew Parnell
</div>
""", unsafe_allow_html=True)
