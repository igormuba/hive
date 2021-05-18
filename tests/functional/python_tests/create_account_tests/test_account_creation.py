from test_tools import Account, logger, World

def test_account_creation():
    with World() as world:
        init_node = world.create_init_node()
        init_node.config.plugin.append('database_api')
        init_node.config.plugin.append('network_broadcast_api')
        init_node.config.plugin.append('account_history_rocksdb')
        init_node.config.plugin.append('account_history')
        init_node.config.plugin.append('account_history_api')
        init_node.run()

        wallet = init_node.attach_wallet()

        logger.info('Waiting until initminer will be able to create account...')
        init_node.wait_number_of_blocks(3)

        #**************************************************************
        response = wallet.api.create_account('initminer', 'newaccount', '{}', True)
        logger.info(response)

        assert 'result' in response
        assert 'operations' in response['result']

        _operations = response['result']['operations']
        assert len(_operations) == 1

        _operation = _operations[0]
        assert 'value' in _operation
        assert 'fee' in _operation['value']
        assert _operation['value']['fee'] == '0.000 TESTS'

        assert 'owner' in _operation['value']
        _owner = _operation['value']['owner']
        assert 'key_auths' in _owner
        _key_auths = _owner['key_auths']
        assert len(_key_auths) == 1
        __key_auths = _key_auths[0]
        assert len(__key_auths) == 2
        owner_key = __key_auths[0]

        #**************************************************************
        response = wallet.api.list_my_accounts([owner_key])
        logger.info(response)

        assert 'result' in response
        assert len(response['result']) == 1
        _result = response['result'][0]
        assert 'balance' in _result
        assert _result['balance'] == '0.000 TESTS'
        assert 'savings_balance' in _result
        assert _result['savings_balance'] == '0.000 TESTS'

        #**************************************************************
        response = wallet.api.list_accounts('na', 1)
        logger.info(response)
        assert 'result' in response
        assert len(response['result']) == 1
        assert response['result'][0] == 'newaccount'

        #**************************************************************
        response = wallet.api.get_account('newaccount')
        logger.info(response)
        assert 'result' in response
        _result = response['result']
        assert 'hbd_balance' in _result
        assert _result['hbd_balance'] == '0.000 TBD'

        #**************************************************************
        response = wallet.api.get_account_history('newaccount', 0, 1)
        logger.info(response)
        assert 'result' in response
        assert len(response['result']) == 0

        #**************************************************************
        response = wallet.api.transfer("initminer", "newaccount", "1.000 TESTS", "banana", True)
        logger.info(response)
        response = wallet.api.get_account_history('initminer', 3, 3)
        logger.info(response)
        assert 'result' in response
        assert len(response['result']) == 0
