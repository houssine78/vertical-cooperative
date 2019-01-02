# -*- coding: utf-8 -*-
##############################################################################
#
#    BOSS, Business Open Source Solution
#    Copyright (C) 2013-2017 Open Architects Consulting SPRL.
#    Copyright (C) 2018-     Coop IT Easy SCRLfs
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Easy MY Coop",
    "version": "1.0",
    "depends": ["base", 
                "sale", 
                "account_accountant", 
                "l10n_be", 
                "product",
                "portal", 
                "base_iban",
                "base_iban_bic_not_required",
                "boss_report"],
    "author": "Houssine BAKKALI <houssine@coopiteasy.coop>",
    "category": "Connector",
    "description": """
    Aim to allow the synchronisation between Wordpress users and OpenERP.    
    """,
    'data': [
        'security/energiris_security.xml',
        'security/ir.model.access.csv',
        'view/external_db_view.xml',  
        'view/job_sync_view.xml',
        'view/res_partner_view.xml',
        'view/cooperator_register_view.xml',
        'view/invoice_view.xml',
        'view/operation_request_view.xml',
        'view/dividend_year_view.xml',
        'data/energiris_data.xml', 
        'data/bank_data.xml',
        'data/scheduler_data.xml',
        'report/energiris_report.xml',
        'data/mail_template_data.xml',
        'wizard/cooperative_history_wizard.xml',
        'wizard/export_global_wizard.xml'
    ],
    'installable': True,
}