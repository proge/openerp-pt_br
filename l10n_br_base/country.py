# -*- encoding: utf-8 -*-

from osv import osv, fields


class res_country(osv.osv):
    _inherit = 'res.country'
    _columns = {
        'bc_code': fields.char('Cód. BC', size=5),
        }

res_country()


class res_country_state(osv.osv):
    _inherit = 'res.country.state'
    _columns = {
        'ibge_code': fields.char('Cód. IBGE', size=2),
        }

res_country_state()
