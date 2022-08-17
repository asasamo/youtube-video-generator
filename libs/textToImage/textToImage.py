import re
import json
import imgkit
import requests
from pathlib import Path
from options import headers

import logging

logger = logging.getLogger(__name__)

ABOUT_SUB = "https://reddit.com/r/%%sub%%/about.json"


def loadJsonFromFile(filename):
    with open(filename, "r") as f:
        content = f.read()
        f.close()
        return json.loads(content)


def getSubIcon(subName):
    logger.info("Getting sub icon...")
    r = requests.get(
        f'https://reddit.com/r/{subName.strip().lower()}/about.json', headers=headers)
    if r.status_code != 200:
        logger.error("Error getting sub icon!")
        exit(1)

    jsonResponse = json.loads(r.text)

    logger.info("Done!")
    return jsonResponse["data"]["icon_img"] if jsonResponse["data"]["icon_img"] != '' else str(jsonResponse['data']['community_icon']).split('?')[0]


def getPostTitle(postUrl):
    logger.info("Getting post title...")
    r = requests.get(postUrl + ".json", headers=headers)
    if r.status_code != 200:
        logger.error("Error getting post title!")
        exit(1)

    jsonResponse = json.loads(r.text)

    # jsonResponse = loadJsonFromFile("postResponse.json")
    logger.info("Done!")
    return (jsonResponse[0]["data"]["children"][0]["data"]["title"], jsonResponse[0]["data"]["children"][0]["data"]["id"])


def generateHTML(subName, subIconURL, postTitle):
    logger.info("Generating HTML...")
    # load base HTML file
    baseHTML = ""
    with open(Path(__file__).parent / "base.html", "r") as f:
        baseHTML = f.read()
        f.close()

    # replace contents
    baseHTML = baseHTML.replace("%%subIcon%%", subIconURL)
    baseHTML = baseHTML.replace("%%subName%%", subName)
    baseHTML = baseHTML.replace("%%title%%", postTitle)

    logger.info("Done!")
    return baseHTML


def genImgFromPostUrl(postUrl: str, outPath: Path):
    logger.info("Generating overlay image from post...")

    subName = re.search(
        r"https:\/\/www.reddit.com\/r\/([\w\d]+)\/.+", postUrl).group(1)

    subIconURL = getSubIcon(subName=subName)

    postTitle, postId = getPostTitle(postUrl)

    imgkit.from_string(generateHTML(subName, subIconURL,
                       postTitle), outPath, options={'crop-w': '850', 'log-level': 'none'})

    logger.info("Done generating overlay image!")
    return (postTitle, postId)


def genImgFromPost(post: dict, outPath: Path):
    logger.info("Generating overlay image from post...")

    # needs wkhtmltoimage 0.12.6 (with patched qt)
    imgkit.from_string(generateHTML(post['subName'], post['subIconUrl'],
                       post['title']), outPath, options={'log-level': 'none', 'transparent': ''})

    logger.info("Done generating overlay image!")
    return


if __name__ == "__main__":
    imgkit.from_string(generateHTML("r/sos", "",
                       "TITLE TITLE TITLE TITLE TITLE TITLE TITLE TITLE TITLE TITLE TITLE TITLE "), "out.png",
                       options={'log-level': 'none', 'transparent': ''})
