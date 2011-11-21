

def test_services_sale_to_invoice(oerp):
    #create empty fiscal classification for the service
    prod_fc_obj = oerp.pool.get('account.product.fiscal.classification')
    prod_fc_id = prod_fc_obj.create(oerp.cr, 1, {
        'name': 'isento',
        'description': 'isento'
        })

    assert prod_fc_obj.browse(oerp.cr, 1, [prod_fc_id])[0].id == prod_fc_id

    # create service fiscal operation category
    cfop_obj = oerp.pool.get('l10n_br_account.cfop')
    cfop_id = cfop_obj.search(oerp.cr, 1, [])[0]
    fiscal_doc_obj = oerp.pool.get('l10n_br_account.fiscal.document')
    fiscal_doc_id = fiscal_doc_obj.search(oerp.cr, 1, [('nfe', '=', 'TRUE')])[0]

    fopc_obj = oerp.pool.get('l10n_br_account.fiscal.operation.category')
    fopc_id = fopc_obj.create(oerp.cr, 1, {
        'code': 'isento',
        'name': 'isento',
        'type': 'output',
        'use_sale': 'TRUE',
        'use_invoice': 'TRUE',
        'fiscal_type': 'service'
        })

    assert fopc_obj.browse(oerp.cr, 1, [fopc_id])[0].id == fopc_id

    # create service fiscal operation
    fop_obj = oerp.pool.get('l10n_br_account.fiscal.operation')
    fop_id = fop_obj.create(oerp.cr, 1, {
        'code': 'servico01',
        'name': 'servico01',
        'type': 'output',
        'fiscal_operation_category_id': fopc_id,
        'cfop_id': cfop_id,
        'fiscal_document_id': fiscal_doc_id,
        'use_sale': 'TRUE',
        'use_invoice': 'TRUE',
        'fiscal_type': 'service'
        })

    assert fop_obj.browse(oerp.cr, 1, [fop_id])[0].id == fop_id

    # create service template
    prod_obj = oerp.pool.get('product.product')
    prod_tpl_obj = oerp.pool.get('product.template')

    prod_tpl_id = prod_tpl_obj.create(oerp.cr, 1, {
        'supply_method': 'buy',
        'standard_price': 1.00,
        'list_price': 100.00,
        'mes_type': 'fixed',
        'name': 'service test',
        'uom_po_id': 1,
        'type': 'service',
        'procure_method': 'make_to_stock',
        'cost_method': 'standard',
        'categ_id': 1
        })

    assert prod_tpl_obj.browse(oerp.cr, 1, [prod_tpl_id])[0].id == prod_tpl_id

    # create service obj
    prod_id = prod_obj.create(oerp.cr, 1, {
        'product_tmpl_id': prod_tpl_id,
        'valuation': 'manual_periodic'
        })

    assert prod_obj.browse(oerp.cr, 1, [prod_id])[0].id == prod_id

    # create ISS tax code with tax_include
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

    # create ISS 2% tax with type tax_include
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

    # create sale order with above data
    sale_order_obj = oerp.pool.get('sale.order')

    sale_order_lines = []

    prod = prod_obj.browse(oerp.cr, 1, [prod_id])[0]

    sol = {'name': prod.name,
            'product_uom_qty': 1,
            'product_id': prod.id,
            'product_uom': 1,
            'price_unit': prod.price_get('list_price')[prod.id]
            }

    sale_order_lines.append((0, 0, sol))

    order_id = sale_order_obj.create(oerp.cr, 1, {
        'user_id': 1,
        'partner_id': 1,
        'partner_order_id': partner_client_address_id,
        'partner_invoice_id': partner_client_address_id,
        'partner_shipping_id': partner_client_address_id,
        'pricelist_id': 1,
        'order_line': sale_order_lines,
        'fiscal_operation_category_id': fopc_id
        #'fiscal_position': 1
        })

    assert sale_order_obj.browse(oerp.cr, 1, [order_id])[0].id == order_id

    # TODO create_invoice with above sale order
