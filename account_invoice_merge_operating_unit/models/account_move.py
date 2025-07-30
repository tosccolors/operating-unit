 #-*- coding: utf-8 -*-
# Copyright 2025 The Open Source Company ((www.tosc.nl).)

from odoo import api, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _get_invoice_key_cols_out(self):
        res = super()._get_invoice_key_cols_out()
        res.append('operating_unit_id')
        return res

    @api.model
    def _get_invoice_key_cols_in(self):
        res = super()._get_invoice_key_cols_in()
        res.append('operating_unit_id')
        return res


