# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from odoo.osv import expression


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    grade_ids = fields.Many2many('res.partner.grade', string='Partner Level')
    max_authorized_eshop_amount = fields.Float(default=0.0, help="Maximum amount allowed on eshop with this pricelist.")

    def _is_available_on_website(self, website_id):
        """ To be able to be used on a website, a pricelist should either:
        - Have its `website_id` set to current website (specific pricelist).
        - Have no `website_id` set and should be `selectable` (generic pricelist)
          or should have a `code` (generic promotion).
        - Have no `company_id` or a `company_id` matching its website one.

        Note: A pricelist without a website_id, not selectable and without a
              code is a backend pricelist.

        Change in this method should be reflected in `_get_website_pricelists_domain`.
        """
        self.ensure_one()
        if self.grade_ids and self.env.user.grade_id not in self.grade_ids:
            return False
        return super()._is_available_on_website(website_id)

    def _get_website_pricelists_domain(self, website_id):
        ''' Check above `_is_available_on_website` for explanation.
        Change in this method should be reflected in `_is_available_on_website`.
        '''
        return expression.AND([
            super()._get_website_pricelists_domain(website_id),
            [
                '|',
                ('grade_ids', '=', False),
                ('grade_ids', '=', self.env.user.grade_id.id),
            ]
        ])
