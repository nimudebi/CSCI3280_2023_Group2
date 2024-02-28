# `pip3 install assemblyai` (macOS)
# `pip install assemblyai` (Windows)

import assemblyai as aai


def speech_to_text(file):
    aai.settings.api_key = "0e6b8b15c65e49afbb439469bb6da09a"
    transcriber = aai.Transcriber()

    transcript = transcriber.transcribe(file).text

    return transcript
