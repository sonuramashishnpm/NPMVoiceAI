from flask import Flask, render_template, request, jsonify, session
from npmai import Ollama
import json
import os
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "48a35791177f22fba22b2cd08ad4436c1c4a1587b289ae9a75419280b934b7de")

# Initialize LLM
llm = Ollama(
    model="llama3.2", 
    temperature=0.3
)

class Memory:
    def __init__(self, user_id):
        self.filename = f"memory_{user_id}.json"

    def save_context(self, user_input, ai_output):
        with open(self.filename, "a") as data:
            json.dump({"Human": user_input, "AI": ai_output}, data)
            data.write("\n")

    def load_memory_variables(self):
        string_history = ""
        if os.path.exists(self.filename) and os.path.getsize(self.filename) > 0:
            with open(self.filename, "r") as data:
                for line in data:
                    try:
                        ldata = json.loads(line)
                        string_history += f"Human: {ldata['Human']}\nAI: {ldata['AI']}\n"
                    except json.JSONDecodeError:
                        continue
        return string_history

@app.route("/")
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template("index.html")

@app.route("/askAI", methods=["POST"])
def NPMai_ask():
    user_id = session.get('user_id', str(uuid.uuid4()))
    memory = Memory(user_id)
    
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt.strip():
        return jsonify({"response": "❗ Please provide a question."})

    try:
        history = memory.load_memory_variables()
        full_prompt = f"Context history:\n{history}\nHuman: {prompt}\nAI:"
        
        result = llm.invoke(full_prompt)
        response = str(result)
        
        memory.save_context(prompt, response)
        
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"response": f"❌ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
