# Copyright (C) 2024 Willem Hulsof
# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.tools.misc import get_lang

class AccountMove(models.Model):
    _inherit = "account.move"


    def _find_invoice_mail_template(self):
        self.ensure_one()
        template = templateObj = self.env['mail.template'].sudo()

        is_OU_installed = self.env['ir.module.module'].search(
            [('state', '=', 'installed'), ('name', '=', 'account_operating_unit')])

        # Operating Unit:
        if is_OU_installed:
            subj = 'Invoice: Send by email'

            template = templateObj.search(
                [('model', '=', self._name), ('operating_unit_id', '=', self.operating_unit_id.id),
                 ('name', 'ilike', '%' + subj + '%')], limit=1)
            template = template and template[0] or templateObj

        # If None: default template
        if not template:
            template = self.env.ref('account.email_template_edi_invoice', raise_if_not_found=False)

        return template

    # Overridden:
    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self._find_invoice_mail_template()

        lang = False
        if template:
            lang = template._render_lang(self.ids)[self.id]
        if not lang:
            lang = get_lang(self.env).code
        compose_form = self.env.ref('account.account_invoice_send_wizard_form', raise_if_not_found=False)
        ctx = dict(
            default_model='account.move',
            default_res_id=self.id,
            # For the sake of consistency we need a default_res_model if
            # default_res_id is set. Not renaming default_model as it can
            # create many side-effects.
            default_res_model='account.move',
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_operating_unit_id=self.operating_unit_id.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            custom_layout="mail.mail_notification_paynow",
            model_description=self.with_context(lang=lang).type_name,
            force_email=True
        )
        return {
            'name': _('Send Invoice'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.send',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
