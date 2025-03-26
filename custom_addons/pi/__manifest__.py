# -*- coding: utf-8 -*-
{
    'name': "Pi Model",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'data/module_category_pi.xml',
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/pi_model_views.xml',
        'views/pi_import_wizard_views.xml',
        'views/pi_import_action.xml',
        'views/product_view.xml',
        'views/pi_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'pi/static/src/js/pi_custom_screen.js',
            # 'pi/static/src/js/pi_extend.js',
            'pi/static/src/xml/pi_custom_template.xml',
            # 'pi/static/src/xml/pi_extend.xml'
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
