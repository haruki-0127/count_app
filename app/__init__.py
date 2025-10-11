from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None

    if request.method == 'POST':
        text = request.form.get('input_text','')
        
        data = {
            'whole_length': len(text),
            'no_space_length': len(re.sub(r'\s+', '', text)),
            'hiragana': len(re.findall(r'[\u3040-\u309F]', text)),
            'katakana': len(re.findall(r'[\u30A0-\u30FF]', text)),
            'kanji': len(re.findall(r'[\u4E00-\u9FFF]', text)),
            'half_alpha': len(re.findall(r'[A-Za-z]', text)),
            'full_alpha': len(re.findall(r'[\uFF21-\uFF3A\uFF41-\uFF5A]', text)),
            'half_num': len(re.findall(r'[0-9]', text)),
            'full_num': len(re.findall(r'[\uff10-\uff19]', text)),
            'space': len(re.findall(r'\s+', text))
        }

        data['other'] = len(text) - sum(list(data.values())[2:])

        data = {k: f'{str(v):>5}' for k, v in data.items()}
    
    return render_template('index.html', data=data)