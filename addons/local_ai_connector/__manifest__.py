{
    'name': 'Local AI Connector (LM Studio & Ollama)',
    'version': '18.0.1.0.0',
    'summary': 'Private, 100% On-Premise AI for CRM, Natural Language SQL, Invoice OCR, and Helpdesk',
    'description': """
Local AI Engine for Odoo Enterprise Suite
=========================================
- 100% Private On-Premise Execution via LM Studio or Ollama
- Natural Language Business Intelligence (NL-to-SQL) for Discuss Channels
- Smart Invoice & Receipt Data Parsing (Vision/OCR)
- Autonomous Helpdesk Response Drafting
- Upstream model synchronization support
    """,
    'category': 'Productivity/AI',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/local_ai_config_views.xml',
        'views/account_move_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
