from func_connections import connect_dydx


if __name__ == '__main__':
    #conncet to client
    client=connect_dydx()
    account=client.private.get_account()
    account_id=account.data["account"]["id"]
    quote_balance=account.data["account"]["quoteBalance"]
    print(account_id,quote_balance)