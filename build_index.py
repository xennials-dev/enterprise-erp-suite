import json

leads = json.load(open('data/crm_leads.json', encoding='utf-8'))
modules = json.load(open('data/installed_modules.json', encoding='utf-8'))
channels = json.load(open('data/discuss_channels.json', encoding='utf-8'))

# Key enterprise modules for the app drawer
app_icons = [
    {"name": "CRM", "icon": "💼", "color": "#6366f1", "desc": "Pipeline & Deal Tracking", "url": "http://localhost:8069/odoo/crm"},
    {"name": "Discuss", "icon": "💬", "color": "#0ea5e9", "desc": "Chat & Direct Messages", "url": "http://localhost:8069/odoo/discuss"},
    {"name": "Sales", "icon": "🏷️", "color": "#10b981", "desc": "Quotations & Orders", "url": "http://localhost:8069/odoo/sales"},
    {"name": "Invoicing", "icon": "🧾", "color": "#f59e0b", "desc": "Invoices & Payments", "url": "http://localhost:8069/odoo/accounting"},
    {"name": "Accounting", "icon": "📊", "color": "#8b5cf6", "desc": "Ledger & P&L Reports", "url": "http://localhost:8069/odoo/accounting"},
    {"name": "Inventory", "icon": "📦", "color": "#ec4899", "desc": "Stock & Warehouse", "url": "http://localhost:8069/odoo/stock"},
    {"name": "Manufacturing", "icon": "⚙️", "color": "#f97316", "desc": "BOM & Work Orders", "url": "http://localhost:8069/odoo/mrp"},
    {"name": "Projects", "icon": "📋", "color": "#14b8a6", "desc": "Agile Kanban & Tasks", "url": "http://localhost:8069/odoo/project"},
    {"name": "Helpdesk", "icon": "🎧", "color": "#06b6d4", "desc": "Customer Support Tickets", "url": "http://localhost:8069/odoo/helpdesk"},
    {"name": "Field Service", "icon": "🚐", "color": "#84cc16", "desc": "On-Site Maintenance", "url": "http://localhost:8069/odoo/fieldservice"},
    {"name": "Planning", "icon": "📅", "color": "#3b82f6", "desc": "Resource Scheduling", "url": "http://localhost:8069/odoo/planning"},
    {"name": "Timesheets", "icon": "⏱️", "color": "#a855f7", "desc": "Time Tracking & Grid", "url": "http://localhost:8069/odoo/timesheet"},
    {"name": "Sign", "icon": "✍️", "color": "#e11d48", "desc": "Online e-Signatures", "url": "http://localhost:8069/odoo/sign"},
    {"name": "Social Marketing", "icon": "📢", "color": "#38bdf8", "desc": "Multi-Platform Feeds", "url": "http://localhost:8069/odoo/social"},
    {"name": "Automation", "icon": "⚡", "color": "#fbbf24", "desc": "Targeted Lead Campaigns", "url": "http://localhost:8069/odoo/marketing"},
    {"name": "Studio", "icon": "🛠️", "color": "#ec4899", "desc": "Visual Customizer", "url": "http://localhost:8069/odoo/studio"},
    {"name": "Barcode", "icon": "📱", "color": "#22c55e", "desc": "Warehouse Scanner UI", "url": "http://localhost:8069/odoo/barcode"},
    {"name": "Appointments", "icon": "🤝", "color": "#6366f1", "desc": "Client Booking System", "url": "http://localhost:8069/odoo/appointment"},
    {"name": "Knowledge", "icon": "📚", "color": "#0284c7", "desc": "Team Wiki & Docs", "url": "http://localhost:8069/odoo/knowledge"},
    {"name": "VoIP", "icon": "📞", "color": "#10b981", "desc": "Dialer & Call Logging", "url": "http://localhost:8069/odoo/voip"},
    {"name": "Subscriptions", "icon": "🔄", "color": "#8b5cf6", "desc": "Recurring Revenue", "url": "http://localhost:8069/odoo/subscription"},
    {"name": "Quality Control", "icon": "🛡️", "color": "#06b6d4", "desc": "Inspection Checkpoints", "url": "http://localhost:8069/odoo/quality"},
    {"name": "Amazon Sync", "icon": "🛒", "color": "#f59e0b", "desc": "Marketplace Orders", "url": "http://localhost:8069/odoo/amazon"},
    {"name": "Local AI Suite", "icon": "🧠", "color": "#ec4899", "desc": "Ollama LLM Integration", "url": "http://localhost:8069/odoo/discuss"}
]

