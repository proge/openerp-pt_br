# -*- coding: utf-8 -*-

from osv import osv, fields


class res_company(osv.osv):
    _inherit = "res.company"
    _columns = {
        'boleto_company_config_ids': fields.many2many('boleto.company_config', 'res_company_boleto_rel', 'company_id', 'boleto_company_config_id', u'Configurações de Boleto da Empresa')
        }

res_company()
