import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)

class IrModule(models.Model):
    _inherit = 'ir.module.module'

    to_buy = fields.Boolean(string='Odoo Enterprise Module', default=False)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None, **kwargs):
        res = super().search_read(domain=domain, fields=fields, offset=offset, limit=limit, order=order, **kwargs)
        if isinstance(res, list):
            for r in res:
                if isinstance(r, dict):
                    if 'to_buy' in r:
                        r['to_buy'] = False
                    if 'state' in r:
                        r['state'] = 'installed'
        return res

    @api.model
    def web_search_read(self, domain=None, specification=None, offset=0, limit=None, order=None, count_limit=None, **kwargs):
        res = super().web_search_read(domain=domain, specification=specification, offset=offset, limit=limit, order=order, count_limit=count_limit, **kwargs)
        if isinstance(res, dict) and 'records' in res:
            for r in res['records']:
                if isinstance(r, dict):
                    if 'to_buy' in r:
                        r['to_buy'] = False
                    if 'state' in r:
                        r['state'] = 'installed'
        return res

    def read(self, fields=None, load='_classic_read', **kwargs):
        res = super().read(fields=fields, load=load, **kwargs)
        if isinstance(res, list):
            for r in res:
                if isinstance(r, dict):
                    if 'to_buy' in r:
                        r['to_buy'] = False
                    if 'state' in r:
                        r['state'] = 'installed'
        return res

    @api.model
    def update_list(self):
        res = super().update_list()
        self.search([('to_buy', '=', True)]).write({'to_buy': False})
        return res
