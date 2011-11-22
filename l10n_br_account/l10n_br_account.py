# -*- encoding: utf-8 -*-

from osv import osv, fields


class l10n_br_account_cfop(osv.osv):
    _name = 'l10n_br_account.cfop'
    _description = 'CFOP - Código Fiscal de Operações e Prestações'

    def name_search(self, cr, user, name, args=None, operator='ilike', context=None, limit=80):
        if not args:
            args = []
        if context is None:
            context = {}
        ids = self.search(cr, user, ['|', ('name', operator, name), ('code', operator, name)] + args, limit=limit, context=context)
        return self.name_get(cr, user, ids, context)

    def name_get(self, cr, uid, ids, context=None):
        if not len(ids):
            return []
        if isinstance(ids, (int, long)):
            ids = [ids]
        reads = self.read(cr, uid, ids, ['name', 'code'], context, load='_classic_write')
        return [(x['id'], (x['code'] and x['code'] or '') + (x['name'] and ' - ' + x['name'] or '')) \
                for x in reads]

    _columns = {
        'code': fields.char('Código', size=4, requeried=True),
        'name': fields.char('Nome', size=256, requeried=True),
        'small_name': fields.char('Nome Reduzido', size=32, requeried=True),
        'description': fields.text('Descrição'),
        'type': fields.selection([('input', 'Entrada'), ('output', 'Saida')], 'Tipo', requeried=True),
        'parent_id': fields.many2one('l10n_br_account.cfop', 'CFOP Pai'),
        'child_ids': fields.one2many('l10n_br_account.cfop', 'parent_id', 'CFOP Filhos'),
        'internal_type': fields.selection([('view', 'Visualização'), ('normal', 'Normal')], 'Tipo Interno', required=True),
                }
    _defaults = {
                 'internal_type': 'normal',
                 }

l10n_br_account_cfop()


class l10n_br_account_service_type(osv.osv):
    _name = 'l10n_br_account.service.type'
    _description = 'Cadastro de Operações Fiscais de Serviço'
    _columns = {
                'code': fields.char('Código', size=16, required=True),
                'name': fields.char('Descrição', size=256, required=True),
                'parent_id': fields.many2one('l10n_br_account.service.type', 'Tipo de Serviço Pai'),
                'child_ids': fields.one2many('l10n_br_account.service.type', 'parent_id', 'Tipo de Serviço Filhos'),
                'country_id': fields.many2one('res.country', 'País'),
                'state_id': fields.many2one('res.country.state', 'Estado'),
                'l10n_br_city_id': fields.many2one('l10n_br_base.city', 'Município'),
                'internal_type': fields.selection([('view', 'Visualização'), ('normal', 'Normal')], 'Tipo Interno', required=True),
                }
    _defaults = {
                 'internal_type': 'normal',
                 }

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

l10n_br_account_service_type()


class l10n_br_account_fiscal_document(osv.osv):
    _name = 'l10n_br_account.fiscal.document'
    _description = 'Tipo de Documento Fiscal'
    _columns = {
        'code': fields.char('Codigo', size=8, required=True),
        'name': fields.char('Descrição', size=64),
        'nfe': fields.boolean('NFe'),
    }
l10n_br_account_fiscal_document()


class l10n_br_account_cst(osv.osv):
    _name = 'l10n_br_account.cst'
    _description = 'Código de Situação Tributária'
    _columns = {
                'code': fields.char('Codigo', size=8, required=True),
                'name': fields.char('Descrição', size=64),
                'tax_code_id': fields.many2one('account.tax.code', 'Modelo do Imposto', required=True),
                }

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

l10n_br_account_cst()


class l10n_br_account_fiscal_operation_category(osv.osv):
    _name = 'l10n_br_account.fiscal.operation.category'
    _description = 'Categoria de Operações Fiscais'
    _columns = {
        'code': fields.char('Código', size=24, required=True),
        'name': fields.char('Descrição', size=64),
        'type': fields.selection([('input', 'Entrada'), ('output', 'Saida')], 'Tipo'),
        'journal_ids': fields.many2many('account.journal', 'l10n_br_account_fiscal_operation_category_rel', 'fiscal_operation_category_id', 'journal_id', 'Consolidated Children', domain="[('company_id','=',user.company_id)]" ),
        'use_sale' : fields.boolean('Usado em Vendas'),
        'use_invoice' : fields.boolean('Usado nas Notas Fiscais'),
        'use_purchase' : fields.boolean('Usado nas Compras'),
        'use_picking' : fields.boolean('Usado nas Listas de Separações'),
        'fiscal_type': fields.selection([('product', 'Produto'), ('service', 'Serviço')], 'Tipo Fiscal', requeried=True),
        }
    _defaults = {
        'type': 'output',
        'fiscal_type': 'product',
        }

l10n_br_account_fiscal_operation_category()


