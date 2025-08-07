from flask import Flask, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.json
    input_text = data.get("input")
    source_lang = data.get("source", "en")
    target_lang = data.get("target", "ar")

    try:
        translated = translator.translate(input_text, src=source_lang, dest=target_lang)
        return jsonify({
            "status": "success",
            "translated_text": translated.text
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5002)
