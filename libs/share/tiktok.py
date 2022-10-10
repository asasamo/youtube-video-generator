# NOT TESTED

from pathlib import Path
import requests
import logging
import os

logger = logging.getLogger(__name__)


def uploadToTikTok(videoPath: Path):
    logger.info(
        f"Uploading video [ {videoPath.name} - {round(float(os.path.getsize(videoPath) / 1024 / 1024), 2)}MB ] to TikTok...")

    res = requests.post('https://open-api.tiktok.com/share/video/upload/',
                        params={
                            'open_id': os.getenv('TIKTOK_OPEN_ID'),
                            'access_token': os.getenv('TIKTOK_ACCESS_TOKEN')
                        },
                        files={'file': (videoPath.name, open(videoPath, 'rb'), 'multipart/form-data')})

    if res.json()['data']['error_code'] != 0:
        logger.info(
            f"Request failed with error code {res.json()['data']['error_code']}: {res.json()['data']['error_msg']}")

    logger.info("Done uploading video!")


if __name__ == '__main__':
    uploadToTikTok(Path(
        '/home/elia/Projects/youtube-commentary/out/r-showerthoughts_2_posts_music_dnesig.mp4'))
