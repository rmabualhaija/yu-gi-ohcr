import requests
import logging
from typing import Any

log = logging.getLogger(__name__)

def _remove_unecessary_keys(data) -> list[dict[str, Any]]:
    """
    Remove the card images field (and any other future fields that are necessary)
    """
    for card in data:
        del card['card_images']
    return data


def get_all_cards() -> list[dict[str, Any]]:
    try:
        log.info("Getting card info from ygoprodeck...")
        response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
        data = response.json()['data']
        data = _remove_unecessary_keys(data)

    except Exception as e:
        log.exception(f"Failed to get information from ygoprodeck with exception:\n\n {e}")
    return data
