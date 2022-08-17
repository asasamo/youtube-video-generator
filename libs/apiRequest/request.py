import requests
import logging

from options import headers

logger = logging.getLogger(__name__)


def request(subName: str, n: int):
    logger.info('Getting %d posts from r/%s...', n, subName)

    # url builder
    url = f'https://www.reddit.com/r/{subName.strip().lower()}/top.json?t=week'

    # request
    response = requests.get(url, headers=headers)

    ret = []  # return

    for post in response.json()['data']['children'][0:n]:  # json filter
        # ret.append('https://www.reddit.com' + post['data']['permalink']) # old
        ret.append({
            'title': post['data']['title'],
            'id': post['data']['id'],
            'link': 'https://www.reddit.com' + post['data']['permalink'],
            'subName': post['data']['subreddit_name_prefixed']
        })

    logger.info('Done getting posts!')
    return ret  # return array with posts


if __name__ == '__main__':
    #request('subreddit name', 'number of links returned')
    print(request('Showerthoughts', 3))
