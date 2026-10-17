import logging
import re
from odoo import models, api

_logger = logging.getLogger(__name__)

class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    def _get_or_create_assistant_partner(self):
        assistant_partner = self.env['res.partner'].sudo().search([('name', '=', 'Assistant')], limit=1)
        if not assistant_partner:
            assistant_partner = self.env['res.partner'].sudo().create({
                'name': 'Assistant',
                'email': 'assistant@yourcompany.internal',
                'active': True,
            })
        return assistant_partner

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        """Intercepts messages mentioning Assistant to trigger local AI response"""
        msg = super().message_post(**kwargs)
        
        body = kwargs.get('body', '') or ''
        author_id = kwargs.get('author_id')
        
        assistant_partner = self._get_or_create_assistant_partner()
        if author_id and author_id == assistant_partner.id:
            return msg

        # Check if message mentions @Assistant or if this is a direct channel with Assistant
        is_channel = self._name == 'discuss.channel'
        is_assistant_mentioned = 'Assistant' in body or '@Assistant' in body or '@assistant' in body
        
        is_direct_chat = False
        if is_channel:
            channel = self.env['discuss.channel'].browse(self.id)
            if channel.channel_type == 'chat' and assistant_partner in channel.channel_partner_ids:
                is_direct_chat = True

        if is_assistant_mentioned or is_direct_chat:
            self._handle_local_ai_response(body, assistant_partner)

        return msg

    def _handle_local_ai_response(self, user_prompt, assistant_partner):
        """Dispatches to local AI and posts response back into thread"""
        try:
            # Clean prompt
            clean_text = re.sub(r'<[^>]+>', '', user_prompt).replace('@Assistant', '').replace('@assistant', '').replace('Assistant', '').strip()
            if not clean_text:
                return

            ai_config = self.env['local.ai.config'].get_active_config()
            
            # Detect if user is asking for database analytics / reporting
            bi_keywords = ['show', 'list', 'leads', 'revenue', 'sales', 'invoice', 'how many', 'total', 'quarter', 'orders', 'customers', 'pipeline']
            is_bi_query = any(k in clean_text.lower() for k in bi_keywords)

            if is_bi_query:
                res = ai_config.execute_nl_to_sql(clean_text)
                if res.get('success'):
                    reply_body = f"""
<div style="font-family: sans-serif; line-height: 1.5;">
    <p>🤖 <strong>Local AI Business Intelligence</strong> (via <em>{ai_config.provider.upper()}</em>):</p>
    <div style="background: #1e1e2e; color: #a6adc8; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 12px; margin-bottom: 8px;">
        <strong style="color: #89b4fa;">Generated Safe Query:</strong><br/>
        <code>{res.get('query')}</code>
    </div>
    <div>
        <strong>Results ({res.get('count', 0)} records):</strong>
        <pre style="background: #f8f9fa; border: 1px solid #e9ecef; padding: 10px; border-radius: 6px; overflow-x: auto;">{res.get('table')}</pre>
    </div>
</div>
"""
                else:
                    ai_reply = ai_config.ask_ai(clean_text)
                    reply_body = f"<p>🤖 <strong>Assistant</strong> (Local AI):</p><p>{ai_reply}</p>"
            else:
                ai_reply = ai_config.ask_ai(clean_text)
                reply_body = f"<p>🤖 <strong>Assistant</strong> (Local AI):</p><p>{ai_reply}</p>"

            from markupsafe import Markup
            # Post the response as the Assistant with raw HTML Markup
            self.with_context(mail_create_nosubscribe=True).message_post(
                body=Markup(reply_body),
                message_type='comment',
                author_id=assistant_partner.id,
            )
        except Exception as e:
            _logger.exception("Failed to post local AI reply: %s", e)
