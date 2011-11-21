# -*- encoding: utf-8 -*-

from osv import osv, fields
from tools.translate import _


class stock_picking(osv.osv):
    _inherit = "stock.picking"
    _description = "Picking List"
    _columns = {
        'fiscal_operation_category_id': fields.many2one('l10n_br_account.fiscal.operation.category', 'Categoria'),
        'fiscal_operation_id': fields.many2one('l10n_br_account.fiscal.operation', 'Operação Fiscal', domain="[('fiscal_operation_category_id','=',fiscal_operation_category_id)]"),
        'fiscal_position': fields.many2one('account.fiscal.position', 'Posição Fiscal', domain="[('fiscal_operation_id','=',fiscal_operation_id)]"),
        }

    def common_event(self, cr, uid, ids, context, partner_id, company_id, fiscal_operation_category_id):
        result = {'value': {}}

        if not partner_id or not company_id or not fiscal_operation_category_id:
            result['value']['fiscal_position'] = False
            result['value']['fiscal_operation_id'] = False
            return result

        partner_addr_default = self.pool.get('res.partner.address').browse(cr, uid, [partner_id])[0]

        to_country = partner_addr_default.country_id.id
        to_state = partner_addr_default.state_id.id

        obj_partner = self.pool.get('res.partner').browse(cr, uid, [partner_addr_default.partner_id.id])[0]
        partner_fiscal_type = obj_partner.partner_fiscal_type_id.id
        fiscal_position = obj_partner.property_account_position

        if fiscal_position:
            result['value']['fiscal_position'] = fiscal_position
            result['value']['fiscal_operation_id'] = obj_partner.property_account_position.fiscal_operation_id and obj_partner.property_account_position.fiscal_operation_id.id
            return result

        obj_company = self.pool.get('res.company').browse(cr, uid, [company_id])[0]

        company_addr = self.pool.get('res.partner').address_get(cr, uid, [obj_company.partner_id.id], ['default'])
        company_addr_default = self.pool.get('res.partner.address').browse(cr, uid, [company_addr['default']])[0]

        from_country = company_addr_default.country_id.id
        from_state = company_addr_default.state_id.id

        fsc_pos_id = self.pool.get('account.fiscal.position.rule').search(cr, uid, [
            '&',
            ('company_id', '=', company_id), ('use_picking', '=', True),
            ('fiscal_operation_category_id', '=', fiscal_operation_category_id),
            '|', ('from_country', '=', from_country), ('from_country', '=', False),
            '|', ('to_country', '=', to_country), ('to_country', '=', False),
            '|', ('from_state', '=', from_state), ('from_state', '=', False),
            '|', ('to_state', '=', to_state), ('to_state', '=', False),
            '|', ('partner_fiscal_type_id', '=', False), ('partner_fiscal_type_id', '=', partner_fiscal_type)])

        if fsc_pos_id:
            obj_fpo_rule = self.pool.get('account.fiscal.position.rule').browse(cr, uid, fsc_pos_id)[0]
            result['value']['fiscal_position'] = obj_fpo_rule.fiscal_position_id.id
            result['value']['fiscal_operation_id'] = obj_fpo_rule.fiscal_position_id.fiscal_operation_id.id

        return result

    def onchange_partner_in(self, cr, uid, context=None, partner_id=None, company_id=None, fiscal_operation_category_id=None):
        # TODO review this, maybe we should not throw the return away
        super(stock_picking, self).onchange_partner_in(cr, uid, context, partner_id)
        return self.common_event(cr, uid, None, partner_id, company_id, fiscal_operation_category_id)

    def onchange_fiscal_operation_category_id(self, cr, uid, ids, partner_id, company_id=None, fiscal_operation_category_id=None):
        return self.common_event(cr, uid, ids, partner_id, company_id, fiscal_operation_category_id)

    def _invoice_line_hook(self, cr, uid, move_line, invoice_line_id):
        '''Call after the creation of the invoice line'''

        fiscal_operation_id = fiscal_operation_category_id = False

        if move_line.sale_line_id:
            fiscal_operation_id = move_line.sale_line_id.fiscal_operation_id or move_line.sale_line_id.order_id.fiscal_operation_id
            fiscal_operation_category_id = move_line.sale_line_id.fiscal_operation_category_id or move_line.sale_line_id.order_id.fiscal_operation_category_id

        if move_line.purchase_line_id:
            fiscal_operation_id = move_line.purchase_line_id.fiscal_operation_id or move_line.purchase_line_id.order_id.fiscal_operation_id
            fiscal_operation_category_id = move_line.purchase_line_id.fiscal_operation_category_id or move_line.purchase_line_id.order_id.fiscal_operation_category_id

        if not move_line.purchase_line_id and not move_line.sale_line_id:
            fiscal_operation_id = move_line.picking_id.fiscal_operation_id
            fiscal_operation_category_id = move_line.picking_id.fiscal_operation_category_id

        if not fiscal_operation_id:
            raise osv.except_osv(_(u'Movimentação sem operação fiscal !'), _(u"Não existe operação fiscal para uma linha de vendas relacionada ao produto %s .") % (move_line.product_id.name))

        self.pool.get('account.invoice.line').write(cr, uid, invoice_line_id, {
            'cfop_id': fiscal_operation_id.cfop_id.id,
            'fiscal_operation_category_id': fiscal_operation_category_id.id,
            'fiscal_operation_id': fiscal_operation_id.id,
            })

        return super(stock_picking, self)._invoice_line_hook(cr, uid, move_line, invoice_line_id)

    def _invoice_hook(self, cr, uid, picking, invoice_id):
        '''Call after the creation of the invoice'''
        if not picking.sale_id and not picking.purchase_id:
            salesman = uid

        if picking.sale_id:
            salesman = picking.sale_id.user_id.id

        if picking.purchase_id:
            salesman = picking.purchase_id.validator.id

        company_id = self.pool.get('res.company').browse(cr, uid, picking.company_id.id)
        if not company_id.document_serie_product_ids:
            raise osv.except_osv(_(u'Nenhuma série de documento fiscal !'), _(u"Empresa não tem uma série de documento fiscal cadastrada: '%s', você deve informar uma série no cadastro de empresas") % (picking.company_id.name,))

        comment = ''
        if picking.fiscal_operation_id.inv_copy_note:
            comment = picking.fiscal_operation_id.note

        if picking.note:
            comment += ' - ' + picking.note

        self.pool.get('account.invoice').write(cr, uid, invoice_id, {'fiscal_operation_category_id': picking.fiscal_operation_category_id.id,
                                                                     'fiscal_operation_id': picking.fiscal_operation_id.id,
                                                                     'cfop_id': picking.fiscal_operation_id.cfop_id.id,
                                                                     'fiscal_document_id': picking.fiscal_operation_id.fiscal_document_id.id,
                                                                     'fiscal_position': picking.fiscal_position.id,
                                                                     'document_serie_id': company_id.document_serie_product_ids[0].id,
                                                                     'user_id': salesman,
                                                                     'comment': comment})

        return super(stock_picking, self)._invoice_hook(cr, uid, picking, invoice_id)

stock_picking()
