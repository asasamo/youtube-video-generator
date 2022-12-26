from pathlib import Path

tmp_dir = Path(__file__).parent / "tmp_dir"

out_dir = Path(__file__).parent / "out"

in_dir = Path(__file__).parent / "input"

inputVideo = in_dir / "input.mp4"

tmpVideo = tmp_dir / "blur_overlay_tmp.mp4"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

videoSchedule = 'day'  # day, week, month, year, alltime

# input video already blurred? - not time saving
isVideoAlreadyBlurred = False

SPEECH_REGION = 'northeurope'
VOICE = 'en-US-DavisNeural'
