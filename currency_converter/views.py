from os import stat
from django.http import HttpResponse
import requests
import xml.etree.ElementTree as ET
from currency_converter.models import ExchangeRates
import time
from django.core.cache import cache
from datetime import datetime

THROTTLE_RATE_SECONDS = 10 
GLOBAL_THROTTLE_KEY = 'global_index_throttle'


def index(_request):
    last_request_time = cache.get(GLOBAL_THROTTLE_KEY)
    current_time = time.time()

    if last_request_time is not None:
        time_elapsed = current_time - last_request_time
        
        if time_elapsed < THROTTLE_RATE_SECONDS:
            time_to_wait = int(THROTTLE_RATE_SECONDS - time_elapsed) + 1
            
            response = HttpResponse(
                f"Слишком много запросов. Повторите через {time_to_wait} секунд.", 
                status=429
                )
            response['Retry-After'] = str(time_to_wait)
            return response

    cache.set(GLOBAL_THROTTLE_KEY, current_time, timeout=THROTTLE_RATE_SECONDS)
    
    try:
        r = requests.get('https://www.cbr.ru/scripts/XML_daily.asp?date_req=26/11/2025')
    except Exception as e:
        response = HttpResponse(e, status=500)
        return response

    if r.status_code == 200:
        tree = ET.fromstring(r.text)
        currencies = 0
        
        for item in tree:
            if item.attrib['ID'] == 'R01235':
                for subitem in item:
                    if subitem.tag == 'Value':
                        currencies = float(subitem.text.replace(',', '.'))

    e = ExchangeRates(currency_request = currencies, date = datetime.now())
    e.save()

    all_entries = ExchangeRates.objects.order_by('id').all()[:10]

    response = f'Текущий курс: {currencies} Последние 10 запросов: '
    for entries in all_entries:
        response += f'{str(entries)} | '

    return HttpResponse(response)

