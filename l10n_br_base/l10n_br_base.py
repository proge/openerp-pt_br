# -*- encoding: utf-8 -*-

from osv import osv, fields


class l10n_br_base_city(osv.osv):
    _name = 'l10n_br_base.city'
    _description = 'Municipios e Códigos do IBGE'
    _columns = {
        'name': fields.char('Nome', size=64, required=True),
        'state_id': fields.many2one('res.country.state', 'Estado', required=True),
        'ibge_code': fields.char('Codigo IBGE', size=7),
        }

l10n_br_base_city()


class l10n_br_base_cep(osv.osv):
    _name = 'l10n_br_base.cep'
    _rec_name = 'code'
    _columns = {
        'code': fields.char('CEP', size=8, required=True),
        'street_type': fields.char('Tipo', size=26),
        'street': fields.char('Logradouro', size=72),
        'district': fields.char('Bairro', size=72),
        'state_id': fields.many2one('res.country.state', 'Estado', required=True),
        'l10n_br_city_id': fields.many2one('l10n_br_base.city', 'Cidade', required=True, domain="[('state_id','=',state_id)]"),
    }

l10n_br_base_cep()
