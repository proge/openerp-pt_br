# -*- encoding: utf-8 -*-
#################################################################################
#                                                                               #
# Copyright (C) 2011  Renato Lima - Akretion, Vinicius Dittgen - Proge.com.br   #
#                                                                               #
#This program is free software: you can redistribute it and/or modify           #
#it under the terms of the GNU General Public License as published by           #
#the Free Software Foundation, either version 3 of the License, or              #
#(at your option) any later version.                                            #
#                                                                               #
#This program is distributed in the hope that it will be useful,                #
#but WITHOUT ANY WARRANTY; without even the implied warranty of                 #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                  #
#GNU General Public License for more details.                                   #
#                                                                               #
#You should have received a copy of the GNU General Public License              #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.          #
#################################################################################

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from operator import itemgetter

import netsvc
import pooler
from osv import fields, osv
import decimal_precision as dp
from tools.misc import currency
from tools.translate import _
from tools import config

class account_journal(osv.osv):
    
    _inherit = 'account.journal'
    
    _columns = {
                'revenue_expense' : fields.boolean('Gera Financeiro'),
                }
    
account_journal()

class account_tax(osv.osv):
    _inherit = 'account.tax'
  
  
    def compute_all(self, cr, uid, taxes, price_unit, quantity, address_id=None, product=None, partner=None):
        """
        RETURN: {
                'total': 0.0,                 # Total without taxes
                'total_included': 0.0,        # Total with taxes
                'total_tax_discount': 0.0,    # Total Tax Discounts
                'taxes': []                   # List of taxes, see compute for the format
                    'total_base': 0.0,            # Total Base by tax
            }
        """
        totaldc = 0.0 
        totalbr = 0.0
        
        icms_base = 0
        icms_value = 0
        icms_percent = 0
        ipi_base = 0
        ipi_value = 0
        ipi_percent = 0
        
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
        totalin = totalex = round(price_unit * quantity, precision)
        tin = [] #tax_include
        tad = [] #tax_add
        tre = [] #tax_retain
        pin = [] #price_include        
        ntax = [] #normal tax 
        
        for tax in taxes:
            if tax.tax_discount: 
                if tax.tax_include:
                    tin.append(tax)
                elif tax.tax_retain:
                    tax.amount = (tax.amount * -1)
                    tre.append(tax)
                elif tax.tax_add:
                    tad.append(tax)
            elif tax.price_include:
                pin.append(tax)
            else:
                ntax.append(tax)

        pin = self.compute_inv(cr, uid, pin, price_unit, quantity, address_id=address_id, product=product, partner=partner)
        for r in pin:
                totalex -= r.get('amount', 0.0)
        totlex_qty = 0.0
        try:
            totlex_qty=totalex/quantity
        except:
            pass

        tin = self.l10n_br_compute_inv(cr, uid, tin, price_unit, quantity, address_id=address_id, product=product, partner=partner)
        
        all_tad = tad + ntax + tre
        all_tad = self._l10n_br_compute(cr, uid, all_tad, totlex_qty, quantity, address_id=address_id, product=product, partner=partner)
#        tre = self._l10n_br_compute(cr, uid, tre, totlex_qty, quantity, address_id=address_id, product=product, partner=partner)
        for r in all_tad:
            totalin += r.get('amount', 0.0)
