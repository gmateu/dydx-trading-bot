from func_connections import *
from func_private import *
from func_public import *
from func_cointegration import *
from func_entry_pairs import open_positions


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
        try:
            print("fetching prices ... 3 mins")
            df_market_prices = construct_market_prices(client)
            # close_prices = get_candles_historical(client,"SOL-USD")
        except Exception as e:
            print("error fetching prices",e)
            exit(1)

        # Store Cointegrated Pairs
        try:
            print("Storing cointegrated pairs...")
            stores_result = store_cointegration_results(df_market_prices)
            if stores_result != "saved":
                print("Error saving cointegrated pairs")
                exit(1)
        except Exception as e:
            print("Error saving cointegrated pairs: ", e)
            #send_message(f"Error saving cointegrated pairs {e}")
            exit(1)



        

    #place trades for opening positions
    if PLACE_TRADES:
        try:
            open_positions(client)
        except Exception as e:
            print("error trading ", e)
            exit(1)