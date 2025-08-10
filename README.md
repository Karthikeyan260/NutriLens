# 🍎 NutriLens - AI-Powered Food Nutrition Analysis

**NutriLens** (also known as NutrifyAI) is an intelligent food nutrition analysis application that leverages Google's Gemini AI to provide instant nutritional insights from food images. Simply upload or capture a photo of your meal, and get detailed nutritional information, calorie counts, and personalized meal suggestions.

![NutriLens](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔍 **Multi-Mode Analysis**
- **Calorie Count**: Get accurate calorie estimates for each food item
- **Macronutrient Breakdown**: Detailed protein, carbs, and fats analysis
- **Allergen Detection**: Identify potential allergens in your food
- **Custom Analysis**: Ask specific nutrition questions about your meals

### 📱 **Flexible Image Input**
- Upload images from your device (JPG, JPEG, PNG)
- Real-time camera capture for instant analysis
- High-quality image processing with PIL

### 🤖 **AI-Powered Insights**
- Powered by Google's Gemini 1.5 Flash model
- Intelligent meal suggestions based on your food analysis
- Interactive chat interface for nutrition questions
- Context-aware responses about your uploaded food images

### 🎨 **Modern User Interface**
- Clean, responsive design with custom CSS styling
- Professional color scheme and typography
- Intuitive navigation and user experience
- Mobile-friendly interface

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google API key for Gemini AI
- Webcam (optional, for camera capture feature)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Karthikeyan260/NutriLens.git
   cd NutriLens
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   
   Get your Google API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

4. **Run the application**
   ```bash
   streamlit run ap.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 🎯 Usage Guide

### Basic Nutrition Analysis

1. **Choose Input Method**: Select either "Upload" to choose an image file or "Use Camera" to take a photo
2. **Select Analysis Type**: Choose from:
   - Calorie Count
   - Macronutrient Breakdown
   - Allergen Detection
   - Custom Prompt
3. **Upload/Capture Image**: Provide a clear image of your food
4. **Get Results**: Click "Analyze Image" to receive detailed nutrition insights
5. **View Meal Suggestions**: Get AI-generated meal recommendations based on your analysis

### Interactive Chat

- Use the chat interface at the bottom to ask follow-up questions
- Ask about specific ingredients, cooking methods, or nutritional concerns
- Get personalized advice based on your uploaded food images

### Tips for Best Results

- **Good Lighting**: Ensure your food is well-lit for accurate analysis
- **Clear Images**: Take photos from a good angle showing all food items
- **Single Meal Focus**: For best results, analyze one meal at a time
- **Detailed Questions**: Be specific in your custom prompts for better insights

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **AI/ML**: Google Gemini 1.5 Flash
- **Image Processing**: Pillow (PIL)
- **Environment Management**: python-dotenv
- **Development**: Dev Containers support
- **Language**: Python 3.11+

## 📁 Project Structure

```
NutriLens/
├── ap.py                 # Main Streamlit application
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
├── karthi.jpeg         # Profile image for sidebar
├── .devcontainer/      # Development container configuration
│   └── devcontainer.json
└── README.md           # Project documentation
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google Gemini API key | Yes |

### Streamlit Configuration

The application runs with the following default settings:
- Port: 8501
- CORS: Disabled for development
- XSRF Protection: Disabled for development

## 🐳 Development with Dev Containers

This project includes Dev Container support for consistent development environments:

1. Open the project in VS Code
2. Install the Dev Containers extension
3. Press `F1` and select "Dev Containers: Reopen in Container"
4. The environment will be automatically set up with all dependencies

## 🤝 Contributing

We welcome contributions to NutriLens! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes**
   - Follow Python best practices
   - Add appropriate comments
   - Test your changes thoroughly
4. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
5. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
6. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to new functions
- Test with different types of food images
- Ensure compatibility with the existing UI design

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Karthikeyan**
- GitHub: [@Karthikeyan260](https://github.com/Karthikeyan260)

## 🙏 Acknowledgments

- [Google Gemini AI](https://ai.google.dev/) for providing the powerful AI capabilities
- [Streamlit](https://streamlit.io/) for the excellent web framework
- The open-source community for the various libraries used in this project

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/Karthikeyan260/NutriLens/issues) page
2. Create a new issue with detailed information
3. Include screenshots and error messages if applicable

## 🔮 Future Enhancements

- [ ] Meal planning and tracking features
- [ ] Integration with fitness apps
- [ ] Barcode scanning for packaged foods
- [ ] Multiple language support
- [ ] Nutritional goal setting and tracking
- [ ] Export functionality for nutrition reports

---

**Made with ❤️ by [Karthikeyan](https://github.com/Karthikeyan260)**

*Empowering healthier eating through AI-powered nutrition insights*