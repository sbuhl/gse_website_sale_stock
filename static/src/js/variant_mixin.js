odoo.define('gse_website_sale_stock.VariantMixin', function (require) {
'use strict';

const publicWidget = require('web.public.widget');
const core = require('web.core');
const Dialog = require('web.Dialog');
const QWeb = core.qweb;

require('website_sale.website_sale');

publicWidget.registry.WebsiteSale.include({
    events: Object.assign({}, publicWidget.registry.WebsiteSale.prototype.events, {
        'click .gse_change_warehouse': '_onChangeWarehouseClick',
    }),
    xmlDependencies: (publicWidget.registry.WebsiteSale.prototype.xmlDependencies || [])
        .concat([
            '/gse_website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml',
            '/website_sale_stock/static/src/xml/website_sale_stock_product_availability.xml', // Needed for inherit?
        ]),

    _onChangeWarehouseClick(ev) {
        const gseWhQty = $(ev.target).data('gse-wh-qty');
        const dialog = new Dialog(this, {
            size: 'medium',
            title: 'Select another warehouse',
            technical: false,
            $content: QWeb.render('gse_website_sale_stock.popup_content_warehouse_select', {
                'qty': gseWhQty,
            }),
            buttons: [
                {
                    text: "Save",
                    classes: 'btn-primary',
                    close: true,
                    click: function () {
                        const selectedWarehouse = dialog.$el.find('input[name="gse_select_warehouse"]:checked');
                        const whId = selectedWarehouse[0].value;
                        const search = $.deparam(window.location.search.substring(1));
                        search['gse_forced_warehouse_id'] = whId;
                        window.location.search = $.param(search);
                    },
                },
                {
                    text: "Cancel",
                    close: true,
                },
            ],
        }).open();
    },
});

});