from flask import Flask, render_template_string, request
from datetime import datetime
import pytz

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Hello World App</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(to right, #83a4d4, #b6fbff);
            color: #333;
            padding: 40px;
            text-align: center;
        }
        h1 {
            color: #2c3e50;
        }
        .time {
            color: #34495e;
            font-style: italic;
            margin-bottom: 30px;
        }
        .input-form {
            margin-top: 20px;
        }
        input[type="text"] {
            padding: 10px;
            width: 250px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-top: 10px;
        }
        input[type="submit"] {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin-left: 10px;
        }
        input[type="submit"]:hover {
            background-color: #2980b9;
        }
    </style>
</head>
<body>
    <h1>Hello {{ name }}!</h1>
    <p class="time">🕒 Current server time is: <strong>{{ time }}</strong></p>

    <div class="input-form">
        <form method="POST">
            <label for="name">Enter your name:</label><br>
            <input type="text" id="name" name="name" placeholder="Your name here" required>
            <input type="submit" value="Greet me!">
        </form>
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        name = request.form.get("name", "World")
    else:
        name = "World"

    # Set to your preferred time zone
    timezone = pytz.timezone("Europe/Dublin")  # Change as needed
    current_time = datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")

    return render_template_string(HTML_TEMPLATE, name=name, time=current_time)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
