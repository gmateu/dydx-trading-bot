from func_connections import *
from func_private import *


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