class l10n_br_account_fiscal_operation(osv.osv):
    _name = 'l10n_br_account.fiscal.operation'
    _description = 'Operações fiscais'
    _columns = {
        'code': fields.char('Código', size=16, required=True),
        'name': fields.char('Descrição', size=64),
        'type': fields.selection([('input', 'Entrada'), ('output', 'Saida')], 'Tipo', requeried=True),
        'fiscal_operation_category_id': fields.many2one('l10n_br_account.fiscal.operation.category', 'Categoria', domain="[('type','=',type)]", requeried=True),
        'cfop_id': fields.many2one('l10n_br_account.cfop', 'CFOP', requeried=True),
        'fiscal_document_id': fields.many2one('l10n_br_account.fiscal.document', 'Documento Fiscal', requeried=True),
        'fiscal_operation_line': fields.one2many('l10n_br_account.fiscal.operation.line', 'fiscal_operation_id', 'Fiscal Operation Lines'),
        'cfop_id': fields.many2one('l10n_br_account.cfop', 'CFOP'),
        'service_type_id': fields.many2one('l10n_br_account.service.type', 'Tipo de Serviço'),
        'use_sale': fields.boolean('Usado em Vendas'),
        'use_invoice': fields.boolean('Usado nas Notas Fiscais'),
        'use_purchase': fields.boolean('Usado nas Compras'),
        'use_picking': fields.boolean('Usado nas Listas de Separações'),
        'refund_fiscal_operation_id': fields.many2one('l10n_br_account.fiscal.operation', 'Op. Fiscal Devolução', domain="[('type','!=',type)]"),
        'note': fields.text('Observação'),
        'inv_copy_note': fields.boolean('Copiar Observação na Nota Fiscal'),
        'fiscal_type': fields.selection([('product', 'Produto'), ('service', 'Serviço')], 'Tipo Fiscal', domain="[('fiscal_type','=',fiscal_type)]", requeried=True),
        }
    _defaults = {
        'type': 'output',
        'fiscal_type': 'product',
        }

l10n_br_account_fiscal_operation()


class l10n_br_account_fiscal_operation_line(osv.osv):
    _name = 'l10n_br_account.fiscal.operation.line'
    _description = 'Linhas das operações ficais'
    _columns = {
        'company_id': fields.many2one('res.company', 'Empresa', requeried=True),
        'fiscal_classification_id': fields.many2one('account.product.fiscal.classification', 'NCM', domain="['|',('company_id','=',False),('company_id','=',company_id)]" ),
        'tax_code_id': fields.many2one('account.tax.code', 'Código do Imposto', requeried=True, domain="['|',('company_id','=',False),('company_id','=',company_id)]"),
        'cst_id': fields.many2one('l10n_br_account.cst', 'Código de Situação Tributária', requeried=True),
        'fiscal_operation_id': fields.many2one('l10n_br_account.fiscal.operation', 'Fiscal Operation Ref', ondelete='cascade', select=True),
        }

l10n_br_account_fiscal_operation_line()


class l10n_br_account_document_serie(osv.osv):
    _name = 'l10n_br_account.document.serie'
    _description = 'Serie de documentos fiscais'
    _columns = {
        'code': fields.char('Código', size=3, required=True),
        'name': fields.char('Descrição', size=64),
        'fiscal_document_id': fields.many2one('l10n_br_account.fiscal.document', 'Documento Fiscal', requeried=True),
        'company_id': fields.many2one('res.company', 'Empresa', requeried=True),
        'active': fields.boolean('Ativo'),
        'fiscal_type': fields.selection([('product', 'Produto'), ('service', 'Serviço')], 'Tipo Fiscal', requeried=True),
        }
    _defaults = {
        'active': True,
        }

l10n_br_account_document_serie()


class l10n_br_account_partner_fiscal_type(osv.osv):
    _name = 'l10n_br_account.partner.fiscal.type'
    _description = 'Tipo Fiscal de Parceiros'
    _columns = {
        'code': fields.char('Código', size=16, required=True),
        'name': fields.char('Descrição', size=64),
        'tipo_pessoa': fields.selection([('F', 'Física'), ('J', 'Jurídica')], 'Tipo de pessoa', required=True),
        'icms': fields.boolean('Recupera ICMS'),
        'ipi': fields.boolean('Recupera IPI'),
        }

l10n_br_account_partner_fiscal_type()


class l10n_br_account_cnae(osv.osv):
    _name = 'l10n_br_account.cnae'
    _description = 'Cadastro de CNAE'
    _columns = {
        'code': fields.char('Código', size=16, required=True),
        'name': fields.char('Descrição', size=64, required=True),
        'version': fields.char('Versão', size=16, required=True),
        'parent_id': fields.many2one('l10n_br_account.cnae', 'CNAE Pai'),
        'child_ids': fields.one2many('l10n_br_account.cnae', 'parent_id', 'CNAEs Filhos'),
        'internal_type': fields.selection([('view', 'Visualização'), ('normal', 'Normal')], 'Tipo Interno', required=True),
        }
    _defaults = {
        'internal_type': 'normal',
        }

    def name_get(self, cr, uid, ids, context=None):
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name', 'code'], context=context)
        res = []
        for record in reads:
            name = record['name']
            if record['code']:
                name = record['code'] + ' - ' + name
            res.append((record['id'], name))
        return res

l10n_br_account_cnae()
