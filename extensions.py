import requests
import json
from config import keys


class ConverterException(Exception):
    pass


class APIException:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        # ошибка: одинаковая валюта
        if quote == base:
            raise ConverterException(f'Невозможно перевести одинаковую валюту: {quote} в {base}')

        # ошибка: неправильно написана первая валюта
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту: {quote} \n\n Проверьте правильность написания валюты:\n /value\
 показывает список доступных валют для конвертирования')

        # ошибка: неправильно написана вторая валюта
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту: {base} \n\n Проверьте правильность написания валюты:\n /value\
        показывает список доступных валют для конвертирования')

        # ошибка: неправильно написано количество: не цифрами
        try:
            amount = int(amount)
        except ValueError:
            raise ConverterException(f'Не удалось обработать количество валюты: {amount}')

        r = requests.get(f'https://v6.exchangerate-api.com/v6/e6a740ca02026bd49b92990b/pair/{quote_ticker}/{base_ticker}/{amount}')
        conversion_result = json.loads(r.content)['conversion_result']

        return conversion_result

