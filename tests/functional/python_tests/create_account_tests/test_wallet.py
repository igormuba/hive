from test_tools import Account, logger, World

def test_getters():
    with World() as world:
        init_node = world.create_init_node()
        init_node.config.plugin.append('database_api')
        init_node.run()

        wallet = init_node.attach_wallet()

        pswd = 'pear_peach'

        #**************************************************************
        logger.info('is_locked...')
        response = wallet.api.is_locked()
        logger.info(response)

        assert 'result' in response
        response['result'] = False

        #**************************************************************
        logger.info('set_password...')
        response = wallet.api.set_password(pswd)
        logger.info(response)

        assert 'result' in response
        response['result'] = None

        #**************************************************************
        logger.info('is_locked...')
        response = wallet.api.is_locked()
        logger.info(response)

        assert 'result' in response
        response['result'] = True

        #**************************************************************
        logger.info('unlock...')
        response = wallet.api.unlock(pswd)
        logger.info(response)

        assert 'result' in response
        response['result'] = None

        #**************************************************************
        logger.info('is_locked...')
        response = wallet.api.is_locked()
        logger.info(response)

        assert 'result' in response
        response['result'] = False

        #**************************************************************
        logger.info('lock...')
        response = wallet.api.lock()
        logger.info(response)

        assert 'result' in response
        response['result'] = None

        #**************************************************************
        logger.info('is_locked...')
        response = wallet.api.is_locked()
        logger.info(response)

        assert 'result' in response
        response['result'] = True

        #**************************************************************
        logger.info('unlock...')
        response = wallet.api.unlock(pswd)
        logger.info(response)

        assert 'result' in response
        response['result'] = None

        #**************************************************************
        logger.info('is_locked...')
        response = wallet.api.is_locked()
        logger.info(response)

        assert 'result' in response
        response['result'] = False

        #**************************************************************
        logger.info('list_keys...')
        response = wallet.api.list_keys()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) == 1
        _keys = _result[0]

        assert len(_keys) == 2
        assert _keys[0] == 'TST6LLegbAgLAy28EHrffBVuANFWcFgmqRMW13wBmTExqFE9SCkg4'
        assert _keys[1] == '5JNHfZYKGaomSFvd4NUdQ9qMcEAC43kujbfjueTHpVapX1Kzq2n'

        #**************************************************************
        logger.info('import_key...')
        response = wallet.api.import_key('5JE4eBgPiRiVcdcpJ8tQpMpm6dgm1uAuq9Kn2nn1M9xK94EE5nU')
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        #**************************************************************
        logger.info('list_keys...')
        response = wallet.api.list_keys()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) == 2
        _keys = _result[1]

        assert len(_keys) == 2
        assert _keys[0] == 'TST8LRQW8NXuDnextVpzKA5Fp47k591mHJjKnfTMdfQvjR5qA1yqK'
        assert _keys[1] == '5JE4eBgPiRiVcdcpJ8tQpMpm6dgm1uAuq9Kn2nn1M9xK94EE5nU'

        #**************************************************************
        logger.info('get_private_key_from_password...')
        response = wallet.api.get_private_key_from_password('hulabula', 'owner', "apricot")
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) == 2

        assert _result[0] == 'TST5Fuu7PnmJh5dxguaxMZU1KLGcmAh8xgg3uGMUmV9m62BDQb3kB'
        assert _result[1] == '5HwfhtUXPdxgwukwfjBbwogWfaxrUcrJk6u6oCfv4Uw6DZwqC1H'

        #**************************************************************
        logger.info('get_private_key...')
        response = wallet.api.get_private_key('TST6LLegbAgLAy28EHrffBVuANFWcFgmqRMW13wBmTExqFE9SCkg4')
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert _result == '5JNHfZYKGaomSFvd4NUdQ9qMcEAC43kujbfjueTHpVapX1Kzq2n'
