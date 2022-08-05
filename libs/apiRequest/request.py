import requests
import logging

logger = logging.getLogger(__name__)


def request(subName, n):
    logger.info("Getting %d posts from r/%s...", n, subName)

    i = 0  # to define the number of links

    # url builder
    subName.strip()  # remove spaces
    subName.lower()

    url = f"https://www.reddit.com/r/{subName}/top.json?t=week"

    # request
    response = requests.get(url, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'})
    response.json()  # raw api return

    ret = []  # return

    for post in response.json()['data']['children']:  # json filter
        ret.append('https://www.reddit.com' + post['data']['permalink'])

        # index utilized to avoid installing numpy
        i += 1
        if (i >= n):
            break

    logger.info("Done getting posts!")
    return ret[0:n]  # return array with the link reddit of the posts


if __name__ == "__main__":
    #request("subreddit name", "number of links returned")
    print(request("Showerthoughts", 3))
