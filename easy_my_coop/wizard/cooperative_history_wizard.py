# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Ben
#    Copyright Boss Consulting
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
from openerp.osv import fields, osv
from openerp.tools.translate import _


class cooperative_report(osv.TransientModel):
    _name = 'cooperative.history.report'
    
    _columns = {
        'name':fields.char('Name',size=64),
        'report': fields.selection([('coop_register', 'Cooperators Register'),
                                     ('operation_register', 'Operations Register')],
                                    'Report',
                                    required=True),
        'display_cooperator': fields.selection([('all', 'All'),
                                             ('member', 'Effective member')],
                                            'Display cooperator',
                                            required=True),
    }
    
    _defaults = {
        'display_cooperator': 'member',
        'report': 'coop_register',
    }
       
    def _print_report(self, cursor, uid, ids, data, context=None):
        
        return {'type': 'ir.actions.report.xml',
                'report_name': data['report'],
                'datas': data}
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = {}
        
        wizard = self.browse(cr, uid, ids, context)[0]
        report_name = ''
        obj_ids = []
        if context.get('active_ids') : 
            data['ids'] = context.get('active_ids', [])
        else: 
            if wizard.report == 'coop_register':
                report_name = 'easy_my_coop.cooperator_register'
                res_partner_obj = self.pool.get('res.partner')
                domain = []
                domain.append(('cooperator','=',True))
                if wizard.display_cooperator == 'member' :
                    domain.append(('member','=',True))
                obj_ids = res_partner_obj.search(cr,uid, domain, order='int_cooperator_register_number')    
            elif wizard.report == 'operation_register' :
                report_name = 'easy_my_coop.subscription_register'
                obj_ids = self.pool.get('subscription.register').search(cr,uid,[], order='register_number_operation')
            else : 
                raise osv.except_osv(_("Error!"), _("the report you've specified doesn't exist !"))
            
        data['model'] = context.get('active_model', 'ir.ui.menu')
        data['report'] = report_name 
        data['ids'] = obj_ids
         
        return self._print_report(cr, uid, ids, data, context=context)
