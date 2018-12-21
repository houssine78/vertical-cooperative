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

import logging
from datetime import datetime

from openerp import netsvc
from openerp.osv import fields, osv, orm
from openerp import tools
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

import pymysql

_logger = logging.getLogger(__name__)

COOPERATOR_LEVEL = {'subscriber':'\'a:1:{s:10:\"subscriber\";b:1;}\'',
                    'level1':'\'a:1:{s:15:\"s2member_level1\";b:1;}\'',
                    'level2':'\'a:1:{s:15:\"s2member_level2\";b:1;}\'',
                    'level3':'\'a:1:{s:15:\"s2member_level3\";b:1;}\''
                    }

LANG_MAPPING = {'FR':'fr_BE',
                'EN':'en_US',
                'NL':'nl_BE',
                'DE':'de_DE',
                'IT':'it_IT',
                'ES':'es_ES',
                }

class external_db(orm.Model):
    _name = 'external.db'
    _description = 'External DB'
    
    def test_connection(self, cr, uid, ids, context=None):
        try:
            server = self.browse(cr, uid, ids, context)[0]
            conn = pymysql.connect(host=server.host, port=int(server.port), user=server.user,passwd=server.password,database=server.database)
            cur = conn.cursor()
    
            cur.close()
            conn.close()
        except Exception, e:
            _logger.exception("Failed to connect to %s with user %s.", server.host, server.user)
            raise osv.except_osv(_("Connection test failed!"), _("Here is what we got instead:\n %s.") % tools.ustr(e))
        raise osv.except_osv(_("Connection Test Succeeded!"), _("Everything seems properly set up!"))
    
    _columns = {
        'name' : fields.char('Name', size=64, required=True),
        'host' : fields.char('Host', size=64, required=True),
        'port' : fields.char('Port', size=4, required=True),
        'user': fields.char('User',size=64),
        'password': fields.char('Password',size=64),
        'database': fields.char('Database',size=64),
    }
    
    def get_connection(self, cr, uid, context=None):
        ids = self.search(cr, uid, [], context=context)
        server = self.browse(cr, uid, ids, context)
        if server !=None and len(server)!=0:
            server = server[0]
            return pymysql.connect(host=server.host, port=int(server.port), user=server.user, passwd=server.password,database=server.database)
        return False
    