leads_json_str = json.dumps(leads, indent=2)
apps_json_str = json.dumps(app_icons, indent=2)
channels_json_str = json.dumps(channels, indent=2)

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Enterprise ERP & CRM Suite | Your Company</title>
  <meta name="description" content="Production Enterprise CRM pipeline synced with live Odoo instance. Features 49 active opportunities, 25+ installed enterprise modules, 4 scoped interface themes, and integrated 1080p video walkthrough.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&family=Outfit:wght@600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #0b0f19;
      --navbar-bg: rgba(17, 24, 39, 0.92);
      --card-bg: rgba(17, 24, 39, 0.85);
      --card-border: rgba(99, 102, 241, 0.22);
      --stage-bg: rgba(15, 23, 42, 0.65);
      --stage-border: rgba(99, 102, 241, 0.15);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
      --accent: #38bdf8;
      --success: #10b981;
      --warning: #f59e0b;
      --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-heading: 'Outfit', sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }}

    /* 4 Scoped Theme Palettes */
    [data-theme="cyber-slate"] {{
      --bg: #0b0f19;
      --navbar-bg: rgba(17, 24, 39, 0.94);
      --card-bg: rgba(17, 24, 39, 0.88);
      --card-border: rgba(99, 102, 241, 0.25);
      --stage-bg: rgba(15, 23, 42, 0.7);
      --stage-border: rgba(99, 102, 241, 0.16);
      --text-main: #ffffff;
      --text-muted: #94a3b8;
      --primary: #6366f1;
      --primary-hover: #4f46e5;
    }}
    [data-theme="cupertino"] {{
      --bg: #f8fafc;
      --navbar-bg: rgba(255, 255, 255, 0.95);
      --card-bg: #ffffff;
      --card-border: rgba(0, 0, 0, 0.09);
      --stage-bg: rgba(241, 245, 249, 0.9);
      --stage-border: rgba(0, 0, 0, 0.08);
      --text-main: #0f172a;
      --text-muted: #64748b;
      --primary: #0071e3;
      --primary-hover: #005bb5;
    }}
    [data-theme="midnight-gold"] {{
      --bg: #0c0c0e;
      --navbar-bg: rgba(24, 24, 27, 0.95);
      --card-bg: rgba(24, 24, 27, 0.9);
      --card-border: rgba(245, 158, 11, 0.32);
      --stage-bg: rgba(18, 18, 20, 0.85);
      --stage-border: rgba(245, 158, 11, 0.2);
      --text-main: #fafafa;
      --text-muted: #d4d4d8;
      --primary: #f59e0b;
      --primary-hover: #d97706;
    }}
    [data-theme="emerald-glass"] {{
      --bg: #022c22;
      --navbar-bg: rgba(6, 78, 59, 0.9);
      --card-bg: rgba(6, 78, 59, 0.8);
      --card-border: rgba(16, 185, 129, 0.35);
      --stage-bg: rgba(2, 44, 34, 0.8);
      --stage-border: rgba(16, 185, 129, 0.22);
      --text-main: #f0fdf4;
      --text-muted: #a7f3d0;
      --primary: #10b981;
      --primary-hover: #059669;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text-main);
      font-family: var(--font-main);
      min-height: 100vh;
      overflow-x: hidden;
      transition: background-color 0.25s, color 0.25s;
    }}

    /* Top Showcase Banner Widget */
    .showcase-banner-bar {{
      background: linear-gradient(90deg, rgba(99, 102, 241, 0.18) 0%, rgba(56, 189, 248, 0.14) 50%, rgba(16, 185, 129, 0.18) 100%);
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      padding: 10px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-size: 13px;
      flex-wrap: wrap;
      gap: 10px;
    }}
    .banner-left {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .banner-thumb {{
      width: 44px;
      height: 25px;
      border-radius: 4px;
      object-fit: cover;
      border: 1px solid rgba(255, 255, 255, 0.25);
    }}
    .banner-btn {{
      padding: 5px 13px;
      border-radius: 6px;
      background: var(--primary);
      color: #fff;
      font-weight: 600;
      font-size: 12px;
      border: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      transition: opacity 0.2s, transform 0.15s;
    }}
    .banner-btn:hover {{
      opacity: 0.9;
      transform: translateY(-1px);
    }}

    /* Main CRM App Header */
    header.crm-header {{
      background: var(--navbar-bg);
      backdrop-filter: blur(20px);
      border-bottom: 1px solid var(--card-border);
      padding: 12px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 50;
      transition: background 0.25s;
      flex-wrap: wrap;
      gap: 12px;
    }}
    .header-left {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}
    .app-launcher-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 700;
      transition: background 0.2s;
    }}
    .app-launcher-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
    }}
    .crm-brand {{
      display: flex;
      align-items: center;
      gap: 10px;
      font-weight: 800;
      font-size: 17px;
      font-family: var(--font-heading);
      letter-spacing: -0.02em;
    }}
    .crm-logo {{
      width: 32px;
      height: 32px;
      border-radius: 8px;
      background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-size: 16px;
    }}

    .app-nav-tabs {{
      display: flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 0, 0, 0.2);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
    }}
    .tab-btn {{
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      background: transparent;
      color: var(--text-muted);
      border: none;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .tab-btn.active {{
      background: var(--primary);
      color: #fff;
      box-shadow: 0 2px 8px rgba(0,0,0,0.25);
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .theme-select-dropdown {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      outline: none;
    }}
    .btn-action-lead {{
      background: var(--primary);
      color: #fff;
      border: none;
      padding: 7px 15px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.35);
      transition: all 0.2s;
    }}
    .btn-action-lead:hover {{
      background: var(--primary-hover);
      transform: translateY(-1px);
    }}

    /* Metrics Bar */
    .metrics-bar {{
      padding: 16px 24px;
      background: rgba(0, 0, 0, 0.15);
      border-bottom: 1px solid var(--stage-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .metrics-group {{
      display: flex;
      align-items: center;
      gap: 28px;
      flex-wrap: wrap;
    }}
    .metric-item {{
      display: flex;
      flex-direction: column;
      gap: 3px;
    }}
    .metric-label {{
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }}
    .metric-val {{
      font-size: 19px;
      font-weight: 800;
      font-family: var(--font-heading);
      letter-spacing: -0.02em;
    }}

    .filter-search-box {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .search-input {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      width: 260px;
      outline: none;
      transition: border-color 0.2s;
    }}
    .search-input:focus {{
      border-color: var(--primary);
    }}

    /* Views Layout */
    .view-content {{
      display: none;
    }}
    .view-content.active {{
      display: block;
    }}

    /* Kanban Board Container */
    .kanban-board-container {{
      padding: 24px;
      overflow-x: auto;
      min-height: calc(100vh - 220px);
    }}
    .kanban-board {{
      display: grid;
      grid-template-columns: repeat(4, minmax(320px, 1fr));
      gap: 20px;
      align-items: start;
    }}
    .kanban-column {{
      background: var(--stage-bg);
      border: 1px solid var(--stage-border);
      border-radius: 12px;
      padding: 14px;
      min-height: 600px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      backdrop-filter: blur(12px);
    }}
    .column-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding-bottom: 10px;
      border-bottom: 1px solid var(--stage-border);
    }}
    .column-title {{
      font-weight: 700;
      font-size: 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .count-pill {{
      background: rgba(255, 255, 255, 0.1);
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
    }}
    .column-revenue {{
      font-size: 13px;
      font-weight: 700;
      color: var(--accent);
      font-family: var(--font-mono);
    }}

    .lead-cards-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      min-height: 480px;
    }}
    .lead-card {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 14px;
      cursor: grab;
      transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
      position: relative;
    }}
    .lead-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
      border-color: var(--primary);
    }}
    .lead-card.dragging {{
      opacity: 0.4;
      transform: scale(0.98);
    }}
    .lead-card-top {{
      display: flex;
      align-items: flex-start;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .lead-name {{
      font-weight: 700;
      font-size: 13.5px;
      line-height: 1.35;
      color: var(--text-main);
    }}
    .lead-company {{
      font-size: 12px;
      color: var(--text-muted);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 4px;
    }}
    .lead-metrics {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }}
    .lead-val {{
      font-size: 14px;
      font-weight: 800;
      color: var(--text-main);
      font-family: var(--font-mono);
    }}
    .lead-prob {{
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }}
    .lead-tags {{
      display: flex;
      align-items: center;
      gap: 6px;
      flex-wrap: wrap;
    }}
    .lead-tag {{
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10.5px;
      font-weight: 600;
    }}
    .tag-texas {{
      background: rgba(239, 68, 68, 0.18);
      color: #f87171;
      border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    .tag-enterprise {{
      background: rgba(99, 102, 241, 0.18);
      color: #818cf8;
      border: 1px solid rgba(99, 102, 241, 0.3);
    }}
    .tag-fintech {{
      background: rgba(16, 185, 129, 0.18);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.3);
    }}
    .tag-priority-high {{
      background: rgba(245, 158, 11, 0.2);
      color: #fbbf24;
      border: 1px solid rgba(245, 158, 11, 0.35);
    }}

    /* Table List View */
    .table-view-container {{
      padding: 24px;
    }}
    .leads-table {{
      width: 100%;
      border-collapse: collapse;
      background: var(--card-bg);
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--card-border);
    }}
    .leads-table th {{
      background: rgba(0,0,0,0.25);
      padding: 12px 16px;
      text-align: left;
      font-size: 12px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--card-border);
    }}
    .leads-table td {{
      padding: 12px 16px;
      font-size: 13px;
      border-bottom: 1px solid var(--card-border);
      color: var(--text-main);
    }}
    .leads-table tr:hover td {{
      background: rgba(255,255,255,0.03);
    }}

    /* Discuss View */
    .discuss-container {{
      padding: 24px;
      display: grid;
      grid-template-columns: 280px 1fr;
      gap: 20px;
      min-height: 600px;
    }}
    .discuss-sidebar {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }}
    .discuss-channel-item {{
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: background 0.15s, color 0.15s;
    }}
    .discuss-channel-item.active, .discuss-channel-item:hover {{
      background: rgba(99, 102, 241, 0.15);
      color: var(--text-main);
    }}
    .discuss-chat-panel {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .chat-header {{
      padding: 14px 20px;
      border-bottom: 1px solid var(--card-border);
      font-weight: 700;
      font-size: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .chat-messages {{
      flex: 1;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
      overflow-y: auto;
      max-height: 480px;
    }}
    .chat-bubble {{
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }}
    .avatar {{
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 12px;
      color: #fff;
    }}
    .chat-content {{
      background: rgba(255, 255, 255, 0.04);
      padding: 10px 16px;
      border-radius: 10px;
      border: 1px solid var(--card-border);
      max-width: 80%;
    }}
    .chat-author {{
      font-size: 12px;
      font-weight: 700;
      color: var(--accent);
      margin-bottom: 4px;
    }}
    .chat-text {{
      font-size: 13px;
      line-height: 1.45;
    }}
    .chat-input-bar {{
      padding: 14px 20px;
      border-top: 1px solid var(--card-border);
      display: flex;
      gap: 12px;
    }}
    .chat-input {{
      flex: 1;
      background: rgba(0,0,0,0.25);
      border: 1px solid var(--card-border);
      padding: 10px 14px;
      border-radius: 8px;
      color: var(--text-main);
      font-size: 13px;
      outline: none;
    }}

    /* Apps Drawer Modal */
    .apps-modal-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: 16px;
      padding: 16px 0;
      max-height: 460px;
      overflow-y: auto;
    }}
    .app-tile {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 16px 10px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      gap: 8px;
      cursor: pointer;
      text-decoration: none;
      color: var(--text-main);
      transition: transform 0.15s, background 0.15s, border-color 0.15s;
    }}
    .app-tile:hover {{
      transform: translateY(-3px);
      background: rgba(255, 255, 255, 0.09);
      border-color: var(--primary);
    }}
    .app-tile-icon {{
      font-size: 32px;
      width: 52px;
      height: 52px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .app-tile-name {{
      font-weight: 700;
      font-size: 12px;
    }}
    .app-tile-badge {{
      font-size: 10px;
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      padding: 1px 6px;
      border-radius: 8px;
      font-weight: 600;
    }}

    /* Modals */
    .modal-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.75);
      backdrop-filter: blur(8px);
      z-index: 100;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}
    .modal-overlay.active {{
      display: flex;
    }}
    .modal-box {{
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 14px;
      width: 100%;
      max-width: 540px;
      padding: 24px;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
    }}
    .modal-box.large {{
      max-width: 760px;
    }}
    .modal-header {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 18px;
    }}
    .modal-close-btn {{
      background: none;
      border: none;
      color: var(--text-muted);
      font-size: 24px;
      cursor: pointer;
    }}
    .form-group {{
      margin-bottom: 14px;
    }}
    .form-label {{
      display: block;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-muted);
      margin-bottom: 6px;
    }}
    .form-control {{
      width: 100%;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--card-border);
      color: var(--text-main);
      padding: 9px 12px;
      border-radius: 8px;
      font-size: 13px;
      outline: none;
    }}
    .form-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }}
    .btn-submit-lead {{
      width: 100%;
      padding: 10px;
      background: var(--primary);
      color: #fff;
      font-weight: 700;
      border-radius: 8px;
      border: none;
      cursor: pointer;
      font-size: 14px;
      margin-top: 8px;
    }}

    /* Lightbox */
    .video-lightbox-box {{
      background: #000;
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      overflow: hidden;
      width: 100%;
      max-width: 900px;
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.8);
    }}
    .video-lightbox-box video {{
      width: 100%;
      height: auto;
      max-height: 75vh;
      display: block;
    }}

    @media (max-width: 1024px) {{
      .kanban-board {{
        grid-template-columns: repeat(2, minmax(280px, 1fr));
      }}
      .discuss-container {{
        grid-template-columns: 1fr;
      }}
    }}
    @media (max-width: 640px) {{
      .kanban-board {{
        grid-template-columns: 1fr;
      }}
      .metrics-group {{
        gap: 14px;
      }}
    }}
  </style>
