import os
import tinvest
import time

TOKEN = "t.3AVYcoRFiwegFJxOxhgrXEV5Hhuq86jVmqRcJETCxY8Ee8CuTGhj4ABuhS37gnAuM2bcbBhtU1fvb-q2TGs_IA"

def getStocks(client):
    try:
        stocks = client.get_market_stocks();
        return stocks;
    except tinvest.BadRequestError as err:
        print(err.response)
        time.sleep(10)
        getStocks(client)

def main():
    client = tinvest.SyncClient(token = TOKEN, use_sandbox = True);
    stocks = getStocks(client)
    payload = stocks.payload
    print(payload)

if __name__ == '__main__':
    main()