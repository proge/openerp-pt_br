

def test_create_service_productobj(oerp):
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

    prod_id = prod_obj.create(oerp.cr, 1, {
        'product_tmpl_id': prod_tpl_id,
        'valuation': 'manual_periodic'
        })

    assert prod_obj.browse(oerp.cr, 1, [prod_id])[0].id == prod_id
