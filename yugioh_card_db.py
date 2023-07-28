from typing import Any
import logging
from pymongo import MongoClient

log = logging.getLogger(__name__)

class YugiohCardDB:
    def __init__(self):
        self._cards_collection = None
    
    @property
    def cards_collection(self) -> MongoClient:
        if self._cards_collection is None: 
            try:
                client = MongoClient("localhost", 27017)
                self._cards_collection = client.cards.all_cards
            except Exception as e:
                log.exception(f"Connection issue: {e}")

        return self._cards_collection

    def _upload_all_cards_to_mongo(self, cards) -> None:
        self.cards_collection.insert_many(cards)
    
    def update_card_sets_and_prices(self):
        for card in self.cards_collection:
            card_id = card['id']
            update = {'card_prices': {'$set': card['card_prices']},
                      'card_sets': {'$set': card['card_sets']}
                      }
            self.cards_collection.update(filter={card_id}, update=update)
    
    def get_card_by_set_id(self, set_id: str):
        print(f'looking for card with set_id : {set_id}')
        return (set_id, self.cards_collection.find_one(filter={"card_sets.set_code":set_id}))
    
    def get_cards_by_set_id(self, set_ids: list[str]):
         print(f'looking for cards with set_ids: {set_ids}')
         results = []
         for set_id in set_ids:
            card = self.cards_collection.find_one(filter={"card_sets.set_code":set_id})
            if card is None: 
                print(f"Couldn't find card for card with set id: {set_id}, attempting to resolve card with name")
                cards = self.cards_collection.find(filter={"$text":{ "$search":set_id}})
                match_counter = 0
                for card in cards:
                    match_counter += 1
                    print(card['name'])
                print(match_counter)
                
            results.append((set_id, card))
         return results
    
    def get_all_cards(self) -> list[dict[str, Any]]:
        cards = []
        results = self.cards_collection.find(limit=0)
        for doc in results:
            cards.append(doc)
        return cards
