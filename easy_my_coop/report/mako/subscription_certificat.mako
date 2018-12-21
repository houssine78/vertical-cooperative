<html>

<head>
    <style type="text/css">
        ${css}
        
.list_certificat_table {
    border-collapse: collapse;
    border: 1px solid #00ccff;
    margin-top: 20px; 
	margin-bottom: 20px;
}

.list_certificat_table th {
    border-collapse: collapse;
    border: 1px solid #00ccff;
}

.list_certificat_table tr {
    border-collapse: collapse;
    border: 1px solid #00ccff;
}

.list_certificat_table td {
    border-collapse: collapse;
    border: 1px solid #00ccff;
}
    </style>
</head>
<body>
    <%page expression_filter="entity"/>
    <%
    def carriage_returns(text):
        return text.replace('\n', '<br />')
    %>

    %for cert in objects:
    <% setLang(cert.partner_id.lang) %>
    <div class="address">
        <table class="recipient">
            <br /><br /><br /><br />
            %if cert.partner_id.parent_id.name:
            	<tr><td><b>${cert.partner_id.parent_id.name}</b></td></tr>    
                <tr><td>${cert.partner_id.title and cert.partner_id.title.name or ''} ${cert.partner_id.name }</td></tr>
             %else:
                <tr><td class="name">${cert.partner_id.title and cert.partner_id.title.name or ''} ${cert.partner_id.name }</td></tr>
			 	<tr><td> <br/> </td></tr>
			 %endif             
            
            <tr><td>${cert.partner_id.street or ''}</td></tr>
            <tr><td>${cert.partner_id.street2 or ''}</td></tr>
            <tr><td>${cert.partner_id.zip or ''} ${cert.partner_id.city or ''}</td></tr>
            %if cert.partner_id.country_id:
            <tr><td>${cert.partner_id.country_id.name or ''} </td></tr>
            %endif
        </table>
    </div>
    
    <h1 style="clear: both; padding-bottom: 15px; border-bottom: #00ccff 1px solid;width: 600px;text-align: center">
        <br /><br /><br /><br />
        ${cert.partner_id.name} ${_("is registered in the cooperator register under the number ")} ${cert.partner_id.cooperator_register_number or ''}
    </h1>
 
    <table width="100%" class="list_certificat_table">   
        <br />
        <tr>
            <th width="15%" style="text-align: center;" >${_("Effective date")}</th>
            <th width="15%" style="text-align: center;">${_("Quantity")}</th>
            <th width="15%" style="text-align: center;" >${_("Unit price")}</th>
            <th width="15%" style="text-align: center;" >${_("Total")}</th>
        </tr>
        <!-- Compteur de ligne-->
        <% rowNumber=0 %>
        <% moduloNumber=0 %>
        <% number_of_share = 0 %>
			<% total_amount = 0.0 %>
        %for line in cert.partner_id.share_ids :
        	<% number_of_share += line.share_number %>
        	<% total_amount += line.total_amount_line %>
          	<% rowNumber = rowNumber + 1 %>
 			%if (rowNumber % 2)==0 : 
 			<tr style="background-color: #b2e5dc">
 			%else :
            <tr>
             %endif
                <td width="15%" class="amount">${line.effective_date}</td>
                <td width="15%" class="amount">${line.share_number}</td>
                <td width="15%" class="amount">${formatLang(line.unit_price,digits=get_digits(dp='Account'))} ${_("€")}</td>
                <td width="15%" class="amount">${formatLang(line.total_amount_line,digits=get_digits(dp='Account'))} ${_("€")}</td>
            </tr>
        %endfor
    </table>
    
    <table class="list_certificat_table" style="margin-top:10px ;margin-left:50%; margin-bottom:10px;" width="50%">
		<br /><br />
		<tr>
            <td width="35%" style="text-align:center;" class="cell_gradiant"><b>${_("Total number of share")}</b></td>
        	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("Total")}</b></td>
        </tr>
        <tr>
        	<td style="text-align:center;"><b>${number_of_share}</b></td>
        	<td class="amount"><b>${formatLang(total_amount, digits=get_digits(dp='Account'))} ${_("€")}</b></td>
        </tr>
    </table>
    %endfor

    <p style="page-break-after:always"></p>
</body>
</html>
