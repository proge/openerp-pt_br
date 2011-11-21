# -*- coding: utf-8 -*-

from osv import osv, fields
import base64


class l10n_br_account_nfe_export(osv.osv_memory):
    """ Exportar Nota Fiscal Eletrônica """

    _name = "l10n_br_account.nfe_export"
    _description = "Exportação de Nota Fiscal Eletrônica"
    _inherit = "ir.wizard.screen"
    _columns = {
        'file': fields.binary('Arquivo', readonly=True),
        'company_id': fields.many2one('res.company', 'Company'),
        'file_type': fields.selection([('xml', 'XML'), ('txt', 'TXT')], 'Tipo do Arquivo'),
        'import_status_draft': fields.boolean('Importar NFs com status em rascunho'),
        'state': fields.selection([('init', 'init'), ('done', 'done')], 'state', readonly=True),
        }
    _defaults = {
        'state': 'init',
        'company_id': lambda self, cr, uid, c: self.pool.get('res.company')._company_default_get(cr, uid, 'account.invoice', context=c),
        'file_type': 'txt',
        'import_status_draft': False,
        }

    def nfe_export(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, [], context=context)[0]

        inv_obj = self.pool.get('account.invoice')
        inv_ids = inv_obj.search(cr, uid, [('state', '=', 'sefaz_export'), ('nfe_export_date', '=', False), ('company_id', '=', data['company_id']), ('own_invoice', '=', True)])

        if data['file_type'] == 'xml':
            file = inv_obj.nfe_export_xml(cr, uid, inv_ids)
        else:
            file = inv_obj.nfe_export_txt(cr, uid, inv_ids)
        file_total = file

        self.write(cr, uid, ids, {'file': base64.b64encode(file_total), 'state': 'done'}, context=context)

        return False

l10n_br_account_nfe_export()
