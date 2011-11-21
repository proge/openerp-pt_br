# -*- encoding: utf-8 -*-

from osv import osv, fields


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _description = "Picking List"
    _columns = {
        'vehicle_id': fields.many2one('l10n_br_delivery.carrier.vehicle', 'Veículo'),
        'incoterm': fields.many2one('stock.incoterms', 'Tipo do Frete', help="Incoterm which stands for 'International Commercial terms' implies its a series of sales terms which are used in the commercial transaction."),
        }

    def _invoice_hook(self, cr, uid, picking, invoice_id):
        '''Call after the creation of the invoice'''

        self.pool.get('account.invoice').write(cr, uid, invoice_id, {
            'partner_shipping_id': picking.address_id.id,
            'fiscal_operation_category_id': picking.fiscal_operation_category_id.id,
            'fiscal_operation_id': picking.fiscal_operation_id.id,
            'cfop_id': picking.fiscal_operation_id.cfop_id.id,
            'fiscal_document_id': picking.fiscal_operation_id.fiscal_document_id.id,
            'fiscal_position': picking.fiscal_position.id,
            'carrier_id': picking.carrier_id.id,
            'vehicle_id': picking.vehicle_id.id,
            'incoterm': picking.incoterm.id,
            'weight': picking.weight,
            'weight_net': picking.weight_net,
            'number_of_packages': picking.number_of_packages
            })

        return super(stock_picking, self)._invoice_hook(cr, uid, picking, invoice_id)

stock_picking()