#        for r in tre:
#            totalin += r.get('amount', 0.0)
            
        tax_obj = self.pool.get('account.tax')        
        res_taxes = pin + tin + all_tad       
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Account')
 
        for tax in res_taxes:

            tax_brw = tax_obj.browse(cr, uid, tax['id'])
            
            if tax_brw.type == 'quantity':
                tax['amount'] = round((quantity * product.weight_net) * tax_brw.amount, precision)
            
            if tax_brw.tax_discount:
                if tax_brw.base_reduction <> 0:
                    tax['amount'] = round(tax['amount'] * (1 - tax_brw.base_reduction), precision)    

                totaldc += tax['amount']
            
            if tax_brw.amount <> 0:
                if tax_brw.include_base_amount:
                    tax['total_base'] = tax['price_unit']
                else:
                    tax['total_base'] = round(totalex * (1 - tax_brw.base_reduction), precision)
            else:
                tax['total_base'] = 0
            
            #Guarda o valor do icms para ser usado para calcular a st 
            if tax_brw.domain == 'icms':
                icms_base = tax['total_base']
                icms_value = tax['amount']
                icms_percent = tax_brw.amount
            
            #Guarda o valor do ipi para ser usado para calcular a st 
            if tax_brw.domain == 'ipi':
                ipi_base = tax['total_base']
                ipi_value = tax['amount']
                ipi_percent = tax_brw.amount
            
        for tax_sub in res_taxes:
            tax_brw_sub = tax_obj.browse(cr, uid, tax_sub['id'])
            if tax_brw_sub.domain == 'icmsst':
                tax_sub['total_base'] += (totalex + ipi_value) * (1 + tax_brw_sub.amount_mva)
                tax_sub['amount'] += (((totalex + ipi_value)  * (1 + tax_brw_sub.amount_mva)) * icms_percent) - icms_value 

        return {
            'total': totalex,
            'total_included': totalin,
            'total_tax_discount': totaldc,
            'taxes': res_taxes,
            }
        
        
    def _l10n_br_compute(self, cr, uid, taxes, price_unit, quantity, address_id=None, product=None, partner=None):
        """
        Compute tax values for given PRICE_UNIT, QUANTITY and a buyer/seller ADDRESS_ID.

        RETURN:
            [ tax ]
            tax = {'name':'', 'amount':0.0, 'account_collected_id':1, 'account_paid_id':2}
            one tax for each tax id in IDS and their children
        """
        res = self._l10n_br_unit_compute(cr, uid, taxes, price_unit, address_id, product, partner, quantity)
        total = 0.0
        precision_pool = self.pool.get('decimal.precision')
        for r in res:
            if r.get('balance',False):
                r['amount'] = round(r.get('balance', 0.0) * quantity, precision_pool.precision_get(cr, uid, 'Account')) - total
            else:
                r['amount'] = round(r.get('amount', 0.0) * quantity, precision_pool.precision_get(cr, uid, 'Account'))
                total += r['amount']
        return res

    def _l10n_br_unit_compute(self, cr, uid, taxes, price_unit, address_id=None, product=None, partner=None, quantity=0):
        taxes = self._applicable(cr, uid, taxes, price_unit, address_id, product, partner)
        res = []
        cur_price_unit=price_unit
        obj_partener_address = self.pool.get('res.partner.address')
        for tax in taxes:
            # we compute the amount for the current tax object and append it to the result

            data = {'id':tax.id,
                    'name':tax.description and tax.description + " - " + tax.name or tax.name,
                    'account_collected_id':tax.account_collected_id.id,
                    'account_paid_id':tax.account_paid_id.id,
                    'base_code_id': tax.base_code_id.id,
                    'ref_base_code_id': tax.ref_base_code_id.id,
                    'sequence': tax.sequence,
                    'base_sign': tax.base_sign,
                    'tax_sign': tax.tax_sign,
                    'ref_base_sign': tax.ref_base_sign,
                    'ref_tax_sign': tax.ref_tax_sign,
                    'price_unit': cur_price_unit,
                    'tax_code_id': tax.tax_code_id.id,
                    'ref_tax_code_id': tax.ref_tax_code_id.id,
            }
            res.append(data)
            if tax.type=='percent':
                amount = cur_price_unit * tax.amount
                data['amount'] = amount

            elif tax.type=='fixed':
                data['amount'] = tax.amount
                data['tax_amount']=quantity
               # data['amount'] = quantity
            elif tax.type=='code':
                address = address_id and obj_partener_address.browse(cr, uid, address_id) or None
                localdict = {'price_unit':cur_price_unit, 'address':address, 'product':product, 'partner':partner}
                exec tax.python_compute in localdict
                amount = localdict['result']
                data['amount'] = amount
            elif tax.type=='balance':
                data['amount'] = cur_price_unit - reduce(lambda x,y: y.get('amount',0.0)+x, res, 0.0)
                data['balance'] = cur_price_unit

            amount2 = data.get('amount', 0.0)
            if tax.child_ids:
                if tax.child_depend:
                    latest = res.pop()
                amount = amount2
                child_tax = self._unit_compute(cr, uid, tax.child_ids, amount, address_id, product, partner, quantity)
                res.extend(child_tax)
                if tax.child_depend:
                    for r in res:
                        for name in ('base','ref_base'):
                            if latest[name+'_code_id'] and latest[name+'_sign'] and not r[name+'_code_id']:
                                r[name+'_code_id'] = latest[name+'_code_id']
                                r[name+'_sign'] = latest[name+'_sign']
                                r['price_unit'] = latest['price_unit']
                                latest[name+'_code_id'] = False
                        for name in ('tax','ref_tax'):
                            if latest[name+'_code_id'] and latest[name+'_sign'] and not r[name+'_code_id']:
                                r[name+'_code_id'] = latest[name+'_code_id']
                                r[name+'_sign'] = latest[name+'_sign']
                                r['amount'] = data['amount']
                                latest[name+'_code_id'] = False
            if tax.include_base_amount:
                cur_price_unit+=amount2
        return res
    
    def l10n_br_compute_inv(self, cr, uid, taxes, price_unit, quantity, address_id=None, product=None, partner=None):
        """
        Compute tax values for given PRICE_UNIT, QUANTITY and a buyer/seller ADDRESS_ID.
        Price Unit is a VAT included price

        RETURN:
            [ tax ]
            tax = {'name':'', 'amount':0.0, 'account_collected_id':1, 'account_paid_id':2}
            one tax for each tax id in IDS and their children
        """
        res = self._l10n_br_unit_compute_inv(cr, uid, taxes, price_unit, address_id, product, partner=None)
        total = 0.0
        obj_precision = self.pool.get('decimal.precision')
        for r in res:
            prec = obj_precision.precision_get(cr, uid, 'Account')
            if r.get('balance',False):
                r['amount'] = round(r['balance'] * quantity, prec) - total
            else:
                r['amount'] = round(r['amount'] * quantity, prec)
                total += r['amount']
        return res

    def _l10n_br_unit_compute_inv(self, cr, uid, taxes, price_unit, address_id=None, product=None, partner=None):
        taxes = self._applicable(cr, uid, taxes, price_unit, address_id, product, partner)
        obj_partener_address = self.pool.get('res.partner.address')
        res = []
        taxes.reverse()
        cur_price_unit = price_unit

        tax_parent_tot = 0.0
        for tax in taxes:
            if (tax.type=='percent') and not tax.include_base_amount:
                tax_parent_tot += tax.amount

        for tax in taxes:
            if (tax.type=='fixed') and not tax.include_base_amount:
                cur_price_unit -= tax.amount

        for tax in taxes:
            if tax.type=='percent':
                amount = cur_price_unit * tax.amount
                #if tax.include_base_amount:
                    #amount = cur_price_unit * tax.amount
                    #amount = cur_price_unit - (cur_price_unit / (1 + tax.amount))
                #else:
                    #amount = cur_price_unit * tax_parent_tot
                    #amount = (cur_price_unit / (1 + tax_parent_tot)) * tax.amount

            elif tax.type=='fixed':
                amount = tax.amount

            elif tax.type=='code':
                address = address_id and obj_partener_address.browse(cr, uid, address_id) or None
                localdict = {'price_unit':cur_price_unit, 'address':address, 'product':product, 'partner':partner}
                exec tax.python_compute_inv in localdict
                amount = localdict['result']
            elif tax.type=='balance':
                amount = cur_price_unit - reduce(lambda x,y: y.get('amount',0.0)+x, res, 0.0)

            final_price_unit = cur_price_unit
            if tax.include_base_amount:
                cur_price_unit += amount
                #todo = 1
            #else:
                #final_price_unit = cur_price_unit
                #todo = 0
            todo = 0

            res.append({
                'id': tax.id,
                'todo': todo,
                'name': tax.name,
                'amount': amount,
                'account_collected_id': tax.account_collected_id.id,
                'account_paid_id': tax.account_paid_id.id,
                'base_code_id': tax.base_code_id.id,
                'ref_base_code_id': tax.ref_base_code_id.id,
                'sequence': tax.sequence,
                'base_sign': tax.base_sign,
                'tax_sign': tax.tax_sign,
                'ref_base_sign': tax.ref_base_sign,
                'ref_tax_sign': tax.ref_tax_sign,
                'price_unit': final_price_unit,
                'tax_code_id': tax.tax_code_id.id,
                'ref_tax_code_id': tax.ref_tax_code_id.id,
            })
            if tax.child_ids:
                if tax.child_depend:
                    del res[-1]
                    amount = price_unit

            parent_tax = self._l10n_br_unit_compute_inv(cr, uid, tax.child_ids, amount, address_id, product, partner)
            res.extend(parent_tax)
        #total = 0.0
        #for r in res:
        #    if r['todo']:
        #        total += r['amount']
        #for r in res:
        #    r['price_unit'] -= total
        #    r['todo'] = 0
        return res

        
account_tax()

