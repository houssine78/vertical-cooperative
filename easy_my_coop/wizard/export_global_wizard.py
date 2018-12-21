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

import time
from cStringIO import StringIO
import base64

import xlsxwriter

HEADER = [
        'Num. Coop',
        'Numero de registre national',
        'Nom',
        'Email',
        'Banque',
        'Mobile',
        'Adresse',
        'Rue',
        'Code Postal',
        'Ville',
        'Pays',
        'Nombre de part total',
        'Montant total des parts',
        'Numero de demande',
        'Statut',
        'Demande de liberation de capital',
        'Communication',
        'Nombre de part',
        'Montant',
        'Reception du paiement',
        'Date de la souscription'
        ]
HEADER2 = [
        'Date de la souscription',
        'Nom',
        'Type',
        'Nombre de part',
        'Montant',
        'Statut',
        'Numero de registre national',
        'Email',
        'Mobile',
        'Adresse',
        'Code Postal',
        'Ville',
        'Pays',
        ]
            
class export_global_report(osv.Model):
    _name = 'export.global.report'
    
    _columns = {
        'name': fields.char('Name',size=64),
    }
    
    def write_header(self, worksheet,headers):
        i = 0
        for header in headers:
            worksheet.write(0,i, header)
            i+=1
        return True
    
    def export_global_report_xlsx(self, cr,uid,ids,context):
        wizard_data = self.browse(cr, uid, ids, context)[0]
        partner_obj = self.pool.get('res.partner')
        invoice_obj = self.pool.get('account.invoice')
        subscription_obj = self.pool.get('job.sync.line')
        
        file_data = StringIO()
        workbook = xlsxwriter.Workbook(file_data)
        worksheet1 = workbook.add_worksheet()

        self.write_header(worksheet1,HEADER)
        cooperators = partner_obj.search(cr, uid, [('cooperator','=',True),('member','=',True)])
        
        j=1
        for coop in partner_obj.browse(cr,uid,cooperators,context):
            i = 0
            worksheet1.write(j,i, coop.int_cooperator_register_number)
            i+=1
            worksheet1.write(j,i, coop.national_register_number)
            i+=1
            worksheet1.write(j,i, coop.name)
            i+=1
            worksheet1.write(j,i, coop.email)
            i+=1
            worksheet1.write(j,i, coop.bank_ids[0].acc_number)
            i+=1
            worksheet1.write(j,i, coop.phone)
            i+=1
            worksheet1.write(j,i, coop.street + ' ' + coop.zip + ' ' + coop.city+ ' ' + coop.country_id.name)
            i+=1
            worksheet1.write(j,i, coop.street)
            i+=1
            worksheet1.write(j,i, int(coop.zip))
            i+=1
            worksheet1.write(j,i, coop.city)
            i+=1
            worksheet1.write(j,i, coop.country_id.name)
            i+=1
            worksheet1.write(j,i, coop.number_of_share)
            i+=1
            worksheet1.write(j,i, coop.total_value)

            invoice_ids = invoice_obj.search(cr,uid,[('release_capital_request','=',True),('partner_id','=',coop.id)])
            j+=1
            for invoice in invoice_obj.browse(cr,uid,invoice_ids,context):
                i=11
                worksheet1.write(j,i, invoice.internal_number)
                i+=1
                worksheet1.write(j,i, invoice.state)
                i+=1
                worksheet1.write(j,i, invoice.date_invoice)
                i+=1
                worksheet1.write(j,i, invoice.reference)
                i+=1
                for line in invoice.invoice_line:
                    worksheet1.write(j,i, line.quantity)
                    i+=1
                    worksheet1.write(j,i, line.price_subtotal)
                    i+=1
                if invoice.payment_ids :
                    worksheet1.write(j,i, invoice.payment_ids[0].date)
                i+=1
                if invoice.subscription_request:
                    ind = len(invoice.subscription_request)-1
                    worksheet1.write(j,i, invoice.subscription_request[ind].sync_date)
                j+=1
            
            sub_requests = subscription_obj.search(cr, uid, ['|',('state','=','draft'),('state','=','waiting'),('partner_id','=',coop.id)])
            for sub_request in subscription_obj.browse(cr,uid,sub_requests,context):
                i=11
                worksheet1.write(j,i, dict(subscription_obj._columns['type'].selection).get(sub_request.type,False))
                i+=1
                worksheet1.write(j,i, sub_request.state)
                i+=3
                quantity = int(sub_request.ordered_parts)
                worksheet1.write(j,i, quantity)
                i+=1
                amount = quantity * 250
                worksheet1.write(j,i, amount)
                i+=2 
                worksheet1.write(j,i, sub_request.sync_date)
                j+=1
        
        worksheet1bis = workbook.add_worksheet()
        self.write_header(worksheet1bis,HEADER)
        cooperators = partner_obj.search(cr, uid, [('cooperator','=',True),('member','=',False)])
        
        j=1
        for coop in partner_obj.browse(cr,uid,cooperators,context):
            i = 0
            worksheet1bis.write(j,i, coop.int_cooperator_register_number)
            i+=1
            worksheet1bis.write(j,i, coop.national_register_number)
            i+=1
            worksheet1bis.write(j,i, coop.name)
            i+=1
            worksheet1bis.write(j,i, coop.email)
            i+=1
            worksheet1bis.write(j,i, coop.phone)
            i+=1
            worksheet1bis.write(j,i, coop.street)
            i+=1
            worksheet1bis.write(j,i, int(coop.zip))
            i+=1
            worksheet1bis.write(j,i, coop.city)
            i+=1
            worksheet1bis.write(j,i, coop.country_id.name)
            i+=1
            worksheet1bis.write(j,i, coop.number_of_share)
            i+=1
            worksheet1bis.write(j,i, coop.total_value)

            invoice_ids = invoice_obj.search(cr,uid,[('release_capital_request','=',True),('partner_id','=',coop.id)])
            j+=1
            for invoice in invoice_obj.browse(cr,uid,invoice_ids,context):
                i=11
                worksheet1bis.write(j,i, invoice.internal_number)
                i+=1
                worksheet1bis.write(j,i, invoice.state)
                i+=1
                worksheet1bis.write(j,i, invoice.date_invoice)
                i+=1
                worksheet1bis.write(j,i, invoice.reference)
                i+=1
                for line in invoice.invoice_line:
                    worksheet1bis.write(j,i, line.quantity)
                    i+=1
                    worksheet1bis.write(j,i, line.price_subtotal)
                    i+=1
                if invoice.payment_ids :
                    worksheet1bis.write(j,i, invoice.payment_ids[0].date)
                i+=1
                if invoice.subscription_request:
                    ind = len(invoice.subscription_request)-1
                    worksheet1bis.write(j,i, invoice.subscription_request[ind].sync_date)
                j+=1
            
            sub_requests = subscription_obj.search(cr, uid, ['|',('state','=','draft'),('state','=','waiting'),('partner_id','=',coop.id)])
            for sub_request in subscription_obj.browse(cr,uid,sub_requests,context):
                i=11
                worksheet1bis.write(j,i, dict(subscription_obj._columns['type'].selection).get(sub_request.type,False))
                i+=1
                worksheet1bis.write(j,i, sub_request.state)
                i+=3
                quantity = int(sub_request.ordered_parts)
                worksheet1bis.write(j,i, quantity)
                i+=1
                amount = quantity * 250
                worksheet1bis.write(j,i, amount)
                i+=2 
                worksheet1bis.write(j,i, sub_request.sync_date)
                j+=1  
                     
        worksheet2 = workbook.add_worksheet()
        self.write_header(worksheet2,HEADER2)
        sub_requests = subscription_obj.search(cr, uid, ['|',('state','=','draft'),('state','=','waiting')])

        j=1
        for sub_request in subscription_obj.browse(cr,uid,sub_requests,context):
            i=0
            worksheet2.write(j,i, sub_request.sync_date)
            i+=1
            worksheet2.write(j,i, sub_request.name)
            i+=1
            worksheet2.write(j,i, dict(subscription_obj._columns['type'].selection).get(sub_request.type,False))
            i+=1
            quantity = int(sub_request.ordered_parts)
            worksheet2.write(j,i, quantity)
            i+=1
            amount = quantity * 250
            worksheet2.write(j,i, amount)
            i+=1 
            worksheet2.write(j,i, sub_request.state)
            i+=1     
            worksheet2.write(j,i, sub_request.no_registre)
            i+=1
            worksheet2.write(j,i, sub_request.email)
            i+=1
            worksheet2.write(j,i, sub_request.phone)
            i+=1
            worksheet2.write(j,i, sub_request.adresse)
            i+=1
            worksheet2.write(j,i, sub_request.ville)
            i+=1
            worksheet2.write(j,i, int(sub_request.codepostal))
            i+=1
            worksheet2.write(j,i, sub_request.pays)
            j+=1

        workbook.close()
        file_data.seek(0)
        
        data = base64.encodestring(file_data.read())

        attachment_id = self.pool.get('ir.attachment').create(cr,uid,{
                'name':"Global export" + time.strftime('%Y-%m-%d %H:%M') +".xlsx",
                'datas':data,
                'datas_fname': 'Global_export.xlsx',
                'res_model':'export.global.report',
                'res_id':wizard_data.id, 
                'partner_id': 1,                       
                },)   
        return {
            'name': 'Exported file',
            'res_model': 'ir.attachment',
            'view_id': False,
            'res_id':attachment_id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'context': context,
        }