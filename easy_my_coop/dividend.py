# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013-2014 Open Architects Consulting SPRL.
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
from __future__ import division
import logging
from datetime import datetime
import openerp.addons.decimal_precision as dp

from openerp.osv import fields, orm

class dividend_year(orm.Model):
    _name= 'dividend.year'
    
    def _compute_dividend_info(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for dividend in self.browse(cr, uid, ids, context=context):
            res[dividend.id]= {'grand_total_dividend': 0.0, 'grand_total_taxes': 0.0}
            for line in dividend.dividend_ids:
                res[dividend.id]['grand_total_dividend'] += line.dividend_amount
                res[dividend.id]['grand_total_taxes'] += line.dividend_taxes
        return res
    
    _columns = {
        'name': fields.char('Code'),
        'fiscal_year_id': fields.many2one('account.fiscalyear', string='Fiscal year'), 
        'percentage': fields.float('Percentage'),
        'withholding_tax': fields.float('Withholding tax'),
        'detailed_dividend_ids': fields.one2many('detailed.dividend.line', 'dividend_year_id', string='Dividend lines'),
        'dividend_ids': fields.one2many('dividend.line', 'dividend_year_id', string='Dividend lines'),
        'date_from': fields.date('Date from'),
        'date_to': fields.date('Date to'),
        'grand_total_dividend': fields.function(_compute_dividend_info, string='Grand total dividend', type='float', multi='total', digits_compute=dp.get_precision('Account')),
        'grand_total_taxes': fields.function(_compute_dividend_info, string='Grand total taxes', type='float', multi='total', digits_compute=dp.get_precision('Account')),
    }
    
    def compute_dividend(self, cr, uid, ids, context=None):
        dividend = self.browse(cr, uid, ids, context)[0]
        det_div_line_obj = self.pool.get('detailed.dividend.line')
        div_line_obj = self.pool.get('dividend.line')
        res_partner_obj = self.pool.get('res.partner')
        
        # delete lines if any
        detailed_dividend_ids = det_div_line_obj.search(cr,uid,[('dividend_year_id','=',dividend.id)])
        det_div_line_obj.unlink(cr,uid, detailed_dividend_ids)
        dividend_ids = div_line_obj.search(cr,uid,[('dividend_year_id','=',dividend.id)])
        div_line_obj.unlink(cr,uid, dividend_ids)
        
        partner_ids = res_partner_obj.search(cr,uid, [('cooperator','=',True),('member','=',True)], order='int_cooperator_register_number')
        number_of_days = (datetime.strptime(dividend.date_to , '%Y-%m-%d') - datetime.strptime(dividend.date_from , '%Y-%m-%d')).days + 1
        print number_of_days
        
        for partner in res_partner_obj.browse(cr, uid, partner_ids, context):
            total_amount_dividend = 0.0
            for line in partner.share_ids:
                vals = {}
                vals2 = {}
                line_id = False
                if line.effective_date >= dividend.date_from and line.effective_date <= dividend.date_to:
                    date_res = (datetime.strptime(dividend.date_to , '%Y-%m-%d') - datetime.strptime(line.effective_date, '%Y-%m-%d')).days
                    coeff = (date_res / number_of_days) * dividend.percentage
                    dividend_amount = line.total_amount_line * coeff
                    vals['days'] = date_res
                    vals['dividend_year_id'] = dividend.id
                    vals['coop_number'] = line.partner_id.int_cooperator_register_number
                    vals['partner_id'] = partner.id
                    vals['share_line_id'] = line.id
                    vals['coeff'] = coeff
                    vals['dividend_amount'] = dividend_amount
                    total_amount_dividend += dividend_amount                    
                    
                    line_id = det_div_line_obj.create(cr, uid, vals, context)
                elif line.effective_date < dividend.date_from:
                    dividend_amount = line.total_amount_line * dividend.percentage
                    vals['days'] = number_of_days
                    vals['dividend_year_id'] = dividend.id
                    vals['coop_number'] = line.partner_id.int_cooperator_register_number
                    vals['partner_id'] = partner.id
                    vals['share_line_id'] = line.id
                    vals['coeff'] = dividend.percentage
                    vals['dividend_amount'] = dividend_amount
                    total_amount_dividend += dividend_amount                    
                    
                    line_id = det_div_line_obj.create(cr, uid, vals, context)
            if line_id:
                vals2['coop_number'] = line.partner_id.int_cooperator_register_number
                vals2['dividend_year_id'] = dividend.id
                vals2['partner_id'] = line.partner_id.id 
                
                vals2['dividend_amount_net'] = total_amount_dividend
                vals2['dividend_amount'] = total_amount_dividend
                
                if total_amount_dividend <= 190.00:
                    vals2['dividend_taxes'] = 0.0
                else:
                    div_tax = (total_amount_dividend - 190) * dividend.withholding_tax
                    vals2['dividend_taxes'] = div_tax
                    vals2['dividend_amount_net'] = total_amount_dividend - div_tax                
                              
                self.pool.get('dividend.line').create(cr, uid, vals2, context)
        return True
    
class detailed_dividend_line(orm.Model):
    _name='detailed.dividend.line'
    
    def _compute_total_line(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.unit_price * line.share_number
        return res
    
    _columns = {
        'dividend_year_id': fields.many2one('dividend.year', string='Dividend year'),
        'coop_number': fields.integer('Coop Number'),
        'days': fields.integer('Days'),
        'partner_id': fields.many2one('res.partner', string='Cooperator', readonly=True),
        'share_line_id': fields.many2one('share.line', string='Share line', readonly=True),
        'share_number': fields.related('share_line_id', 'share_number', type='integer', string='Number of Share'),
        'unit_price': fields.related('share_line_id', 'unit_price', type='float', string='Unit price'),
        'effective_date': fields.related('share_line_id', 'effective_date', type='date', string='Effective date'),
        'total_amount_line': fields.function(_compute_total_line, type='float', string='Total value of share', readonly=True),
        'coeff': fields.float('Coefficient to apply', digits=(2,4)),
        'dividend_amount': fields.float('Gross Dividend'),
        'dividend_amount_net': fields.float('Dividend net'),
        'dividend_taxes': fields.float('Taxes'),
    }
    
class dividend_line(orm.Model):
    _name= 'dividend.line'
     
    def _get_account_number(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            bank_accounts_ids = self.pool.get('res.partner.bank').search(cr,uid,[('partner_id','=',line.partner_id.id)])
            bank_accounts = self.pool.get('res.partner.bank').browse(cr,uid,bank_accounts_ids,context)
            res[line.id]= bank_accounts[0].acc_number
            
        return res
     
    _columns = {
        'dividend_year_id': fields.many2one('dividend.year', string='Dividend year'),
        'coop_number': fields.integer('Coop Number'),
        'partner_id': fields.many2one('res.partner', string='Cooperator', readonly=True),
        'account_number':fields.function(_get_account_number,type='char',string="Account Number"), 
        'dividend_amount': fields.float('Gross Dividend'),
        'dividend_amount_net': fields.float('Dividend net'),
        'dividend_taxes': fields.float('Taxes'),
    }