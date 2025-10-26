AI Chatbot Web App

A Flask-based AI chatbot that integrates OpenAI’s GPT model with OpenWeatherMap’s API to provide real-time weather updates and intelligent chat responses in a single interactive web interface.

Features

AI Conversations: Chat with an intelligent assistant powered by OpenAI’s GPT models.

Live Weather Updates: Get real-time weather information by entering a city name or GPS coordinates.

Context Awareness: Maintains chat history for smoother, more natural responses.

Error Handling: Gracefully handles missing API keys and rate limit issues.

Simple Web Interface: Clean, user-friendly interface built with Flask and HTML.

Tech Stack

Backend: Python, Flask

APIs: OpenAI API, OpenWeatherMap API

Libraries: requests, python-dotenv, openai

Frontend: HTML, Jinja Templates

Installation

1️⃣ Clone the repository
git clone https://github.com/yourusername/ai-chatbot-weather.git
cd ai-chatbot-weather

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate      # For Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Add environment variables

Create a .env file in the project root with the following:

OPENAI_API_KEY=your_openai_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key

5️⃣ Run the application
python app.py


Visit http://127.0.0.1:5000
 in your browser.
