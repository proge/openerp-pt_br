# -*- coding: utf-8 -*-

from osv import fields, osv


class res_partner(osv.osv):
    _inherit = 'res.partner'
    _columns = {
        'boleto_config': fields.many2one('boleto.partner_config', u'Configurações de Boleto')
    }

res_partner()
