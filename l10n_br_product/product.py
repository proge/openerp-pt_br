# -*- encoding: utf-8 -*-

from osv import osv, fields


class product_product(osv.osv):
    _inherit = "product.product"
    _columns = {
        'origin': fields.selection((('0', 'Nacional'),
                                    ('1', 'Internacional'),
                                    ('2', 'Inter. Adiquirido Internamente')), 'Origem'),
        }

product_product()
