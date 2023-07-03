# -*- coding: utf-8 -*-

from odoo import http
from odoo.addons.website_sale.controllers.main import PaymentPortal, WebsiteSale
from odoo.http import request
from odoo.exceptions import ValidationError

from werkzeug.urls import url_decode, url_encode, url_parse


class WebsiteSale(WebsiteSale):

    def _prepare_product_values(self, product, category, search, **kwargs):
        gse_forced_warehouse_id = int(request.params.pop('gse_forced_warehouse_id', 0))
        if gse_forced_warehouse_id and gse_forced_warehouse_id in request.env['stock.warehouse'].sudo().search([
            ('company_id', '=', request.website.company_id.id)]
        ).ids:
            request.session['GSE_FORCED_WAREHOUSE_ID'] = gse_forced_warehouse_id
            order = request.website.sale_get_order()
            if order and order.state == 'draft':
                order.warehouse_id = gse_forced_warehouse_id

                for line in order.order_line:
                    if line.exists():
                        order._cart_update(product_id=line.product_id.id, line_id=line.id, add_qty=0)

        return super()._prepare_product_values(product, category, search, **kwargs)

    @http.route(['/shop/change_pricelist/<model("product.pricelist"):pl_id>'], type='http', auth="public", website=True, sitemap=False)
    def pricelist_change(self, pl_id, **post):
        res = super().pricelist_change(pl_id, **post)
        # If the selected PL has a maximum amount linked to it, and that it was
        # really selected, inform the user through a toast about the max amount.
        if (
            pl_id.max_authorized_eshop_amount
            and request.session['website_sale_current_pl'] == pl_id.id
        ):
            decoded_url = url_parse(res.location)
            args = url_decode(decoded_url.query)
            args['show_max_amount_toast'] = pl_id.max_authorized_eshop_amount
            redirect_url = decoded_url.replace(query=url_encode(args)).to_url()
            return request.redirect(
                redirect_url,
                code=res.status_code,
            )
        return res


class PaymentPortal(PaymentPortal):

    @http.route()
    def shop_payment_transaction(self, *args, **kwargs):
        """ Payment transaction override to double check cart quantities before
        placing the order
        """
        order = request.website.sale_get_order()
        max_authorized_eshop_amount = order.pricelist_id.max_authorized_eshop_amount
        if max_authorized_eshop_amount and order.amount_total > max_authorized_eshop_amount:
            raise ValidationError("Le montant de la commande dépasse le maximum autorise (%s)." % max_authorized_eshop_amount)
        return super().shop_payment_transaction(*args, **kwargs)
