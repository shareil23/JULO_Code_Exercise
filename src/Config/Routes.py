from ..Controller import *
from .Config import api

def Routes(api):
    api.add_resource(WalletInitAPI, '/api/v1/init')
    api.add_resource(EnableWalletAPI, '/api/v1/wallet')
    api.add_resource(DepositsWalletAPI, '/api/v1/wallet/deposits')
    api.add_resource(WithdrawalsWalletAPI, '/api/v1/wallet/withdrawals')

Routes(api)