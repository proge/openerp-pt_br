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