class sync_job(orm.Model):
    _name='job.sync'
    _description = 'Job Sync'
    
    def custom_fields_str_to_dic(self, custom_fields):
        custom_fields_list = []
        custom_fields = custom_fields.split(';')
        for custom_field in custom_fields:
            start = custom_field.find('"')
            end = custom_field.find('"', start+1)
            custom_fields_list.append(custom_field[start+1:end])
        return dict(zip(custom_fields_list[0::2],custom_fields_list[1::2]))
    
    def get_job_sync_line(self, cr, uid, raw_records, operation_type):
        mapping_line_dict = {0:'ext_id',1:'user_login',2:'email',3:'name',4:'meta_key'}
        job_sync_line_vals = {}
        for raw_record in raw_records:
            if not job_sync_line_vals.has_key(raw_record[0]):
                job_sync_line_vals[str(raw_record[0])] = {}
            for index in range(len(raw_record)-1): 
                job_sync_line_vals[str(raw_record[0])]['type'] = operation_type
                    
                if mapping_line_dict[index] == 'meta_key': 

                    if raw_record[index] == 'first_name':
                        job_sync_line_vals[str(raw_record[0])]['firstname'] = raw_record[5]
                    elif raw_record[index] == 'last_name':
                        job_sync_line_vals[str(raw_record[0])]['lastname'] = raw_record[5]
                    elif raw_record[index] == 'wp_s2member_custom_fields':
                        custom_fields = self.custom_fields_str_to_dic(raw_record[5])
                        job_sync_line_vals[str(raw_record[0])].update(custom_fields)
                else:
                    job_sync_line_vals[str(raw_record[0])][mapping_line_dict[index]] = str(raw_record[index])
        return job_sync_line_vals  
    
    def run_wp_sync(self, cr, uid, context=None):
        self.get_coop_cat1(cr, uid, context)
        
        return True
          
    def get_coop_cat1(self, cr, uid, context=None):
        job_sync_vals = {'name': 'need sequence', 'user_id':uid, 'date':datetime.now()}
        external_db_obj = self.pool.get('external.db') 
        try:
            conn = external_db_obj.get_connection(cr, uid, context)
        except Exception, e:
            job_sync_vals['job_sync_status'] = 'failed'
            job_sync_vals['error_message'] = tools.ustr(e)
            super(sync_job, self).create(cr, uid, job_sync_vals, context)
            cr.commit()
            raise osv.except_osv(_("Connection failed!"), _("Here is what we got instead:\n %s.") % tools.ustr(e))
        if conn != False:    
            try:
                source_id = external_db_obj.search(cr, uid, [('host','=',conn.host)], context=context)  
                job_sync_vals['source_id'] = source_id[0]
                cur = conn.cursor()
                cur.execute("SELECT DISTINCT u.id, u.user_login, u.user_email, u.display_name, um.meta_key, um.meta_value "
                            "FROM wp_users u, wp_usermeta um "
                            "WHERE u.id = um.user_id "
                            "AND (meta_key = 'wp_s2member_custom_fields' OR meta_key = 'first_name' "
                            "OR meta_key = 'last_name' )"
                            "AND um.user_id IN (SELECT user_id FROM wp_usermeta WHERE (meta_key = 'wp_capabilities' AND meta_value=%s))" % COOPERATOR_LEVEL['subscriber'])                   
                res = cur.fetchall()
                cur.close()
                conn.close()
                
                job_sync_lines_vals = self.get_job_sync_line(cr, uid, res,'0')
                if len(job_sync_lines_vals) > 0:
                    job_sync_vals['job_sync_status'] = 'success'
                    job_sync_id = super(sync_job, self).create(cr, uid, job_sync_vals, context)
                    
                    created_job_sync_line_ids = []
                    for job_sync_line_vals in job_sync_lines_vals.values():
                        job_sync_line_vals['job_sync_id'] = job_sync_id
                        job_sync_line_vals['user_id'] = uid
                        language = job_sync_line_vals.get('language',False)
                        if language:
                            language_code = LANG_MAPPING[language]
                            lang_obj = self.pool.get('res.lang')
                            lang_id = lang_obj.search(cr, uid, [('code','=',language_code)])
                            if len(lang_id) > 0:
                                lang = lang_obj.browse(cr, uid, lang_id, context)[0]
                                job_sync_line_vals['lang'] = lang.code
                        job_sync_line_id = self.pool.get('job.sync.line').create(cr, uid,job_sync_line_vals, context)
                        created_job_sync_line_ids.append(job_sync_line_id)
                    
                    conn = external_db_obj.get_connection(cr, uid, context)
                    cur = conn.cursor()
                    # we set the status to level 1 in WordPress to flag the record as imported in Odoo
                    for job_sync_line_vals in job_sync_lines_vals.values():
                        cur.execute("UPDATE wp_usermeta set meta_value=%s WHERE (meta_key = 'wp_capabilities' AND user_id=%s)" % (COOPERATOR_LEVEL['level1'], job_sync_line_vals['ext_id']))
                    cur.close
                    conn.close
                    
                    # we send the email confirmation to the requester
                    email_template_obj = self.pool.get('email.template')
                    for job_sync_line_id in created_job_sync_line_ids:
                        confirmation_email_template_id = email_template_obj.search(cr, uid, [('name', '=', 'Confirmation Email')])[0]
                        email_template_obj.send_mail(cr, uid, confirmation_email_template_id, job_sync_line_id, True, context)
                
            except Exception, e:
                _logger.exception("Failed to get coop cat 1")
                job_sync_vals['job_sync_status'] = 'failed'
                job_sync_vals['error_message'] = tools.ustr(e)
                super(sync_job, self).create(cr, uid, job_sync_vals, context)
                cr.commit()
                raise osv.except_osv(_("Something failed!"), _("Here is what we got :\n %s.") % tools.ustr(e))
        
        return True
    
    def run_job_sync(self, cr, uid, ids, context=None):
        self.get_coop_cat1(cr, uid, context)
        
        return True
    
    _columns = {
        'name' : fields.char('Name', size=64, required=True),
        'source_id': fields.many2one('external.db', 'Source'),
        'date' : fields.datetime('Date Time', required=True),
        'user_id': fields.many2one('res.users', 'User',required=True),
        'job_sync_lines': fields.one2many('job.sync.line','job_sync_id','Job Lines'),
        'job_sync_status': fields.selection([('success','Success'),('failed','Failed')],'Job Sync Status', required=True),
        'error_message': fields.text('Error Message')
    }

