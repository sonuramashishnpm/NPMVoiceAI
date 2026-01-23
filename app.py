from flask import Flask, render_template, request, jsonify
from npmai import Ollama

app = Flask(__name__)

# Initialize LLM
llm = Ollama(
    model="llama3.2",
    temperature=0.8
)

@app.route("/")
def index():
    return render_template("index.html")

# Endpoint to handle AI chat
@app.route("/askAI", methods=["POST"])
def NPMai_ask():
    data = request.get_json()
    prompt = data.get("prompt", "")

    if not prompt.strip():
        return jsonify({"response": "❗ Please provide a question."})

    try:
        result = llm.invoke(prompt)
        response = str(result)
    except Exception as e:
        response = f"❌ Error: {str(e)}"

    return jsonify({"response": response})

if __name__=="__main__":
    app.run(debug=False)



