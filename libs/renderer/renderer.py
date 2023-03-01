import logging
import math
import subprocess
from pathlib import Path
from random import randrange

import ffmpeg
from options import inputVideo, isVideoAlreadyBlurred, tmp_dir, tmpVideo
from classes.post import Post

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


def genVideoFromPost(post: Post, outPath: Path):
    logger.info("Generating video...")

    try:
        video_duration = getDuration(str(inputVideo))
        video_width, video_height = getDimensions(str(inputVideo))

        overlay_file = ffmpeg.input(str(post.overlayPath))
        overlay_width, overlay_height = getDimensions(str(post.overlayPath))

        audio_duration = getDuration(str(post.voiceoverPath)) + PADDING*2
        start = randrange(0 + PADDING, video_duration - audio_duration)

        # centered image coords
        x = int(video_width / 2) - int(overlay_width / 2)
        y = int(video_height / 2) - int(overlay_height / 2)
        logger.debug("Image coords: %d %d", x, y)

        # hwaccel
        # sudo ffmpeg -vaapi_device /dev/dri/renderD128 -i input.mp4 -vf 'format=nv12,hwupload' -c:v hevc_vaapi -f mp4 -rc_mode 1 -qp 25 output.mp4
        # overlay image
        if not isVideoAlreadyBlurred:
            logger.info("Current step: blur and overlay")
            out, err = (ffmpeg
                        .input(str(inputVideo))
                        .trim(start=start, end=start + audio_duration)
                        .setpts("PTS-STARTPTS")
                        .filter("boxblur", 10)
                        .overlay(overlay_file, x=x, y=y)
                        .output(str(tmpVideo))
                        .overwrite_output()
                        .run(capture_stdout=True, capture_stderr=True)
                        )
        else:
            logger.info("Current step: overlay")
            out, err = (ffmpeg
                        .input(str(inputVideo))
                        .trim(start=start, end=start + audio_duration)
                        .setpts("PTS-STARTPTS")
                        .overlay(overlay_file, x=x, y=y)
                        .output(str(tmpVideo))
                        .overwrite_output()
                        .run(capture_stdout=True, capture_stderr=True)
                        )

        # add audio
        logger.info("Current step: add voiceover")
        tmp = ffmpeg.input(str(tmpVideo))
        out, err = (
            ffmpeg
            .input(str(post.voiceoverPath))
            .output(tmp.video, str(outPath), shortest=None, vcodec='copy')
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
    with open(str(tmp_dir / "video_file_list.txt"), 'w') as vfl:
        vfl.write(
            '\n'.join([f'file \'{videoFile}\'' for videoFile in videoList]))

    concatCmd = f"ffmpeg -f concat -i {str(tmp_dir / 'video_file_list.txt')} -c copy -y {str(outVideo_path)}"

    try:
        subprocess.check_call(concatCmd.split(
            " "),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        logger.error(e)
        exit(1)

    logger.info("Done concatenating!")


def addBackgroundMusic(inputVideo_path: Path, bgMusic_path: Path, outVideo_path: Path):
    logger.info("Adding background music to video...")

    bgCmd = f"ffmpeg -i {str(inputVideo_path)} -stream_loop -1 -i {str(bgMusic_path)} -c:v copy -filter_complex [0:a]aformat=fltp:44100:stereo,apad[0a];[1]aformat=fltp:44100:stereo,volume=0.1[1a];[0a][1a]amerge[a] -map 0:v -map [a] -ac 2 -shortest -y {str(outVideo_path)}"

    try:
        subprocess.check_call(bgCmd.split(
            " "),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        logger.error(e)
        exit(1)

    logger.info("Done adding music!")


if __name__ == "__main__":
    concatVideos([], "sos")
