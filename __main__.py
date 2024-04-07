import requests

def get_bitcoin_price(api_key, currencies):
    url = f"https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms={','.join(currencies)}&api_key={api_key}"
    response = requests.get(url)
    data = response.json()
    bitcoin_prices = {currency: data[currency] for currency in currencies}
    return bitcoin_prices

# Ваш ключ API
api_key = "68be2293c8af0f8d8868c9c47c07d77a6d7952eab6e74f5b3fef2abaf163ed21"

# Получение и вывод курса биткойна в рублях и долларах
currencies = ['RUB', 'USD']
bitcoin_prices = get_bitcoin_price(api_key, currencies)

for currency, price in bitcoin_prices.items():
    if currency == 'RUB':
        currency_symbol = '₽'
    elif currency == 'USD':
        currency_symbol = '$'
    print(f"Текущий курс биткойна в {currency}: {price} {currency_symbol}")