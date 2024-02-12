import aiohttp
import asyncio
import argparse
from datetime import datetime, timedelta

class PrivatBankCurrencyAPI:
    BASE_URL = 'https://api.privatbank.ua/p24api'

    async def fetch_exchange_rate(self, currency, date):
        async with aiohttp.ClientSession() as session:
            url = f'{self.BASE_URL}/exchange_rates?json&date={date}'
            async with session.get(url) as response:
                data = await response.json()
                if currency == 'USD':
                    return {'sale': data['exchangeRate'][0]['saleRate'], 'purchase': data['exchangeRate'][0]['purchaseRate']}
                elif currency == 'EUR':
                    return {'sale': data['exchangeRate'][1]['saleRate'], 'purchase': data['exchangeRate'][1]['purchaseRate']}
                else:
                    raise ValueError('Invalid currency')

    async def get_exchange_rate_for_days(self, currency, days):
        rates = []
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%d.%m.%Y')
            try:
                rate = await self.fetch_exchange_rate(currency, date)
                rates.append({date: {currency: rate}})
            except Exception as e:
                print(f'Error fetching exchange rate for {currency} on {date}: {e}')
        return rates

async def main():
    parser = argparse.ArgumentParser(description='Fetch currency exchange rates from PrivatBank API')
    parser.add_argument('-d', '--days', type=int, default=10, help='Number of days to show exchange rates (default: 10)')
    args = parser.parse_args()

    api = PrivatBankCurrencyAPI()
    try:
        usd_rates = await api.get_exchange_rate_for_days('USD', args.days)
        eur_rates = await api.get_exchange_rate_for_days('EUR', args.days)

        for usd_rate, eur_rate in zip(usd_rates, eur_rates):
            print(usd_rate)
            print(eur_rate)
            print()
    except Exception as e:
        print(f'Error: {e}')

if __name__ == '__main__':
    asyncio.run(main())
