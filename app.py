import streamlit as st
from PIL import Image
import numpy as np
import cv2
from ultralytics import YOLO
import time
import base64


def apply_background():
    st.markdown(
        """
        <style>
            body, .stApp {
                background-color: white !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def load_model():
    model = YOLO(r"C:\Users\Prathyusha\Desktop\mini\detect\train\weights\best.pt")   # Load YOLO model
    return model

def detect_objects(model, image):
    results = model(image)
    return results

def draw_boxes(image, results):
    image = np.array(image)
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            label = result.names[int(box.cls[0])]
            conf = box.conf[0].item()

            # Bounding Box
            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 6)  

            # Text with Background for Clarity
            text = f"{label}: {conf:.2f}"
            (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)
            
            # Draw filled rectangle for text background
            cv2.rectangle(image, (x1, y1 - h - 10), (x1 + w, y1), (0, 255, 0), -1)  
            
            # Put text over the rectangle
            cv2.putText(image, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3)

    return Image.fromarray(image)
def get_disposal_methods():
    return {
         "Aerosol": (
            "🛢️ <b>Hazardous Waste - Follow these steps:</b><br>"
            "1. Ensure the can is completely empty.\n"
            "2. Do NOT puncture, crush, or burn it.\n"
            "3. Drop it off at a hazardous waste collection point.\n"
            "4. Follow local disposal instructions."
        ),
        "Aluminium blister pack": (
            "♻️ **Mixed Material - Follow these steps:**\n"
            "1. Attempt to separate the aluminum from the plastic.\n"
            "2. Recycle aluminum part with metals.\n"
            "3. Dispose plastic in general waste if not recyclable.\n"
            "4. Return to pharmacy if a take-back program is available."
        ),
        "Aluminium foil": (
            "♻️ **Recyclable if clean - Follow these steps:**\n"
            "1. Rinse off food residue.\n"
            "2. Crumple into a ball to prevent loss in recycling.\n"
            "3. Place in metal recycling bin.\n"
            "4. If greasy, discard in general waste."
        ),
        "Battery": (
            "⚡ **E-Waste - Follow these steps:**\n"
            "1. Store safely in a non-metal container.\n"
            "2. Tape terminals of lithium or damaged batteries.\n"
            "3. Drop off at battery recycling locations.\n"
            "4. Never dispose in general waste or regular recycling."
        ),
        "Broken glass": (
            "🚨 **Sharp Waste - Follow these steps:**\n"
            "1. Wrap in thick newspaper or cardboard.\n"
            "2. Seal and label as 'Broken Glass'.\n"
            "3. Place in general waste bin.\n"
            "4. Do not place in recycling as it’s unsafe."
        ),
        "Carded blister pack": (
            "♻️ **Mixed Materials - Follow these steps:**\n"
            "1. Try to separate plastic from cardboard.\n"
            "2. Recycle cardboard if clean.\n"
            "3. Dispose plastic in general waste unless marked recyclable.\n"
            "4. Return to pharmacy if applicable."
        ),
        "Cigarette": (
            "🚬 **Non-Recyclable - Follow these steps:**\n"
            "1. Fully extinguish before disposal.\n"
            "2. Use designated ashtrays or sand bins.\n"
            "3. Never throw on the ground or in drains.\n"
            "4. Dispose of filters in general waste."
        ),
        "Clear plastic bottle": (
            "♻️ **Highly Recyclable - Follow these steps:**\n"
            "1. Rinse thoroughly.\n"
            "2. Remove and recycle cap separately if instructed.\n"
            "3. Crush to save space.\n"
            "4. Place in plastic recycling bin."
        ),
        "Corrugated carton": (
            "📦 **Recyclable - Follow these steps:**\n"
            "1. Remove packing tape and labels.\n"
            "2. Flatten to save space.\n"
            "3. Ensure dry and clean.\n"
            "4. Place in cardboard recycling."
        ),
        "Crisp packet": (
            "🚮 **Non-Recyclable (mostly) - Follow these steps:**\n"
            "1. Clean if food-free and accepted in soft plastics.\n"
            "2. Drop at specific soft plastic collection points (like supermarkets).\n"
            "3. Otherwise, dispose in general waste.\n"
            "4. Prefer recyclable alternatives in the future."
        ),
        
        
        
        "Disposable food container": (
            "♻️ **Container Recycling**\n"
            "1. Scrape off food remains and rinse thoroughly.\n"
            "2. Check for recycling symbol and number.\n"
            "3. If recyclable, place in recycling bin.\n"
            "4. If greasy or wax-coated, dispose in general waste."
        ),
        "Disposable plastic cup": (
            "♻️ **Plastic Cup Sorting**\n"
            "1. Check for recycling symbol (usually on the bottom).\n"
            "2. Rinse the cup.\n"
            "3. If labeled recyclable, place in recycling bin.\n"
            "4. If unmarked or contaminated, discard in general waste."
        ),
        "Drink can": (
            "♻️ **Can Recycling**\n"
            "1. Rinse the can to remove liquids.\n"
            "2. Crush to save space if required.\n"
            "3. Place in the metal recycling bin."
        ),
        "Drink carton": (
            "♻️ **Carton Disposal**\n"
            "1. Rinse out any remaining liquid.\n"
            "2. Flatten to save space.\n"
            "3. Place in designated carton recycling bin.\n"
            "4. If unsure, check local recycling rules."
        ),
        "Egg carton": (
            "🌱 **Biodegradable Carton Disposal**\n"
            "1. If made of paper/cardboard – compost or recycle.\n"
            "2. If plastic – rinse and recycle.\n"
            "3. If Styrofoam – dispose in general waste (non-recyclable in most areas)."
        ),
        "Foam cup": (
            "🚯 **Non-Recyclable Foam**\n"
            "1. Avoid using Styrofoam products.\n"
            "2. Dispose of in general waste.\n"
            "3. Choose paper or reusable alternatives in the future."
        ),
        "Foam food container": (
            "🚯 **Foam Disposal**\n"
            "1. Clean out food residues.\n"
            "2. Place in general waste (not accepted in curbside recycling).\n"
            "3. Look for biodegradable containers next time."
        ),
        "Food Can": (
            "♻️ **Metal Food Can Recycling**\n"
            "1. Rinse to remove any leftover food.\n"
            "2. Remove labels if required by your local recycling center.\n"
            "3. Place in metal recycling bin."
        ),
        "Food waste": (
            "🌱 **Organic Waste Disposal**\n"
            "1. Separate food scraps from packaging.\n"
            "2. Compost at home or use a municipal compost bin.\n"
            "3. Avoid putting food waste in regular recycling."
        ),
        "Garbage bag": (
            "🚮 **General Waste Disposal**\n"
            "1. Fill with non-recyclable waste only.\n"
            "2. Tie securely to prevent spillage.\n"
            "3. Place in general waste collection bin.\n"
            "4. Use compostable bags if disposing of organic waste."
        ),
        "Glass bottle": (
            "🟢 **Glass Bottle Recycling**\n"
            "1. Empty and rinse the bottle.\n"
            "2. Remove caps or corks.\n"
            "3. Place in glass recycling bin."
        ),
        "Glass cup": (
            "🚯 **Non-Recyclable Glassware**\n"
            "1. Wrap safely in paper or bubble wrap.\n"
            "2. Label as 'glass' and place in general waste.\n"
            "3. Do not mix with recyclable container glass."
        ),
        "Glass jar": (
            "🟢 **Jar Recycling**\n"
            "1. Remove food residue and rinse clean.\n"
            "2. Take off lid – recycle separately based on material.\n"
            "3. Place jar in glass recycling bin."
        ),
        "Magazine paper": (
            "📄 **Glossy Paper Recycling**\n"
            "1. Remove staples or bindings if possible.\n"
            "2. Recycle unlaminated and clean pages.\n"
            "3. Do not recycle metallic or glittered pages – place in general waste."
        ),
        "Meal carton": (
            "♻️ **Food Carton Disposal**\n"
            "1. Rinse out any leftovers.\n"
            "2. Flatten the carton.\n"
            "3. Place in mixed recycling or carton-specific bin."
        ),
        "Metal bottle cap": (
            "♻️ **Small Metal Recycling**\n"
            "1. Collect multiple caps in a steel can.\n"
            "2. Once full, crimp the can shut.\n"
            "3. Place the sealed can in the metal recycling bin."
        ),
        "Metal lid": (
            "♻️ **Lid Disposal**\n"
            "1. Remove from jars or containers.\n"
            "2. Rinse off any residues.\n"
            "3. Recycle with other metal items."
        ),
        "Normal paper": (
            "📄 **Paper Recycling**\n"
            "1. Ensure paper is dry and clean.\n"
            "2. Remove staples or tape if possible.\n"
            "3. Place in the paper recycling bin."
        ),
        "Other carton": (
            "♻️ **Mixed Carton Disposal**\n"
            "1. Clean and dry.\n"
            "2. Flatten to save space.\n"
            "3. Recycle with other cardboard or drink cartons."
        ),
        "Other plastic": (
            "🚮 **Unlabeled Plastic Disposal**\n"
            "1. Check for recycling symbol.\n"
            "2. If missing or unaccepted locally, dispose in general waste.\n"
            "3. Avoid purchasing non-recyclable plastic products."
        ),
        
        "Other plastic bottle": (
            "♻️ **Plastic Bottle Recycling**\n"
            "1. Check recycling code on the bottle (usually 1, 2, or 5 are widely accepted).\n"
            "2. Rinse thoroughly and remove caps.\n"
            "3. Crush if needed and place in plastic recycling bin."
        ),
        "Other plastic container": (
            "♻️ **Container Sorting**\n"
            "1. Identify recycling code and confirm local acceptance.\n"
            "2. Clean thoroughly.\n"
            "3. Place in recycling or general waste based on recyclability."
        ),
        "Other plastic cup": (
            "♻️ **Cup Disposal**\n"
            "1. Look for recycling code.\n"
            "2. Rinse and place in appropriate recycling bin.\n"
            "3. If no label, discard in general waste."
        ),
        "Other plastic wrapper": (
            "🚯 **Soft Plastic Disposal**\n"
            "1. Clean of food residues.\n"
            "2. Take to soft plastic drop-off points (e.g., supermarkets).\n"
            "3. If no program available, dispose in general waste."
        ),
        "Paper bag": (
            "📄 **Paper Bag Recycling/Composting**\n"
            "1. Ensure it's uncoated and clean.\n"
            "2. Recycle or compost it.\n"
            "3. If greasy or lined with plastic, place in general waste."
        ),
        "Paper cup": (
            "♻️ **Cup Disposal**\n"
            "1. Check if lined with plastic.\n"
            "2. If recyclable in your area, rinse and recycle.\n"
            "3. Compost if uncoated paper and clean."
        ),
        "Paper straw": (
            "🌱 **Eco-Friendly Straw Disposal**\n"
            "1. Compost if clean and uncoated.\n"
            "2. Otherwise, place in paper recycling bin.\n"
            "3. Avoid plastic alternatives."
        ),
        "Pizza box": (
            "♻️ **Greasy Cardboard Disposal**\n"
            "1. Tear off clean parts and recycle them.\n"
            "2. Compost greasy sections if possible.\n"
            "3. Otherwise, discard greasy parts in general waste."
        ),
        "Plastic bottle cap": (
            "♻️ **Cap Recycling**\n"
            "1. Remove from bottle.\n"
            "2. Check if your local center accepts them.\n"
            "3. Recycle with bottles or collect and place inside a plastic container before recycling."
        ),
        "Plastic film": (
            "🔄 **Plastic Film Disposal**\n"
            "1. Keep clean and dry.\n"
            "2. Collect and return to store drop-off points for soft plastics.\n"
            "3. Never place in curbside recycling."
        ),
        "Plastic gloves": (
            "🚯 **Glove Disposal**\n"
            "1. Ensure gloves are clean (no medical waste).\n"
            "2. Dispose in general waste bin.\n"
            "3. Switch to reusable or compostable gloves when possible."
        ),
        "Plastic lid": (
            "♻️ **Lid Recycling**\n"
            "1. Rinse and check recycling code.\n"
            "2. If accepted, place in appropriate bin.\n"
            "3. If unmarked or too small, place in general waste."
        ),
        "Plastic straw": (
            "🚯 **Single-Use Straw Disposal**\n"
            "1. Place directly in general waste bin.\n"
            "2. Avoid single-use plastic by using metal or bamboo straws."
        ),
        "Plastic utensils": (
            "🚯 **Plastic Cutlery Disposal**\n"
            "1. Rinse if needed.\n"
            "2. Place in general waste (rarely recyclable).\n"
            "3. Use compostable or reusable alternatives instead."
        ),
        "Polypropylene bag": (
            "♻️ **Reusable Bag Disposal**\n"
            "1. Reuse as many times as possible.\n"
            "2. Recycle at plastic bag drop-off points if available.\n"
            "3. Dispose in general waste if damaged and not accepted."
        ),
        "Pop tab": (
            "♻️ **Pop Tab Recycling**\n"
            "1. Collect in a container.\n"
            "2. Recycle with aluminum cans.\n"
            "3. Avoid scattering loose tabs in bins."
        ),
        "Rope - strings": (
            "🚯 **String Disposal**\n"
            "1. Cut into smaller pieces.\n"
            "2. Tie up to avoid tangling machinery.\n"
            "3. Place in general waste bin."
        ),
        "Scrap metal": (
            "🔧 **Scrap Metal Recycling**\n"
            "1. Collect and store safely.\n"
            "2. Take to local scrap metal or e-waste collection centers.\n"
            "3. Never place in regular recycling bins."
        ),
        "Shoe": (
            "👞 **Footwear Disposal**\n"
            "1. Donate usable shoes to charities or recycling programs.\n"
            "2. If torn or unusable, place in textile recycling if available.\n"
            "3. Otherwise, dispose in general waste."
        ),
        "Single-use carrier bag": (
            "♻️ **Plastic Bag Recycling**\n"
            "1. Reuse multiple times before discarding.\n"
            "2. Return to plastic bag drop-off bins.\n"
            "3. Avoid single-use by switching to cloth bags."
        ),
        "Six pack rings": (
            "🚯 **Wildlife-Safe Disposal**\n"
            "1. Cut each loop to prevent entanglement.\n"
            "2. Dispose in general waste.\n"
            "3. Use eco-friendly can carriers where available."
        ),
        "Spread tub": (
            "♻️ **Plastic Tub Recycling**\n"
            "1. Clean and remove food residue.\n"
            "2. Check recycling symbol.\n"
            "3. Recycle if accepted in your area."
        ),
        "Squeezable tube": (
            "🚯 **Tube Disposal**\n"
            "1. Empty the contents completely.\n"
            "2. If marked recyclable, rinse and recycle.\n"
            "3. If unmarked, discard in general waste."
        ),
        "Styrofoam piece": (
            "🚯 **Foam Disposal**\n"
            "1. Break into smaller pieces.\n"
            "2. Bag and place in general waste.\n"
            "3. Avoid using Styrofoam when alternatives exist."
        ),
        "Tissues": (
            "🗑️ **Used Tissue Disposal**\n"
            "1. Do not recycle used tissues.\n"
            "2. Compost if clean and unbleached.\n"
            "3. Otherwise, discard in general waste."
        ),
        "Toilet tube": (
            "🌱 **Tube Disposal**\n"
            "1. Recycle with paper/cardboard.\n"
            "2. Or compost at home (fully biodegradable)."
        ),
        "Tupperware": (
            "♻️ **Reusable Container Disposal**\n"
            "1. Donate if in good condition.\n"
            "2. Recycle if labeled and accepted locally.\n"
            "3. Otherwise, dispose in general waste."
        ),
        "Unlabeled litter": (
            "🚯 **Uncategorized Waste**\n"
            "1. If unsure, do not recycle to avoid contamination.\n"
            "2. Place safely in general waste.\n"
            "3. Try to identify or avoid unmarked items."
        ),
        "Wrapping paper": (
            "🎁 **Gift Wrap Disposal**\n"
            "1. Remove tape and decorations.\n"
            "2. If non-metallic and uncoated, recycle.\n"
            "3. Otherwise, place in general waste."
        )
        # Remaining waste types will be continued below due to length
    }




# Home Page
def home_page():

    apply_background()
    st.markdown(
        """
        <style>
            /* Background Color */
            body {
                background-color: #e8f5e9 !important; /* Softer Green Background */
            }

            /* Animated Title */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .title {
                font-size: 52px; /* Larger for Emphasis */
                font-weight: bold;
                text-align: center;
                color: #1B5E20; /* Deep Green */
                text-transform: uppercase;
                letter-spacing: 2px;
                text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.3);
                animation: fadeIn 1s ease-in-out, pulse 2s infinite alternate;
                padding: 20px;
            }

            /* Pulsing Effect */
            @keyframes pulse {
                0% { transform: scale(1); }
                100% { transform: scale(1.08); }
            }

            /* Content Styling */
            .content {
                font-size: 22px;
                color: black; /* Dark Green for Readability */
                text-align: center;
                margin-top: 15px;
                animation: fadeIn 1.5s ease-in-out;
                line-height: 1.6;
                font-weight: 500;
            }

            /* Highlighted Text */
            .highlight {
                font-size: 24px;
                font-weight: bold;
                color: #FBC02D; /* Yellow-Gold for Attention */
            }

            /* Button Container */
            .button-container {
                display: flex;
                justify-content: center;
                margin-top: 30px;
            }

            /* Animated Start Button */
            .start-button {
                font-size: 22px;
                font-weight: bold;
                background: linear-gradient(135deg, #2E7D32, #81C784); /* Green Gradient */
                color: white;
                padding: 16px 32px;
                border-radius: 14px;
                border: none;
                cursor: pointer;
                transition: all 0.3s ease-in-out;
                animation: fadeIn 2s ease-in-out;
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
                text-transform: uppercase;
            }

            .start-button:hover {
                background: linear-gradient(135deg, #1B5E20, #66BB6A);
                transform: scale(1.1);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
            }

            /* Footer */
            .footer {
                text-align: center;
                font-size: 18px;
                color: #4E342E;
                margin-top: 40px;
                padding: 10px;
                animation: fadeIn 2s ease-in-out;
                font-weight: 600;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

    # Title Section
    st.markdown('<p class="title">♻️ Waste Vision – AI-Based Waste Management System</p>', unsafe_allow_html=True)

    # Introduction Section
    st.markdown(
        """
        <p class="content">
        🌱 Welcome to <span class="highlight">Waste Vision</span>, an innovative AI-powered system designed to revolutionize waste management 
        and promote environmental sustainability. 
        Using AI, we provide a <span class="highlight">smart, efficient, and eco-friendly</span> solution for waste identification and responsible disposal.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p class="footer">
        ✅ <b>Join us in making the world cleaner and greener! 🌍✨</b>
        </p>
        """,
        unsafe_allow_html=True
    )

    # Get Started Button (Centered)
    if st.button("🚀 Get Started"):
        st.session_state.page = "upload"

    # Footer


    
# Upload Page
def upload_page():
    apply_background()
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Upload Image", "About Page", "Technical Details"])
    
    if page == "Upload Image":
        # Custom CSS for Styling & Animations
        st.markdown(
            """
            <style>
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(-20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            @keyframes glow {
                0% { text-shadow: 0px 0px 10px #4CAF50; }
                50% { text-shadow: 0px 0px 20px #81C784; }
                100% { text-shadow: 0px 0px 10px #4CAF50; }
            }

            .title {
                font-size: 42px;
                font-weight: bold;
                color: #2E7D32;
                text-align: center;
                animation: fadeIn 1.2s ease-in-out, glow 2s infinite alternate;
                padding: 10px;
            }

            .info-card {
                padding: 15px;
                margin: 10px 0;
                border-radius: 12px;
                background: #f0f0f0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                animation: fadeIn 1.5s ease-in-out;
            }

            .content {
                font-size: 18px;
                color: black !important;
                text-align: justify;
                animation: fadeIn 2s ease-in-out;
            }

            .highlight {
                font-size: 20px;
                font-weight: bold;
                color: #1B5E20;
                background: #E8F5E9;
                padding: 5px 10px;
                border-radius: 8px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title
        st.markdown('<p class="title">📤 Upload an Image</p>', unsafe_allow_html=True)

        # File Upload Section
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            
            
            st.image(image, width=500)

            # Custom Caption with Black Color
            st.markdown(
                """
                <p style="text-align: center; font-size: 16px; color: black; font-weight: bold;">
                Uploaded Image
                </p>
                """,
                unsafe_allow_html=True
            )
                
            model = load_model()
            results = detect_objects(model, image)
            processed_image = draw_boxes(image, results)
            # Display Processed Image
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.image(processed_image, width=500)  # Display image without caption

            # Custom Caption with Black Color
            st.markdown(
                """
                <p style="text-align: center; font-size: 16px; color: black; font-weight: bold;">
                ✅ Processed Image
                </p>
                """,
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Disposal Methods
            st.markdown('<p class="title">♻️ Disposal Methods</p>', unsafe_allow_html=True)
            disposal_methods = get_disposal_methods()

            for result in results:
                for box in result.boxes:
                    label = result.names[int(box.cls[0])]

                    # Styled disposal info
                     # Styled disposal info
                    st.markdown('<div class="info-card">', unsafe_allow_html=True)
                    st.markdown(
                        f'<p class="content"><span class="highlight">{label}</span> - {disposal_methods.get(label, "No disposal method found.")}</p>',
                        unsafe_allow_html=True
                    )
                    st.markdown('</div>', unsafe_allow_html=True)

    elif page == "About Page":

        apply_background()
        # Add custom styles and animations
        st.markdown(
            """
            <style>
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(-20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            @keyframes glow {
                0% { text-shadow: 0px 0px 10px #4CAF50; }
                50% { text-shadow: 0px 0px 20px #81C784; }
                100% { text-shadow: 0px 0px 10px #4CAF50; }
            }

            .title {
                font-size: 42px;
                font-weight: bold;
                color: #2E7D32;
                text-align: center;
                animation: fadeIn 1.2s ease-in-out, glow 2s infinite alternate;
                padding: 10px;
            }

            .subheading {
                font-size: 24px;
                font-weight: bold;
                margin-top: 20px;
                color: #FBC02D;
                animation: fadeIn 1.5s ease-in-out;
            }

            .content, p, li {
                font-size: 18px;
                color: black;
                text-align: justify;
                animation: fadeIn 2s ease-in-out;
            }

            .highlight {
                font-size: 20px;
                font-weight: bold;
                color: #1B5E20;
                background: #E8F5E9;
                padding: 5px 10px;
                border-radius: 8px;
            }

            .info-card {
                padding: 15px;
                margin: 10px 0;
                border-radius: 12px;
                background: #f0f0f0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                animation: fadeIn 1.5s ease-in-out;
            }

            .icon {
                font-size: 22px;
                margin-right: 5px;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title Section
        st.markdown('<p class="title">🌱 About Us – Waste Vision</p>', unsafe_allow_html=True)

        # Introduction Section
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="content">
            Welcome to <span class="highlight">Waste Vision</span>, an innovative AI-powered waste classification system designed to revolutionize 
            waste management and promote environmental sustainability. Our goal is to help users make **eco-friendly** waste disposal choices with AI.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Why Waste Vision?
        st.markdown('<p class="subheading">🌍 Why Waste Vision?</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="content">
            Many people struggle to correctly dispose of waste, leading to pollution and landfill waste. 
            <span class="highlight">Waste Vision</span> classifies waste items and suggests correct disposal methods, helping users make **eco-conscious** choices.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # How It Works
        st.markdown('<p class="subheading">🛠️ How It Works</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="content">
            <span class="icon">🚀</span> <span class="highlight">Step 1:</span> Upload an image of the waste item.<br>
            <span class="icon">🧠</span> <span class="highlight">Step 2:</span> AI model classifies the waste.<br>
            <span class="icon">📌</span> <span class="highlight">Step 3:</span> System suggests correct disposal or recycling methods.<br>
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Key Features
        st.markdown('<p class="subheading">✨ Key Features</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            - ✔️ **AI-Powered Waste Identification** – Uses Deep Learning for accurate classification.  
            - ✔️ **Instant Disposal Guidance** – Provides **eco-friendly** disposal recommendations.  
            - ✔️ **User-Friendly Interface** – Built with **Streamlit** for smooth interaction.  
            - ✔️ **Sustainable Impact** – Helps reduce pollution and encourages recycling.  
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Main Aim
        st.markdown('<p class="subheading">🎯 Main Aim of the Project</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            - ✅ **Reduce incorrect waste disposal** and promote **recycling**.  
            - ✅ **Assist individuals and waste management authorities** in identifying recyclable materials.  
            - ✅ **Contribute to environmental conservation** by reducing landfill waste.  
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Benefits
        st.markdown('<p class="subheading">🌱 Benefits of Waste Vision</p>', unsafe_allow_html=True)
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            - 🌍 **Eco-Friendly** – Supports sustainable waste management.  
            - 🔬 **AI-Powered** – Uses **Computer Vision & ML** for waste identification.  
            - 📊 **Educational** – Helps users understand **correct disposal methods**.  
            - 💡 **Future Scope** – Can be integrated into **municipal waste management**.  
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Closing Message
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <p class="content">
            By using <span class="highlight">Waste Vision</span>, you take a step toward a **cleaner and greener** planet! 🌏♻️  
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown('</div>', unsafe_allow_html=True)


    elif page == "Technical Details":
        apply_background()

        # Add custom styles
        st.markdown(
            """
            <style>
            @keyframes fadeIn {
                0% { opacity: 0; transform: translateY(-20px); }
                100% { opacity: 1; transform: translateY(0); }
            }

            .tech-title {
                font-size: 42px;
                font-weight: bold;
                text-align: center;
                color: #2E7D32;
                background: linear-gradient(to right, #1b5e20, #66bb6a);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                animation: fadeIn 1.2s ease-in-out;
                padding: 10px;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }

            .tech-content {
                font-size: 20px;
                color: black;
                text-align: left;
                animation: fadeIn 1.5s ease-in-out;
            }

            .tech-card {
                padding: 15px;
                margin: 10px 0;
                border-radius: 12px;
                background: #f0f0f0;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                animation: fadeIn 1s ease-in-out;
            }

            .tech-list {
                font-size: 18px;
                color: black;
                padding-left: 20px;
            }

            .tech-list li {
                margin-bottom: 10px;
                padding: 10px;
                background: #e8f5e9;
                border-left: 5px solid #2E7D32;
                border-radius: 5px;
                list-style-type: none;
                animation: fadeIn 1.5s ease-in-out;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Title
        st.markdown('<h1 class="tech-title">💡 Technical Details</h1>', unsafe_allow_html=True)

        # Introduction Section
        st.markdown('<p class="tech-content">Here are the technologies used to build Waste Vision:</p>', unsafe_allow_html=True)

        # Styled technology list
        st.markdown(
            """
            <div class="tech-card">
            <ul class="tech-list">
                <li>🧠 <strong>YOLO Model:</strong> Used for waste classification.</li>
                <li>💻 <strong>Streamlit:</strong> Interactive UI for the application.</li>
                <li>📷 <strong>OpenCV & PIL:</strong> Image processing and object detection.</li>
                <li>📊 <strong>NumPy:</strong> Data handling & manipulation.</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

# Main Function
def main():
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if st.session_state.page == "home":
        home_page()
    else:
        upload_page()

if __name__ == "__main__":
    main()