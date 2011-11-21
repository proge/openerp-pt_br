# -*- encoding: utf-8 -*-

{
    "name": "Brazilian Localisation Data Extension for Account",
    "description": "Brazilian Localisation Data Extension for Account",
    "author": "Akretion, OpenERP Brasil",
    "version": "0.1",
    "depends": [
        "l10n_br_account",
        ],
    'init_xml': [
        #Arquivos com dados Fiscais
        'l10n_br_account.cfop.csv',
        'l10n_br_account.fiscal.document.csv',
        'account_product_fiscal_classification_data.xml',
        'l10n_br_account.cnae.csv',
        'l10n_br_account.service.type.csv',
        ],
    "update_xml": [],
    'demo_xml': ['l10n_br_account_demo.xml'],
    "category": "Localisation",
    "active": False,
    "installable": True
}
