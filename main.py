from flask import Flask, render_template
import random
import datetime
import requests

app = Flask(__name__)


@app.route('/')
def home():
    random_number = random.randint(1, 10)
    current_year = datetime.datetime.now().year
    return render_template("index.html", num=random_number, year=current_year)


@app.route("/guess/<name>")
def guess(name):
    gender_response = requests.get(f"https://api.genderize.io?name={name}")
    response = requests.get("https://api.agify.io", params={"name": "michael"})
    # print(response.json())
    return render_template("guess.html", response=response.json(), gender_data=gender_response.json())



if __name__ == "__main__":
    app.run(debug=True)


