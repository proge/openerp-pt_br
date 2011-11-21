# -*- encoding: utf-8 -*-

from osv import fields, osv
import decimal_precision as dp
from tools.translate import _


class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'carrier_id': fields.many2one("delivery.carrier", "Carrier", readonly=True, states={'draft': [('readonly', False)]}),
        'vehicle_id': fields.many2one('l10n_br_delivery.carrier.vehicle', 'Veículo', readonly=True, states={'draft': [('readonly', False)]}),
        'incoterm': fields.many2one('stock.incoterms', 'Tipo do Frete', readonly=True, states={'draft': [('readonly', False)]}, help="Incoterm which stands for 'International Commercial terms' implies its a series of sales terms which are used in the commercial transaction."),
        'weight': fields.float('Gross weight', help="The gross weight in Kg.", readonly=True, states={'draft': [('readonly', False)]}),
        'weight_net': fields.float('Net weight', help="The net weight in Kg.", readonly=True, states={'draft': [('readonly', False)]}),
        'number_of_packages': fields.integer('Volume', readonly=True, states={'draft': [('readonly', False)]}),
        'amount_insurance': fields.float('Valor do Seguro', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft': [('readonly', False)]}),
        'amount_costs': fields.float('Outros Custos', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft': [('readonly', False)]}),
        'amount_freight': fields.float('Frete', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft': [('readonly', False)]}),
        }

    def nfe_check(self, cr, uid, ids, context=None):
        res = super(account_invoice, self).nfe_check(cr, uid, ids)
        strErro = u''
        for inv in self.browse(cr, uid, ids):
            #Transportadora
            if inv.carrier_id:

                if not inv.carrier_id.partner_id.legal_name:
                    strErro = u'Transportadora - Razão Social\n'

                if not inv.carrier_id.partner_id.cnpj_cpf:
                    strErro = u'Transportadora - CNPJ/CPF\n'

            #Dados do Veiculo
            if inv.vehicle_id:

                if not inv.vehicle_id.plate:
                    strErro = u'Transportadora / Veículo - Placa\n'

                if not inv.vehicle_id.plate.state_id.code:
                    strErro = u'Transportadora / Veículo - UF da Placa\n'

                if not inv.vehicle_id.rntc_code:
                    strErro = u'Transportadora / Veículo - RNTC\n'
        if strErro:
            raise osv.except_osv(_('Error !'), _(u"Validação da Nota fiscal:\n '%s'") % (strErro,))

        return res

account_invoice()
