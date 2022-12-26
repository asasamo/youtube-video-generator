import os
import logging
import requests

from options import SPEECH_REGION, VOICE

from classes.post import Post

logger = logging.getLogger(__name__)


def genVoiceover(post: Post):
    logger.info("Getting tts for \"%s\"...", post.title)

    url = f'https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1'

    headers = {'Ocp-Apim-Subscription-Key': os.getenv('SPEECH_KEY'),
               'Content-Type': 'application/ssml+xml',
               'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3',
               'User-Agent': 'curl'}

    data = f"""<speak version='1.0' xml:lang='en-US'><voice xml:lang='en-US' xml:gender='Male'
              name='{VOICE}'>
              {post.title}
              </voice></speak>"""

    r = requests.post(url, headers=headers, data=data)

    with open(post.voiceoverPath, 'wb') as audioOut:
        audioOut.write(r.content)
        audioOut.close()

    logger.info("Done getting voiceover!")
