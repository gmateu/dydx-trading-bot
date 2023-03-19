#crear virtual env: python3 -m venv venv
#utilitzar virtual env: source venv/bin/activate
#imports
from constants import *
from dydx3 import Client
from web3 import Web3
from pprint import pprint
from datetime import datetime,timedelta
from dydx3.constants import MARKET_BTC_USD





#Create client connection
client = Client(
    host=HOST,
    api_key_credentials={
        "key": DYDX_API_KEY,
        "secret": DYDX_API_SECRET,
        "passphrase": DYDX_API_PASSPHRASE
    },
    stark_private_key=STARK_PRIVATE_KEY,
    eth_private_key=ETH_PRIVATE_KEY,
    default_ethereum_address=ETHEREUM_ADDRESS,
    web3=Web3(Web3.HTTPProvider(HTTP_PROVIDER))
)

if __name__ == "__main__":
    #CHECK CONNECTION
    account = client.private.get_account()
    account_id=account.data["account"]["id"]
    print(account_id)

    #OHLC Candelstik data
    candles = client.public.get_candles(
        market="BTC-USD",
        resolution="1HOUR",
        limit=3
    )

    #pprint(candles.data)

    orderbook = client.public.get_orderbook(
    market=MARKET_BTC_USD,
    )
    #pprint(orderbook.data)

    #Get position ID
    position_id=account.data["account"]["positionId"]

    #Get Expiration time
    server_time=client.public.get_time()
    print(server_time.data["iso"])
    expiration = datetime.fromisoformat(server_time.data["iso"].replace("Z",""))+timedelta(seconds=3670)
    #delta=timedelta(seconds=70)
    #expiration += delta
    print(expiration)
    place_order = client.private.create_order(
        position_id=position_id,
        market="BTC-USD",
        side="BUY",
        order_type="MARKET",
        post_only=False,
        size='0.001',
        price='100000',
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK", #FAil or kill
        reduce_only=False
    )
    pprint(place_order.data)

