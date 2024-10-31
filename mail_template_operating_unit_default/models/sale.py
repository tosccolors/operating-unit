# Copyright (C) 2024 Willem Hulsof
# -*- coding: utf-8 -*-

from odoo import _, api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Overridden:
    def _find_mail_template(self, force_confirmation_template=False):
        self.ensure_one()
        template_id = False

        is_OU_installed = self.env['ir.module.module'].sudo().search(
            [('state', '=', 'installed'), ('name', '=', 'sale_operating_unit')])

        # Operating Unit:
        if is_OU_installed:
            subj = 'Sales Order: Send by email'
            if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
                subj = 'Sales Order: Confirmation Email'

            template_id = self.env['mail.template'].sudo().search(
                [('model', '=', self._name), ('operating_unit_id', '=', self.operating_unit_id.id),
                 ('name', 'ilike', '%' + subj + '%')])
            template_id = template_id and template_id[0].id or False # pick first template

        else: # Standard (System Parameters)
            if force_confirmation_template or (self.state == 'sale' and not self.env.context.get('proforma', False)):
                template_id = int(self.env['ir.config_parameter'].sudo().get_param('sale.default_confirmation_template'))
                template_id = self.env['mail.template'].sudo().search([('id', '=', template_id)]).id
                if not template_id:
                    template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.mail_template_sale_confirmation', raise_if_not_found=False)

        # If None: default template
        if not template_id:
            template_id = self.env['ir.model.data'].xmlid_to_res_id('sale.email_template_edi_sale', raise_if_not_found=False)

        return template_id



