import logging
import os
from pathlib import Path

import requests

from libs.share.tiktok.tiktokToken import Token

logger = logging.getLogger(__name__)


token = Token()
retry = 0


def upload(videoPath: Path):
    res = requests.post('https://open-api.tiktok.com/share/video/upload/',
                        params={
                            'open_id': os.getenv('TIKTOK_OPEN_ID'),
                            'access_token': token.access_token,
                        },
                        files={'video': (videoPath.name, open(videoPath, 'rb'), 'multipart/form-data')})

    if res.json()['data']['err_code'] != 0:
        logger.error(
            f"Request failed with error code {res.json()['data']['err_code']}: {res.json()['data']['error_msg']}")

        global retry
        retry += 1

        if retry < 3:
            logger.error("Uploading failed! Retrying...")
            upload(videoPath)
            return

        else:
            logger.error("Failed to upload video!")
            exit(1)
