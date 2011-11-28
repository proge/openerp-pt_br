# -*- encoding: utf-8 -*-

import pooler
from osv import fields, osv

_columns = {
    'domain': fields.char('Domain', size=32, help="This field is only used if you develop your own module allowing developers to create specific taxes in a custom domain."),
    'tax_discount': fields.boolean('Tax Discounted in Price', help="Mark it for (ICMS, PIS e etc.)."),
    'tax_include': fields.boolean('Include the Tax Amount in Price', help="Mark it to include the Tax Amount in Price."),
    }


class account_tax_code_template(osv.osv):
    _inherit = 'account.tax.code.template'
    _columns = _columns

account_tax_code_template()


class account_tax_code(osv.osv):
    _inherit = 'account.tax.code'
    _columns = _columns

account_tax_code()


def change_digit_tax(cr):
    res = pooler.get_pool(cr.dbname).get('decimal.precision').precision_get(cr, 1, 'Account')
    return (16, res + 2)


_columns_tax = {
    'tax_discount': fields.boolean('Tax Discounted in Price', help="Mark it for Brazilian legal Taxes(ICMS, PIS e etc.)."),
    'tax_add': fields.boolean('Add the Tax Amount in Price', help="Mark it to add the Tax Amount in Price."),
    'tax_include': fields.boolean('Include the Tax Amount in Price', help="Mark it to include the Tax Amount in Price."),
    'tax_retain': fields.boolean('Discount the Tax Amount in Price', help="Mark it to for clients who retain the Taxes."),
    'base_reduction': fields.float('Redution', required=True, digits_compute=change_digit_tax, help="Um percentual decimal em % entre 0-1."),
    'amount_mva': fields.float('MVA Percent', required=True, digits_compute=change_digit_tax, help="Um percentual decimal em % entre 0-1."),
    'type': fields.selection([('percent', 'Percentage'), ('fixed', 'Fixed Amount'),
                              ('none', 'None'), ('code', 'Python Code'),
                              ('balance', 'Balance'), ('quantity', 'Quantity')], 'Tax Type', required=True,
                             help="The computation method for the tax amount."),
    }

_defaults_tax = {
    'base_reduction': 0,
    'amount_mva': 0,
    }


class account_tax_common(object):
    tax_code_name = 'account.tax.code.template'

    def onchange_tax_code_id(self, cr, uid, ids, tax_code_id, context=None):
        result = {'value': {}}
        if not tax_code_id:
            return result

        tax_code = self.pool.get(self.tax_code_name).browse(cr, uid, tax_code_id)
        if tax_code:
            result['value']['tax_discount'] = tax_code.tax_discount
            result['value']['tax_include'] = tax_code.tax_include
            result['value']['domain'] = tax_code.domain

        return result


class account_tax_template(account_tax_common, osv.osv):
    _inherit = 'account.tax.template'
    tax_code_name = 'account.tax.code.template'
    _columns = _columns_tax
    _defaults = _defaults_tax

account_tax_template()


class account_tax(account_tax_common, osv.osv):
    _inherit = 'account.tax'
    tax_code_name = 'account.tax.code'
    _columns = _columns_tax
    _defaults = _defaults_tax

account_tax()


class account_journal(osv.osv):
    _inherit = "account.journal"
    _columns = {
        'internal_sequence': fields.many2one('ir.sequence', 'Internal Sequence'),
        }

account_journal()


class wizard_multi_charts_accounts(osv.osv_memory):
    _inherit = 'wizard.multi.charts.accounts'

    def execute(self, cr, uid, ids, context=None):
        super(wizard_multi_charts_accounts, self).execute(cr, uid, ids, context)

        obj_multi = self.browse(cr, uid, ids[0])
        obj_acc_tax = self.pool.get('account.tax')
        obj_tax_code = self.pool.get('account.tax.code')
        obj_tax_code_tmp = self.pool.get('account.tax.code.template')

        # Creating Account
        tax_code_root_id = obj_multi.chart_template_id.tax_code_root_id.id
        company_id = obj_multi.company_id.id

        children_tax_code_template = obj_tax_code_tmp.search(cr, uid, [('parent_id', 'child_of', [tax_code_root_id])], order='id')
        children_tax_code_template.sort()
        for tax_code_template in obj_tax_code_tmp.browse(cr, uid, children_tax_code_template, context=context):
            tax_code_id = obj_tax_code.search(cr, uid, [('code', '=', tax_code_template.code),
                                                        ('company_id', '=', company_id)])
            if tax_code_id:
                obj_tax_code.write(cr, uid, tax_code_id, {'domain': tax_code_template.domain,
                                                          'tax_discount': tax_code_template.tax_discount,
                                                          'tax_include': tax_code_template.tax_include})

        tax_ids = obj_acc_tax.search(cr, uid, [('company_id', '=', company_id)])
        for tax in obj_acc_tax.browse(cr, uid, tax_ids, context=context):
            if tax.tax_code_id:
                obj_acc_tax.write(cr, uid, tax.id, {'domain': tax.tax_code_id.domain,
                                                    'tax_discount': tax.tax_code_id.tax_discount,
                                                    'tax_include': tax.tax_code_id.tax_include})

wizard_multi_charts_accounts()
