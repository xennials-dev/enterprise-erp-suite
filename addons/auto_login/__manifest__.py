{
    'name': 'Auto Login to Desktop & Apps Unlock',
    'version': '18.0.1.0.0',
    'summary': 'Bypasses login screen, unlocks all apps to Activate, and applies blank canvas debranding',
    'description': 'Direct desktop access, activation buttons for all apps, and white-label branding.',
    'category': 'Extra Tools',
    'author': 'Antigravity',
    'license': 'LGPL-3',
    'depends': ['web', 'base'],
    'data': [
        'views/ir_module_views.xml',
        'views/webclient_templates.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'auto_login/static/src/css/interface_themes.css',
            'auto_login/static/src/js/interface_switcher.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
