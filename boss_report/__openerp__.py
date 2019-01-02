# -*- coding: utf-8 -*-

{
    'name' : 'Boss report',
    'version' : '0.1',
    'author' : 'Boss Consulting',
    'sequence': 110,
    'website' : 'http://www.boss.com',
    'summary' : 'Boss report',
    'description' : """
    
Boss report
============
""",
    'depends': [
        'account',
        'report_webkit',
        'report_webkit_lib',
        #'invoice_webkit',
        'base_headers_webkit',
        'account_financial_report_webkit',
    ],
  
    'data': [
        'report/boss_headers_data.xml',
        'report/boss_report.xml',
    ],
    'installable' : True,
    'application' : False,
}
