# -*- coding: utf-8 -*-

from osv import fields, osv


class boleto_partner_config(osv.osv):
    """Boleto Partner Configuration"""
    _name = 'boleto.partner_config'
    _columns = {
        'name': fields.char('Name', size=20, required=True),
        'carteira': fields.char('Carteira', size=20, required=True),
#        'juros': fields.float('Juros', digits=(1, 6)),
#        'multa': fields.float('Multa', digits=(12, 6)),
        'instrucoes': fields.text(u'Instruções'),
        }

boleto_partner_config()


class boleto_company_config(osv.osv):
    """Boleto Company Configuration"""
    _name = 'boleto.company_config'
    _columns = {
        'name': fields.char('Name', size=20, required=True),
        'banco': fields.selection([('bb', 'Banco do Brasil'), ('real', 'Banco Real'), ('bradesco', 'Banco Bradesco'), ('caixa', 'Banco Caixa Federal')], 'Banco', required=True),
        'agencia_cedente': fields.char('Agencia', size=6, required=True),
        'conta_cedente': fields.char('Conta', size=8, required=True),
        'convenio': fields.char(u'Convenio', size=8, required=True),
        'nosso_numero': fields.integer(u'Nosso Número'),
        }

boleto_company_config()


class boleto_boleto(osv.osv):
    """Boleto"""
    _name = 'boleto.boleto'
    _columns = {
        'name': fields.char('Name', size=20, required=True),
        # do cliente
        'carteira': fields.char('Carteira', size=10),
#        'juros': fields.float('Juros', digits=(12, 6)),
#        'multa': fields.float('Multa', digits=(12, 6)),
        'instrucoes': fields.text(u'Instruções'),
        'sacado': fields.many2one('res.partner', 'Sacado'),
        # da empresa
        'banco': fields.selection([('bb', 'Banco do Brasil'), ('real', 'Banco Real'), ('bradesco', 'Banco Bradesco'), ('caixa', 'Banco Caixa Federal')], 'Banco'),
        'agencia_cedente': fields.char('Agencia', size=6),
        'conta_cedente': fields.char('Conta', size=8),
        'convenio': fields.char('Convenio', size=8),
        'nosso_numero': fields.integer(u'Nosso Número'),
        'cedente': fields.many2one('res.company', 'Empresa'),
        # da fatura
        'move_line_id': fields.many2one('account.move.line', 'Move Line'),
        'data_vencimento': fields.date('Data do Vencimento'),
        'data_documento': fields.date('Data do Documento'),
        'data_processamento': fields.date('Data do Processamento'),
        'valor': fields.float('Valor', digits=(12, 6)),
        'numero_documento': fields.char(u'Número do Documento', size=20),
        'endereco': fields.char(u'Endereço', size=20),
        }

boleto_boleto()
