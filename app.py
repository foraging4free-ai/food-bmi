# app.py
import streamlit as st
import streamlit as st

# --- WATERMARK CONFIGURATION ---
# This injects custom CSS to stick your name to the bottom-right of the Firefox window
st.markdown(
    """
    <style>
    .sticky-watermark {
        position: fixed;
        bottom: 15px;
        right: 15px;
        background-color: rgba(255, 255, 255, 0.75); /* Soft white background */
        color: #111111;                             /* Dark text for contrast */
        padding: 6px 12px;
        font-family: 'Source Sans Pro', sans-serif;
        font-size: 13px;
        font-weight: 600;
        border-radius: 6px;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.1);
        z-index: 999999;                            /* Keeps it on top of other elements */
        pointer-events: none;                       /* Allows clicks to pass through it */
    }
    
    /* Dark mode adaptation */
    @media (prefers-color-scheme: dark) {
        .sticky-watermark {
            background-color: rgba(38, 39, 48, 0.85);
            color: #ffffff;
            box-shadow: 0px 2px 5px rgba(0,0,0,0.3);
        }
    }
    </style>
    <div class="sticky-watermark">
        👤 Matthew Parnell
    </div>
    """,
    unsafe_allow_html=True
)

import datetime
from foods import FOOD_DATABASE

# --- MAIN PAGE ENGINE LAYER ---
st.set_page_config(page_title="Metabolic Digestion Calculator", page_icon="🍽️", layout="centered")
st.title("🍽️ Fully Automated Metabolic Calculator")
st.markdown("---")
st.subheader("Your plate automatically decodes its own biological structure and layout speeds.")

if "current_meal" not in st.session_state:
    st.session_state.current_meal = []

# --- INGREDIENT REGISTRATION SECTION ---
st.markdown("### 🛒 Log Batch Ingredients")

# Search and filter options
search_query = st.text_input("Search food item:", placeholder="Search ingredients...")

if not search_query.strip():
    filtered_options = list(FOOD_DATABASE.keys())
else:
    filtered_options = [food for food in FOOD_DATABASE.keys() if search_query.lower() in food.lower()]

if filtered_options:
    selected_food = st.selectbox("Select exact matched ingredient:", filtered_options)
    
    # === SMART PORTION DECODER ===
    sel_lower = selected_food.lower()
    
    if "slice" in sel_lower or "crumpet" in sel_lower or "bun" in sel_lower or "croissant" in sel_lower or "wrap" in sel_lower or "muffin" in sel_lower:
        unit_type = "slices/pieces"
        default_weight = 40 if "sourdough" in sel_lower else 35  
    elif "egg" in sel_lower:
        unit_type = "eggs"
        default_weight = 50
    elif "sausage" in sel_lower:
        unit_type = "sausages"
        default_weight = 60
    elif "tbsp" in sel_lower or "tallow" in sel_lower or "oil" in sel_lower or "butter" in sel_lower or "honey" in sel_lower or "syrup" in sel_lower:
        unit_type = "tablespoons"
        default_weight = 15
    elif "black pudding" in sel_lower or "haggis" in sel_lower:
        unit_type = "standard slices"
        default_weight = 50
    elif "steak" in sel_lower or "breast" in sel_lower or "thigh" in sel_lower or "fillet" in sel_lower or "chop" in sel_lower or "kippers" in sel_lower:
        unit_type = "whole cuts/pieces"
        default_weight = 150
    elif "potato" in sel_lower or "tomato" in sel_lower or "mushroom" in sel_lower or "onion" in sel_lower:
        unit_type = "whole items"
        default_weight = 80
    elif "milk" in sel_lower or "broth" in sel_lower or "stock" in sel_lower or "water" in sel_lower:
        unit_type = "cups/mugs"
        default_weight = 250
    elif "beans" in sel_lower or "oats" in sel_lower or "rice" in sel_lower or "pasta" in sel_lower or "lentils" in sel_lower or "chickpeas" in sel_lower:
        unit_type = "hearty handfuls / scoops"
        default_weight = 75
    else:
        unit_type = "servings"
        default_weight = 100

    item_count = st.slider(f"How many {unit_type} did you add to the whole recipe batch?", 1, 12, 2)
    batch_weight = item_count * default_weight

    if st.button("➕ Add to Recipe Batch", use_container_width=True):
        f, p, base_m, w = FOOD_DATABASE[selected_food]
        total_item_fat = (f / 100) * batch_weight
        total_item_protein = (p / 100) * batch_weight
        
        display_name = f"{item_count} {unit_type} of {selected_food.split(' - ')[-1]}"
        
        st.session_state.current_meal.append({
            "name": display_name,
            "weight": batch_weight,
            "fat": total_item_fat,
            "protein": total_item_protein,
            "baseline": base_m,
            "is_wheat": w
        })
        st.toast("Logged into your cooking batch!")
else:
    st.error("❌ No matching items found.")

st.markdown("---")

# --- BATCH VIEWPORT LAYER ---
st.markdown("### 🥣 Current Recipe Batch Components")

batch_fat, batch_protein, is_wheat_present = 0.0, 0.0, False
auto_baseline = 15 

if not st.session_state.current_meal:
    st.info("Your recipe batch is empty. Log items above to map totals.")
else:
    for item in st.session_state.current_meal:
        st.write(f"• **{item['name']}**")
        batch_fat += item['fat']
        batch_protein += item['protein']
        if item['is_wheat'] == 1: 
            is_wheat_present = True
        auto_baseline = max(auto_baseline, item['baseline'])
            
    if st.button("🗑️ Clear Batch", type="primary"):
        st.session_state.current_meal = []
        st.rerun()

st.markdown("---")

# --- PORTION CONTROL & TIMING SIDEBAR ---
st.sidebar.header("📋 Servings & Timing")

