from func_connections import *
from func_private import *
from func_public import *


if __name__ == '__main__':
    #conncet to client
    try:
        client=connect_dydx()
    except Exception as e:
        print("error connecting to client",e)
        exit(1)
    account=client.private.get_account()
    account_id=account.data["account"]["id"]
    quote_balance=account.data["account"]["quoteBalance"]
    print(account_id,quote_balance)

    #abort all open possitions
    if ABORT_ALL_POSITIONS:
        try:
            print("aborting all positions")
            close_orders=abort_all_positions(client)
        except Exception as e:
            print("error clossing positions",e)
            exit(1)
        
    #find cointegrated pairs
    if FIND_COINTEGRATED:
        #CONSTRUCT MARKET PRICES
        df_market_prices = construct_market_prices(client)
        try:
            print("fetching prices ... 3 mins")
        except Exception as e:
            print("error fetching prices",e)
            exit(1)