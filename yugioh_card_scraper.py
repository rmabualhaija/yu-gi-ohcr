import json
import logging
import requests
from typing import Any
from pymongo import MongoClient

from ygo_pro_api import get_all_cards

log = logging.getLogger(__name__)

class YugiohCardScraper:
    def __init__(self):
        self._cards_response = None
        self._cards_collection = None
    
    @property
    def cards_response(self) -> list[dict[str, Any]]:
        if self._cards_response is None:
            self._cards_response = get_all_cards()
        return self._cards_response

    def _save_cards_response_to_file(self, path) -> None:
        log.info(f'Saving cards json response to {path}')
        if self.cards_response is not None:
            with open(path, 'w') as f:
                f.write(json.dumps(self.cards_response))
        
   
        

# scraper = YugiohCardScraper()
# scraper._upload_all_cards_to_mongo()
# scraper._save_cards_response_to_file('all_yugioh_cards.json')
