# -*- encoding: utf-8 -*-

{
    'name': 'Brazilian Localization',
    'description': 'Brazilian Localization',
    'category': 'Localisation',
    'author': 'Akretion, OpenERP Brasil',
    'website': 'http://openerpbrasil.org',
    'version': '0.6',
    'depends': [
        'l10n_br',
        'l10n_br_base',
        'product',
        'account_fiscal_position_rule',
        'account_product_fiscal_classification'
        ],
    'init_xml': [
        # 'data/l10n_br_account.cst.csv',
        ],
    'update_xml': [
        'account_view.xml',
        'account_fiscal_position_rule_view.xml',
        'account_invoice_view.xml',
        'account_invoice_workflow.xml',
        'l10n_br_account_data.xml',
        'l10n_br_account_view.xml',
        'partner_view.xml',
        'product_view.xml',
        'res_company_view.xml',
        'security/ir.model.access.csv',
        'security/l10n_br_account_security.xml',
        'wizard/l10n_br_account_nfe_export_view.xml',
        'wizard/nfe_export_from_invoice_view.xml',
        ],
    'demo_xml': ['l10n_br_account_demo.xml'],
    'installable': True
}
