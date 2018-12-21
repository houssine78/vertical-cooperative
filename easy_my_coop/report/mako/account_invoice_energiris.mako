<html>

<head>
    <style type="text/css">
        ${css}

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
            <br /><br /><br /><br />
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
            <tr><td>${_(inv.partner_id.country_id.name) or ''} </td></tr>
            %endif
            %if inv.partner_id.vat:
            <tr><td>${'TVA : '} ${inv.partner_id.vat or '-'}</td></tr>
            %endif
        </table>
    </div>
    

    <h1 style="clear: both; padding-bottom: 5px; border-bottom: #5fe5ce 1px solid;width: 300px;text-align: center">
		<br /><br />
		%if inv.release_capital_request == True :
			${_("Request to release capital")}
        %elif inv.type == 'out_invoice' and inv.state == 'proforma2':
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
 
<br /><br />
    <table class="info_table" width="40%">
        <tr>
        	%if inv.type == 'out_refund':
                <th style="text-align: center;" class="cell_gradiant" width="12%" >${_("Date document")}</th>
            %else :
                <th style="text-align: center;" class="cell_gradiant" width="12%" >${_("Date document")}</th>
            %endif       
 
            <th style="text-align: center;" class="cell_gradiant " width="12%" >${_("Due Date")}</th>
            <th style="text-align: center;" class="cell_gradiant " width="12%" >${_("Document Number")}</th>
            %if inv.origin:
            <th style="text-align: center;" class="cell_gradiant " width="20%">${_("Votre reference")}</th>
            %endif
        </tr>
        <tr>
            <td style="text-align: center;border-right: #5fe5ce 1px solid;" class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td style="text-align: center;border-right: #5fe5ce 1px solid;" class="date">${formatLang(inv.date_due, date=True)}</td>
            %if inv.origin:
            <td width="20%" style="text-align: left;text-indent:20px">${inv.origin or ''}</td>
            %endif
            <td style="text-align: center;border-right: #5fe5ce 1px solid;" class="date">${inv.number or ''}</td>
        </tr>
    </table>

	</br></br>
    
    <table class="list_line_table_head" width="100%" style="margin-top: 20px;">
            <tr>
                <th width="55%" style="text-align: left;text-indent:20px"  >${_("Description")}</th>
                <th width="7%" style="text-align: center;">${_("Quantity")}</th>
                <th width="8%" style="text-align: center;" >${_("UoM")}</th>
                <th width="15%" style="text-align: center;" >${_("Unit price")}</th>
                %if inv.release_capital_request == True :
            	<th width="15%" style="text-align: center;" >${_("Total")}</th>
                %else:
                <th width="15%" style="text-align: center;" >${_("HTVA")}</th>
                %endif
            </tr>
    </table>
    
    <table width="100%" style="margin-top: 20px; margin-bottom: 20px;">   
        
        <!-- Compteur de ligne-->
        <% rowNumber=0 %>
        <% moduloNumber=0 %>
        %for line in inv.invoice_line :
          	<% rowNumber = rowNumber + 1 %>
 			%if (rowNumber % 2)==0 : 
 			<tr style="background-color: #b2e5dc">
            %else :
            <tr>
            %endif
                <td width="55%">${line.name}</td>
                <td width="7%" class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                %if inv.release_capital_request == True :
                <td width="8%" class="amount">${_("Part(s)")}</td>
                %else:
                <td width="8%" class="amount">${line.uos_id and line.uos_id.name or ''}</td>
                %endif
                <td width="15%" class="amount">${formatLang(line.price_unit,digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
                <td width="15%" class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            
            
        %endfor
    </table>
    
    <hr style="border-top : 1px solid #5fe5ce;" width="100%">
    %if len(inv.tax_line) > 0:

    <table class="list_line_table_head" style="margin-top:10px ;margin-left:50%; margin-bottom:10px;border:1px solid #5fe5ce;" width="50%">
			<tr></tr>
			<tr>
                <th width="25%" style="text-indent:5px;border-bottom:1px solid #5fe5ce" ><b>${_("Taux")}</b></th>
                <th width="10%" style="text-align:center;border-bottom:1px solid #5fe5ce" ><b>${_("Base TVA")}</b></th>
                <th width="15%" style="text-align:center;border-bottom:1px solid #5fe5ce" ><b>${_("Taxe")}</b></th>
            </tr>

            %if inv.tax_line :
            %for t in inv.tax_line :
            <tr>
                <td style="text-align:left;text-indent:5px;">${ t.name } </td>
                <td class="amount">${ formatLang(t.base, digits=get_digits(dp='Account')) } ${inv.currency_id.symbol}</td>
                <td class="amount">${ formatLang(t.amount, digits=get_digits(dp='Account')) } ${inv.currency_id.symbol}</td>
            </tr>
            %endfor
            %endif

     </table>
 
    <hr style="margin-left:50%;border-top : 1px solid #5fe5ce;" width="50%">
     %endif
    
     %for bank in company.bank_ids :     
         <% bank_account = bank.acc_number %>
    %endfor

    <table style="margin-top:10px ;margin-left:50%; margin-bottom:10px;border:1px solid #5fe5ce;" width="70%">
			<tr>
				<td width="20%" style="text-align:center;" class="cell_gradiant"><b>${_("Bank Account")}</b></td>
                
                <td width="35%" style="text-align:center;" class="cell_gradiant"><b>${_("Payment reference")}</b></td>

        		%if inv.type == 'out_refund':
                	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("A valoir")}</b></td>
                %else :
                	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("To pay")}</b></td>
                %endif                
            </tr>
            <tr>
            	<td style="text-align:center;"><b>${bank_account}</b></td>
            	<td style="text-align:center;"><b>${inv.reference or ''}</b></td>
            	<td class="amount"><b>${formatLang(inv.amount_total, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</b></td>
            </tr>
    </table>
         
    %if inv.comment :
        <p class="fiducis_text">${inv.comment | carriage_returns}</p>
    %endif
    %endfor

    <p style="page-break-after:always"></p>
</body>
</html>