class sync_job_line(orm.Model):
    _name='job.sync.line'
    _description = 'Job Sync Line'
    
    def _lang_get(self, cr, uid, context=None):
        lang_pool = self.pool.get('res.lang')
        ids = lang_pool.search(cr, uid, [], context=context)
        res = lang_pool.read(cr, uid, ids, ['code', 'name'], context)
        return [(r['code'], r['name']) for r in res]
     
    def check_belgian_identification_id(self,nat_register_num):
        if not self.check_empty_string(nat_register_num):
            return False
        if len(nat_register_num) != 11:
            return False
        if not nat_register_num.isdigit():
            return False
        birthday_number = nat_register_num[0:9]
        controle = nat_register_num[9:11]
        check_controle = 97 - (int(birthday_number) % 97)
        if int(check_controle) != int(controle):
            check_controle = 97 - ((2000000000 + int(birthday_number)) % 97)
            if int(check_controle) != int(controle):
                return False
        return True
    
    def check_empty_string(self, value):
        if value == None or value == False or value == '':
            return False
        return True
    
    def _validated_lines(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            if (not self.check_empty_string(line.iban)  or not self.check_empty_string(line.no_registre) or 
            not self.pool.get('res.partner.bank').is_iban_valid(cr,uid, line.iban, context) or
            (not line.skip_control_ng and not self.check_belgian_identification_id(line.no_registre))):
                res[line.id] = False
            else:
                res[line.id] = True
        return res
    
    def get_date_now(self, cr, uid, context):
        return datetime.strftime(datetime.now(), '%Y-%m-%d')
    
    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'firstname': fields.char('Firstname', size=64),
        'lastname': fields.char('Lastname', size=64),
        'job_sync_id': fields.many2one('job.sync','Job', ondelete='cascade'),
        'type': fields.selection([('0','New Cooperator'),('3','Increase number of share')],'Type'),
        'state': fields.selection([('draft','Draft'),
                                   ('done','Done'),
                                   ('waiting','Waiting'),
                                   ('cancelled','Cancelled'),
                                   ('failed','Failed')], 'State',required=True),
        'error_message': fields.char('Error Message',size=256),
        'ext_id': fields.integer('WP External Id', required=True),
        'email': fields.char('Email', size=128, required=True),
        'iban': fields.char('Account Number', size=64),
        'user_login': fields.char('Login', size=64, required=True),
        'user_status':fields.char('user_status',size=2),
        'partner_id': fields.many2one('res.partner','Cooperator'),
        'nb_parts': fields.char('Number of Share', size=4),
        'ordered_parts': fields.char('Number of Share', size=4),
        'adresse': fields.char('Address', size=128),
        'ville': fields.char('City', size=64),
        'codepostal': fields.char('Zip Code', size=10),
        'pays': fields.char('Country', size=64),
        'phone': fields.char('Phone', size=32),
        'no_registre': fields.char('Register Number', size=64),
        'lang': fields.selection(_lang_get, 'Language'),
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, readonly=True, states={'draft':[('readonly',False)]}),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
        'validated':fields.function(_validated_lines, type='boolean', string='Valid Line?', readonly=True),
        'skip_control_ng': fields.boolean("Skip control", help="if this field is checked then no control will be done on the national register number and on the iban bank account. To be done in case of the id card is from abroad or in case of a passport"),
        'language': fields.char('Language', size=2),
        'sync_date': fields.date('Date', help='Date of the importation of the subscription into OpenERP from WP'),
        'invoice_id': fields.many2one('account.invoice', string='Capital release request'),
    }    
    
    _order = "sync_date desc, id desc"
    
    _defaults = {
        'state': 'draft',
        'lang': 'fr_BE',
        'language': 'FR',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, context=c),
        'sync_date': lambda self,cr,uid,c: self.get_date_now(cr, uid, context=c)
    }

    def create_invoice(self, cr, uid, vals, sync_line, context=None):
        # getting info in order to fill in the invoice
        product_obj = self.pool.get('product.product')
        product_id = product_obj.search(cr, uid, [('default_code','=','share_250')])[0]
        product = product_obj.browse(cr, uid, product_id, context)
        journal_id = self.pool.get('account.journal').search(cr, uid, [('code','=','SUBJ')])[0]
        # TODO check that this account in the right one and do the same on the product 
        account_id = self.pool.get('account.account').search(cr, uid, [('code','=','416000')])[0]
        # creating invoice and invoice lines
        account_obj = self.pool.get('account.invoice')
        account_invoice_id = account_obj.create(cr, uid, {'partner_id':vals['partner_id'], 
                                                            'journal_id':journal_id,'account_id':account_id,
                                                            'type': 'out_invoice', 'release_capital_request':True}, context)
        result = self.pool.get('account.invoice.line').product_id_change(cr, uid, False, product_id, False, vals['quantity'], '', 'out_invoice', vals['partner_id'])
        self.pool.get('account.invoice.line').create(cr, uid, {'invoice_id':account_invoice_id,
                                            'product_id':product_id,'quantity':vals['quantity'],
                                            'price_unit':result['value']['price_unit'],
                                            'uos_id':result['value']['uos_id'],'account_id':result['value']['account_id'],
                                            'name':product.name}, context)
        #link the subscription line with the invoice
        self.write(cr, uid, sync_line.id, {'invoice_id':account_invoice_id}, context)
        # run the validation on the invoice
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'account.invoice', account_invoice_id, 'invoice_open', cr)
        #we get the print service for the invoice and send directly the invoice by mail
        email_template_obj = self.pool.get('email.template')
        invoice_email_template_id = email_template_obj.search(cr, uid, [('name', '=', 'Request to Release Capital - Send by Email')])[0]
        # we send the email with the invoice in attachment 
        email_template_obj.send_mail(cr, uid, invoice_email_template_id, account_invoice_id, True, context)
        account_obj.write(cr, uid, account_invoice_id,{'sent':True},context)
        return account_invoice_id
    
    def action_cancel(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'cancelled'}, context)
        return True
    
    def action_waiting(self, cr, uid, ids, context=None):
        self.write(cr, uid, ids, {'state':'waiting'}, context)
        return True
    
    def copy(self, cr, uid, ids, default=None, context=None):
        default = default or {}
        default.update({
            'invoice_id':False,
        })
        return super(sync_job_line, self).copy(cr, uid, ids, default, context)
       
    def validate_sync_line(self, cr, uid, ids, context=None):
        sync_line = self.browse(cr, uid, ids, context)[0]
        
        partner_obj = self.pool.get('res.partner')
        partner_id = partner_obj.search(cr,uid, [('national_register_number','=',sync_line.no_registre)])
        if not partner_id:
            partner_vals = {'name' : sync_line.name, 'firstname':sync_line.firstname, 'lastname': sync_line.lastname,
                            'customer':False, 'cooperator':True, 'street':sync_line.adresse,'zip':sync_line.codepostal,
                            'city': sync_line.ville,'phone': sync_line.phone,'email':sync_line.email,
                            'national_register_number':sync_line.no_registre,'out_inv_comm_type':'bba',
                            'out_inv_comm_algorithm':'random','wp_external_id':sync_line.ext_id, 'lang':sync_line.lang}
            if sync_line.pays:
                trans_obj = self.pool.get('ir.translation')
                trans_id = trans_obj.search(cr,uid,[('name','=','res.country,name'),('type','=','model'),('value','=',sync_line.pays)])
                trans = trans_obj.browse(cr, uid, trans_id, context)
                if trans:
                    country_id = self.pool.get('res.country').search(cr,uid,[('name','=',trans[0].src)])
                    partner_vals.update({'country_id':country_id[0]})
            partner_id = partner_obj.create(cr, uid, partner_vals, context)
            self.pool.get('res.partner.bank').create(cr, uid, {'partner_id':partner_id,'acc_number':sync_line.iban,'state':'iban'}, context)
        else:
            partner_id = partner_id[0]
        invoice_vals = {'quantity':sync_line.ordered_parts, 'partner_id':partner_id}
        self.create_invoice(cr, uid, invoice_vals, sync_line, context)
        self.write(cr, uid, sync_line.id, {'partner_id':partner_id, 'state':'done'}, context)
                    
        return True

