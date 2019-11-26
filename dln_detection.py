import pytesseract
import re

TESSERACT_CONFIG = '-l eng --oem 1 --psm 7'

# In alphabetical order by state, not by abbreviation
STATE_FORMATS = {
    'AL': r'\b(\d{7,8})\b',
    'AK': r'\b(\d{7})\b',
    'AZ': r'\b([ADBY]\d{8}|\d{9})\b',
    'AR': r'\b(\d{9})\b',
    'CA': r'\b([A-Z]\d{7})\b',
    'CO': r'\b(\d{9}|[A-Z]\d{6})\b',
    'CT': r'\b(\d{9})\b',
    'DE': r'\b(\d{7,8})\b',
    'DC': r'\b(\d{7}|\d{9})\b',
    'FL': r'\b([A-Z]\d{1,12})\b',  # TODO: maybe INCORRECT
    'GA': r'\b(\d{9})\b',
    'HI': r'\b(\d{9}|H\d{8})\b',
    'ID': r'\b(\d{9}|[A-Z]{2}\d{6}[A-Z])\b',
    'IL': r'\b([A-Z0-9-]{14})\b',
    'IN': r'\b(\d{4}-\d{2}-\d{4})\b',
    'IA': r'\b(\d{9}|\d{3}[A-Z]{2}\d{4})\b',
    'KS': r'\b(K\d{2}-\d{2}-\d{4}|\d{3}-\d{2}-\d{4})\b',
    'KY': r'\b([A-Z]\d{2}-\d{3}-\d{3})\b',
    'LA': r'\b(\d{9})\b',
    'ME': r'\b(\d{7})\b',
    'MD': r'\b([A-Z]-\d{3}-\d{3}-\d{3}-\d{3})\b',
    'MA': r'\b(S\d{8}|\d{9})\b',
    'MI': r'\b([A-Z] \d{3} \d{3} \d{3} \d{3})\b',
    'MN': r'\b([A-Z]\d{3}-\d{3}-\d{3}-\d{3})\b',
    'MS': r'\b(\d{9})\b',
    'MO': r'\b([A-Z]\d{9}|\d{9})\b',
    'MT': r'\b(\d{13}|[A-Z]{9})\b',
    'NE': r'\b([ABCEGHV]\d{8})\b',
    'NV': r'\b(\d{10}|\d{12}|X\d{8})\b',
    'NH': r'\b(\d{2}[A-Z]{3}\d{5})\b',  # TODO: maybe INCORRECT
    'NJ': r'\b([A-Z]\d{4} \d{5} \d{5})\b',
    'NM': r'\b(\d{9})\b',
    'NY': r'\b(\d{3} \d{3} \d{3})\b',
    'NC': r'\b(\d{12})\b',
    'ND': r'\b([A-Z]{3}-\d{2}-\d{4}|\d{9})\b',
    'OH': r'\b([A-Z]{2}\d{6})\b',
    'OK': r'\b([A-Z]\d{9}|\d{9})\b',
    'OR': r'\b(\d{7}|[A-Z]\d{6})\b',
    'PA': r'\b(\d{2} \d{3} \d{3})\b',
    'RI': r'\b(\d{7}|V\d{6})\b',  # TODO: maybe INCORRECT
    'SC': r'\b(\d{9})\b',
    'SD': r'\b(\d{8})\b',
    'TN': r'\b(\d{9})\b',
    'TX': r'\b(\d{8})\b',
    'UT': r'\b(\d{9,10})\b',
    'VT': r'\b(\d{8}|\d{7}[A-Z])\b',
    'VA': r'\b([A-Z]\d{8}|\d{9})\b',  # TODO: maybe INCORRECT (second part)
    'WA': r'\b([A-Z*]{7}\d{3}[0-9A-Z]{2}|WDL[0-9A-Z]{9})\b',
    'WV': r'\b(\d{7}|[A-Z]{1,2}\d{5,6})\b',
    'WI': r'\b([A-Z]\d{3}-\d{4}-\d{4}-\d{2})\b',
    'WY': r'\b(\d{6}-\d{3})\b'
}


class DLNDetection:

    def __init__(self):
        self.matches = []
        self.dln = None

    def detect(self, img):
        text = self.image_to_string(img)
        self._recognition(text)

    # TODO
    def _filter(self, img, filter):
        pass

    def _recognition(self, text):
        for state, mask in STATE_FORMATS.items():
            re_match = re.findall(mask, text)
            if len(re_match):
                self.matches.append((state, re_match[0]))

    def _best_match(self, supposed_state):
        for state, dln in self.matches:
            if supposed_state == state:
                self.dln = dln
                break

        if not self.dln and len(self.matches):
            self.dln = self.matches[0][1]

    @staticmethod
    def image_to_string(img):
        text = pytesseract.image_to_string(img, config=TESSERACT_CONFIG)
        return text

    def get_result(self, supposed_state):
        self._best_match(supposed_state)
        return self.dln
