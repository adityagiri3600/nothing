from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")

app = Flask(__name__, static_folder='', static_url_path='')
CORS(app)

@app.route('/')
def serve_react():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.json.get('prompt', '')
    previous_page = request.json.get('page', '')
    page_history = request.json.get('pageHistory', '')
    print(previous_page)
    if not prompt:
        return jsonify({"error": "prompt is required"})
    system = "youre an ai that gives html code for user prompt, do not give anything else. output in plain text and not in code block. do not use html,body,head and title tag"
    system += "page history: \n"
    for i in range(len(page_history)):
        system += f'{i+1}. prompt: {page_history[i]["prompt"]}, output: {page_history[i]["page"]}\n'
    system += "prompt: "+prompt
    page = model.generate_content(system).text
    if page[0] == "`":
        page = "\n".join(page.split("\n")[1:-2])
    print("prompt: "+prompt + "\n\noutput: "+page)
    return jsonify({"page": page})

if __name__ == '__main__':
    app.run(debug=True)
