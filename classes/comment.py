class Comment:

    def __init__(self, id: str, author: str, body: str, link: str, subName: str) -> None:
        self.id = id
        self.author = author
        self.body = body
        self.link = link if link[len(
            link) - 1] != '/' else link[:len(link) - 2]
        self.subName = subName
