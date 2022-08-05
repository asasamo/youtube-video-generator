from gtts import gTTS
import logging

logger = logging.getLogger(__name__)


def genVoiceover(text, outFile):
    logger.info("Getting tts for \"%s\"...", text)
    tts = gTTS(text)
    logger.info("Saving file")
    tts.save(outFile)
    logger.info("Done getting voiceover!")


if __name__ == "__main__":
    genVoiceover("test",
                 "../renderer/hello.mp3")
