# -*- encoding: utf-8 -*-

from osv import osv, fields


class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        'fiscal_category_operation_default_ids': fields.one2many('l10n_br_account.product.operation.category', 'product_id', 'Categoria de Operação Fiscal Padrões'),
        'fiscal_type': fields.selection([('product', 'Produto'), ('service', 'Serviço')], 'Tipo Fiscal', requeried=True),
        }
    _defaults = {
        'fiscal_type': 'product',
        }

product_product()


class l10n_br_account_product_fiscal_operation_category(osv.osv):
    _name = 'l10n_br_account.product.operation.category'
    _columns = {
        'fiscal_operation_category_source_id': fields.many2one('l10n_br_account.fiscal.operation.category', 'Categoria de Origem'),
        'fiscal_operation_category_destination_id': fields.many2one('l10n_br_account.fiscal.operation.category', 'Categoria de Destino'),
        'product_id': fields.many2one('product.product', 'Produto', ondelete='cascade'),
        }

l10n_br_account_product_fiscal_operation_category()
