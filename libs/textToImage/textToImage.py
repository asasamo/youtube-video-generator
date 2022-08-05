import re
import json
import imgkit
import requests
from pathlib import Path

import logging

logger = logging.getLogger(__name__)

ABOUT_SUB = "https://reddit.com/r/%%sub%%/about.json"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}


def loadJsonFromFile(filename):
    with open(filename, "r") as f:
        content = f.read()
        f.close()
        return json.loads(content)


def getSubIcon(subName):
    logger.info("Getting sub icon...")
    r = requests.get(ABOUT_SUB.replace("%%sub%%", subName), headers=headers)
    if r.status_code != 200:
        logger.error("Error getting sub icon!")
        exit(1)

    jsonResponse = json.loads(r.text)

    # jsonResponse = loadJsonFromFile("aboutResponse.json")
    logger.info("Done!")
    return jsonResponse["data"]["header_img"]


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


def genImgFromPostUrl(postUrl, outPath):
    logger.info("Generating overlay image from post...")

    subName = re.search(
        r"https:\/\/www.reddit.com\/r\/([\w\d]+)\/.+", postUrl).group(1)

    subIconURL = getSubIcon(subName=subName)

    postTitle, postId = getPostTitle(postUrl)

    imgkit.from_string(generateHTML(subName, subIconURL,
                       postTitle), outPath, options={'crop-w': '700', 'log-level': 'none'})

    logger.info("Done generating overlay image!")
    return (postTitle, postId)


if __name__ == "__main__":
    genImgFromPostUrl(
        "https://www.reddit.com/r/Showerthoughts/comments/vj154x/with_no_advertising_antismoking_campaigns_etc_the/", 'out.png')
