# -*- encoding: utf-8 -*-

from osv import osv, fields


class account_fiscal_position_common(object):
    _columns = {
        'partner_fiscal_type_id': fields.many2one('l10n_br_account.partner.fiscal.type', 'Tipo Fiscal do Parceiro'),
        'fiscal_operation_category_id': fields.many2one('l10n_br_account.fiscal.operation.category', 'Categoria', requeried=True),
        'use_picking': fields.boolean('Use in Picking'),
        }


class account_fiscal_position_rule_template(account_fiscal_position_common, osv.osv):
    _inherit = 'account.fiscal.position.rule.template'

account_fiscal_position_rule_template()


class account_fiscal_position_rule(account_fiscal_position_common, osv.osv):
    _inherit = 'account.fiscal.position.rule'

account_fiscal_position_rule()
