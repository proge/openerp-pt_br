

def test_create_empty_fiscal_classification(oerp):
    prod_fc_obj = oerp.pool.get('account.product.fiscal.classification')
    prod_fc_id = prod_fc_obj.create(oerp.cr, 1, {
        'name': 'isento',
        'description': 'isento'
        })

    assert prod_fc_obj.browse(oerp.cr, 1, [prod_fc_id])[0].id == prod_fc_id
