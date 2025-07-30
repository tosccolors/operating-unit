# Copyright (C) 2024 Willem Hulsof
# -*- coding: utf-8 -*-


{
    "name": "Mail Template Operating Unit (Default)",
    "version": "14.0.1.0.0",
    "author" : "Deepa Venkatesh (DK), " "Willem Hulsof, The Open Source Company (TOSC)",
    'website': 'https://www.tosc.nl',
    "license": "LGPL-3",
    'description': """
This module further extends mechanism of 'mail_template_operating_unit', and finds a template to use based on operating unit set
on that document.

Applies on Sale Order and Invoice.

Note:
=====

In case of multi custom template scenarios, please retain the original name, with prefix/suffix with custom name.
 Ex: Sales Order: Send by email, below format would be best.

* 'custom template 1': Sales Order: Send by email <custom name>
* 'custom template 2' : <custom name> Sales Order: Send by email

""",
    "category": "Base",
    "depends": [
        "mail_template_operating_unit",
        "sale", "account"
    ],
    "data": [
        "views/mail_compose_views.xml",
        "views/invoice_send_views.xml",
    ],
    "installable": True,
}
