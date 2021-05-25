from test_tools import Account, logger, World

def test_getters():
    with World() as world:
        init_node = world.create_init_node()
        init_node.config.plugin.append('database_api')
        init_node.config.plugin.append('network_broadcast_api')
        init_node.config.plugin.append('account_history_rocksdb')
        init_node.config.plugin.append('account_history')
        init_node.config.plugin.append('account_history_api')
        init_node.config.plugin.append('block_api')
        init_node.run()

        wallet = init_node.attach_wallet()

        #**************************************************************
        logger.info('create_account...')
        response = wallet.api.create_account('initminer', 'alice', '{}', True)
        logger.info(response)

        #**************************************************************
        logger.info('transfer_to_vesting...')
        response = wallet.api.transfer_to_vesting('initminer', 'alice', '500.000 TESTS', True)
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert 'ref_block_num' in _result
        block_number = _result['ref_block_num'] + 1

        #**************************************************************
        logger.info('get_active_witnesses...')
        response = wallet.api.get_active_witnesses()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert len(_result) > 0
        assert _result[0] == 'initminer'

        #**************************************************************
        logger.info('get_block...')
        response = wallet.api.get_block(block_number)
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert 'transactions' in _result
        assert len(_result['transactions']) == 1
        _trx = _result['transactions'][0]

        assert 'operations' in _trx
        _ops = _trx['operations']

        assert len(_ops) == 1

        _op = _ops[0]
        assert 'value' in _op
        _value = _op['value']

        assert 'amount' in _value
        assert _value['amount'] == '500.000 TESTS'

        #**************************************************************
        logger.info('get_encrypted_memo...')
        response = wallet.api.get_encrypted_memo('alice', 'initminer', '#this is memo')
        logger.info(response)

        assert 'result' in response
        response['result'] == '#FZNN15uqMGdU1vzeMiHyzo6p8hT4V4WHGLNbTUGprhQFMVDYD4jc35zgSYf3BDL6vpbvNkBo831ttojfstt7bH58PC1etd9qbUHtoA6ZRqqpnzAsPg4rubGd2ANGyHvce'

        #**************************************************************
        logger.info('decrypt_memo...')
        response = wallet.api.decrypt_memo('#FZNN15uqMGdU1vzeMiHyzo6p8hT4V4WHGLNbTUGprhQFMVDYD4jc35zgSYf3BDL6vpbvNkBo831ttojfstt7bH58PC1etd9qbUHtoA6ZRqqpnzAsPg4rubGd2ANGyHvce')
        logger.info(response)

        assert 'result' in response
        response['result'] == 'this is memo'

        #**************************************************************
        logger.info('get_feed_history...')
        response = wallet.api.get_feed_history()
        logger.info(response)

        assert 'result' in response
        _result = response['result']

        assert 'current_median_history' in _result
        _current_median_history = _result['current_median_history']

        assert 'base' in _current_median_history
        _current_median_history['base'] == '0.001 TBD'

        assert 'quote' in _current_median_history
        _current_median_history['quote'] == '0.001 TESTS'
