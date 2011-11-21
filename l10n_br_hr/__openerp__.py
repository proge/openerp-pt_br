# -*- coding: utf-8 -*-

{
    "name": "Brazilian Localisation Human Resources",
    "version": "0.1",
    "author": "Proge",
    "category": "Localisation",
    "website": "http://www.proge.com.br",
    "description": """
    Brazilian Localization of the Human Resources module.
    """,
    'depends': ['l10n_br', 'hr'],
    'init_xml': [],
    'update_xml': [
        # TODO: Security
        'hr_view.xml',
        # TODO: Data
        ],
    'demo_xml': [],  # TODO: Demo data
    'test': [],  # TODO: Functional tests
    'installable': True,
    'active': False,
}
