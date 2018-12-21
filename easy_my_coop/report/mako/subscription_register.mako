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
	        <th width="15%" style="text-align: center;" >${_("Register number operation")}</th>
	        <th width="15%" style="text-align: center;" >${_("Cooperator")}</th>
	        <th width="15%" style="text-align: center;">${_("Share number")}</th>
	        <th width="15%" style="text-align: center;" >${_("Subscription date")}</th>
	        <th width="15%" style="text-align: center;" >${_("Operation type")}</th>
	    </tr>
	    <!-- line counter-->
	    <% rowNumber=0 %>
	    <% moduloNumber=0 %>
    %for subscription in objects:
    <% setLang(subscription.partner_id.lang) %>
    	<% rowNumber = rowNumber + 1 %>
		%if (rowNumber % 2)==0 : 
		<tr style="background-color: #b2e5dc">
		%else :
        <tr>
         %endif
            <td width="15%" class="amount">${subscription.name}</td>
            <td width="15%" class="amount">${subscription.partner_id.name}</td>
            <td width="15%" class="amount">${subscription.quantity}</td>
            <td width="15%" class="amount">${subscription.date}</td>
            <td width="15%" class="amount">${subscription.type}</td>            
        </tr>
    %endfor
	</table>
    <p style="page-break-after:always"></p>
</body>
</html>
