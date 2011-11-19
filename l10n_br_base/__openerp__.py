# -*- encoding: utf-8 -*-

{
    'name': 'Brazilian Localization Base',
    'description': 'Brazilian Localization Base',
    'category': 'Localisation',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': ['l10n_br'],
    'init_xml': [
        'res.country.state.csv',
        'res.bank.csv',
        'l10n_br_base.city.csv',
        ],
    'update_xml': [
    'l10n_br_base_data.xml',
        'l10n_br_base_view.xml',
        'country_view.xml',
        'partner_view.xml',
        'security/ir.model.access.csv',
        'security/l10n_br_base_security.xml',
        ],
    'demo_xml': ['l10n_br_base_demo.xml'],
    'installable': True
}
