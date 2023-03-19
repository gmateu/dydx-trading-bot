#crear virtual env: python3 -m venv venv
#utilitzar virtual env: source venv/bin/activate
#imports
from dydx3 import Client
from web3 import Web3
from pprint import pprint
from datetime import datetime,timedelta
from dydx3.constants import MARKET_BTC_USD


#use testnet
from dydx3.constants import API_HOST_GOERLI

#use mnainet
from dydx3.constants import API_HOST_MAINNET

#CONSTANTS  
ETHEREUM_ADDRESS = "0x6680beE0202cb15eD12Bf27A7919A30128628814"
ETH_PRIVATE_KEY = "0X7a130dd03df81cac3918f81e392e38132536e8814d7f59b83d13941d3637c183"

STARK_PRIVATE_KEY = "03c57e02bd988bcf236f6662fa1f3c5c21167f86fc50ff1a787a002861d19c93"
DYDX_API_KEY = "2ac602b5-c7b9-c566-fa31-cddf664e3251"
DYDX_API_SECRET = "RQrd7zqwJxltcrZg5Ly0D1YVMjcNMjzIX3tGjY9c"
DYDX_API_PASSPHRASE = "Zmkhz8OxXUbAC1Uk4l3i"
HOST = API_HOST_GOERLI

#provider
HTTP_PROVIDER = "https://eth-goerli.g.alchemy.com/v2/cukxgabNFOTQDa8gjlREHzeaSKDjK-om"

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

