from flask import Flask, render_template_string, request, jsonify
from deep_translator import GoogleTranslator
import speech_recognition as sr

app = Flask(__name__)

# Define Indian languages (with full names and their language codes)
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Tamil": "ta",
    "Telugu": "te",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa"
}

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ARMY PUBLIC SCHOOL AGRA - Speech Translation App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #120052;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .title {
            text-align: center;
            background-color: red;
            padding: 20px;
            border-radius: 10px;
            color: #FFD700;
            font-size: 50px;
            font-weight: bold;
            width: 80%;
            box-sizing: border-box;
            margin-top: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 28px;
            color: #fff;
            margin: 20px 0;
            font-weight: bold;
            border-bottom: 3px solid #fff;
            padding-bottom: 10px;
            width: 80%;
        }
        .container {
            background-color: #7B68EE;
            padding: 20px;
            border-radius: 10px;
            width: 80%;
            max-width: 600px;
            box-shadow: 0 0 10px rgba(255,255,255,0.1);
        }
        select, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: none;
            font-size: 16px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        .output-box {
            background-color: #f0f0f0;
            padding: 20px;
            border-radius: 10px;
            border: 2px solid #ccc;
            margin-top: 20px;
            word-wrap: break-word;
        }
        #status {
            color: white;
            margin-top: 10px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="title">ARMY PUBLIC SCHOOL AGRA</div>
    <div class="subtitle">Speech Translation App</div>
    <div class="container">
        <select id="source_language">
            {% for language, code in languages.items() %}
                <option value="{{ code }}">{{ language }}</option>
            {% endfor %}
        </select>
        <select id="target_language">
            {% for language, code in languages.items() %}
                <option value="{{ code }}">{{ language }}</option>
            {% endfor %}
        </select>
        <button onclick="startListening()">Start Listening</button>
        <div id="status"></div>
        <div id="transcription" class="output-box" style="display: none;"></div>
        <div id="translation" class="output-box" style="display: none;"></div>
    </div>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        function startListening() {
            $('#status').text('Listening... Please speak.');
            $.ajax({
                url: '/translate',
                type: 'POST',
                data: {
                    source_language: $('#source_language').val(),
                    target_language: $('#target_language').val()
                },
                success: function(response) {
                    $('#status').text('');
                    if (response.error) {
                        alert(response.error);
                    } else {
                        $('#transcription').text('Transcription: ' + response.transcription).show();
                        $('#translation').text('Translation: ' + response.translation).show();
                    }
                },
                error: function() {
                    $('#status').text('');
                    alert('An error occurred while processing your request.');
                }
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(html_template, languages=languages)

@app.route('/translate', methods=['POST'])
def translate():
    recognizer = sr.Recognizer()
    source_language = request.form.get('source_language')
    target_language = request.form.get('target_language')

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        spoken_text = recognizer.recognize_google(audio, language=source_language)
        translated_text = GoogleTranslator(source=source_language, target=target_language).translate(spoken_text)
        return jsonify({'transcription': spoken_text, 'translation': translated_text})
    except sr.UnknownValueError:
        return jsonify({'error': "Sorry, I couldn't understand the audio."})
    except sr.RequestError as e:
        return jsonify({'error': f"Could not request results from Google Speech Recognition service; {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)