import logging
from pathlib import Path
import time
import sys

from libs.renderer.renderer import genVideoFromPost, concatVideos
from libs.textToImage.textToImage import genImgFromPostUrl
from libs.textToSpeech.textToSpeech import genVoiceover
from libs.apiRequest.request import request

from options import tmp_dir, out_dir, in_dir

start = time.time()

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] - %(message)s")

if len(sys.argv) < 3:
    logging.error("Missing subreddit name and post number!")
    exit(1)

posts = request(sys.argv[1], int(sys.argv[2]))

generatedVideosList = []

for currentPost in posts:
    title, id = genImgFromPostUrl(
        currentPost, Path(tmp_dir) / "overlay.png")

    generatedVideosList.append(str(id + "_final.mp4"))

    genVoiceover(title, Path(tmp_dir) / "voiceover.mp3")

    genVideoFromPost(Path(in_dir) / "input.mp4", Path(tmp_dir) / "overlay.png",
                     Path(tmp_dir) / "voiceover.mp3", Path(out_dir) / str(id + "_final.mp4"))

    end = time.time()

# 2 or more posts -> concat
if int(sys.argv[2]) > 1:
    concatVideos(generatedVideosList, Path(out_dir) /
                 f"r-{sys.argv[1]}_{len(generatedVideosList)}_posts.mp4")

logging.info("Finished in %d seconds.", end - start)
