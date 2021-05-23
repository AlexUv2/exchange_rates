import requests
from time import sleep

MAX_TRY_COUNT = 5
SLEEP_BETWEEN_TRY_SEC = 5


class RatesAPI:

    def __init__(self, token: str):
        self._url = 'https://free.currconv.com/api/v7/convert?'
        self._token = token

    def get_response(self, params: dict, try_count: int = 0):
        try:
            try_count += 1
            response = requests.get(url=self._url, params=params)
            if response.status_code == 200:
                return response.json()
            raise Exception('Status code not 200')
        except Exception as e:
            sleep(SLEEP_BETWEEN_TRY_SEC)
            print(f'''[RatesAPI][get_response] Except {e.__class__.name}! Try count: {try_count} 
                     Sleep {SLEEP_BETWEEN_TRY_SEC} sec between next try''')
            if try_count == MAX_TRY_COUNT:
                raise Exception("Can't reach domain")

            return self.get_response(params=params, try_count=try_count)

    def get_rate(self, curr_pair: str) -> dict:
        params = {
            'q': curr_pair.upper().strip(),
            'compact': 'ultra',
            'apiKey': self._token
        }
        return self.get_response(params=params)
