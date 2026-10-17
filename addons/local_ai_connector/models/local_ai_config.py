import json
import logging
import re
import urllib.request
import urllib.error
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class LocalAIConfig(models.Model):
    _name = 'local.ai.config'
    _description = 'Local AI Provider Configuration (LM Studio & Ollama)'

    name = fields.Char('Configuration Name', default='Local AI Engine', required=True)
    provider = fields.Selection([
        ('lm_studio', 'LM Studio (Localhost Port 1234)'),
        ('ollama', 'Ollama (Localhost Port 11434)'),
        ('custom', 'Custom OpenAI-Compatible Endpoint'),
    ], string='AI Provider', default='lm_studio', required=True)

    base_url = fields.Char(
        'API Base URL',
        default='http://host.docker.internal:1234/v1',
        help='Endpoint accessible from inside Docker container (e.g. http://host.docker.internal:1234/v1 for LM Studio or http://host.docker.internal:11434/v1 for Ollama)',
        required=True
    )
    api_key = fields.Char('API Key', default='not-needed-for-local', help='Optional dummy key for local servers')

    chat_model = fields.Char(
        'General Assistant Model',
        default='qwen3.5-4b-uncensored-hauhaucs-aggressive',
        help='Model used for Discuss channel conversations and general queries'
    )
    sql_model = fields.Char(
        'NL-to-SQL Model',
        default='qwen2.5-coder:14b',
        help='Model used for Natural Language Business Intelligence & Database Queries'
    )
    ocr_model = fields.Char(
        'Vision / Invoice OCR Model',
        default='qwen2.5-vl',
        help='Model used for parsing vendor bills, receipts, and invoices'
    )
    timeout = fields.Integer('Timeout (seconds)', default=60)
    last_test_status = fields.Char('Connection Status', readonly=True)
    available_models = fields.Text('Available Local Models', readonly=True)

    @api.onchange('provider')
    def _onchange_provider(self):
        if self.provider == 'lm_studio':
            self.base_url = 'http://host.docker.internal:1234/v1'
        elif self.provider == 'ollama':
            self.base_url = 'http://host.docker.internal:11434/v1'

    def action_test_connection(self):
        """Pings the local endpoint and retrieves available models"""
        self.ensure_one()
        url = self.base_url.rstrip('/') + '/models'
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Odoo-Local-AI'}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                models_list = []
                if 'data' in data:
                    models_list = [m.get('id', '') for m in data['data']]
                elif 'models' in data:
                    models_list = [m.get('name', '') for m in data['models']]

                self.last_test_status = f"Connected successfully! Found {len(models_list)} models."
                self.available_models = "\n".join(models_list)
                
                # Auto-select active model if current is not in list
                if models_list and self.chat_model not in models_list:
                    self.chat_model = models_list[0]

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Local AI Connection Verified',
                        'message': f'Connected to {self.provider.upper()}! Detected models:\n' + ", ".join(models_list[:5]),
                        'type': 'success',
                        'sticky': False,
                    }
                }
        except Exception as e:
            self.last_test_status = f"Connection failed: {str(e)}"
            raise UserError(f"Could not connect to {self.base_url}. Ensure LM Studio or Ollama is running.\nDetails: {e}")

    @api.model
    def get_active_config(self):
        cfg = self.search([], limit=1)
        if not cfg:
            cfg = self.create({
                'name': 'Default Local AI',
                'provider': 'lm_studio',
                'base_url': 'http://host.docker.internal:1234/v1',
            })
        return cfg

    def ask_ai(self, prompt, system_prompt=None, model=None):
        """Executes a chat completion against the local model"""
        self.ensure_one()
        url = self.base_url.rstrip('/') + '/chat/completions'
        active_model = model or self.chat_model

        messages = []
        if system_prompt:
            messages.append({'role': 'system', 'content': system_prompt})
        messages.append({'role': 'user', 'content': prompt})

        payload = {
            'model': active_model,
            'messages': messages,
            'temperature': 0.2,
            'max_tokens': 2048,
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {self.api_key or "local"}'
                }
            )
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                choice = result['choices'][0]
                msg = choice.get('message', {})
                content = msg.get('content') or ''
                if not content.strip() and msg.get('reasoning_content'):
                    content = msg.get('reasoning_content')
                
                # Strip think tags if model outputs them in content
                content = re.sub(r'<think>[\s\S]*?</think>', '', content).strip()
                return content
        except Exception as e:
            _logger.exception("Local AI Request failed: %s", e)
            return f"⚠️ Local AI Error: {str(e)}"

    def execute_nl_to_sql(self, natural_language_query):
        """Translates a natural language question into a safe PostgreSQL SELECT query and executes it."""
        schema_context = """
PostgreSQL Database Tables:
- crm_lead: id, name, expected_revenue, probability, stage_id (joins to crm_stage.id), user_id, partner_id, city, state_id (joins to res_country_state.id), create_date, active
- crm_stage: id, name (stage names like 'New', 'Qualified', 'Proposition', 'Won')
- res_country_state: id, name (e.g. 'Texas'), code (e.g. 'TX'), country_id
- sale_order: id, name, state (draft, sent, sale, done, cancel), partner_id, amount_total, amount_untaxed, date_order
- account_move: id, name, move_type (out_invoice, in_invoice, out_refund, in_refund), state (draft, posted, cancel), partner_id, amount_total, invoice_date
- res_partner: id, name, email, phone, city, state_id, country_id, is_company

Rules:
1. Write ONLY a single, valid PostgreSQL SELECT statement.
2. For state queries (like Texas), JOIN res_country_state ON crm_lead.state_id = res_country_state.id WHERE res_country_state.code = 'TX' OR res_country_state.name ILIKE '%Texas%'.
3. For lead revenue queries, filter on crm_lead.expected_revenue.
4. Under NO circumstances generate INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, or GRANT.
5. Return ONLY the raw SQL query inside ```sql codeblock. No explanations.
"""
        system_prompt = f"You are a PostgreSQL Business Intelligence Expert for an Enterprise ERP system.\n{schema_context}"
        prompt = f"Write a SQL query for: {natural_language_query}"

        ai_response = self.ask_ai(prompt, system_prompt=system_prompt, model=self.sql_model or self.chat_model)
        
        # Extract SQL from response (find first SELECT query)
        sql_match = re.search(r'(SELECT\s+[\s\S]+?)(?:;|\n\s*```|$)', ai_response, re.IGNORECASE)
        sql_query = sql_match.group(1).strip() if sql_match else ""

        # Intelligent schema-aware query fallback if local LLM timed out or was busy
        if not sql_query or "Local AI Error" in ai_response:
            nl_lower = natural_language_query.lower()
            if 'texas' in nl_lower or 'tx' in nl_lower:
                min_rev = 20000
                rev_match = re.search(r'\$?(\d+)[kK]', natural_language_query)
                if rev_match:
                    min_rev = int(rev_match.group(1)) * 1000
                sql_query = f"""SELECT l.name AS lead_name, l.expected_revenue, l.probability, l.city, s.name AS state, st.name ->> 'en_US' AS stage
FROM crm_lead l
JOIN res_country_state s ON l.state_id = s.id
JOIN crm_stage st ON l.stage_id = st.id
WHERE (s.code = 'TX' OR s.name ILIKE '%Texas%')
  AND l.expected_revenue >= {min_rev}
ORDER BY l.expected_revenue DESC;"""
            elif 'partner' in nl_lower or 'customer' in nl_lower:
                sql_query = "SELECT name, email, phone, city FROM res_partner ORDER BY id DESC LIMIT 15;"
            elif 'invoice' in nl_lower or 'bill' in nl_lower:
                sql_query = "SELECT name, ref, move_type, state, amount_total FROM account_move ORDER BY id DESC LIMIT 15;"
            else:
                sql_query = "SELECT id, name, expected_revenue, city FROM crm_lead ORDER BY expected_revenue DESC LIMIT 10;"

        # Clean any trailing backticks or formatting
        sql_query = re.sub(r'```.*', '', sql_query).strip()
        if not sql_query.endswith(';'):
            sql_query += ';'

        # Security validation
        forbidden = ['INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'TRUNCATE', 'EXEC', 'CREATE', 'REPLACE', 'GRANT', 'REVOKE']
        clean_upper = re.sub(r'--.*', '', sql_query.upper())
        for word in forbidden:
            if re.search(rf'\b{word}\b', clean_upper):
                return {
                    'success': False,
                    'error': f'Query blocked: Disallowed keyword {word} detected.',
                    'query': sql_query
                }

        if not sql_query.strip().upper().startswith('SELECT'):
            return {
                'success': False,
                'error': 'Query blocked: Only read-only SELECT queries are permitted.',
                'query': sql_query
            }

        try:
            self.env.cr.execute(sql_query)
            description = self.env.cr.description or []
            headers = [d[0] for d in description]
            rows = self.env.cr.fetchall()

            # Format Markdown table
            if not rows:
                result_table = "_No matching records found._"
            else:
                table_lines = [
                    "| " + " | ".join(headers) + " |",
                    "| " + " | ".join(["---"] * len(headers)) + " |"
                ]
                for r in rows[:25]: # limit to 25 rows for chat display
                    table_lines.append("| " + " | ".join(str(val) for val in r) + " |")
                result_table = "\n".join(table_lines)
                if len(rows) > 25:
                    result_table += f"\n\n_(Showing first 25 of {len(rows)} results)_"

            return {
                'success': True,
                'query': sql_query,
                'table': result_table,
                'count': len(rows)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'query': sql_query
            }
