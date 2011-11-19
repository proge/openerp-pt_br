

def test_create_service_fiscal_operation_and_category(oerp):
    cfop_obj = oerp.pool.get('l10n_br_account.cfop')
    cfop_id = cfop_obj.search(oerp.cr, 1, [])[0]
    fiscal_doc_obj = oerp.pool.get('l10n_br_account.fiscal.document')
    fiscal_doc_id = fiscal_doc_obj.search(oerp.cr, 1, [('nfe', '=', 'TRUE')])[0]

    fopc_obj = oerp.pool.get('l10n_br_account.fiscal.operation.category')
    fopc_id = fopc_obj.create(oerp.cr, 1, {
        'code': 'isento',
        'name': 'isento',
        'type': 'output',
        'use_sale': 'TRUE',
        'use_invoice': 'TRUE',
        'fiscal_type': 'service'
        })

    assert fopc_obj.browse(oerp.cr, 1, [fopc_id])[0].id == fopc_id

    fop_obj = oerp.pool.get('l10n_br_account.fiscal.operation')
    fop_id = fop_obj.create(oerp.cr, 1, {
        'code': 'servico01',
        'name': 'servico01',
        'type': 'output',
        'fiscal_operation_category_id': fopc_id,
        'cfop_id': cfop_id,
        'fiscal_document_id': fiscal_doc_id,
        'use_sale': 'TRUE',
        'use_invoice': 'TRUE',
        'fiscal_type': 'service'
        })

    assert fop_obj.browse(oerp.cr, 1, [fop_id])[0].id == fop_id
