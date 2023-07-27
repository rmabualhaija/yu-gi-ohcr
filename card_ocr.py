import requests
import json
import re

from google.cloud import vision

class CardOCR:
    def __init__(self):
        pass

    def _detect_text(self, path):
        """Detects text in the file."""

        client = vision.ImageAnnotatorClient()

        with open(path, "rb") as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        text_pieces = []
        for text in texts:
            text_pieces.append(text.description)

        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
            )
            return []
        return text_pieces

    def _get_set_ids(self, text_pieces:  list[str]) -> str:
        pattern = re.compile("^[a-zA-Z0-9]{4}-[a-zA-Z0-9]{5}$")
        with open('temp_ocr_text.txt', 'w') as f:
            f.writelines(text_pieces)
        matches = []
        with open('temp_ocr_text.txt', 'r') as f:
            lines = f.readlines()
            for text_piece in lines:
                print(text_piece)
                match = pattern.match(text_piece.strip()+'\n')
                print(match)
                if match:
                    matches.append(match.string.strip())
            return matches
    
    def get_card_set_ids(self, path):
        text_pieces = self._detect_text(path)
        set_ids = self._get_set_ids(text_pieces)
        return set_ids

