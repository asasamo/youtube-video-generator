from options import headers, videoSchedule
import requests
import logging

from classes.post import Post
from classes.comment import Comment


logger = logging.getLogger(__name__)


def requestPosts(subName: str, n: int) -> tuple:
    logger.info('Getting %d posts from r/%s...', n, subName)

    # url builder
    url = f'https://www.reddit.com/r/{subName.strip().lower()}/top.json?t={videoSchedule}'

    # request
    response = requests.get(url, headers=headers)

    ret = []  # return

    for post in response.json()['data']['children'][0:n]:  # json filter

        ret.append(Post(post['data']['id'], post['data']['title'], 'https://www.reddit.com' +
                   post['data']['permalink'], post['data']['subreddit_name_prefixed']))

    logger.info('Done getting posts!')
    return ret  # return array with posts


def requestComments(post: Post, n: int, sort: str = 'top') -> list:
    logger.info('Getting %d comments from post %s...', n, post.id)

    # url builder
    url = f'https://www.reddit.com/{post.link}.json?sort={sort}'

    # request
    response = requests.get(url, headers=headers)

    ret = []  # return

    # filter comments from moderators
    for comment in list(filter(lambda c: c['data']['distinguished'] != 'moderator', response.json()[1]['data']['children']))[0:n]:

        ret.append(Comment(comment['data']['id'], comment['data']['author'], comment['data']['body'], 'https://www.reddit.com' +
                   comment['data']['permalink'], comment['data']['subreddit_name_prefixed']))

    logger.info('Done getting comments!')
    return ret  # return array with posts


if __name__ == '__main__':
    #request('subreddit name', 'number of links returned')
    pass