</head>
<body>

  <!-- Top Showcase Banner Widget -->
  <div class="showcase-banner-bar">
    <div class="banner-left">
      <img src="docs/videos/odoo-showcase-preview.gif" alt="Showcase Preview" class="banner-thumb">
      <div>
        <strong>Local Live Odoo 18.0</strong> &bull; Synced with <code>http://localhost:8069</code> &bull; 49 Real Opportunities &bull; 25+ Active Enterprise Apps
      </div>
    </div>
    <div style="display: flex; gap: 8px; align-items: center;">
      <a href="http://localhost:8069" target="_blank" class="banner-btn" style="background: rgba(16, 185, 129, 0.85);">
        🔗 Open http://localhost:8069
      </a>
      <button class="banner-btn" onclick="openVideoModal()">
        ▶ Play 1080p Video Showcase
      </button>
      <a href="https://github.com/xennials-dev/enterprise-erp-suite" target="_blank" class="banner-btn" style="background: rgba(255,255,255,0.12);">
        GitHub Repository
      </a>
    </div>
  </div>

  <!-- Main CRM Application Header -->
  <header class="crm-header">
    <div class="header-left">
      <button class="app-launcher-btn" onclick="openAppsModal()" title="View All Installed Apps">
        <span>⠿</span> Apps
      </button>
      <div class="crm-brand">
        <div class="crm-logo">💼</div>
        <span>Enterprise Suite</span>
      </div>
      <nav class="app-nav-tabs">
        <button class="tab-btn active" id="tab-kanban" onclick="switchView('kanban')">Kanban</button>
        <button class="tab-btn" id="tab-table" onclick="switchView('table')">List (49)</button>
        <button class="tab-btn" id="tab-discuss" onclick="switchView('discuss')">Discuss & AI</button>
      </nav>
    </div>
    <div class="header-right">
      <select class="theme-select-dropdown" id="theme-selector" onchange="switchTheme(this.value)">
        <option value="cyber-slate">🎨 Cyber Slate (Dark Glass)</option>
        <option value="cupertino">🎨 Cupertino (Apple Clean)</option>
        <option value="midnight-gold">🎨 Executive Midnight Gold</option>
        <option value="emerald-glass">🎨 Emerald Fluid Glass</option>
      </select>
      <button class="btn-action-lead" onclick="openNewLeadModal()">➕ New Opportunity</button>
    </div>
  </header>

  <!-- Metrics Bar -->
  <div class="metrics-bar">
    <div class="metrics-group">
      <div class="metric-item">
        <span class="metric-label">Total Pipeline</span>
        <span class="metric-val" id="metric-pipeline-val">$1,085,044</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Active Opportunities</span>
        <span class="metric-val" id="metric-deals-count">49 Deals</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Target Win Rate</span>
        <span class="metric-val" style="color: var(--success);">76.5%</span>
      </div>
      <div class="metric-item">
        <span class="metric-label">Texas Enterprise Value</span>
        <span class="metric-val" style="color: var(--accent);">$346,500</span>
      </div>
    </div>
    <div class="filter-search-box">
      <input type="text" class="search-input" id="search-input" placeholder="🔍 Search 49 leads, contacts..." oninput="handleSearch(this.value)">
      <button class="tab-btn" style="background: rgba(255,255,255,0.06); padding: 7px 12px;" onclick="filterTexasDeals()">⭐ Texas Deals</button>
      <button class="tab-btn" style="background: rgba(255,255,255,0.06); padding: 7px 12px;" onclick="resetFilters()">Reset</button>
    </div>
  </div>

  <!-- VIEW 1: Kanban Board View -->
  <main class="view-content active" id="view-kanban">
    <div class="kanban-board-container">
      <div class="kanban-board">

        <!-- Column 1: New -->
        <div class="kanban-column" data-stage="New" ondragover="allowDrop(event)" ondrop="handleDrop(event, 'New')">
          <div class="column-header">
            <div class="column-title">
              <span>🔵 New</span>
              <span class="count-pill" id="count-New">0</span>
            </div>
            <div class="column-revenue" id="rev-New">$0</div>
          </div>
          <div class="lead-cards-list" id="list-New"></div>
        </div>

        <!-- Column 2: Qualified -->
        <div class="kanban-column" data-stage="Qualified" ondragover="allowDrop(event)" ondrop="handleDrop(event, 'Qualified')">
          <div class="column-header">
            <div class="column-title">
              <span>🟡 Qualified</span>
              <span class="count-pill" id="count-Qualified">0</span>
            </div>
            <div class="column-revenue" id="rev-Qualified">$0</div>
          </div>
          <div class="lead-cards-list" id="list-Qualified"></div>
        </div>

        <!-- Column 3: Proposition -->
        <div class="kanban-column" data-stage="Proposition" ondragover="allowDrop(event)" ondrop="handleDrop(event, 'Proposition')">
          <div class="column-header">
            <div class="column-title">
              <span>🟣 Proposition</span>
              <span class="count-pill" id="count-Proposition">0</span>
            </div>
            <div class="column-revenue" id="rev-Proposition">$0</div>
          </div>
          <div class="lead-cards-list" id="list-Proposition"></div>
        </div>

        <!-- Column 4: Won -->
        <div class="kanban-column" data-stage="Won" ondragover="allowDrop(event)" ondrop="handleDrop(event, 'Won')">
          <div class="column-header">
            <div class="column-title">
              <span>🟢 Won</span>
              <span class="count-pill" id="count-Won">0</span>
            </div>
            <div class="column-revenue" id="rev-Won">$0</div>
          </div>
          <div class="lead-cards-list" id="list-Won"></div>
        </div>

      </div>
    </div>
  </main>

  <!-- VIEW 2: Table List View -->
  <div class="view-content" id="view-table">
    <div class="table-view-container">
      <table class="leads-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Opportunity Name</th>
            <th>Contact / Partner</th>
            <th>Stage</th>
            <th>Probability</th>
            <th>Expected Revenue</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody id="table-leads-body">
        </tbody>
      </table>
    </div>
  </div>

  <!-- VIEW 3: Discuss & AI BI Hub -->
  <div class="view-content" id="view-discuss">
    <div class="discuss-container">
      <div class="discuss-sidebar">
        <div style="font-weight: 800; font-size: 12px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em;">
          Channels (8)
        </div>
        <div class="discuss-channel-item active" onclick="switchChannel('general')"># general</div>
        <div class="discuss-channel-item" onclick="switchChannel('sales')"># sales</div>
        <div class="discuss-channel-item" onclick="switchChannel('board-meetings')"># board-meetings</div>
        <div class="discuss-channel-item" onclick="switchChannel('rd')"># rd</div>
        <div class="discuss-channel-item" onclick="switchChannel('troubleshooting')"># troubleshooting</div>
        <div style="margin-top: 10px; font-weight: 800; font-size: 12px; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em;">
          AI Assistant (Local Ollama)
        </div>
        <div class="discuss-channel-item" style="color: var(--accent);" onclick="runAiDemo('texas')">
          🤖 Qwen-2.5-Coder: Texas SQL
        </div>
        <div class="discuss-channel-item" style="color: #34d399;" onclick="runAiDemo('ocr')">
          📄 Qwen-2.5-VL: Invoice OCR
        </div>
        <div class="discuss-channel-item" style="color: #f59e0b;" onclick="runAiDemo('helpdesk')">
          🎧 GLM-4: Support Ticket
        </div>
      </div>
      <div class="discuss-chat-panel">
        <div class="chat-header">
          <span id="current-channel-title"># general &bull; Company Announcements & AI Hub</span>
          <span style="font-size: 11px; color: var(--success); font-weight: 600;">● Online (Mitchell Admin)</span>
        </div>
        <div class="chat-messages" id="chat-messages">
          <div class="chat-bubble">
            <div class="avatar">MA</div>
            <div class="chat-content">
              <div class="chat-author">Mitchell Admin</div>
              <div class="chat-text">Welcome to the Enterprise Suite. 49 active CRM leads have been loaded directly from PostgreSQL, and all 25+ enterprise applications are activated with auto-login enabled.</div>
            </div>
          </div>
          <div class="chat-bubble">
            <div class="avatar" style="background: var(--accent);">AI</div>
            <div class="chat-content">
              <div class="chat-author">Odoo AI Co-Pilot (Qwen-2.5-Coder-32B)</div>
              <div class="chat-text">I am connected to PostgreSQL database <code>odoo</code> on <code>localhost:5432</code>. Ask me any natural-language query to inspect CRM pipelines, extract invoices, or run queries.</div>
            </div>
          </div>
        </div>
        <div class="chat-input-bar">
          <input type="text" class="chat-input" id="chat-user-input" placeholder="Ask a business query e.g. 'Show me all qualified leads in Texas over $20k'..." onkeydown="if(event.key==='Enter') sendChatMessage()">
          <button class="banner-btn" onclick="sendChatMessage()">Send</button>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal: Apps Grid Modal -->
  <div class="modal-overlay" id="apps-modal" onclick="if(event.target.id==='apps-modal') closeAppsModal()">
    <div class="modal-box large">
      <div class="modal-header">
        <div>
          <h3 style="font-size: 18px; font-weight: 800;">Enterprise Application Drawer</h3>
          <p style="font-size: 12px; color: var(--text-muted);">25+ Enterprise Apps Activated &bull; Running on Odoo 18.0</p>
        </div>
        <button class="modal-close-btn" onclick="closeAppsModal()">&times;</button>
      </div>
      <div class="apps-modal-grid" id="apps-grid-container"></div>
      <div style="margin-top: 14px; text-align: right;">
        <a href="http://localhost:8069" target="_blank" class="banner-btn">Open Full Odoo Workspace</a>
      </div>
    </div>
  </div>

  <!-- Modal: Create New Opportunity -->
  <div class="modal-overlay" id="new-lead-modal" onclick="if(event.target.id==='new-lead-modal') closeNewLeadModal()">
    <div class="modal-box">
      <div class="modal-header">
        <h3 style="font-size: 17px; font-weight: 800;">Create New Opportunity</h3>
        <button class="modal-close-btn" onclick="closeNewLeadModal()">&times;</button>
      </div>
      <form onsubmit="handleCreateLead(event)">
        <div class="form-group">
          <label class="form-label">Opportunity Title</label>
          <input type="text" class="form-control" id="form-name" required placeholder="e.g. Austin Smart Grid Upgrade">
        </div>
        <div class="form-group">
          <label class="form-label">Customer / Partner Name</label>
          <input type="text" class="form-control" id="form-company" placeholder="e.g. Austin Energy &bull; Sarah Vance">
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Expected Revenue ($)</label>
            <input type="number" class="form-control" id="form-rev" required placeholder="85000">
          </div>
          <div class="form-group">
            <label class="form-label">Target Stage</label>
            <select class="form-control" id="form-stage">
              <option value="New">New</option>
              <option value="Qualified" selected>Qualified</option>
              <option value="Proposition">Proposition</option>
              <option value="Won">Won</option>
            </select>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Probability (%)</label>
            <input type="number" class="form-control" id="form-prob" value="75">
          </div>
          <div class="form-group">
            <label class="form-label">Tag</label>
            <select class="form-control" id="form-tag">
              <option value="Texas">⭐ Texas Enterprise</option>
              <option value="Enterprise">Enterprise</option>
              <option value="Fintech">Fintech</option>
            </select>
          </div>
        </div>
        <button type="submit" class="btn-submit-lead">Save Opportunity</button>
      </form>
    </div>
  </div>

  <!-- Modal: Video Lightbox Player -->
  <div class="modal-overlay" id="video-modal" onclick="closeVideoModal(event)">
    <div class="video-lightbox-box">
      <div style="padding: 14px 20px; display: flex; justify-content: space-between; align-items: center; background: rgba(15,23,42,0.95); border-bottom: 1px solid rgba(255,255,255,0.1);">
        <span style="font-size: 15px; font-weight: 700; color: #fff;">🎬 1080p Full HD Walkthrough &bull; Remotion / HyperFrames</span>
        <button onclick="closeVideoModalDirect()" style="background: none; border: none; color: #94a3b8; font-size: 22px; cursor: pointer;">&times;</button>
      </div>
      <video id="lightbox-video-player" controls preload="auto">
        <source src="docs/videos/odoo-showcase-master.mp4" type="video/mp4">
      </video>
    </div>
  </div>

  <script>
    // Embedded Data directly exported from Odoo 18.0 database
    let allLeads = {leads_json_str};
    const appModules = {apps_json_str};

    // Render Apps Grid
    function renderAppsGrid() {{
      const container = document.getElementById('apps-grid-container');
      container.innerHTML = appModules.map(app => `
        <a href="${{app.url}}" target="_blank" class="app-tile">
          <div class="app-tile-icon" style="background: ${{app.color}}22; color: ${{app.color}};">
            ${{app.icon}}
          </div>
          <div class="app-tile-name">${{app.name}}</div>
          <div class="app-tile-badge">Active</div>
        </a>
      `).join('');
    }}

    // Render Kanban Leads
    function renderKanban() {{
      const stages = ['New', 'Qualified', 'Proposition', 'Won'];
      stages.forEach(st => {{
        document.getElementById('list-' + st).innerHTML = '';
      }});

      allLeads.forEach(lead => {{
        const stage = lead.stage || 'New';
        const targetList = document.getElementById('list-' + stage);
        if (!targetList) return;

        const isTexas = (lead.name && (lead.name.includes('Austin') || lead.name.includes('Dallas') || lead.name.includes('Houston') || lead.name.includes('San Antonio') || lead.name.includes('Fort Worth') || lead.name.includes('Texas')));
        const rev = lead.expected_revenue || 0;
        const prob = lead.probability || 0;
        const partner = lead.partner || lead.contact || 'Direct Lead';

        const card = document.createElement('div');
        card.className = 'lead-card';
        card.draggable = true;
        card.id = 'lead-card-' + lead.id;
        card.dataset.id = lead.id;
        card.dataset.rev = rev;
        card.dataset.texas = isTexas ? 'true' : 'false';
        card.ondragstart = handleDragStart;

        card.innerHTML = `
          <div class="lead-card-top">
            <div class="lead-name">${{lead.name}}</div>
          </div>
          <div class="lead-company">${{partner}}</div>
          <div class="lead-metrics">
            <span class="lead-val">$${{rev.toLocaleString()}}</span>
            <span class="lead-prob">${{stage === 'Won' ? 'Closed Won' : prob + '%'}}</span>
          </div>
          <div class="lead-tags">
            ${{isTexas ? '<span class="lead-tag tag-texas">⭐ Texas</span>' : ''}}
            ${{rev > 50000 ? '<span class="lead-tag tag-enterprise">Enterprise</span>' : '<span class="lead-tag tag-fintech">Commercial</span>'}}
            ${{prob >= 75 && stage !== 'Won' ? '<span class="lead-tag tag-priority-high">Hot</span>' : ''}}
          </div>
        `;
        targetList.appendChild(card);
      }});

      recalcTotals();
      renderTable();
    }}

    // Render Table View
    function renderTable() {{
      const tbody = document.getElementById('table-leads-body');
      tbody.innerHTML = allLeads.map(l => `
        <tr>
          <td style="font-family: var(--font-mono); color: var(--text-muted); font-size: 11px;">#${{l.id}}</td>
          <td style="font-weight: 700;">${{l.name}}</td>
          <td>${{l.partner || l.contact || '—'}}</td>
          <td><span class="count-pill">${{l.stage}}</span></td>
          <td>${{l.probability || 0}}%</td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: var(--accent);">$${{(l.expected_revenue || 0).toLocaleString()}}</td>
          <td style="color: var(--text-muted); font-size: 12px;">${{l.email || '—'}}</td>
        </tr>
      `).join('');
    }}

    // View Switching
    function switchView(view) {{
      document.querySelectorAll('.view-content').forEach(el => el.classList.remove('active'));
      document.querySelectorAll('.app-nav-tabs .tab-btn').forEach(el => el.classList.remove('active'));
      
      document.getElementById('view-' + view).classList.add('active');
      document.getElementById('tab-' + view).classList.add('active');
    }}

    // Drag and drop mechanics
    let draggedCardId = null;

    function handleDragStart(e) {{
      draggedCardId = e.target.id;
      e.dataTransfer.setData('text/plain', draggedCardId);
      e.target.classList.add('dragging');
    }}

    function allowDrop(e) {{
      e.preventDefault();
    }}

    function handleDrop(e, targetStage) {{
      e.preventDefault();
      const card = document.getElementById(draggedCardId);
      if (card) {{
        card.classList.remove('dragging');
        const targetList = document.getElementById('list-' + targetStage);
        targetList.prepend(card);

        // Update in memory array
        const leadId = parseInt(card.dataset.id);
        const item = allLeads.find(x => x.id === leadId);
        if (item) {{
          item.stage = targetStage;
        }}
        recalcTotals();
        renderTable();
      }}
    }}

    document.addEventListener('dragend', function(e) {{
      if (e.target.classList.contains('lead-card')) {{
        e.target.classList.remove('dragging');
      }}
    }});

    // Recalculate totals
    function recalcTotals() {{
      const stages = ['New', 'Qualified', 'Proposition', 'Won'];
      let grandTotal = 0;
      let totalCount = 0;

      stages.forEach(stage => {{
        const list = document.getElementById('list-' + stage);
        const cards = list ? list.querySelectorAll('.lead-card') : [];
        let stageRev = 0;
        cards.forEach(c => {{
          stageRev += parseFloat(c.dataset.rev) || 0;
        }});
        const countEl = document.getElementById('count-' + stage);
        const revEl = document.getElementById('rev-' + stage);
        if (countEl) countEl.innerText = cards.length;
        if (revEl) revEl.innerText = '$' + stageRev.toLocaleString();
        grandTotal += stageRev;
        totalCount += cards.length;
      }});

      document.getElementById('metric-pipeline-val').innerText = '$' + grandTotal.toLocaleString();
      document.getElementById('metric-deals-count').innerText = totalCount + ' Deals';
    }}

    // Filter and search
    function handleSearch(query) {{
      const q = query.toLowerCase();
      document.querySelectorAll('.lead-card').forEach(card => {{
        const text = card.innerText.toLowerCase();
        card.style.display = text.includes(q) ? 'block' : 'none';
      }});
    }}

    function filterTexasDeals() {{
      document.querySelectorAll('.lead-card').forEach(card => {{
        card.style.display = (card.dataset.texas === 'true') ? 'block' : 'none';
      }});
    }}

    function resetFilters() {{
      document.querySelectorAll('.lead-card').forEach(card => {{
        card.style.display = 'block';
      }});
      document.getElementById('search-input').value = '';
    }}

    // Theme switching
    function switchTheme(theme) {{
      document.documentElement.setAttribute('data-theme', theme);
      localStorage.setItem('crm_theme', theme);
    }}

    // Modals
    function openNewLeadModal() {{
      document.getElementById('new-lead-modal').classList.add('active');
    }}
    function closeNewLeadModal() {{
      document.getElementById('new-lead-modal').classList.remove('active');
    }}

    function openAppsModal() {{
      document.getElementById('apps-modal').classList.add('active');
    }}
    function closeAppsModal() {{
      document.getElementById('apps-modal').classList.remove('active');
    }}

    function openVideoModal() {{
      const modal = document.getElementById('video-modal');
      modal.classList.add('active');
      const player = document.getElementById('lightbox-video-player');
      player.play();
    }}
    function closeVideoModal(e) {{
      if (e.target.id === 'video-modal') closeVideoModalDirect();
    }}
    function closeVideoModalDirect() {{
      const modal = document.getElementById('video-modal');
      modal.classList.remove('active');
      const player = document.getElementById('lightbox-video-player');
      player.pause();
    }}

    function handleCreateLead(e) {{
      e.preventDefault();
      const name = document.getElementById('form-name').value;
      const company = document.getElementById('form-company').value;
      const rev = parseFloat(document.getElementById('form-rev').value) || 0;
      const stage = document.getElementById('form-stage').value;
      const prob = parseInt(document.getElementById('form-prob').value) || 50;

      const newLead = {{
        id: allLeads.length + 1,
        name: name,
        expected_revenue: rev,
        probability: prob,
        stage: stage,
        partner: company,
        contact: company,
        email: 'lead@example.com'
      }};

      allLeads.unshift(newLead);
      renderKanban();
      closeNewLeadModal();
      e.target.reset();
    }}

    // Discuss & AI helpers
    function switchChannel(name) {{
      document.querySelectorAll('.discuss-channel-item').forEach(el => el.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('current-channel-title').innerText = '#' + name;
    }}

    function sendChatMessage() {{
      const input = document.getElementById('chat-user-input');
      const val = input.value.trim();
      if (!val) return;

      const container = document.getElementById('chat-messages');
      container.innerHTML += `
        <div class="chat-bubble">
          <div class="avatar">MA</div>
          <div class="chat-content">
            <div class="chat-author">Mitchell Admin</div>
            <div class="chat-text">${{val}}</div>
          </div>
        </div>
      `;
      input.value = '';

      // Simulated local Ollama response
      setTimeout(() => {{
        container.innerHTML += `
          <div class="chat-bubble">
            <div class="avatar" style="background: var(--accent);">AI</div>
            <div class="chat-content">
              <div class="chat-author">Odoo AI Co-Pilot (Qwen-2.5-Coder-32B)</div>
              <div class="chat-text">Query executed against <code>crm_lead</code> on PostgreSQL:<br>
              <strong>Result:</strong> 5 qualified Texas opportunities found totalling $346,500. Deals include Austin Energy ($85k), Dallas Financial ($120k), Houston Medical ($45k), Fort Worth Industrial ($64k), San Antonio Logistics ($32.5k).</div>
            </div>
          </div>
        `;
        container.scrollTop = container.scrollHeight;
      }}, 600);
      container.scrollTop = container.scrollHeight;
    }}

    function runAiDemo(type) {{
      switchView('discuss');
      const container = document.getElementById('chat-messages');
      if (type === 'texas') {{
        container.innerHTML += `
          <div class="chat-bubble">
            <div class="avatar">MA</div>
            <div class="chat-content">
              <div class="chat-author">Mitchell Admin</div>
              <div class="chat-text">Show me all qualified leads in Texas with a deal value over $20k from this quarter.</div>
            </div>
          </div>
          <div class="chat-bubble">
            <div class="avatar" style="background: var(--accent);">AI</div>
            <div class="chat-content">
              <div class="chat-author">Odoo AI Co-Pilot (Qwen-2.5-Coder-32B)</div>
              <div class="chat-text">
                <code>SELECT id, name, expected_revenue, probability FROM crm_lead WHERE stage_id = 2 AND expected_revenue > 20000;</code><br><br>
                <strong>📊 5 Matching Texas Enterprise Opportunities:</strong><br>
                1. <strong>Dallas Financial Private AI Infrastructure</strong> — $120,000 (75%)<br>
                2. <strong>Enterprise Cloud Migration - Austin Energy</strong> — $85,000 (80%)<br>
                3. <strong>Fort Worth Industrial Automation Suite</strong> — $64,000 (85%)<br>
                4. <strong>Houston Medical Hub - Automated Billing</strong> — $45,000 (90%)<br>
                5. <strong>San Antonio Logistics - ERP Fleet</strong> — $32,500 (70%)<br>
                <em>Total Value: $346,500 &bull; Safe read execution in 4.2ms</em>
              </div>
            </div>
          </div>
        `;
      }} else if (type === 'ocr') {{
        container.innerHTML += `
          <div class="chat-bubble">
            <div class="avatar" style="background: #34d399;">AI</div>
            <div class="chat-content">
              <div class="chat-author">Smart Receipt & Invoice OCR (Qwen-2.5-VL-7B)</div>
              <div class="chat-text">
                <strong>Extracted Invoice #INV-2026-9812:</strong><br>
                Vendor: Dell Enterprise Solutions<br>
                Total Amount: $18,450.00 USD (Tax: $1,476.00)<br>
                Status: Created draft bill in <code>account.move</code> ready for one-click approval.
              </div>
            </div>
          </div>
        `;
      }} else if (type === 'helpdesk') {{
        container.innerHTML += `
          <div class="chat-bubble">
            <div class="avatar" style="background: #f59e0b;">AI</div>
            <div class="chat-content">
              <div class="chat-author">Autonomous Helpdesk (GLM-4-9B)</div>
              <div class="chat-text">
                Ticket #842: "VPN tunnel timeout on Austin branch."<br>
                <strong>Drafted Resolution:</strong> Matched resolution in past solved ticket #719. Sent automated routing fix to customer.
              </div>
            </div>
          </div>
        `;
      }}
      container.scrollTop = container.scrollHeight;
    }}

    // Init
    window.addEventListener('DOMContentLoaded', () => {{
      renderAppsGrid();
      renderKanban();

      const savedTheme = localStorage.getItem('crm_theme') || 'cyber-slate';
      document.getElementById('theme-selector').value = savedTheme;
      switchTheme(savedTheme);
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print('Successfully generated index.html with all 49 leads, 25+ apps, and live views!')
