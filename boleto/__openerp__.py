# -*- coding: utf-8 -*-

{
    "name": "Boletos",
    "version": "0.1",
    "author": "Proge",
    "category": "Account",
    "website": "http://proge.com.br",
    "description": """
    Module to create boletos
    """,
    'depends': ['l10n_br_account'],
    'init_xml': [],
    'update_xml': [
        # 'boleto_view.xml',
        'partner_view.xml',
        'res_company_view.xml',
        'wizard/boleto_create_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'installable': True,
    'active': False,
}
