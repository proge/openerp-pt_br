# -*- encoding: utf-8 -*-

{
    'name': 'Brazilian Localization',
    'description': 'Brazilian Localization',
    'category': 'Localisation/Account Charts',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': ['account', 'account_chart'],
    'init_xml': [
        'data/account.account.type.csv',
        'data/account.tax.code.template.csv',
        'data/account.account.template.csv',
        'data/l10n_br_account_chart_template.xml',
        'data/account_tax_template.xml'
        ],
    'update_xml': [
        'account_view.xml',
    ],
    'installable': True,
    'certificate': '001280994939126801405',
}