class operation_request(orm.Model):
    _name = 'operation.request'
    
    def get_date_now(self, cr, uid, context):
        return datetime.strftime(datetime.now(), '%Y-%m-%d')
    
    _columns = {
        'request_date': fields.date('Request date'),
        'partner_id': fields.many2one('res.partner','Cooperator', domain=[('member','=',True)],required=True),
        'operation_type': fields.selection([('subscription','Subscription'),('transfer','Transfer'),('sell_back','Sell Back')],'Operation Type', required=True),
        'quantity': fields.integer('Number of share', required=True),
        'approved': fields.boolean('Approved?'),
        'state': fields.selection([('draft','Draft'),('done','Done'),('cancelled','Cancelled'),('refused','Refused')], 'State',required=True),
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, readonly=True),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
    }
    
    _defaults = {
        'state': 'draft',
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, context=c),
        'user_id': lambda s, cr, u, c: u,
        'request_date': lambda self,cr,uid,c: self.get_date_now(cr, uid, context=c),
    }
    
    def create_credit_note(self, cr, uid, vals, context=None):
        # getting info in order to fill in the invoice
        product_obj = self.pool.get('product.product')
        product_id = product_obj.search(cr, uid, [('default_code','=','share_250')])[0]
        product = product_obj.browse(cr, uid, product_id, context)
        journal_id = self.pool.get('account.journal').search(cr, uid, [('code','=','SUBJ')])[0]
        # TODO check that this account in the right one and do the same on the product 
        account_id = self.pool.get('account.account').search(cr, uid, [('code','=','416000')])[0]
        capital_account_id = self.pool.get('account.account').search(cr, uid, [('code','=','416000')])[0]
        # creating invoice and invoice lines
        account_obj = self.pool.get('account.invoice')
        account_invoice_id = account_obj.create(cr, uid, {'partner_id':vals['partner_id'], 
                                                            'journal_id':journal_id,'account_id':account_id,
                                                            'type': 'out_invoice', 'release_capital_request':True}, context)
        result = self.pool.get('account.invoice.line').product_id_change(cr, uid, False, product_id, False, vals['quantity'], '', 'out_invoice', vals['partner_id'])
        self.pool.get('account.invoice.line').create(cr, uid, {'invoice_id':account_invoice_id,
                                            'product_id':product_id,'quantity':vals['quantity'],
                                            'price_unit':result['value']['price_unit'],
                                            'uos_id':result['value']['uos_id'],'account_id':result['value']['account_id'],
                                            'name':product.name}, context)
        # run the validation on the invoice
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_validate(uid, 'account.invoice', account_invoice_id, 'invoice_open', cr)
        #we get the print service for the invoice and send directly the invoice by mail
        email_template_obj = self.pool.get('email.template')
        invoice_email_template_id = email_template_obj.search(cr, uid, [('name', '=', 'Request to Release Capital - Send by Email')])[0]
        # we send the email with the invoice in attachment 
        email_template_obj.send_mail(cr, uid, invoice_email_template_id, account_invoice_id, True, context)
        account_obj.write(cr, uid, account_invoice_id,{'sent':True},context) 
        return True
    
    def validate_operation(self, cr, uid, ids, context=None):
        operation = self.browse(cr, uid, ids, context)[0]
        shl_obj = self.pool.get('share.line')
        
        if operation.operation_type == 'sell_back': 
            if operation.partner_id.member:
                if operation.quantity > operation.partner_id.number_of_share:
                    raise osv.except_osv(_("Error!"), _("The cooperator can't sell more shares that he owns."))
                else:
                    share_ind = len(operation.partner_id.share_ids)
                    quantity = operation.quantity
                    i = 1
                    while quantity > 0:
                        share_id = operation.partner_id.share_ids[share_ind-i]
                        if quantity >= share_id.share_number:
                            quantity -= share_id.share_number
                            shl_obj.unlink(cr, uid, share_id.id, context)
                        else:
                            share_left = share_id.share_number - quantity
                            quantity = 0
                            shl_obj.write(cr,uid, share_id.id, {'share_number': share_left})
                        i += 1
                    
                    obj_sequence = self.pool.get('ir.sequence')
                    sequence_operation_id = obj_sequence.search(cr, uid, [('name','=','Register Operation')])[0]
                    sub_reg_operation = obj_sequence.next_by_id(cr, uid, sequence_operation_id, context)
            
                    self.pool.get('subscription.register').create(cr,uid,
                                   {'name':sub_reg_operation,
                                    'register_number_operation':int(sub_reg_operation),
                                    'partner_id':operation.partner_id.id,
                                    'quantity':operation.quantity,
                                    'date':self.get_date_now(cr, uid, context),
                                    'type':'sell_back'}, context)
                    # if the cooperator sold all his shares he'll be no more a effective member
                    if operation.quantity == operation.partner_id.number_of_share:
                        self.pool.get('res.partner').write(cr,uid,operation.partner_id.id,{'member': False,'old_member':True}, context)                
        else:
            raise osv.except_osv(_("Error!"), _("This operation is not yet implemented."))
        
        self.write(cr, uid, ids,{'state':'done'}, context)
        
        return True
    
