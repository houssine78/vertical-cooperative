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

	<table width="100%" class="list_certificat_table">   
	    <br />
	    <tr>
	        <th width="15%" style="text-align: center;" >${_("Cooperator number")}</th>
	        <th width="15%" style="text-align: center;" >${_("Name")}</th>
	        <th width="15%" style="text-align: center;" >${_("Email")}</th>
	        <th width="15%" style="text-align: center;" >${_("Effective date")}</th>
	        <th width="15%" style="text-align: center;">${_("Quantity")}</th>
	        <th width="15%" style="text-align: center;" >${_("Total")}</th>
	    </tr>
	    <!-- Compteur de ligne-->
	    <% rowNumber=0 %>
	    <% moduloNumber=0 %>
	    <% grand_total_share = 0 %>
	    <% grand_total_amount = 0.0 %>
    %for partner_id in objects:
    <% setLang(partner_id.lang) %>
    	<% rowNumber = rowNumber + 1 %>
        <% number_of_share = 0 %>
		<% total_amount = 0.0 %>
        %if (rowNumber % 2)==1 : 
 			<tr style="background-color: #b2e5dc">
 			%else :
            <tr>
             %endif
                <td width="15%" class="amount">${partner_id.cooperator_register_number}</td>
                <td width="15%" class="amount">${partner_id.name}</td>
                <td width="15%" class="amount">${partner_id.email}</td>
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount"></td>
            </tr>
        %for line in partner_id.share_ids :
        	<% number_of_share += line.share_number %>
        	<% total_amount += line.total_amount_line %>
          	
 			%if (rowNumber % 2)==1 : 
 			<tr style="background-color: #b2e5dc">
 			%else :
            <tr>
             %endif
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount">${line.payment_ref}</td>
                <td width="15%" class="amount">${line.effective_date}</td>
                <td width="15%" class="amount">${line.share_number}</td>
                <td width="15%" class="amount">${formatLang(line.total_amount_line,digits=get_digits(dp='Account'))} ${_("€")}</td>
            </tr>
        %endfor
        <% grand_total_share += number_of_share %>
    	<% grand_total_amount += total_amount %>
    	%if (rowNumber % 2)==1 : 
 			<tr style="background-color: #b2e5dc">
 			%else :
            <tr>
             %endif
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount"></td>
                <td width="15%" class="amount">${_("Total")}</td>
                <td width="15%" class="amount"><b>${number_of_share}</b></td>
                <td width="15%" class="amount">${formatLang(total_amount, digits=get_digits(dp='Account'))} ${_("€")}</td>
            </tr>
    %endfor
    
    <table class="list_certificat_table" style="margin-top:10px ;margin-left:50%; margin-bottom:10px;" width="50%">
		<br /><br />
		<tr>
            <td width="35%" style="text-align:center;" class="cell_gradiant"><b>${_("Total number of share")}</b></td>
        	<td width="15%" style="text-align:center;" class="cell_gradiant"><b>${_("Total")}</b></td>
        </tr>
        <tr>
        	<td style="text-align:center;"><b>${grand_total_share}</b></td>
        	<td class="amount"><b>${formatLang(grand_total_amount, digits=get_digits(dp='Account'))} ${_("€")}</b></td>
        </tr>
    </table>
	</table>
    <p style="page-break-after:always"></p>
</body>
</html>
