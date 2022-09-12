from pathlib import Path
from options import tmp_dir


class Post:

    postFilename = ''
    overlayPath = tmp_dir / "overlay.png"
    voiceoverPath = tmp_dir / "voiceover.mp3"
    videoOutputPath = Path()

    def __init__(self, id: str, title: str, link: str, subName: str, subIconUrl: str = '') -> None:
        self.id = id
        self.title = title
        self.link = link if link[len(
            link) - 1] != '/' else link[:len(link) - 2]
        self.subName = subName
        self.subIconUrl = subIconUrl

        self.videoOutputPath = self.getVideoOutputPath()
        self.postFilename = self.getFilename()

    def getFilename(self) -> str:
        return f'{self.id}_post.mp4'

    def getVideoOutputPath(self) -> Path:
        return tmp_dir / self.getFilename()
