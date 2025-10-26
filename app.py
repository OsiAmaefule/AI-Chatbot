# file: app.py

from flask import Flask, request, render_template, redirect, url_for
import openai
import os
import requests
from dotenv import load_dotenv
from openai import RateLimitError

load_dotenv()

app = Flask(__name__)
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
openweathermap_key = os.getenv("OPENWEATHERMAP_API_KEY")
chat_history = []

def get_weather_info(city=None, lat=None, lon=None):
    if not openweathermap_key:
        return "[Weather API key missing]"

    if city:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweathermap_key}&units=metric"
    elif lat and lon:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={openweathermap_key}&units=metric"
    else:
        return None

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        desc = data['weather'][0]['description']
        temp = data['main']['temp']
        city_name = data.get('name', 'your area')
        return f"The current weather in {city_name} is {desc} with a temperature of {temp}°C."
    else:
        return "Unable to retrieve weather information."

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history
    response = ""

    if request.method == "POST":
        user_input = request.form.get("user_input", "").strip()
        city_name = request.form.get("city_name", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()
        model = request.form.get("model", "gpt-3.5-turbo")

        weather_info = get_weather_info(
            city=city_name if city_name else None,
            lat=latitude if latitude else None,
            lon=longitude if longitude else None
        )

        if not user_input and weather_info:
            user_input = "Tell me the weather at my location."

        if user_input:
            chat_history.append({"role": "user", "content": f"{weather_info}\n{user_input}"})

            try:
                completion = openai_client.chat.completions.create(
                    model=model,
                    messages=chat_history
                )
            except openai.NotFoundError:
                completion = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=chat_history
                )
            except RateLimitError:
                ai_reply = "You’ve exceeded your OpenAI API quota. Please check your usage or billing."
                chat_history.append({"role": "assistant", "content": ai_reply})
                return render_template("index.html", response=ai_reply, messages=chat_history)

            ai_reply = completion.choices[0].message.content.strip()
            chat_history.append({"role": "assistant", "content": ai_reply})
            response = ai_reply

    return render_template("index.html", response=response, messages=chat_history)

@app.route("/reset")
def reset():
    global chat_history
    chat_history = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