class res_partner(orm.Model):
    _inherit = 'res.partner'
     
    def _compute_share_info(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for partner in self.browse(cr, uid, ids, context=context):
            res[partner.id]= {'number_of_share': 0.0, 'total_value': 0.0}
            for line in partner.share_ids:
                res[partner.id]['number_of_share'] += line.share_number
                res[partner.id]['total_value'] += line.unit_price * line.share_number
        return res
    
    _columns = {
        'cooperator': fields.boolean('Cooperator', help="Check this box if this contact is a cooperator."),
        'member': fields.boolean('Is member', help="Check this box if this cooperator is a effective member."),
        'old_member': fields.boolean('Old member'),
        'firstname': fields.char('Firstname', size=64),
        'lastname': fields.char('Lastname', size=64),
        'national_register_number': fields.char('National Register Number', size=32),
        'share_ids': fields.one2many('share.line','partner_id','Share Lines'),
        'wp_external_id': fields.char('WP External ID', size=64),
        'cooperator_register_number': fields.char('Cooperator Register Number', size=32),
        'int_cooperator_register_number': fields.integer('Cooperator Register Number'),
        'number_of_share': fields.function(_compute_share_info, type='float', multi='share', string='Number of share', readonly=True),
        'total_value': fields.function(_compute_share_info, type='float', multi='share', string='Total value of shares', readonly=True),
    }
    
    _order = "int_cooperator_register_number"
    
class share_line(orm.Model):
    _name='share.line'
    
    def _compute_total_line(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = line.unit_price * line.share_number
        return res
    
    _columns = {
        'share_number': fields.integer('Number of Share', size=4, required=True),
        'unit_price': fields.float('Unit Price',digits_compute=dp.get_precision('Share Price'), required=True),
        'effective_date': fields.date('Effective Date'),
        'release_date': fields.date('Release Date'),
        'payment_ref': fields.char('Payment ref.'),
        'partner_id': fields.many2one('res.partner','Cooperator', required=True, ondelete='cascade'),
        'total_amount_line':fields.function(_compute_total_line, type='float', string='Total', readonly=True),
        'invoice_id': fields.many2one('account.invoice',string='Capital release request'),
    }    
    
    _order = "effective_date asc"
    
class account_invoice(orm.Model):
    _inherit = 'account.invoice'
    
    _columns = {
        'release_capital_request': fields.boolean('Release of capital request'),
        'share_line' : fields.one2many('share.line','invoice_id',string='Share lines'),
        'subscription_request': fields.one2many('job.sync.line','invoice_id',string='Subscription request'),
    } 
    
    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
                }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.webkit',
            'datas': datas,
            'nodestroy' : True
        }
        
    def confirm_paid(self, cr, uid, ids, context=None):
        super(account_invoice, self).confirm_paid(cr, uid, ids, context)
        invoice = self.browse(cr, uid, ids, context)[0]
        if invoice.partner_id.cooperator:
            mail_template_name = ''
            if invoice.partner_id.member :
                mail_template_name = 'Share Increase - Payment Received Confirmation - Send By Email'
            else:
                mail_template_name = 'Payment Received Confirmation - Send By Email'
            effective_date = datetime.now().strftime("%d/%m/%Y")
            #take the effective date from the payment. by default the confirmation date is the payment date
            if invoice.payment_ids :
                move_line = invoice.payment_ids[0]
                effective_date = move_line.date
                    
            # flag the partner as a effective member
            obj_sequence = self.pool.get('ir.sequence')
            # if not yet cooperator we generate a cooperator number
            if invoice.partner_id.member == False :
                sequence_id = obj_sequence.search(cr, uid, [('name','=','Subscription Register')], context)[0]
                sub_reg_num = obj_sequence.next_by_id(cr, uid, sequence_id, context)
                self.pool.get('res.partner').write(cr, uid,invoice.partner_id.id, {'member':True,
                                                                                   'cooperator_register_number':sub_reg_num,
                                                                                   'int_cooperator_register_number':int(sub_reg_num)},context)
            sequence_operation_id = obj_sequence.search(cr, uid, [('name','=','Register Operation')])[0]
            sub_reg_operation = obj_sequence.next_by_id(cr, uid, sequence_operation_id, context)
            sub_reg_id = 0
            
            for line in invoice.invoice_line:
                sub_reg_id = self.pool.get('subscription.register').create(cr,uid,
                                   {'name':sub_reg_operation,
                                    'register_number_operation':int(sub_reg_operation),
                                    'partner_id':invoice.partner_id.id,
                                    'quantity':line.quantity,
                                    'date':effective_date,
                                    'type':'subscription',
                                    'payment_ref':line.invoice_id.reference}
                                   , context)
                self.pool.get('share.line').create(cr, uid, {'share_number':line.quantity,
                                                             'unit_price':line.price_unit,
                                                             'partner_id':invoice.partner_id.id,
                                                             'effective_date':effective_date,
                                                             'invoice_id':invoice.id},context)
            
            email_template_obj = self.pool.get('email.template')
            certificat_email_template_id = email_template_obj.search(cr, uid, [('name', '=', mail_template_name)])[0]
            # we send the email with the certificat in attachment 
            email_template_obj.send_mail(cr, uid, certificat_email_template_id, sub_reg_id, True, context)
        return True

class subscription_register(orm.Model):    
    _name= 'subscription.register'
    
    _columns = {
        'name': fields.char('Register Number Operation', size=10, readonly=True, required=True),
        'register_number_operation' : fields.integer('Register Number Operation', readonly=True , required=True),
        'partner_id': fields.many2one('res.partner','Cooperator', readonly=True , required=True),
        'date': fields.date('Subscription Date', readonly=True , required= True),
        'quantity': fields.integer('Number of share', readonly=True),
        'type': fields.selection([('subscription','Subscription'),('transfer','Transfer'),('sell_back','Sell Back')],'Operation Type', readonly=True),
        'company_id': fields.many2one('res.company', 'Company', required=True, change_default=True, readonly=True),
        'user_id': fields.many2one('res.users', 'Responsible', readonly=True),
    }
    
    _defaults = {
        'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, context=c),
        'user_id': 1,
    }
    
    _order = "register_number_operation asc"
    