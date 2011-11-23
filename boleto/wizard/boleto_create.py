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

from osv import osv, fields


class boleto_create(osv.osv_memory):
    _name = 'boleto.create'

    _columns = {
        'success': fields.char(u'Sucesso', size=20),
        'error': fields.char(u'Erros', size=20),
    }

    def create(self, cr, uid, ids, context=None):
        inv_obj = self.pool.get('account.invoice').browse(cr, uid, ids)
        rec_ids = inv_obj._get_receivable_lines(cr, uid, ids)
        for move_line in self.pool.get('account.move.line').browse(cr, uid, rec_ids):
            pass

        success = ''
        error = ''

        return {'success': success, 'error': error}

boleto_create('account.invoice.boletos_create')
