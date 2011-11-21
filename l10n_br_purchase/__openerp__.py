# -*- coding: utf-8 -*-

{
    'name': 'Brazilian Localization Purchase',
    'description': 'Brazilian Localization for Purchase',
    'category': 'Localisation',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': [
        'l10n_br_account',
        'l10n_br_stock',
        'purchase',
        'account_fiscal_position_rule_purchase',
        ],
    'init_xml': [
        'data/l10n_br_purchase_data.xml',
        ],
    'update_xml': [
        'purchase_view.xml',
        'security/ir.model.access.csv',
        'security/l10n_br_purchase_security.xml',
        ],
    'installable': True
}
