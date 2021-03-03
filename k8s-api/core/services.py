import requests


class Async:
    base_url = 'http://async:8000'

    @classmethod
    def alive(cls) -> bool:
        url = f'{cls.base_url}/core/alive/'
        response = requests.get(url)

        return 200 <= response.status_code < 300
