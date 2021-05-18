from test_tools import Account, logger, World

def test_transfer():
    with World() as world:
        init_node = world.create_init_node()
        init_node.config.plugin.append('database_api')
        init_node.config.plugin.append('network_broadcast_api')
        init_node.run()

        wallet = init_node.attach_wallet()

        logger.info('Waiting until initminer will be able to create account...')
        init_node.wait_number_of_blocks(3)

        #**************************************************************
        logger.info('create_account...')
        response = wallet.api.create_account('initminer', 'newaccount', '{}', True)
        logger.info(response)

        #**************************************************************
        logger.info('get_account...')
        response = wallet.api.get_account('newaccount')
        logger.info(response)
        assert 'result' in response
        _result = response['result']
        assert 'balance' in _result
        assert _result['balance'] == '0.000 TESTS'
        assert 'hbd_balance' in _result
        assert _result['hbd_balance'] == '0.000 TBD'

        #**************************************************************
        logger.info('transfer...')
        response = wallet.api.transfer('initminer', 'newaccount', '5.432 TESTS', 'banana', True)
        logger.info(response)

        #**************************************************************
        logger.info('transfer...')
        response = wallet.api.transfer('initminer', 'newaccount', '9.169 TBD', 'banana', True)
        logger.info(response)

        #**************************************************************
        logger.info('get_account...')
        response = wallet.api.get_account('newaccount')
        logger.info(response)
        assert 'result' in response
        _result = response['result']
        assert 'balance' in _result
        assert _result['balance'] == '5.432 TESTS'
        assert 'hbd_balance' in _result
        assert _result['hbd_balance'] == '9.169 TBD'