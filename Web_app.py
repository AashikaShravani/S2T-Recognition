from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__, static_url_path='/static')
recognizer = sr.Recognizer()

# Route for the home page (index.html)
@app.route('/')
def index():
    return render_template('speech-to-text.html')

@app.route('/recognize-microphone', methods=['POST'])
def recognize_microphone():
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
            recorded_audio = recognizer.listen(source, timeout=4)
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        return jsonify({'text': text})
    except Exception as ex:
        return jsonify({'error': str(ex)})

@app.route('/recognize-audio-file', methods=['POST'])
def recognize_audio_file():
    try:
        with sr.AudioFile("./sample_audio/speech.wav") as source:
            recorded_audio = recognizer.listen(source)
        text = recognizer.recognize_google(recorded_audio, language="en-US")
        return jsonify({'text': text})
    except Exception as ex:
        return jsonify({'error': str(ex)})

if __name__ == '__main__':
    app.run(debug=True)
