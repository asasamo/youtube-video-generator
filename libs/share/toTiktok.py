import logging
import os
from pathlib import Path

from tiktok.upload import upload

logger = logging.getLogger(__name__)


def toTiktok(videoPath: Path):
    logger.info(
        f"Uploading video [ {videoPath.name} - {round(float(os.path.getsize(videoPath) / 1024 / 1024), 2)}MB ] to TikTok...")

    upload(videoPath)

    logger.info("Done uploading video!")
