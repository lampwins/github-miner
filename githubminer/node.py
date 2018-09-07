import logging

import requests

from minemeld.ft.basepoller import BasePollerFT

LOG = logging.getLogger(__name__)


class Miner(BasePollerFT):
    def configure(self):
        super(Miner, self).configure()

        self.polling_timeout = self.config.get('polling_timeout', 20)
        self.verify_cert = self.config.get('verify_cert', True)

        self.type = self.config.get('type', None)
        if self.type is None:
            raise ValueError('%s - type' % self.name)
        self.url = 'https://api.github.com/meta'

    def _build_iterator(self, item):
        # builds the request and retrieves the page
        headers = {
            'Accept': "application/json"
        }

        r = requests.get(
            self.url,
            headers=headers,
        )

        result = r.json()
        result = result.get(self.type)
        if result is None:
            LOG.error('%s - not found in the response', self.name)

        return result

    def _process_item(self, item):
        value = {
            'type': 'IPv4',
            'confidence': 100
        }

        return [[item, value]]
