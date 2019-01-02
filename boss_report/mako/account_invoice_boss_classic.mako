<html>

<!-- Orange : #e36522 Turquoise : #24a9e1-->
<!-- Orange : #f3d2c0 Turquoise : #e3f0f6-->

<head>
    <style type="text/css">
        ${css}

.list_invoice_table {
    text-align:center;
    border-collapse: collapse;
}

.list_invoice_table th {
    border-bottom: #24a9e1 1px solid;
    text-align:center;
    font-size:13;
    font-weight:bold;
    color : #24a9e1;
    padding-right:3px;
    padding-left:3px;
}
.list_invoice_table td {
    text-align:left;
    font-size:13;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}
.list_invoice_table thead {
    display:table-header-group;
}


.list_bank_table {
    text-align:center;
    border-collapse: collapse;
}
.list_bank_table th {
    text-align:left;
    font-size:13;
    font-weight:bold;
    padding-right:3px;
    padding-left:3px;
}
.list_bank_table td {
    text-align:left;
    font-size:13;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}


.list_tax_table {
}

.list_tax_table td {
    text-align:left;
    font-size:13;
}

.list_tax_table th {
}

.list_tax_table thead {
    display:table-header-group;
}

.list_total_table {
    text-align:center;
    border-collapse: collapse;
}

.list_total_table td {
    text-align:left;
    font-size:13;
    padding-right:3px;
    padding-left:3px;
    padding-top:3px;
    padding-bottom:3px;
}

.list_total_table th {
    text-align:center;
    font-size:13;
    font-weight:bold;
    padding-right:3px
    padding-left:3px
}

.list_total_table thead {
    display:table-header-group;
}


.no_bloc {

}

.right_table {
    right: 4cm;
    width:"100%";
}

.std_text {
    font-family:calibri;
    font-size:13;
}

.column_text {
   font-family:calibri;
   font-size:13;
   text-align: center;
   width:150px;
   padding-bottom: 50px;
}

.column_title {
   background-color: #24a9e1;
}


td.amount {
    text-align: right;
}

tfoot.totals tr:first-child td{
    padding-top: 15px;
}

th.date {
    width: 90px;
}

td.date {
    white-space: nowrap;
    width: 90px;
}

