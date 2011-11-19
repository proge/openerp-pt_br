# -*- coding: utf-8 -*-

from osv import osv, fields


class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'banco': fields.selection([('bb', 'Banco do Brasil'), ('real', 'Banco Real')], 'Banco'),
        'agencia_cedente': fields.char('Agencia', size=6),
        'conta_cedente': fields.char('Conta', size=8),
        'nosso_numero': fields.integer(u'Nosso Número'),
    }

res_company()
