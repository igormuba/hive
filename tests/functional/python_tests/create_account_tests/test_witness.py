from test_tools import Account, logger, World

def test_update():
    with World() as world:
        init_node = world.create_init_node()
        init_node.config.plugin.append('database_api')
        init_node.config.plugin.append('network_broadcast_api')
        init_node.run()

        wallet = init_node.attach_wallet()

        #**************************************************************
        logger.info('create_account...')
        response = wallet.api.create_account('initminer', 'alice', '{}')
        logger.info(response)

        #**************************************************************
        logger.info('transfer_to_vesting...')
        response = wallet.api.transfer_to_vesting('initminer', 'alice', '500.000 TESTS')
        logger.info(response)

        #**************************************************************
        logger.info('get_active_witnesses...')
        response = wallet.api.get_active_witnesses()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) > 1
        assert _result[0] == 'initminer'
        assert _result[1] == ''

        #**************************************************************
        logger.info('list_witnesses...')
        response = wallet.api.list_witnesses('a', 4)
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) == 1
        assert _result[0] == 'initminer'
        #**************************************************************
        logger.info('update_witness...')
        response = wallet.api.update_witness('alice', 'http:\\url.html', 'TST6LLegbAgLAy28EHrffBVuANFWcFgmqRMW13wBmTExqFE9SCkg4', { 'account_creation_fee':{"amount":"2789","precision":3,"nai":"@@000000021"}, 'maximum_block_size' : 131072, 'hbd_interest_rate' : 1000 } )
        logger.info(response)

        #**************************************************************
        logger.info('get_active_witnesses...')
        response = wallet.api.get_active_witnesses()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) > 1
        assert _result[0] == 'initminer'
        assert _result[1] == ''

        #**************************************************************
        logger.info('list_witnesses...')
        response = wallet.api.list_witnesses('a', 4)
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) == 2
        assert _result[0] == 'alice'
        assert _result[1] == 'initminer'
        #**************************************************************
        logger.info('get_witness...')
        response = wallet.api.get_witness('alice')
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert 'owner' in _result
        assert _result['owner'] == 'alice'

        assert 'props' in _result
        _props = _result['props']

        assert 'account_creation_fee' in _props
        _props['account_creation_fee'] == '2.789 TESTS'
