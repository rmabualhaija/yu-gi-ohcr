import logging

from card_ocr import CardOCR
from yugioh_card_db import YugiohCardDB

log = logging.getLogger(__name__)

class CardImageReader:

    def __init__(self):
        pass

    def identify_card(self, card_image_path: str):
        card_db = YugiohCardDB()
        card_reader = CardOCR()

        set_ids = card_reader.get_card_set_ids(card_image_path)

        if len(set_ids) > 1:
            cards = card_db.get_cards_by_set_id(set_ids)
            self.display_card_data(cards)
        
        elif len(set_ids) == 1:
            card = card_db.get_card_by_set_id(set_ids[0])
            self.display_card_data(card)

        else:
            print("Couldn't match card set_id")
            log.info("Couldn't match card set id")
    
    def display_card_data(self, cards: list[tuple[str,dict[str,any]]]):
        for card in cards:
            set_id, card_data  = card
            card_name = card_data['name']
            card_sets = card_data['card_sets']
            for set in card_sets:
                if set['set_code'] == set_id:
                    card_price = set['set_price']
                    card_rarity = set['set_rarity']
                    break

            print(f'Card Name: {card_name}\n'
                  f'Card Rarity: {card_rarity}\n'
                  f'Card Price: {card_price}\n'
                  )

cir = CardImageReader()
cir.identify_card('/Users/rushdawg/Downloads/multi_cards_no_binder.jpeg')