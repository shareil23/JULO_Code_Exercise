from flask_restful import Resource
from flask import request
from datetime import datetime, timedelta
import uuid


from ..Config import db
from ..Config.Core import getCache, setCache
from ..Models import WalletUser, Wallet, DelayUpdateBalance, ReferenceLog, DepositLog, WithdrawalLog
from ..Schema import WalletSchemaList, DepositLogSchemaList, WithdrawalLogSchemaList, WalletSchemaListDisabled


class WalletInitAPI(Resource):
    def post(self):
        """
        :target : API
        :return : token for authentication
        """

        # get data from formdata and transform it to dict
        body = request.form.to_dict()

        validate_string = [
            "customer_xid"
        ]

        # validate request body contain required field
        if all(key in body for key in validate_string):
            # query are customer_xid exists
            query         = WalletUser.query.filter(WalletUser.customer_xid == body['customer_xid']).count()
            generate_uuid = str(uuid.uuid4()).replace('-', '')

            # check are customer_xid exists
            if query != 0:
                # set new token to cache
                setCache(generate_uuid, body['customer_xid'])

                datas = {
                    "status": "success",
                    "data": {
                        "token": generate_uuid
                    }
                }

                return datas, 201

            # fill created_at with timestamp data
            body['created_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()

            # insert customer data to wallet_user
            wallet_user_insert_data = WalletUser(**body)
            db.session.add(wallet_user_insert_data)
            db.session.flush()

            # get new id of customer and fill the body data for wallet
            wallet_body = {
                "owned_by": wallet_user_insert_data.id,
                "status": None,
                "balance": 0
            }

            # insert customer data to wallet
            wallet_insert_data = Wallet(**wallet_body)
            db.session.add(wallet_insert_data)
            db.session.commit()

            # set new token to cache
            setCache(generate_uuid, body['customer_xid'])

            datas = {
                "status": "success",
                "data": {
                    "token": generate_uuid
                }
            }

            return datas, 201
        else:
            datas = {
                "status": "error",
                "message": "Missing required field in body request."
            }

            return datas, 400


class EnableWalletAPI(Resource):
    def get(self):
        """
        :target : API
        :return : balance of user wallet
        """

        # get data from header
        head = request.headers.get("Authorization")

        # check the data exists in cache
        remove_white_space = str(head).replace(" ", "")
        remove_token       = remove_white_space.lower().replace('Token', "")
        token_cache        = getCache(remove_token)

        if token_cache is None:
            datas = {
                "status": "error",
                "message": "Access denied due to invalid token."
            }

            return datas, 401

        # get id from token
        query_id_wallet_user = WalletUser.query.filter(WalletUser.customer_xid == token_cache)

        # check the data exists
        if query_id_wallet_user.count() == 0:
            datas = {
                "status": "error",
                "message": "User didn't exists."
            }

            return datas, 400

        # get id data
        id_wallet_user = query_id_wallet_user.first().id

        # query the newest data
        query_new_wallet   = Wallet.query.filter(Wallet.owned_by == id_wallet_user).all()
        wallet_schema_list = WalletSchemaList(many=True)
        output             = wallet_schema_list.dump(query_new_wallet)

        # check the data exists
        if len(output) == 0:
            datas = {
                "status": "error",
                "message": "Wallet data didn't exists."
            }

            return datas, 400

        # check are wallet status disabled
        if output[0]['status'] == 'disabled':
            datas = {
                "status": "error",
                "message": "Wallet status disabled, cannot use this feature."
            }

            return datas, 400

        # add delay if balance updated
        query_delay_update_balance = DelayUpdateBalance.query \
            .filter(DelayUpdateBalance.owned_by == id_wallet_user) \
            .order_by(DelayUpdateBalance.id.desc()).limit(1)

        # check data exists
        if query_delay_update_balance.count() != 0:
            # check the time before time limit
            if datetime.now().strftime("%H:%M:%S") < str(query_delay_update_balance.first().time_limit):
                output[0]['balance'] = query_delay_update_balance.first().old_balance

        datas = {
            "status": "success",
            "data": {
                "wallet": output[0]
            }
        }

        return datas, 200

    def post(self):
        """
        :target : API
        :return : change wallet status to enable
        """

        # get data from header
        head = request.headers.get("Authorization")
        body = {}

        # check the data exists in cache
        remove_white_space = str(head).replace(" ", "")
        remove_token       = remove_white_space.lower().replace('Token', "")
        token_cache        = getCache(remove_token)

        if token_cache is None:
            datas = {
                "status": "error",
                "message": "Access denied due to invalid token."
            }

            return datas, 401

        # get id from token
        query_id_wallet_user = WalletUser.query.filter(WalletUser.customer_xid == token_cache)

        # check the data exists
        if query_id_wallet_user.count() == 0:
            datas = {
                "status": "error",
                "message": "User didn't exists."
            }

            return datas, 400

        # get id data
        id_wallet_user = query_id_wallet_user.first().id

        # get the wallet data
        query_wallet = Wallet.query.filter(Wallet.owned_by == id_wallet_user)

        # check the wallet data exists
        if query_wallet.count() == 0:
            datas = {
                "status": "error",
                "message": "Wallet didn't exists."
            }

            return datas, 400

        # get data status before edit
        status_wallet = query_wallet.first().status

        # check the wallet status data must not enabled
        if status_wallet == "enabled":
            datas = {
                "status": "error",
                "message": "Wallet status has been enabled, cannot change the status again."
            }

            return datas, 400

        # set the status and enabled_at
        body['status']     = "enabled"
        body['enabled_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()

        query_wallet.update(body)
        db.session.commit()

        # query the newest data
        query_new_wallet   = Wallet.query.filter(Wallet.owned_by == id_wallet_user).all()
        wallet_schema_list = WalletSchemaList(many=True)
        output             = wallet_schema_list.dump(query_new_wallet)

        # check the data exists
        if len(output) == 0:
            datas = {
                "status": "error",
                "message": "Wallet data didn't exists."
            }

            return datas, 400

        datas = {
            "status": "success",
            "data": {
                "wallet": output[0]
            }
        }

        return datas, 200

    def patch(self):
        """
        :target : API
        :return : change wallet status to disabled
        """

        # get data from header
        head = request.headers.get("Authorization")
        body = request.form.to_dict()

        validate_string = [
            "is_disabled"
        ]

        # validate request body contain required field
        if all(key in body for key in validate_string):
            # check the data exists in cache
            remove_white_space = str(head).replace(" ", "")
            remove_token       = remove_white_space.lower().replace('Token', "")
            token_cache        = getCache(remove_token)

            if token_cache is None:
                datas = {
                    "status": "error",
                    "message": "Access denied due to invalid token."
                }

                return datas, 401

            # get id from token
            query_id_wallet_user = WalletUser.query.filter(WalletUser.customer_xid == token_cache)

            # check the data exists
            if query_id_wallet_user.count() == 0:
                datas = {
                    "status": "error",
                    "message": "User didn't exists."
                }

                return datas, 400

            # get id data
            id_wallet_user = query_id_wallet_user.first().id

            # get the wallet data
            query_wallet = Wallet.query.filter(Wallet.owned_by == id_wallet_user)

            # check the wallet data exists
            if query_wallet.count() == 0:
                datas = {
                    "status": "error",
                    "message": "Wallet didn't exists."
                }

                return datas, 400

            # get data status before edit
            status_wallet = query_wallet.first().status

            # check status of is_disabled
            if str(body['is_disabled']) == "false":
                datas = {
                    "status": "error",
                    "message": "Wallet status failed to change to disabled."
                }

                return datas, 400

            # check the wallet status data must not enabled
            if status_wallet == "disabled":
                datas = {
                    "status": "error",
                    "message": "Wallet status has been disabled, cannot change the status again."
                }

                return datas, 400

            del body['is_disabled']

            # set the status and enabled_at
            body['status']      = "disabled"
            body['disabled_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()

            query_wallet.update(body)
            db.session.commit()

            # query the newest data
            query_new_wallet   = Wallet.query.filter(Wallet.owned_by == id_wallet_user).all()
            wallet_schema_list = WalletSchemaListDisabled(many=True)
            output             = wallet_schema_list.dump(query_new_wallet)

            # check the data exists
            if len(output) == 0:
                datas = {
                    "status": "error",
                    "message": "Wallet data didn't exists."
                }

                return datas, 400

            datas = {
                "status": "success",
                "data": {
                    "wallet": output[0]
                }
            }

            return datas, 200
        else:
            datas = {
                "status": "error",
                "message": "Missing required field in body request."
            }

            return datas, 400


class DepositsWalletAPI(Resource):
    def post(self):
        """
        :target : API
        :return : add funds to wallet
        """

        # get data from header
        head = request.headers.get("Authorization")
        body = request.form.to_dict()

        validate_string = [
            "reference_id",
            "amount"
        ]

        # validate request body contain required field
        if all(key in body for key in validate_string):
            # check the data exists in cache
            remove_white_space = str(head).replace(" ", "")
            remove_token       = remove_white_space.lower().replace('Token', "")
            token_cache        = getCache(remove_token)

            if token_cache is None:
                datas = {
                    "status": "error",
                    "message": "Access denied due to invalid token."
                }

                return datas, 401

            # get id from token
            query_id_wallet_user = WalletUser.query.filter(WalletUser.customer_xid == token_cache)

            # check the data exists
            if query_id_wallet_user.count() == 0:
                datas = {
                    "status": "error",
                    "message": "User didn't exists."
                }

                return datas, 400

            # get id data
            id_wallet_user = query_id_wallet_user.first().id

            # query get wallet data
            query_wallet = Wallet.query.filter(Wallet.owned_by == id_wallet_user)

            # check are wallet status disabled
            if query_wallet.first().status == 'disabled':
                datas = {
                    "status": "error",
                    "message": "Wallet status disabled, cannot use this feature."
                }

                return datas, 400

            # check the references has been used
            query_reference_log = ReferenceLog.query \
                .filter(ReferenceLog.reference_id == body['reference_id']) \
                .filter(ReferenceLog.category == "deposit")

            # check the data exists
            if query_reference_log.count() == 1:
                # insert data to reference_log
                body_reference_log = {
                    "reference_id": body['reference_id'],
                    "category": "deposit",
                    "created_at": datetime.now().astimezone().replace(microsecond=0).isoformat()
                }

                # insert data to reference log
                reference_log_insert_data = ReferenceLog(**body_reference_log)
                db.session.add(reference_log_insert_data)
                db.session.flush()

                # add rest field for deposit_log body
                body['reference_id'] = reference_log_insert_data.id
                body['deposited_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()
                body['status']       = "failed"
                body['deposit_by']   = id_wallet_user

                # insert deposit log failed status
                deposit_log_insert_data = DepositLog(**body)
                db.session.add(deposit_log_insert_data)
                db.session.commit()

                datas = {
                    "status": "error",
                    "message": "The reference_id has been used before."
                }

                return datas, 400

            # insert data to reference_log
            body_reference_log = {
                "reference_id": body['reference_id'],
                "category": "deposit",
                "created_at": datetime.now().astimezone().replace(microsecond=0).isoformat()
            }

            # insert data to reference log
            reference_log_insert_data = ReferenceLog(**body_reference_log)
            db.session.add(reference_log_insert_data)
            db.session.flush()

            # add rest field for deposit_log body
            body['reference_id'] = reference_log_insert_data.id
            body['deposited_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()
            body['status']       = "success"
            body['deposit_by']   = id_wallet_user

            # insert data to deposit log
            deposit_log_insert_data = DepositLog(**body)
            db.session.add(deposit_log_insert_data)
            db.session.flush()
            db.session.commit()

            # update balance and get the old wallet data
            temp_old_balance = query_wallet.first().balance

            body_wallet  = {
                "balance": int(temp_old_balance) + int(body['amount'])
            }

            # update data to walet
            query_wallet.update(body_wallet)
            db.session.commit()

            # insert delay_update_balance
            time_limit = datetime.now() + timedelta(seconds=5)

            body_delay_update_balance = {
                "owned_by": id_wallet_user,
                "time_limit": time_limit.strftime("%H:%M:%S"),
                "old_balance": temp_old_balance,
            }

            # insert data to delay update balance
            delay_update_balance = DelayUpdateBalance(**body_delay_update_balance)
            db.session.add(delay_update_balance)
            db.session.commit()

            # parse object to schematic json
            deposit_log_schema_list = DepositLogSchemaList(many=False)
            output                  = deposit_log_schema_list.dump(deposit_log_insert_data)

            datas = {
                "status": "success",
                "data": {
                    "deposit": output
                }
            }

            return datas, 200
        else:
            datas = {
                "status": "error",
                "message": "Missing required field in body request."
            }

            return datas, 400


class WithdrawalsWalletAPI(Resource):
    def post(self):
        """
        :target : API
        :return : withdrawal funds to wallet
        """

        # get data from header
        head = request.headers.get("Authorization")
        body = request.form.to_dict()

        validate_string = [
            "reference_id",
            "amount"
        ]

        # validate request body contain required field
        if all(key in body for key in validate_string):
            # check the data exists in cache
            remove_white_space = str(head).replace(" ", "")
            remove_token       = remove_white_space.lower().replace('Token', "")
            token_cache        = getCache(remove_token)

            if token_cache is None:
                datas = {
                    "status": "error",
                    "message": "Access denied due to invalid token."
                }

                return datas, 401

            # get id from token
            query_id_wallet_user = WalletUser.query.filter(WalletUser.customer_xid == token_cache)

            # check the data exists
            if query_id_wallet_user.count() == 0:
                datas = {
                    "status": "error",
                    "message": "User didn't exists."
                }

                return datas, 400

            # get id data
            id_wallet_user = query_id_wallet_user.first().id

            # get the wallet data
            query_wallet = Wallet.query.filter(Wallet.owned_by == id_wallet_user)

            # check are wallet status disabled
            if query_wallet.first().status == 'disabled':
                datas = {
                    "status": "error",
                    "message": "Wallet status disabled, cannot use this feature."
                }

                return datas, 400

            # check the references has been used
            query_reference_log = ReferenceLog.query \
                .filter(ReferenceLog.reference_id == body['reference_id']) \
                .filter(ReferenceLog.category == "withdrawal")

            # check the data exists
            if query_reference_log.count() == 1:
                # insert data to reference_log
                body_reference_log = {
                    "reference_id": body['reference_id'],
                    "category": "withdrawal",
                    "created_at": datetime.now().astimezone().replace(microsecond=0).isoformat()
                }

                # insert data to reference log
                reference_log_insert_data = ReferenceLog(**body_reference_log)
                db.session.add(reference_log_insert_data)
                db.session.flush()

                # add rest field for withdrawal_log body
                body['reference_id'] = reference_log_insert_data.id
                body['withdrawn_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()
                body['status']       = "failed"
                body['withdrawn_by'] = id_wallet_user

                # insert withdrawal log failed status
                withdrawal_log_insert_data = WithdrawalLog(**body)
                db.session.add(withdrawal_log_insert_data)
                db.session.commit()

                datas = {
                    "status": "error",
                    "message": "The reference_id has been used before."
                }

                return datas, 400

            # insert data to reference_log
            body_reference_log = {
                "reference_id": body['reference_id'],
                "category": "withdrawal",
                "created_at": datetime.now().astimezone().replace(microsecond=0).isoformat()
            }

            # insert data to reference log
            reference_log_insert_data = ReferenceLog(**body_reference_log)
            db.session.add(reference_log_insert_data)
            db.session.flush()
            db.session.commit()

            # update balance
            temp_old_balance = query_wallet.first().balance

            # check the amount cannot greater than the balance
            if int(body['amount']) > int(query_wallet.first().balance):
                datas = {
                    "status": "error",
                    "message": "The amount being used must not be more than the current balance."
                }

                return datas, 400

            # add rest field for withdrawal_log body
            body['reference_id'] = reference_log_insert_data.id
            body['withdrawn_at'] = datetime.now().astimezone().replace(microsecond=0).isoformat()
            body['status']       = "success"
            body['withdrawn_by'] = id_wallet_user

            # insert withdrawal log
            withdrawal_log_insert_data = WithdrawalLog(**body)
            db.session.add(withdrawal_log_insert_data)
            db.session.flush()
            db.session.commit()

            body_wallet = {
                "balance": int(temp_old_balance) - int(body['amount'])
            }

            # update data to walet
            query_wallet.update(body_wallet)
            db.session.commit()

            # insert delay_update_balance
            time_limit = datetime.now() + timedelta(seconds=5)

            body_delay_update_balance = {
                "owned_by": id_wallet_user,
                "time_limit": time_limit.strftime("%H:%M:%S"),
                "old_balance": temp_old_balance,
            }

            # insert data to delay update balance
            delay_update_balance = DelayUpdateBalance(**body_delay_update_balance)
            db.session.add(delay_update_balance)
            db.session.commit()

            # parse object to schematic json
            withdrawal_log_schema_list = WithdrawalLogSchemaList(many=False)
            output                     = withdrawal_log_schema_list.dump(withdrawal_log_insert_data)

            datas = {
                "status": "success",
                "data": {
                    "withdrawal": output
                }
            }

            return datas, 200
        else:
            datas = {
                "status": "error",
                "message": "Missing required field in body request."
            }

            return datas, 400