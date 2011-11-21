

def test_create_partner_client(oerp):
    # create client partner
    partner_client_obj = oerp.pool.get('res.partner')
    partner_client_id = partner_client_obj.create(oerp.cr, 1, {
        'name': 'cliente teste',
        'tipo_pessoa': 'J',
        'legal_name': 'cliente teste',
        'cnpj_cpf': '45.225.081/0001-66',
        'partner_fiscal_type_id': 1
        })

    assert partner_client_obj.browse(oerp.cr, 1, [partner_client_id])[0].id == partner_client_id

    # create client partner address
    partner_client_address_obj = oerp.pool.get('res.partner.address')
    partner_client_address_id = partner_client_address_obj.create(oerp.cr, 1, {
        'phone': '5130850096',
        'street': 'av abc',
        'active': 'TRUE',
        'partner_id': partner_client_id,
        'city': 'poa',
        'name': 'Carlos',
        'country_id': 29,
        'type': 'default',
        'email': 'proge@proge.com.br',
        'state_id': 74,
        'l10n_br_city_id': 4530,
        'number': 34,
        'district': 'abcd',
        'zip': 92500000
        })

    assert partner_client_address_obj.browse(oerp.cr, 1, [partner_client_address_id])[0].id == partner_client_address_id
