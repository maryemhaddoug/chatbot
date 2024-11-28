# application.py
import os
from flask import Flask, render_template, request, jsonify
import openai

# Configurer l'application Flask
app = Flask(__name__)

# Configurer la clé API OpenAI
openai.api_key = "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"

# Initialiser l'historique des conversations
conversation_history = [{"role": "system", "content": "Tu es un assistant qui répond poliment."}]

@app.route("/")
def maison():
    return render_template("index.html")

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    user_input = data.get("message", "")

    # Ajouter le message de l'utilisateur à l'historique des conversations
    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history,
            temperature=1,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        bot_response = response['choices'][0]['message']['content']

        # Ajouter la réponse du bot à l'historique de la conversation
        conversation_history.append({"role": "assistant", "content": bot_response})

        return jsonify({"response": bot_response})
    except Exception as e:
        print(f"Erreur : {e}")
        return jsonify({"response": "Désolé, une erreur s'est produite lors du traitement de votre demande."})

if __name__ == "__main__":
    app.run(debug=True)
