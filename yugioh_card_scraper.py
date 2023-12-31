import json
import logging
import requests
from typing import Any
from pymongo import MongoClient


from ygo_pro_api import get_all_cards, request_image
from yugioh_card_db import YugiohCardDB

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
    
    def _save_card_images_to_file(self) -> None:
        yugioh_db = YugiohCardDB()
        cards = yugioh_db.get_all_cards()
        total = len(cards)
        counter = 0 
        for card in cards:
            image_links = card['card_images']
            card_id = card['id']
            for image_link in image_links:
                file_name = f"card_images/{card_id}.jpg"
                request_image(image_link['image_url'], file_name)

            counter += 1
            print(f'Finished Downloading image: {counter}/{total}')

# cdb = YugiohCardDB()        
scraper = YugiohCardScraper()
# cdb._upload_all_cards_to_mongo(scraper.cards_response)
# scraper._save_cards_response_to_file('all_yugioh_cards.json')
scraper._save_card_images_to_file()
