# -*- coding: utf-8 -*-
##############################################################################
#                                                                            #
#  Copyright (C) 2011 Proge Informática Ltda (<http://www.proge.com.br>).    #
#                                                                            #
#  This program is free software: you can redistribute it and/or modify      #
#  it under the terms of the GNU Affero General Public License as            #
#  published by the Free Software Foundation, either version 3 of the        #
#  License, or (at your option) any later version.                           #
#                                                                            #
#  This program is distributed in the hope that it will be useful,           #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#  GNU Affero General Public License for more details.                       #
#                                                                            #
#  You should have received a copy of the GNU Affero General Public License  #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                            #
##############################################################################

import re
from osv import fields, osv

non_digits = re.compile('\D')


def format_one(name, size):
    """Returns a function suitable for an on_change event that formats a string

    Arguments:
    name -- field name that is going to be formated
    size -- number of digits in the field

    The decorated function receives a string and should return a
    formated string.

    """
    def wrap(f):
        def wrapper(self, cr, uid, ids, val):
            if not val:
                return {}

            val_digits = non_digits.sub('', val)
            if len(val_digits) == size:
                val = f(val_digits)

            return {'value': {name: val}}
        return wrapper
    return wrap


def validate_one(name, size, verify_digits):
    """Decorates a validation function for one field

    Arguments:
    name -- the name of the field you want to validate
    size -- number of digits in the field
    verify_digits -- number of digits on the tail used for validation

    The decorated function is called with a list of ints (digits) but
    withtout the verification digits. It should return a complete list
    of digits to be compared with the ones being validated.

    """
    def wrap(f):
        def wrapper(self, cr, uid, ids):
            curr_object = self.browse(cr, uid, ids)[0]
            value = getattr(curr_object, name)
            if not value:
                field = self._columns[name]
                if field.required:
                    return False
                else:
                    return True

            value = non_digits.sub('', value)
            if len(value) != size:
                return False

            value_list = [int(c) for c in value]
            generated_list = f(value_list[:-verify_digits])

            if generated_list == value_list:
                return True
            return False
        return wrapper
    return wrap


class hr_employee(osv.osv):
    """Brazilian localization of hr_employee."""
    _inherit = 'hr.employee'
    _columns = {
        'rg': fields.char('RG', size=10, required=True),
        'rg_data': fields.date('Data Emis.'),
        'rg_orgao': fields.char('Org. Exp.', size=3),
        'rg_state_id': fields.many2one('res.country.state', 'Estado'),
        'cpf': fields.char('CPF', size=14, required=True),
        'ctps': fields.char('CTPS', size=7),
        'ctps_serie': fields.char('Serie', size=5),
        'ctps_state_id': fields.many2one('res.country.state', 'Estado'),
        'pis': fields.char('PIS', size=14),
        'pis_date': fields.date('Data'),
        'tit_eleitor': fields.char('Título de Eleitor', size=11),
        'zona_eleitoral': fields.char('Zona Eleitoral', size=3),
        'secao': fields.char('Seção', size=3),
        'cnh': fields.char('Número da CNH', size=11),
        'cnh_categoria': fields.char('Categoria', size=1),
        'cnh_vencimento': fields.date('Vencimento'),
        'cnh_state_id': fields.many2one('res.country.state', 'Estado'),
        'reservista': fields.char('Nr. Reservista', size=14),
        }

    @format_one('cpf', 11)
    def on_change_cpf(val):
        return '%s.%s.%s-%s' % (val[0:3], val[3:6],
                                val[6:9], val[9:11])

    @format_one('pis', 11)
    def on_change_pis(val):
        return '%s.%s.%s-%s' % (val[0:3], val[3:6],
                                val[6:9], val[9:11])

    @format_one('tit_eleitor', 10)
    def on_change_tit_eleitor(val):
        return '%s/%s' % (val[0:8], val[8:10])

    @format_one('reservista', 11)
    def on_change_reservista(val):
        return '%s %s %s %s' % (val[0:2], val[2:5],
                                val[5:10], val[10:11])

    @validate_one('cpf', 11, 2)
    def validate_cpf(novo):
        for i in range(2):
            r = 0
            for k, c in enumerate(novo):
                r += c * (len(novo) + 1 - k)
            r %= 11
            if r < 2:
                r = 0
            else:
                r = 11 - r
            novo.append(r)

        return novo

    @validate_one('pis', 11, 1)
    def validate_pis(novo):
        r = 0
        for m, c in zip([3, 2, 9, 8, 7, 6, 5, 4, 3, 2], novo):
            r += m * c
        r %= 11
        if r < 2:
            r = 0
        else:
            r = 11 - r
        novo.append(r)
        return novo

    _constraints = [
        (validate_cpf, 'CPF invalido!', ['cpf']),
        (validate_pis, 'PIS invalido!', ['pis']),
        ]

    _sql_constraints = [
        ('hr_employee_cpf_uniq', 'unique (cpf)',
         'Já existe um funcionário cadastrado com esse CPF!')
        ]

hr_employee()

