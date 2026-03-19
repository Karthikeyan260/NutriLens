import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Configure Google Generative AI with API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Retry constants
_MAX_RETRIES = 3
_INITIAL_BACKOFF = 15  # seconds to wait on first rate-limit hit


def _is_rate_limit_error(exc):
    """Return True if the exception signals a 429 / quota-exceeded error."""
    msg = str(exc).lower()
    return "429" in msg or "quota" in msg or "rate_limit_exceeded" in msg or "resource_exhausted" in msg


def _call_with_retry(fn, *args, **kwargs):
    """
    Call *fn* with the supplied arguments and retry up to _MAX_RETRIES times
    when a rate-limit (429) error is received, using exponential back-off.
    Any other exception is re-raised immediately.
    """
    backoff = _INITIAL_BACKOFF
    for attempt in range(_MAX_RETRIES):
        try:
            return fn(*args, **kwargs)
        except Exception as exc:
            if _is_rate_limit_error(exc) and attempt < _MAX_RETRIES - 1:
                st.warning(
                    f"Rate limit reached. Waiting {backoff}s before retrying "
                    f"(attempt {attempt + 1}/{_MAX_RETRIES})…"
                )
                time.sleep(backoff)
                backoff *= 2  # exponential back-off
            else:
                raise


# Function to get the response from the Gemini model
def get_gemini_response(input, image, prompt):
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    parts = [p for p in [input, image[0] if image else None, prompt] if p]
    response = _call_with_retry(model.generate_content, parts)
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
    model = genai.GenerativeModel('gemini-2.5-flash-lite')
    response = _call_with_retry(model.generate_content, suggestion_prompt)
    return response.text

# Set page config
st.set_page_config(page_title="NutrifyAI", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');
        body {
            font-family: 'Roboto', sans-serif;
            background-color: #f9f9f9;
            color: #333333;
        }
        .main {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        .stButton > button:hover {
            background-color: #388E3C;
            transform: translateY(-2px);
        }
        .uploaded-image {
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .response-box, .meal-suggestion-box {
            background-color: #f1f1f1;
            border: 1px solid #dddddd;
            border-radius: 5px;
            padding: 1rem;
            margin-top: 1rem;
            color: #333333;
        }
        .header {
            color: #4CAF50;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
        .subheader {
            color: #777777;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("karthi.jpeg")
    st.title("More Options")
    st.markdown("Upload or capture an image of your food to get nutritional insights and meal suggestions!")

    # Analysis type selection
    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Calorie Count", "Macronutrient Breakdown", "Allergen Detection", "Custom Prompt"],
        index=0
    )

# Main content
st.markdown("<h1 class='header'>NutrifyAI</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Get instant nutritional insights from your food images!!!</p>", unsafe_allow_html=True)

# Choose between upload or camera
upload_method = st.radio("Choose image input method:", ["Upload", "Use Camera"], horizontal=True)

uploaded_file = None
if upload_method == "Upload":
    uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])
elif upload_method == "Use Camera":
    uploaded_file = st.camera_input("Take a picture of your food")

# Show uploaded or captured image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Your Food Image", use_container_width=True)

# Set the appropriate input prompt based on the selected analysis type
if analysis_type == "Calorie Count":
    input_prompt = "Analyze the image and provide a calorie count for each food item. Format your response as a bulleted list."
elif analysis_type == "Macronutrient Breakdown":
    input_prompt = "Analyze the image and provide a breakdown of macronutrients (protein, carbs, fats) for each food item. Format your response as a bulleted list."
elif analysis_type == "Allergen Detection":
    input_prompt = "Analyze the image and identify any potential allergens in the food items. Format your response as a bulleted list."
elif analysis_type == "Custom Prompt":
    input_prompt = st.text_area("Enter your custom prompt:", "Analyze the image and tell me about the nutritional value of the food.")

# Analyze button
if st.button("Analyze Image"):
    if uploaded_file is not None:
        with st.spinner("Analyzing your food image..."):
            try:
                image_data = input_image_setup(uploaded_file)
                response = get_gemini_response("", image_data, input_prompt)

                st.markdown("<h3>Analysis Results:</h3>", unsafe_allow_html=True)
                st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)

                # Small pause between the two API calls to reduce the chance
                # of hitting per-minute rate limits back-to-back.
                time.sleep(2)

                with st.spinner("Generating meal suggestions..."):
                    meal_suggestions = get_meal_suggestions(response)
                    st.markdown("<h3>Meal Suggestions:</h3>", unsafe_allow_html=True)
                    st.markdown(f"<div class='meal-suggestion-box'>{meal_suggestions}</div>", unsafe_allow_html=True)

            except Exception as e:
                if _is_rate_limit_error(e):
                    st.error(
                        "⚠️ **API quota exceeded (rate limit 429).** "
                        "The free-tier per-minute quota for this Google Cloud project has been reached. "
                        "Please wait a minute and try again, or consider requesting a higher quota at "
                        "https://cloud.google.com/docs/quotas/help/request_increase"
                    )
                else:
                    st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please upload or capture an image first!")

# Chat section
st.markdown("---")
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

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if uploaded_file:
                    image_data = input_image_setup(uploaded_file)
                    response = get_gemini_response(prompt, image_data, "")
                else:
                    response = get_gemini_response(prompt, [], "")
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                if _is_rate_limit_error(e):
                    error_msg = (
                        "⚠️ **API quota exceeded (rate limit 429).** "
                        "Please wait a minute and try again, or request a higher quota at "
                        "https://cloud.google.com/docs/quotas/help/request_increase"
                    )
                else:
                    error_msg = f"An error occurred: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
