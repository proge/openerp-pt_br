

def test_create_tax_include(oerp):
    tax_code_obj = oerp.pool.get('account.tax.code')
    tax_code_id = tax_code_obj.create(oerp.cr, 1, {
        'name': 'ISS 2%',
        'company_id': 1,
        'sign': 1,
        'tax_discount': 'TRUE',
        'tax_include': 'TRUE',
        'notprintable': 'TRUE',
        'domain': 'iss'
        })

    assert tax_code_obj.browse(oerp.cr, 1, [tax_code_id])[0].id == tax_code_id

    tax_obj = oerp.pool.get('account.tax')
    tax_id = tax_obj.create(oerp.cr, 1, {
        'sequence': '1',
        'type_tax_use': 'all',
        'applicable_type': 'true',
        'company_id': 1,
        'name': 'ISS 2%',
        'amount': 0.0200,
        'type': 'percent',
        'tax_code_id': tax_code_id,
        'base_reduction': 0.0000,
        'amount_mva': 0.0000,
        'price_include': 'FALSE',
        'tax_discount': 'TRUE',
        'tax_add': 'FALSE',
        'tax_include': 'TRUE',
        'tax_retain': 'FALSE',
        'domain': 'iss',
        })

    assert tax_obj.browse(oerp.cr, 1, [tax_id])[0].id == tax_id
