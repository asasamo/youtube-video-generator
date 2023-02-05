import logging
from pathlib import Path
import time
import sys
import os
import string
import random

from libs.renderer.renderer import genVideoFromPost, concatVideos, addBackgroundMusic, getDuration
from libs.textToImage.textToImage import getSubIcon, genImgFromPost
from libs.apiRequest.request import requestPosts as api
from libs.textToSpeech.textToSpeech import genVoiceover

from classes.post import Post

from options import tmp_dir, out_dir, in_dir

logger = logging.getLogger(__name__)


def genRandomString(length):
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for _ in range(length))


def clearOldFiles(path: Path):
    logger.info('Clearing temp files.')
    for file in os.listdir(path):
        os.remove(path / file)
    logger.info('Done clearing!')


def generateVideo(subName: str, postNumber: int):
    start = time.time()

    logger.info('Generating new video!')

    clearOldFiles(tmp_dir)

    posts = api(subName, postNumber)
    # sort from shortest to longest title
    posts.sort(key=lambda p: len(p.title))

    subIconUrl = getSubIcon(subName)

    generatedVideosList = []

    for currentPost in posts:
        currentPost: Post

        currentPost.subIconUrl = subIconUrl

        genImgFromPost(currentPost)

        genVoiceover(currentPost)

        if len(posts) == 1:
            genVideoFromPost(currentPost, out_dir /
                             f'{currentPost.id}_final_{genRandomString(6)}.mp4')
            return
        else:
            genVideoFromPost(currentPost, currentPost.videoOutputPath)
            generatedVideosList.append(currentPost.postFilename)

    # 2 or more posts -> concat and add music
    if len(posts) > 1:
        finalVideoFileName = f'r-{subName}_{len(generatedVideosList)}_posts_music_{genRandomString(6)}.mp4'
        concatVideos(generatedVideosList, tmp_dir /
                     f"r-{subName}_{len(generatedVideosList)}_posts.mp4")

        addBackgroundMusic(tmp_dir / f'r-{subName}_{len(generatedVideosList)}_posts.mp4', in_dir / 'bgMusic.mp3', out_dir /
                           finalVideoFileName)

    end = time.time()

    logger.info('Finished in %d seconds.', end - start)

    # video duration, gen time, path
    return (getDuration(out_dir / finalVideoFileName if postNumber != 1 else out_dir / generatedVideosList[0]), int(end - start), out_dir / finalVideoFileName if postNumber != 1 else out_dir / generatedVideosList[0])


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="[%(asctime)s] [%(levelname)s] [%(funcName)s] - %(message)s")

    if len(sys.argv) < 3:
        logger.error(
            "Missing subreddit name and post number!\nUsage python main.py <subreddit> <post number>")
        exit(1)

    generateVideo(sys.argv[1], int(sys.argv[2]))
