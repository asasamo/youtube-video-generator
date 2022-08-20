from pathlib import Path

tmp_dir = Path(__file__).parent / "tmp_dir"

out_dir = Path(__file__).parent / "out"

in_dir = Path(__file__).parent / "input"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

# input video already blurred? - not time saving
isVideoAlreadyBlurred = False
