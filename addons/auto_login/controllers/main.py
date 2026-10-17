import logging
import odoo
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.home import Home
from odoo.addons.web.controllers.utils import ensure_db

_logger = logging.getLogger(__name__)

class AutoLoginHome(Home):

    def _do_auto_login(self):
        if not getattr(request, 'session', None):
            return
        if not request.session.uid and request.db:
            try:
                registry = odoo.registry(request.db)
                with registry.cursor() as cr:
                    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
                    admin_user = env['res.users'].search([('login', '=', 'admin')], limit=1)
                    if not admin_user:
                        admin_user = env['res.users'].browse(2)
                    if admin_user and admin_user.exists():
                        request.session.pre_login = admin_user.login
                        request.session.pre_uid = admin_user.id
                        request.session.finalize(env)
                        request.update_env(user=admin_user.id)
                        request.session.touch()
                        _logger.info("Auto-login: successfully authenticated as %s (UID %s)", admin_user.login, admin_user.id)
            except Exception as e:
                _logger.exception("Auto-login failed: %s", e)

    @http.route('/', type='http', auth="none")
    def index(self, s_action=None, db=None, **kw):
        ensure_db()
        self._do_auto_login()
        return request.redirect_query('/odoo', query=request.params)

    @http.route(['/web', '/odoo', '/odoo/<path:subpath>', '/scoped_app/<path:subpath>'], type='http', auth="none", readonly=Home._web_client_readonly)
    def web_client(self, s_action=None, **kw):
        ensure_db()
        self._do_auto_login()
        return super().web_client(s_action=s_action, **kw)

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        ensure_db()
        self._do_auto_login()
        if request.session.uid:
            return request.redirect(self._login_redirect(request.session.uid, redirect=redirect or '/odoo'))
        return super().web_login(redirect=redirect, **kw)

    @http.route('/web/session/logout', type='http', auth="none")
    def logout(self, redirect='/odoo'):
        return request.redirect('/odoo')
