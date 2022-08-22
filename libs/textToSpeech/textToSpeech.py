from gtts import gTTS
import logging

from post import Post

logger = logging.getLogger(__name__)


def genVoiceover(post: Post):
    logger.info("Getting tts for \"%s\"...", post.title)
    tts = gTTS(post.title)
    logger.info("Saving file")
    tts.save(post.voiceoverPath)
    logger.info("Done getting voiceover!")
