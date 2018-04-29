# -*- coding: utf-8 -*-

# Copyright 2014-2018 ACSONE SA/NV (<http://acsone.eu>)
# Copyright 2017-2018 Rémy Taymans <remytaymans@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import api, models


class Report(models.Model):
    _inherit = "report"

    @api.v7
    def get_pdf(self, cr, uid, ids, report_name, html=None, data=None,
                context=None):
        return super(Report, self).get_pdf(cr, uid, ids, report_name,
                                           html=html, data=data,
                                           context=context)

    @api.v8
    def get_pdf(self, records, report_name, html=None, data=None):
        return self._model.get_pdf(self._cr, self._uid,
                                   records.ids, report_name,
                                   html=html, data=data, context=self._context)
