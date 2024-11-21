from flask import Flask, render_template, request, jsonify
from flask_app import app
import json
with open('questions.json', 'r') as f:
    qa_data = json.load(f)
@app.route('/get-response', methods=['POST'])
def get_response():
    data = request.json
    selected_question = data.get('question')
    # Find the response for the selected question
    response = next((qa['response'] for qa in qa_data if qa['question'] == selected_question), "I don't know the answer to that.")
    return jsonify({"response": response})

