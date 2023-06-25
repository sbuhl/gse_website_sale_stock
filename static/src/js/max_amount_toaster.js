/** @odoo-module **/

import publicWidget from 'web.public.widget';
import {registry} from "@web/core/registry";

const MaxAmountToasterWidget = publicWidget.Widget.extend({
    start() {
        const params = new URLSearchParams(window.location.search);
        if (params.get('show_max_amount_toast')) {
            this.displayNotification({
                message: "Le montant maximum de la commande avec cette liste de prix est de " + params.get('show_max_amount_toast'),
                type: 'warning',
            });
        }
        return this._super(...arguments);
    },
});

registry.category("public_root_widgets").add("MaxAmountToasterWidget", {
    Widget: MaxAmountToasterWidget,
    selector: '#wrap',
});

export default MaxAmountToasterWidget;
