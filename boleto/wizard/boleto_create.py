# -*- coding: utf-8 -*-

from osv import osv, fields


class boleto_create(osv.osv_memory):
    _name = 'boleto.create'

    _columns = {
        'success': fields.char(u'Sucesso', size=20),
        'error': fields.char(u'Erros', size=20),
        }

    def create(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice').browse(cr, uid, ids)
        rec_ids = inv_obj._get_receivable_lines(cr, uid, ids)
        for move_line in self.pool.get('account.move.line').browse(cr, uid, rec_ids):
            pass

        success = ''
        error = ''

        return {'success': success, 'error': error}

boleto_create('account.invoice.boletos_create')
