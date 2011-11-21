# -*- encoding: utf-8 -*-

{
    'name': 'Brazilian Localization',
    'description': 'Brazilian Localization',
    'category': 'Localisation',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': [
        'l10n_br_account',
        'stock',
        'account_fiscal_position_rule_stock',
        ],
    'init_xml': [],
    'update_xml': [
        'stock_view.xml',
        'wizard/stock_invoice_onshipping_view.xml',
        ],
    'installable': True
}
