from flask import Flask, render_template_string, request
from datetime import datetime

app = Flask(__name__)

# Simple HTML template with dynamic content
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Hello World App</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 20px; }
        h1 { color: #333; }
        .time { color: #666; font-style: italic; }
        .input-form { margin-top: 20px; }
        input[type="text"] { padding: 8px; width: 250px; }
        input[type="submit"] { padding: 8px 15px; }
    </style>
</head>
<body>
    <h1>Hello {{ name }}!</h1>
    <p class="time">Current server time is: {{ time }}</p>

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

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        name = request.form.get('name', 'World')
    else:
        name = 'World'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(HTML_TEMPLATE, name=name, time=current_time)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

