from flask import Flask, request, jsonify
from chatbot import chatbot_response

app = Flask(__name__)

# Knowledge base (modules)
knowledge = """
Modules:
- Yoga Pose AI: Real-time yoga pose detection and correction
- Sleep Tracker: Feedback on sleep quality
- Diet Tracker: Diet analysis and improvement suggestions
- Nutrition Guide: Personalized diet plan
- Meditation: Meditate with music
"""

@app.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for the wellness chatbot.
    Expects JSON: { "message": "user input here" }
    """
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Invalid request. Provide 'message' field."}), 400

    user_input = data["message"]
    response = chatbot_response(user_input, knowledge)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
