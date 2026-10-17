# Part of enterprise unlocked suite
{
    'name': 'Helpdesk',
    'version': '18.0.1.0.0',
    'category': 'Services/Helpdesk',
    'summary': 'Customer support ticket management with Autonomous Tier-1 AI Resolution',
    'depends': ['mail', 'base', 'local_ai_connector'],
    'data': [
        'security/ir.model.access.csv',
        'views/helpdesk_views.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
