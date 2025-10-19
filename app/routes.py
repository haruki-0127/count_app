from flask import render_template, request
from app import app
import re

@app.route('/', methods=['GET', 'POST'])
def index():
    data = None
    text_formatted = None
    warning_message = None

    if request.method == 'POST':               #　フォームが送信された場合に実行
        if 'text_for_count' in request.form:  #　文字数カウントのフォームが送信された場合
            text = request.form.get('text_for_count','')
            data = {                         #　文章全体と各文字種ごとにカウント
                'whole_length': len(text),
                'no_space_length': len(re.sub(r'\s+', '', text)),
                'hiragana': len(re.findall(r'[\u3040-\u309F]', text)),
                'katakana': len(re.findall(r'[\u30A0-\u30FF]', text)),
                'kanji': len(re.findall(r'[\u4E00-\u9FFF]', text)),
                'half_alpha': len(re.findall(r'[A-Za-z]', text)),
                'full_alpha': len(re.findall(r'[\uFF21-\uFF3A\uFF41-\uFF5A]', text)),
                'half_num': len(re.findall(r'[0-9]', text)),
                'full_num': len(re.findall(r'[\uff10-\uff19]', text)),
                'space': len(re.findall(r'\s', text)),
                'word_count': len(re.findall(r"\b[\w']+\b", text))
            }
        
            data['other'] = len(text) - sum(list(data.values())[2:10])

        
        elif 'text_for_format' in request.form:      #　文章編集のフォームが送信された場合
            selected = request.form.get('selected_item')
            text = request.form.get('text_for_format', '')

            if selected == 'remove':                 #　指定文字削除
                char_remove = request.form.get('char_for_remove', '')
                text_formatted = text.replace(char_remove, '')
            
            elif selected == 'exchange':            #　指定文字置換
                char_before = request.form.get('char_before', '')
                char_after = request.form.get('char_after', '')
                
                if char_before:
                    text_formatted = text.replace(char_before, char_after)
                else:
                    text_formatted = text
            
            elif selected == 'bullet_points':          #　区切り文字で箇条書き化
                separator = request.form.get('separator', '')
                text_formatted = '\n'.join('・' + bullet_point for bullet_point in text.split(f'{separator}') if bullet_point)
            
            elif selected == 'remove_brank_line':        # 空行削除
                text_formatted = re.sub(r'^\s*$\n', '', text, flags=re.MULTILINE)
            
            else:
                warning_message = 'チェックを入れてください'    #　未選択時の警告
                
    return render_template('index.html', data=data, text_formatted=text_formatted, warning_message=warning_message)