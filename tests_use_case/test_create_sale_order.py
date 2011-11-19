

def test_create_sale_order(oerp):
    sale_order_obj = oerp.pool.get('sale.order')
    product_obj = oerp.pool.get('product.product')

    sale_order_lines = []

    prod1 = product_obj.browse(oerp.cr, 1, [5])[0]

    sol = {'name': prod1.name,
            'product_uom_qty': 1,
            'product_id': prod1.id,
            'product_uom': 1,
            'price_unit': prod1.price_get('list_price')[prod1.id]
            }

    #sol_new = sale_order_line_obj.product_id_change(oerp.cr, 1, None, 1, 0, 1, 1,name=prod1.name, partner_id=1,fiscal_position=fp1)['value']

    sale_order_lines.append((0, 0, sol))

    order_id = sale_order_obj.create(oerp.cr, 1, {
        'user_id': 1,
        'partner_id': 1,
        'partner_order_id': 2,
        'partner_invoice_id': 2,
        'partner_shipping_id': 2,
        'pricelist_id': 1,
        'order_line': sale_order_lines,
        'fiscal_operation_category_id': 1,
        'fiscal_position': 1
        })

    assert sale_order_obj.browse(oerp.cr, 1, [order_id])[0].id == order_id
