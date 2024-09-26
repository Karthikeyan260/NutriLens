import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from the Gemini model
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to set up the uploaded image for input
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded!")

# Function to generate meal suggestions
def get_meal_suggestions(analysis_results):
    suggestion_prompt = f"Based on this nutritional analysis: {analysis_results}, suggest 3 healthy meal ideas that complement this diet. Format the response as a bulleted list."
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(suggestion_prompt)
    return response.text

# Set page config
st.set_page_config(page_title="NutriLens", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling with updated color scheme
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #ffffff; /* Lighter Mint */
            color: #ffffff; /* Muted Dark Green */
        }
        .main {
            background-color: #000000;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(5, 79, 65, 0.1); /* Muted Green shadow */
        }
        .stButton > button {
            background-color: #2bbbad; /* Vibrant Teal */
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #388e3c; /* Dark Emerald Green */
            transform: translateY(-2px);
        }
        .uploaded-image {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(5, 79, 65, 0.1); /* Muted Green shadow */
        }
        .response-box {
            background-color: #f3f8f2; /* Lighter Mint */
            border: 1px solid #78c79e; /* Soft Mint */
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            color: #000000;
        }
        .meal-suggestion-box {
            background-color: #f3f8f2; /* Lighter Mint */
            border: 1px solid #27a697; /* Balanced Teal */
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            color: #000000;
        }
        .header {
            color: #1b5e20; /* Deep Forest Green */
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .subheader {
            color: #1a8572; /* Cool Green */
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .chat-input {
            border: 1px solid #78c79e; /* Soft Mint */
            border-radius: 5px;
            padding: 0.5rem;
        }
        .chat-message {
            padding: 1rem;
            border-radius: 5px;
            margin-bottom: 0.5rem;
        }
        .user-message {
            background-color: #f3f8f2; /* Lighter Mint */
            border: 1px solid #78c79e; /* Soft Mint */
        }
        .bot-message {
            background-color: #f3f8f2; /* Lighter Mint */
            border: 1px solid #27a697; /* Balanced Teal */
        }
        .stTextArea textarea {
            background-color: #f3f8f2; /* Lighter Mint */
        }
        .sidebar .sidebar-content {
            background-color: #035c4b; /* Deep Teal */
        }
        .sidebar .sidebar-content {
            color: white; /* Keep text white for contrast */
        }
    </style>
""", unsafe_allow_html=True)


# Sidebar
with st.sidebar:
    st.image("imgs\\Green Beige Circle Healthy Food Logo.svg")
    st.title("More Options")
    st.markdown("Upload an image of your food to get nutritional insights and meal suggestions!")
    
    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Calorie Count", "Macronutrient Breakdown", "Allergen Detection", "Custom Prompt"],
        index=0
    )

# Main content
st.markdown("<h1 class='header'>NutriLens</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Get instant nutritional insights from your food images!!!</p>", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True, output_format="PNG")

# Set the appropriate input prompt based on the selected analysis type
if analysis_type == "Calorie Count":
    input_prompt = "Analyze the image and provide a calorie count for each food item. Format your response as a bulleted list."
elif analysis_type == "Macronutrient Breakdown":
    input_prompt = "Analyze the image and provide a breakdown of macronutrients (protein, carbs, fats) for each food item. Format your response as a bulleted list."
elif analysis_type == "Allergen Detection":
    input_prompt = "Analyze the image and identify any potential allergens in the food items. Format your response as a bulleted list."
elif analysis_type == "Custom Prompt":
    input_prompt = st.text_area("Enter your custom prompt:", "Analyze the image and tell me about the nutritional value of the food.")

# Analysis button
if st.button("Analyze Image"):
    if uploaded_file is not None:
        with st.spinner("Analyzing your food image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response("", image_data, input_prompt)
                
                st.markdown("<h3>Analysis Results:</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)
                
                # Meal Suggestions
                with st.spinner("Generating meal suggestions..."):
                    meal_suggestions = get_meal_suggestions(response)
                    st.markdown("<h3>Meal Suggestions:</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div class='meal-suggestion-box'>{meal_suggestions}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload an image first!")

# Chat section
st.markdown("---")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about nutrition or the analyzed image"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            if uploaded_file:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response(prompt, image_data, "")
            else:
                response = get_gemini_response(prompt, [], "")
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("Developed with ❤️ by VK")