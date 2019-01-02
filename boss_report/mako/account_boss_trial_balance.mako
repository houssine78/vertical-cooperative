<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <style type="text/css">
            .account_level_1 {
                text-transform: uppercase;
                font-size: 15px;
            }

            .account_level_2 {
                font-size: 14px;
            }

            .report_table_title {
                font-size : 14px;
                text-align : center;
            }
            
            .regular_account_type {
                font-weight: normal;
            }

            .view_account_type {
                font-weight: bold;
            }

            .account_level_consol {
                font-weight: normal;
            	font-style: italic;
            }

            ${css}

            .list_table .act_as_row {
                margin-top: 10px;
                margin-bottom: 10px;
                font-size:12px;
            }
        </style>
    </head>
    <body>

        <%setLang(user.lang)%>
        
        <%
        langue = user.lang
        
        def amount(text):

            if '-' in text :
               LongText=float(text)
               print(LongText)
               FormatText=('{0:,.2f}'.format(LongText)) 
               
               if langue == 'fr_FR':
               	  FormatText = FormatText.replace(',', 'T')
               	  FormatText = FormatText.replace('.', ',')
               	  FormatText = FormatText.replace('T', '.')
               	  return FormatText.replace('-', ' ') + ' C'
               else:
               	  return FormatText.replace('-', ' ') + ' C'  
            else : 
               LongText=float(text)
               FormatText=('{0:,.2f}'.format(LongText))
               if langue == 'fr_FR':
               	  FormatText = FormatText.replace(',', 'T')
               	  FormatText = FormatText.replace('.', ',')
               	  FormatText = FormatText.replace('T', '.')
               	  return FormatText + ' D'
               else:
               	  return FormatText + ' D'
               
        def th_separator(text):
               LongText=float(text)
               FormatText=('{0:,.2f}'.format(LongText))
               if langue == 'fr_FR':
               	  FormatText = FormatText.replace(',', 'T')
               	  FormatText = FormatText.replace('.', ',')
               	  FormatText = FormatText.replace('T', '.')
               	  return FormatText 
               else:
               	  return FormatText 
               
        %>

        <%
        initial_balance_text = {'initial_balance': _('Computed'), 'opening_balance': _('Opening Entries'), False: _('No')}
        %>

        <div class="act_as_table data_table">
            <div class="act_as_row labels">
                <div class="act_as_cell">${_('Chart of Account')}</div>
                <div class="act_as_cell">${_('Fiscal Year')}</div>
                <div class="act_as_cell">
                    %if filter_form(data) == 'filter_date':
                        ${_('Dates Filter')}
                    %else:
                        ${_('Periods Filter')}
                    %endif
                </div>
                <div class="act_as_cell">${_('Accounts Filter')}</div>
                <div class="act_as_cell">${_('Target Moves')}</div>
                <div class="act_as_cell">${_('Initial Balance')}</div>
            </div>
            <div class="act_as_row">
                <div class="act_as_cell" >${ chart_account.name }</div>
                <div class="act_as_cell" >${ fiscalyear.name if fiscalyear else '-' }</div>
                <div class="act_as_cell" >
                    ${_('From:')}
                    %if filter_form(data) == 'filter_date':
                        ${formatLang(start_date, date=True) if start_date else u'' }
                    %else:
                        ${start_period.name if start_period else u''}
                    %endif
                    ${_('To:')}
                    %if filter_form(data) == 'filter_date':
                        ${ formatLang(stop_date, date=True) if stop_date else u'' }
                    %else:
                        ${stop_period.name if stop_period else u'' }
                    %endif
                </div>
                <div class="act_as_cell">
                    %if accounts(data):
                        ${', '.join([account.code for account in accounts(data)])}
                    %else:
                        ${_('All')}
                    %endif
                </div>
                <div class="act_as_cell">${ display_target_move(data) }</div>
                <div class="act_as_cell">${ initial_balance_text[initial_balance_mode] }</div>
            </div>
        </div>

        %for index, params in enumerate(comp_params):
            <div class="act_as_table data_table">
                <div class="act_as_row">
                    <div class="act_as_cell">${_('Comparison %s') % (index + 1,)} (${"C%s" % (index + 1,)})</div>
                    <div class="act_as_cell">
                        %if params['comparison_filter'] == 'filter_date':
                            ${_('Dates Filter:')}&nbsp;${formatLang(params['start'], date=True) }&nbsp;-&nbsp;${formatLang(params['stop'], date=True) }
                        %elif params['comparison_filter'] == 'filter_period':
                            ${_('Periods Filter:')}&nbsp;${params['start'].name}&nbsp;-&nbsp;${params['stop'].name}
                        %else:
                            ${_('Fiscal Year :')}&nbsp;${params['fiscalyear'].name}
                        %endif
                    </div>
                    <div class="act_as_cell">${_('Initial Balance:')} ${ initial_balance_text[params['initial_balance_mode']] }</div>
                </div>
            </div>
        %endfor

        <div class="act_as_table list_table" style="margin-top: 20px;">

            <div class="act_as_thead">
                <div class="act_as_row labels">
                    ## code
                    <div class="act_as_cell first_column" style="width: 20px;">${_('Code')}</div>
                    ## account name
                    <div class="act_as_cell" style="width: 80px;">${_('Account')}</div>
                    %if comparison_mode == 'no_comparison':
                        %if initial_balance_mode:
                            ## initial balance
                            <div class="act_as_cell amount" style="width: 30px;">${_('Initial Balance')}</div>
                        %endif
                        ## debit
                        <div class="act_as_cell amount" style="width: 30px;">${_('Debit')}</div>
                        ## credit
                        <div class="act_as_cell amount" style="width: 30px;">${_('Credit')}</div>
                    %endif
                    ## balance
                    <div class="act_as_cell amount" style="width: 30px;">
                    %if comparison_mode == 'no_comparison' or not fiscalyear:
                        ${_('Balance')}
                    %else:
                        ${_('Balance %s') % (fiscalyear.name,)}
                    %endif
                    </div>
                    %if comparison_mode in ('single', 'multiple'):
                        %for index in range(nb_comparison):
                            <div class="act_as_cell amount" style="width: 30px;">
                                %if comp_params[index]['comparison_filter'] == 'filter_year' and comp_params[index].get('fiscalyear', False):
                                    ${_('Balance %s') % (comp_params[index]['fiscalyear'].name,)}
                                %else:
                                    ${_('Balance C%s') % (index + 1,)}
                                %endif
                            </div>
                            %if comparison_mode == 'single':  ## no diff in multiple comparisons because it shows too data
                                <div class="act_as_cell amount" style="width: 30px;">${_('Difference')}</div>
                                <div class="act_as_cell amount" style="width: 30px;">${_('% Difference')}</div>
                            %endif
                        %endfor
                    %endif
                </div>
            </div>

            <div class="act_as_tbody">
                <%
                last_child_consol_ids = []
                last_level = False
  
                total_init_balance = 0
                total_debit = 0
                total_credit = 0
                total_final_balance = 0 
                total_comp_balance = [0,0,0]
                total_diff = 0
                %>
                %for current_account in objects:
                                        
                   <%
                    if not current_account.to_display:
                        continue

                    comparisons = current_account.comparisons

                    if current_account.id in last_child_consol_ids:
                        # current account is a consolidation child of the last account: use the level of last account
                        level = last_level
                        level_class = "account_level_consol"
                    else:
                        # current account is a not a consolidation child: use its own level
                        level = current_account.level or 0
                        level_class = "account_level_%s" % (level,)
                        last_child_consol_ids = [child_consol_id.id for child_consol_id in current_account.child_consol_ids]
                        last_level = current_account.level

                    %>
                    <div class="act_as_row lines ${level_class} ${"%s_account_type" % (current_account.type,)}">
                        ## code
                        <div class="act_as_cell first_column">${current_account.code}</div>
                        ## account name
                        <div class="act_as_cell" style="padding-left: ${level * 5}px;">${current_account.name}</div>
                        
						<%
	                        if current_account.type!='view':
								total_init_balance = total_init_balance + current_account.init_balance
								total_debit = total_debit + current_account.debit
								total_credit = total_credit + current_account.credit
								total_final_balance = total_final_balance + current_account.balance
                        %>                        
                        
                        %if comparison_mode == 'no_comparison':
                            %if initial_balance_mode:
                                ## opening balance
                                <div class="act_as_cell amount">${ (current_account.init_balance) | amount}</div>
                            %endif
                            ## debit
                            <div class="act_as_cell amount">${(current_account.debit) | th_separator}</div>
                            ## credit
                            <div class="act_as_cell amount">${(current_account.credit) | th_separator}</div>
                        %endif
                        ## balance
                        <div class="act_as_cell amount">${(current_account.balance) | amount}</div>

                        %if comparison_mode in ('single', 'multiple'):
                            <% cpt_index = 0 %>
                            %for comp_account in comparisons:
								
								<%
                                    if current_account.type!='view':
								    	total_comp_balance[cpt_index]= total_comp_balance[cpt_index] + comp_account['balance']
								    	cpt_index = cpt_index + 1	
                                %>
								
                                <div class="act_as_cell amount">${(comp_account['balance']) | amount}</div>
                                
                                %if comparison_mode == 'single':  ## no diff in multiple comparisons because it shows too data
                                    <%
                                    if current_account.type!='view':
								    	total_diff = total_diff + comp_account['diff']
                                     %>
                                    
                                    <div class="act_as_cell amount">${(comp_account['diff'])| amount}</div>
                                    <div class="act_as_cell amount"> 
                                    %if comp_account['percent_diff'] is False:
                                     ${ '-' }
                                    %else:
                                       ${int(round(comp_account['percent_diff']))} &#37;
                                    %endif
                                    </div>
                                %endif
                            %endfor
                        %endif
                    </div>
                %endfor
            </div>
        </div>

	## totaux    
    <div class="act_as_table list_table" style="margin-top: 5px;">
            <div class="act_as_thead">
                <div class="act_as_row labels">
                   	<div class="act_as_cell" style="width: 100px; text-align:left">${_('Totals')}</div>

                    %if comparison_mode == 'no_comparison':
                    	<div class="act_as_cell amount" style="width: 30px;">${(total_init_balance) | amount}</div>
                    	<div class="act_as_cell amount" style="width: 30px;">${(total_debit) | th_separator}</div>
	                    <div class="act_as_cell amount" style="width: 30px;">${(total_credit) | th_separator}</div>
    	                <div class="act_as_cell amount" style="width: 30px;">${(total_final_balance) | amount}</div>
    	            %elif comparison_mode == 'single':
    	                <div class="act_as_cell amount" style="width: 30px;">${(total_final_balance) | amount}</div>
    	            	<div class="act_as_cell amount" style="width: 30px;">${total_comp_balance[0] | amount}</div>
    	            	<div class="act_as_cell amount" style="width: 30px;">${total_diff | amount}</div>
    	            	<div class="act_as_cell amount" style="width: 30px;">${int(round((total_diff/total_comp_balance[0])*100))} &#37;</div>
    	            	
    	            %else :
    	                <div class="act_as_cell amount" style="width: 30px;">${(total_final_balance) | amount}</div>
    	            	<% i=0 %>
    	            	
    	            	%while i < nb_comparison :
    	            		<div class="act_as_cell amount" style="width: 30px;">${total_comp_balance[i] | amount}</div>
    	            		<% i = i +1 %>
    	            	%endwhile

    	            %endif
    	            
                </div>
            </div>
    </div>    
        
    </body>
    
  
    
</html>
