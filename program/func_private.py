from datetime import datetime,timedelta
import time
from pprint import pprint
from func_utils import *

#place market order
def place_market_order(client,market,side,size,price,reduce_only):
    account = client.private.get_account()
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
        market=market,
        side=side,
        order_type="MARKET",
        post_only=False,
        size=size,
        price=price,
        limit_fee='0.015',
        expiration_epoch_seconds=expiration.timestamp(),
        time_in_force="FOK", #FAil or kill
        reduce_only=reduce_only
    )

    #return result
    return place_order.data


#abort all open postions
def abort_all_positions(client):
    #cancel all orders
    client.private.cancel_all_orders()

    #proctect API
    time.sleep(0.5)

    #Get markets for reference ok tick size
    markets = client.public.get_markets().data

    time.sleep(0.5)

    #get all open positions
    positions = client.private.get_positions(status="OPEN")
    all_positions = positions.data["positions"]
    #handle open positions
    close_orders=[]
    if len(all_positions) > 0:
        for position in all_positions:
            #determine market
            market = position["market"]

            #determine side
            side = "BUY"
            if position["side"] == "LONG":
                side="SELL"
            
            #GET PRICE
            price = float(position["entryPrice"])
            accept_price = price * 1.7 if side == "BUY" else price*0.3
            tick_size = markets["markets"][market]["tickSize"]
            accept_price=format_number(accept_price, tick_size)

            #place order to close
            order = place_market_order(
                client,
                market,
                side,
                position["sumOpen"],
                accept_price,
                reduce_only=True
            )

            #append the rsult 
            close_orders.append(order)

            time.sleep(0.5)
        #return clsed orders
        return close_orders