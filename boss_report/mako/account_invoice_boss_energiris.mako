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
            <tr><td>${'TVA : '} ${inv.partner_id.vat or '-'}</td></tr>
            %endif
        </table>
    </div>
    
    <div>

    </div>
    <h1 style="clear: both; padding-bottom: 5px; border-bottom: #00ccff 1px solid;width: 150px;text-align: center">
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
 
    <h1 class="center_text">
        ${inv.number or ''}    
    </h1>

    <table class="info_table" width="100%">
        <tr>
        	%if inv.type == 'out_refund':
                <th style="text-align: center;" class="cell_gradiant" width="12%" >${_("Date document")}</th>
            %else :
                <th style="text-align: center;" class="cell_gradiant" width="12%" >${_("Date facture")}</th>
            %endif       
 
            <th style="text-align: center;" class="cell_gradiant " width="12%" >${_("Due Date")}</th>
            <th style="text-align: left;text-indent:20px;" class="cell_gradiant " width="54%">${_("Objet")}</th>
            <th style="text-align: center;" class="cell_gradiant " width="20%">${_("Votre reference")}</th>
        </tr>
        <tr>
            <td style="text-align: center;border-right: #00ccff 1px solid;" class="date">${formatLang(inv.date_invoice, date=True)}</td>
            <td style="text-align: center;border-right: #00ccff 1px solid;" class="date">${formatLang(inv.date_due, date=True)}</td>
            <td width="20%" style="text-align: left;text-indent:20px">${inv.origin or ''}</td>
        </tr>
    </table>

	</br></br>
    
    <table class="list_line_table_head" width="100%" style="margin-top: 20px;">
            <tr>
                <th width="55%" style="text-align: left;text-indent:20px"  >${_("Description")}</th>
                <th width="7%" style="text-align: center;">${_("Qte")}</th>
                <th width="8%" style="text-align: center;" >${_("Unite")}</th>
                <th width="15%" style="text-align: center;" >${_("Prix unitaire")}</th>
                <th width="15%" style="text-align: center;" >${_("HTVA")}</th>
            </tr>
    </table>
    
    <table width="100%" style="margin-top: 20px; margin-bottom: 20px;">   
        
        <!-- Compteur de ligne-->
        <% rowNumber=0 %>
        <% moduloNumber=0 %>
        %for line in inv.invoice_line :
          	<% rowNumber = rowNumber + 1 %>
 			%if (rowNumber % 2)==0 : 
 		
 			<tr style="background-color: #f3d2c0">
                <td width="55%">${line.name}</td>
                <td width="7%" class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                <td width="8%" class="amount">${line.uos_id and line.uos_id.name or ''}</td>
                <td width="15%" class="amount">${formatLang(line.price_unit,digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
                <td width="15%" class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>

            %else :
            <tr>
                <td width="55%">${line.name}</td>
                <td width="7%" class="amount">${formatLang(line.quantity or 0.0,digits=get_digits(dp='Account'))}</td>
                <td width="8%" class="amount">${line.uos_id and line.uos_id.name or ''}</td>
                <td width="15%" class="amount">${formatLang(line.price_unit,digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
                <td width="15%" class="amount">${formatLang(line.price_subtotal, digits=get_digits(dp='Account'))} ${inv.currency_id.symbol}</td>
            </tr>
            
            %endif
        %endfor
    </table>
    
    <hr style="border-top : 1px solid #00ccff;" width="100%">
    
    <table class="list_line_table_head" style="margin-top:10px ;margin-left:50%; margin-bottom:10px;border:1px solid #00ccff;" width="50%">
			<tr></tr>
			<tr>
                <th width="25%" style="text-indent:5px;border-bottom:1px solid #00ccff" ><b>${_("Taux")}</b></th>
                <th width="10%" style="text-align:center;border-bottom:1px solid #00ccff" ><b>${_("Base TVA")}</b></th>
                <th width="15%" style="text-align:center;border-bottom:1px solid #00ccff" ><b>${_("Taxe")}</b></th>
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
 
    <hr style="margin-left:50%;border-top : 1px solid #00ccff;" width="50%">
    
    <table style="margin-top:10px ;margin-left:50%; margin-bottom:10px;border:1px solid #00ccff;" width="50%">
			<tr>
                <td width="35%" style="text-align:center;" class="cell_gradiant"><b>${_("Ref. paiement")}</b></td>

        		%if inv.type == 'out_refund':
                	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("A valoir")}</b></td>
                %else :
                	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("A payer")}</b></td>
                %endif                
            </tr>
            <tr>
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
