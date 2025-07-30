# Copyright (C) 2024 Willem Hulsof
# -*- coding: utf-8 -*-

from odoo import _, api, fields, models, tools

class MailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    #Overridden:
    template_id = fields.Many2one(
        'mail.template', 'Use template', index=True,
        domain="[('model', '=', model), ('operating_unit_id', '=', operating_unit_id)]")

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )


    @api.model
    def default_get(self, fields):
        result = super(MailComposer, self).default_get(fields)

        model = result.get('model', False)
        res_id = result.get('res_id', False)
        if model and res_id:
            Obj = self.env[model].browse(res_id)
            try:
                result['operating_unit_id'] = Obj.operating_unit_id.id
            except:
                pass

        return result