servings = st.sidebar.number_input("How many portions or plates does this batch make?", min_value=1, max_value=20, value=1, step=1)
meal_time = st.sidebar.time_input("What time are you eating your plate?", datetime.time(18, 0))

# --- AUTOMATED PACKET INJECTOR ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏬 Supermarket Packet Injector")
st.sidebar.caption("Save custom items from Tesco or Morrisons packets. Base style is auto-decoded.")

with st.sidebar.form("packet_form", clear_on_submit=True):
    new_name = st.text_input("Product Name & Brand:", placeholder="e.g., Tesco Black Pudding Slices")
    new_fat = st.number_input("Fat per 100g:", min_value=0.0, max_value=100.0, step=0.1)
    new_protein = st.number_input("Protein per 100g:", min_value=0.0, max_value=100.0, step=0.1)
    
    submit_packet = st.form_submit_button("💾 Save Product Permanently")
    
    if submit_packet and new_name:
        name_lower = new_name.lower()
        wheat_val = 1 if any(w in name_lower for w in ["bread", "flour", "sourdough", "pasta", "spaghetti", "orzo", "crumpet", "biscuit", "cracker", "pastry", "rye", "barley"]) else 0
        
        if any(w in name_lower for w in ["broth", "stock", "coffee", "tea", "water", "juice", "milk"]):
            base_mins_val = 45 if "coconut milk" in name_lower else 15
        elif any(w in name_lower for w in ["yogurt", "yoghourt", "mousse", "fraiche", "creme", "cheese"]):
            base_mins_val = 120 if any(w in name_lower for w in ["cheddar", "colby", "parmesan", "feta", "halloumi", "goats", "blue"]) else 45
        elif any(w in name_lower for w in ["cracker", "biscuit", "oatcake", "nib"]):
            base_mins_val = 60
        elif any(w in name_lower for w in ["bread", "flour", "sourdough", "pasta", "spaghetti", "orzo", "rice", "oats", "porridge", "rye", "barley"]):
            base_mins_val = 90
        else:
            base_mins_val = 120
            
        try:
            with open("foods.py", "r", encoding="utf-8") as f_file:
                lines = f_file.readlines()
            for idx, line in reversed(list(enumerate(lines))):
                if "}" in line:
                    lines.insert(idx, f'    "{new_name}": ({new_fat}, {new_protein}, {base_mins_val}, {wheat_val}),\n')
                    break
            with open("foods.py", "w", encoding="utf-8") as f_file:
                f_file.writelines(lines)
            st.sidebar.success(f"Saved custom packet!")
        except:
            st.sidebar.error("Error saving file.")

# --- THE CORRECTED BIOLOGICAL GRAIN GUIDE ---
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧬 The Biological Grain Rules")
st.sidebar.markdown("""
**💧 Water-Soluble Bases:**
* *Examples:* Oats, Rice, Potatoes.
* *How it works:* Pure oats contain *avenin*, which dissolves cleanly into water-based stomach juices instead of building a trap. Acid and bile can break down surrounding fats instantly at normal speeds.

**🍞 Elastic Gluten Sponges:**
* *Examples:* Wheat Bread, Toast, Pasta, Barley, Rye Crackers, Wheaty Black Puddings.
* *How it works:* True gluten (*gliadin/secalin*) forms an elastic, microscopic sponge. If cooking fats are present, they soak *into* the grain sponge, cloaking the food from stomach acid and forcing a heavy **30% time penalty**.
""")

# --- BIOLOGICAL CALCULATOR LOGIC ---
personal_fat = batch_fat / servings
personal_protein = batch_protein / servings

fat_penalty = int((personal_fat / 5) * 15)
protein_penalty = int((personal_protein / 10) * 15)
subtotal = auto_baseline + fat_penalty + protein_penalty

combined_enemy_triggered = False
if is_wheat_present and personal_fat >= 10 and auto_baseline >= 60:
    total_minutes = int(subtotal * 1.3)
    combined_enemy_triggered = True
else:
    total_minutes = subtotal

hours = total_minutes // 60
minutes = total_minutes % 60
meal_datetime = datetime.datetime.combine(datetime.date.today(), meal_time)
clear_datetime = meal_datetime + datetime.timedelta(minutes=total_minutes)
clear_time_str = clear_datetime.strftime("%I:%M %p")
target_time = datetime.time(22, 0)

# --- VISUAL DATA RENDER LAYER ---
if st.session_state.current_meal:
    st.markdown("### 📊 Personal Plate Analysis")
    st.write(f"Your individual serving stats (1 of {servings} portions calculated):")
    st.info(f"🧬 **Fat on Your Plate:** {personal_fat:.1f}g  |  🧬 **Protein on Your Plate:** {personal_protein:.1f}g")

st.metric(label="⏱️ INDIVIDUAL PORTION BREAKDOWN TIME", value=f"{hours}h {minutes}m", delta=f"{total_minutes} total mins", delta_color="inverse")

if combined_enemy_triggered: 
    st.error("⚠️ COMBINED ENEMY TRIGGERED: The calculated plate fat has saturated your porous wheat layers.")
elif st.session_state.current_meal: 
    st.success("✅ Clean Structural Layering: Food elements clear efficiently without stomach clogs.")

st.markdown("### ⏰ Your Biological Timeline")
st.write(f"If consumed at **{meal_time.strftime('%I:%M %p')}**, your stomach clears completely by:")
st.markdown(f"## 👉 **{clear_time_str}**")

if clear_datetime.time() <= target_time and clear_datetime.date() == datetime.date.today():
    st.success("🔥 METABOLIC SUCCESS: Window stays wide open!")
else:
    st.warning("❌ NOTICE: Digestion runs past 10:00 PM tonight.")

st.markdown("<br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