td.vat {
    white-space: nowrap;
}

    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    %for inv in objects:
    <% setLang(inv.partner_id.lang) %>
    <div class="address">
        <table class="recipient">
            
            %if inv.partner_id.parent_id.name:
            	<tr><td><b>${inv.partner_id.parent_id.name}</b></td></tr>    
                <tr><td>${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td></tr>
             %else:
                <tr><td class="name">${inv.partner_id.title and inv.partner_id.title.name or ''} ${inv.partner_id.name }</td></tr>
			 	<tr><td> <br/> </td></tr>
			 %endif             
            
            <tr><td>${inv.partner_id.street or ''}</td></tr>
            <tr><td>${inv.partner_id.street2 or ''}</td></tr>
            <tr><td>${inv.partner_id.zip or ''} ${inv.partner_id.city or ''}</td></tr>
            %if inv.partner_id.country_id:
            <tr><td>${inv.partner_id.country_id.name or ''} </td></tr>
            <tr><td>${'VAT number : '} ${inv.partner_id.vat or '-'}</td></tr>
            %endif
        </table>
    </div>
    
    <div>

    %if inv.note1_webkit :
        <p class="std_text"> ${inv.note1_webkit | carriage_returns} </p>
    %endif
    </div>
    <h1 style="clear: both; padding-bottom: 5px; border-bottom: #24a9e1 1px solid;width: 150px;text-align: center">
        %if inv.type == 'out_invoice' and inv.state == 'proforma2':
            ${_("PRO-FORMA")}
        %elif inv.type == 'out_invoice' and inv.state == 'draft':
            ${_("DRAFT INVOICE")}
        %elif inv.type == 'out_invoice' and inv.state == 'cancel':
            ${_("Cancelled Invoice")}
        %elif inv.type == 'out_invoice':
            ${_("INVOICE")}
        %elif inv.type == 'in_invoice':
            ${_("SUPPLIER INVOICE")}
        %elif inv.type == 'out_refund':
            ${_("REFUND")} 
        %elif inv.type == 'in_refund':
            ${_("SUPPLIER REFUND")} 
        %endif
    </h1>
 
    <h1 class="column_text">
        ${inv.number or ''}    
    </h1>

    <table class="basic_table" width="100%">
        <tr class="column_title">
            <th class="date">${_("Invoice Date")}</td>
            <th class="date">${_("Due Date")}</td>
            <th style="text-align: left;text-indent:20px">${_("Subject")}</td>
            <th style="text-align: left;text-indent:20px">${_("Paiement Ref.")}</td>
        </tr>
        <tr>
            <td class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td class="date">${formatLang(inv.date_due, date=True)}</td>
            <td style="text-align: left;text-indent:20px"> ${inv.object or ''}</td>
            <td width="20%" style="text-align: left;text-indent:20px">${inv.reference or ''}</td>
        </tr>
    </table>

	</br></br>
    <table class="list_invoice_table" width="100%" style="margin-top: 20px;">
        <thead>
            <tr>
                <th colspan="3" style="text-align: left;text-indent:20px">${_("Description")}</th>
                <th style="text-align: right;">${_("Qty")}</th>
                <th style="text-align: right;">${_("Unit")}</th>
                <th style="text-align: right;">${_("Unit Price")}</th>
                <th style="text-align: right;">${_("Net Sub Total")}</th>
            </tr>
        </thead>
        <tbody>
        <!-- Compteur de ligne-->
        <% rowNumber=0 %>
        <% moduloNumber=0 %>
        %for line in inv.invoice_line :
          	<% rowNumber = rowNumber + 1 %>
 			%if (rowNumber % 2)==0 : 
 			<tr style="background-color: #e3f0f6">
                <td colspan="3">${line.name}</td>
                <td class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                <td class="amount">${line.uos_id and line.uos_id.name or ''}</td>
                <td class="amount">${formatLang(line.price_unit)}</td>
                <td class="amount" width="13%">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            %else :
            <tr>
                <td colspan="3">${line.name}</td>
                <td class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                <td class="amount">${line.uos_id and line.uos_id.name or ''}</td>
                <td class="amount">${formatLang(line.price_unit)}</td>
                <td class="amount" width="13%">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            %endif
        %endfor
        </tbody>
        <tfoot class="totals">
            <tr>
            	<td></td>
           	</tr>
            <tr>
                <td colspan="5"></td>
                <td colspan="1" style="text-align:right;border-top: #24a9e1 1px solid;color:#24a9e1">
                    <b>${_("Net :")}</b>
                </td>
                <td class="amount" style="border-top: #24a9e1 1px solid;">
                    ${formatLang(inv.amount_untaxed, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                </td>
            </tr>
            <tr class="no_bloc">
                <td colspan="6" style="color:#24a9e1;text-align:right">
                    <b>${_("Taxes:")}</b>
                </td>
                <td class="amount">
                        ${formatLang(inv.amount_tax, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}
                </td>
            </tr>
            <tr>
                <td colspan="6" style="color:#24a9e1 ;text-align:right;">
                    <b>${_("Total:")}</b>
                </td>
                <td class="amount">
                        <b>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</b>
                </td>
            </tr>
        </tfoot>
    </table>
        <br/></br></br>
    
    <table class="list_total_table" width="40%" >
        <tr>
            <th style="text-align:left;background-color: #24a9e1">${_("Rate")}</th>
            <th style="background-color: #24a9e1">${_("Base")}</th>
            <th style="background-color: #24a9e1">${_("Tax")}</th>            
        </tr>
        %if inv.tax_line :
        %for t in inv.tax_line :
            <tr>
                <td style="text-align:left;">${ t.name } </td>
                <td class="amount">${ formatLang(t.base, digits=get_digits(dp='Account')) }</td>
                <td class="amount">${ formatLang(t.amount, digits=get_digits(dp='Account')) }</td>
            </tr>
        %endfor
        %endif

    </table>
        <br/>
        <br/>
        <br/>
    <br/>
    %if inv.comment :
        <p class="fiducis_text">${inv.comment | carriage_returns}</p>
    %endif
    %if inv.note2_webkit :
        <p class="fiducis_text">${inv.note2_webkit | carriage_returns}</p>
    %endif
    %endfor
    
</body>
</html>
