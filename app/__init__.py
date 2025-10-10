from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    char_count = None

    if request.method == 'POST':
        text = request.form.get('input_text','')
        char_count = len(text)
    
    return render_template('index.html', char_count = char_count)