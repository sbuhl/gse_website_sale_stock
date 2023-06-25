# -*- coding: utf-8 -*-
{
    'name': "gse_website_sale_stock",
    'summary': """Customizations de l'ecommerce pour Goshop Energy""",
    'description': """""",
    'author': "Sébastien Bühl",
    'website': "http://www.buhl.be",
    'category': 'Customizations',
    'version': '0.1',
    'license': 'LGPL-3',

    # any module necessary for this one to work correctly
    'depends': [
        'website_crm_partner_assign',  # res_partner.grade_id
        'website_sale_stock',
    ],
    'data': [
        'views/product_pricelist_views.xml',
    ],
    'demo': [
        'data/demo.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'gse_website_sale_stock/static/src/js/max_amount_toaster.js',
            'gse_website_sale_stock/static/src/js/variant_mixin.js',
        ],
    },
}
