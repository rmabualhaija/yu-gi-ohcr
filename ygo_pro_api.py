import requests
import logging
from PIL import Image
from typing import Any

log = logging.getLogger(__name__)

def get_all_cards() -> list[dict[str, Any]]:
    try:
        log.info("Getting card info from ygoprodeck...")
        response = requests.get('https://db.ygoprodeck.com/api/v7/cardinfo.php')
        data = response.json()['data']

    except Exception as e:
        log.exception(f"Failed to get information from ygoprodeck with exception:\n\n {e}")
    return data

def request_image(image_url: str, file_name: str): 
    print(image_url)
    response = requests.get(image_url, stream=True)
    print(response.status_code)
    response.raw.decode_content = True  
    with open(file_name, 'wb') as f:
        f.write(response.content)