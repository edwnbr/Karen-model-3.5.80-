from flask import Flask, request, jsonify, render_template, send_from_directory
import os, json

app = Flask(__name__, static_folder='dashboard', template_folder='dashboard')

STATE_FILE = 'web_state.json'
if not os.path.exists(STATE_FILE):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'chats': []}, f, ensure_ascii=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json or {}
    msg = data.get('message', '')
    # store chat
    s = json.load(open(STATE_FILE, 'r', encoding='utf-8'))
    reply = f"Карен: Я прочитала '{msg}' и подумаю над этим."
    s['chats'].append({'user': msg, 'karen': reply})
    json.dump(s, open(STATE_FILE, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return jsonify({'reply': reply})

@app.route('/dashboard/<path:filename>')
def dash_file(filename):
    return send_from_directory('dashboard', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
