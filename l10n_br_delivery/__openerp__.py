# -*- encoding: utf-8 -*-

{
    'name': 'Delivery for Brazilian Localization',
    'description': 'Extend delivery module for Brazilian Localization',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': [
        'l10n_br_sale',
        'delivery',
        ],
    'init_xml': [],
    'update_xml':  [
        'account_invoice_view.xml',
        'delivery_view.xml',
        'stock_view.xml',
        ],
    'category': 'Localisation',
    'active': False,
    'installable': True
}
