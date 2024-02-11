import aiohttp
import asyncio
from datetime import datetime, timedelta

class PrivatBankCurrencyAPI:
    BASE_URL = 'https://api.privatbank.ua/p24api'

    async def fetch_exchange_rate(self, currency, date):
        async with aiohttp.ClientSession() as session:
            url = f'{self.BASE_URL}/exchange_rates?json&date={date}'
            async with session.get(url) as response:
                data = await response.json()
                if currency == 'USD':
                    return data['exchangeRate'][0]['purchaseRate']
                elif currency == 'EUR':
                    return data['exchangeRate'][1]['purchaseRate']
                else:
                    raise ValueError('Invalid currency')

    async def get_exchange_rate_for_days(self, currency, days):
        rates = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
            try:
                rate = await self.fetch_exchange_rate(currency, date)
                rates[date] = rate
            except Exception as e:
                print(f'Error fetching exchange rate for {currency} on {date}: {e}')
        return rates

async def main():
    api = PrivatBankCurrencyAPI()
    try:
        usd_rates = await api.get_exchange_rate_for_days('USD', 10)
        print('USD Exchange Rates:')
        for date, rate in usd_rates.items():
            print(f'{date}: {rate}')
        print()
        
        eur_rates = await api.get_exchange_rate_for_days('EUR', 10)
        print('EUR Exchange Rates:')
        for date, rate in eur_rates.items():
            print(f'{date}: {rate}')
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(main())
