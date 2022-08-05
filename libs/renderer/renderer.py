import logging
import math
from pathlib import Path
from random import randrange
import subprocess

import ffmpeg

from options import tmp_dir, out_dir

logger = logging.getLogger(__name__)

PADDING = 2  # seconds


def getDuration(filename):
    return int(str(ffmpeg.probe(filename)[
        "streams"][0]["duration"]).split(".")[0])


def getDimensions(filename):
    return ffmpeg.probe(filename)["streams"][0]["width"], ffmpeg.probe(filename)["streams"][0]["height"]


def getFramerate(filename):
    fraction = ffmpeg.probe(
        filename)["streams"][0]["avg_frame_rate"].split("/")

    return math.ceil(fraction[0]/fraction[1])


def genVideoFromPost(bgVideo_path: Path, overlayImage_path: Path, audio: Path, output: Path):
    logger.info("Generating video...")

    try:
        video_duration = getDuration(str(bgVideo_path))
        video_width, video_height = getDimensions(str(bgVideo_path))

        overlay_file = ffmpeg.input(str(overlayImage_path))
        overlay_width, overlay_height = getDimensions(str(overlayImage_path))

        audio_duration = getDuration(str(audio)) + PADDING*2
        start = randrange(0 + PADDING, video_duration - audio_duration)

        # centered image coords
        x = int(video_width/2) - int(overlay_width / 2)
        y = int(video_height/2) - int(overlay_height / 2)
        logger.debug("Image coords: %d %d", x, y)

        # overlay image
        logger.info("Current step: blur and overlay")
        out, err = (ffmpeg
                    .input(str(bgVideo_path))
                    .trim(start=start, end=start + audio_duration)
                    .setpts("PTS-STARTPTS")
                    .filter("boxblur", 8)
                    .overlay(overlay_file, x=x, y=y)
                    .output(str(Path(tmp_dir) / "blur_overlay_tmp.mp4"))
                    .overwrite_output()
                    .run(capture_stdout=True, capture_stderr=True)
                    )

        # add audio
        logger.info("Current step: add voiceover")
        tmp = ffmpeg.input(str(Path(tmp_dir) / "blur_overlay_tmp.mp4"))
        out, err = (
            ffmpeg
            .input(str(audio))
            .output(tmp.video, str(output), shortest=None, vcodec='copy')
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        logger.error(e.stderr)
        exit(1)

    logger.info("Done generating video!")


def concatVideos(videoList: list, outVideo_path: Path):
    logger.info("Concatenating %d videos...", len(videoList))
    # videoList = ["wb5tmb_final.mp4", "wf6xdf_final.mp4", "wf6xdf_final.mp4"]
    with open(str(Path(out_dir) / "video_file_list.txt"), 'w') as vfl:
        vfl.write(
            '\n'.join([f'file \'{videoFile}\'' for videoFile in videoList]))

    concatCmd = f"ffmpeg -f concat -i {str(Path(out_dir) / 'video_file_list.txt')} -c copy {str(outVideo_path)}"

    try:
        subprocess.check_call(concatCmd.split(
            " "),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        logger.error(e.output)
        exit(1)

    logger.info("Done concatenating!")


if __name__ == "__main__":
    concatVideos([], "sos")
