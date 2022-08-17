import logging
from pathlib import Path
import time
import sys

from libs.renderer.renderer import genVideoFromPost, concatVideos, addBackgroundMusic
from libs.textToImage.textToImage import genImgFromPost, getSubIcon
from libs.textToSpeech.textToSpeech import genVoiceover
from libs.apiRequest.request import request as api

from options import tmp_dir, out_dir, in_dir

start = time.time()

logging.basicConfig(level=logging.INFO,
                    format="[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s] - %(message)s")

if len(sys.argv) < 3:
    logging.error(
        "Missing subreddit name and post number!\nUsage python main.py <subreddit> <post number>")
    exit(1)

posts = api(sys.argv[1], int(sys.argv[2]))
subIconUrl = getSubIcon(sys.argv[1])

generatedVideosList = []

for currentPost in posts:
    currentPost['subIconUrl'] = subIconUrl

    genImgFromPost(currentPost, tmp_dir / "overlay.png")

    genVoiceover(currentPost['title'], tmp_dir / "voiceover.mp3")

    genVideoFromPost(in_dir / "input.mp4", tmp_dir / "overlay.png",
                     tmp_dir / "voiceover.mp3", tmp_dir / str(currentPost['id'] + "_final.mp4"))

    generatedVideosList.append(str(currentPost['id'] + "_final.mp4"))

    end = time.time()

# 2 or more posts -> concat and add music
if int(sys.argv[2]) > 1:
    concatVideos(generatedVideosList, tmp_dir /
                 f"r-{sys.argv[1]}_{len(generatedVideosList)}_posts.mp4")

    addBackgroundMusic(tmp_dir / f"r-{sys.argv[1]}_{len(generatedVideosList)}_posts.mp4", in_dir / "bgMusic.mp3", out_dir /
                       f"r-{sys.argv[1]}_{len(generatedVideosList)}_posts_music.mp4")

logging.info("Finished in %d seconds.", end - start)
