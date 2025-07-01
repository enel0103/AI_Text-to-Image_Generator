from flask import Flask, request, render_template
from dotenv import load_dotenv
import os
import openai

app = Flask(__name__)

# Load API Key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    image_urls = []
    error = None
    if request.method == "POST":
        prompt = request.form["prompt"]
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=4,
                size="1024x1024"
            )
            image_urls = [data["url"] for data in response["data"]]
        except openai.error.RateLimitError:
            error = "Rate limit exceeded. Please wait a moment before trying again."
    return render_template("index.html", image_urls=image_urls, error=error)

if __name__ == "__main__":
    app.run(debug=True)
