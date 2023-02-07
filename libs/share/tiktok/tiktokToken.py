import logging
import os

import requests

from options import tmp_dir

logger = logging.getLogger(__name__)


class Token:
    def __init__(self):
        self._refresh_token = ''
        self._access_token = ''

    @property
    def refresh_token(self) -> str:
        self._refresh_token = self.getRefreshToken()

        return self._refresh_token

    # Save refresh token to file
    def saveRefreshToken(self, newRefreshToken):
        self._refresh_token = newRefreshToken

        with open(tmp_dir / 'tiktok_token', 'w') as f:
            f.write(self._refresh_token)
            f.close()

    # Get refresh token
    def getRefreshToken(self) -> str:
        if not os.path.exists(tmp_dir / 'tiktok_token'):
            return os.environ.get('TIKTOK_REFRESH_TOKEN', '')

        with open(tmp_dir / 'tiktok_token', 'r') as f:
            rt = f.read()
            f.close()
            return rt

    # Refresh access token
    @property
    def access_token(self):
        logger.info("Refreshing TikTok access token...")

        res = requests.post('https://open-api.tiktok.com/oauth/refresh_token/',
                            params={
                                'client_key': os.getenv('TIKTOK_CLIENT_KEY'),
                                'grant_type': 'refresh_token',
                                'refresh_token': self.refresh_token
                            })

        # Check if request failed
        if res.json()['data']['error_code'] != 0:
            logger.error(
                f"Request failed with error code {res.json()['data']['error_code']}: {res.json()['data']['description']}")
            exit(1)

        # Save new refresh token
        self.saveRefreshToken(res.json()['data']['refresh_token'])
        self._access_token = res.json()['data']['access_token']

        logger.info("Done refreshing TikTok access token!")

        return self._access_token
