# -*- coding: utf-8 -*-

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def write(self, values):
        result = super().write(values)
        # needed for `_get_pl_partner_order` to be re-evaluated
        if 'grade_id' in values:
            self.clear_caches()
            self.invalidate_recordset()
        return result
