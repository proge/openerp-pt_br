# -*- encoding: utf-8 -*-

{
    'name': 'Brazilian Localization Sale',
    'description': 'Brazilian Localization for Sale',
    'category': 'Localisation',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': [
        'l10n_br_account',
        'l10n_br_stock',
        'sale',
        'account_fiscal_position_rule_sale',
        ],
    'init_xml': [],
    'update_xml': [
        'sale_view.xml',
        ],
    'installable': True
}
