(function() {
    'use strict';

    const THEMES = [
        {
            id: 'midnight-gold',
            name: 'Executive Midnight Gold',
            category: 'Luxury / Financial Terminal',
            desc: 'Deep noir obsidian background with warm champagne gold trim and status pills.',
            swatches: ['#09090b', '#18181b', '#d97706']
        },
        {
            id: 'cyber-slate',
            name: 'Cyber Slate',
            category: 'Modern Dark Enterprise',
            desc: 'Obsidian glass dark mode with electric indigo accents and luminescent card borders.',
            swatches: ['#0b0f19', '#111827', '#6366f1']
        },
        {
            id: 'cupertino',
            name: 'Cupertino Precision',
            category: 'Apple Minimalist Clean',
            desc: 'Ultra-crisp soft light canvas with frosted translucent navbar and Apple Azure Blue.',
            swatches: ['#f8fafc', '#ffffff', '#0071e3']
        },
        {
            id: 'emerald-glass',
            name: 'Emerald Fluid Glass',
            category: 'Fintech Neo-Glass / BioTech',
            desc: 'Translucent deep emerald tones with electric mint green glow and glassmorphic navbar.',
            swatches: ['#022c22', '#064e3b', '#10b981']
        },
        {
            id: 'classic',
            name: 'Classic Standard',
            category: 'Default Factory Mode',
            desc: 'Original standard system interface palette without custom theme overrides.',
            swatches: ['#ffffff', '#714b67', '#00a09d']
        }
    ];

    function applyTheme(themeId) {
        // Enforce midnight-gold as premier default if classic or empty
        const activeId = (!themeId || themeId === 'classic') ? 'midnight-gold' : themeId;
        document.documentElement.setAttribute('data-theme', activeId);
        document.body.setAttribute('data-theme', activeId);
        localStorage.setItem('odoo_interface_theme', activeId);
        updateActiveCard(activeId);
        updatePillLabel(activeId);
    }

    function getSavedTheme() {
        const saved = localStorage.getItem('odoo_interface_theme');
        if (!saved || saved === 'classic') {
            localStorage.setItem('odoo_interface_theme', 'midnight-gold');
            return 'midnight-gold';
        }
        return saved;
    }

    function updateActiveCard(currentTheme) {
        document.querySelectorAll('.odoo-theme-card').forEach(card => {
            if (card.dataset.theme === currentTheme) {
                card.classList.add('selected');
            } else {
                card.classList.remove('selected');
            }
        });
    }

    function updatePillLabel(themeId) {
        const pill = document.getElementById('odoo-theme-switcher-pill');
        if (!pill) return;
        const found = THEMES.find(t => t.id === themeId);
        pill.innerHTML = `<span>🎨</span> <span>Interface: <strong>${found ? found.name : 'Theme'}</strong></span>`;
    }

    function initThemeSwitcher() {
        // 1. Initial theme load
        const activeTheme = getSavedTheme();
        applyTheme(activeTheme);

        // 2. Create Floating Switcher Pill
        if (!document.getElementById('odoo-theme-switcher-pill')) {
            const pill = document.createElement('div');
            pill.id = 'odoo-theme-switcher-pill';
            pill.title = 'Switch Web Interface Style';
            document.body.appendChild(pill);
            updatePillLabel(activeTheme);

            pill.addEventListener('click', toggleModal);
        }

        // 3. Create Modal
        if (!document.getElementById('odoo-theme-modal-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'odoo-theme-modal-overlay';
            
            let cardsHtml = '';
            THEMES.forEach(t => {
                const swatchesHtml = t.swatches.map(c => `<div class="odoo-swatch" style="background:${c}"></div>`).join('');
                cardsHtml += `
                    <div class="odoo-theme-card ${t.id === activeTheme ? 'selected' : ''}" data-theme="${t.id}">
                        <div>
                            <div style="font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px;">
                                ${t.name}
                                <span style="font-size: 11px; background: rgba(255,255,255,0.1); padding: 2px 8px; border-radius: 12px; font-weight: normal; color: #94a3b8;">${t.category}</span>
                            </div>
                            <div style="font-size: 12px; color: #94a3b8; margin-top: 4px;">${t.desc}</div>
                        </div>
                        <div class="odoo-theme-swatches">${swatchesHtml}</div>
                    </div>
                `;
            });

            overlay.innerHTML = `
                <div id="odoo-theme-modal">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                        <div>
                            <h2 style="font-size: 18px; font-weight: 700; margin: 0; color: #ffffff;">Choose Web Interface Style</h2>
                            <p style="font-size: 13px; color: #94a3b8; margin: 4px 0 0 0;">Zero-breakage themes. Non-destructive aesthetic overlays.</p>
                        </div>
                        <button id="odoo-theme-modal-close" style="background: none; border: none; color: #94a3b8; font-size: 22px; cursor: pointer; padding: 4px 8px;">&times;</button>
                    </div>
                    <div id="odoo-theme-cards-list">
                        ${cardsHtml}
                    </div>
                    <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid rgba(255,255,255,0.1);">
                        <div style="font-size: 13px; font-weight: 600; color: #a5b4fc; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;">
                            <span>🎬</span> Showcase Preview & System Walkthrough
                        </div>
                        <div style="display: flex; gap: 16px; align-items: center; background: rgba(0,0,0,0.3); padding: 12px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                            <img src="/auto_login/static/src/img/odoo-showcase-preview.gif" style="width: 140px; height: auto; border-radius: 8px; border: 1px solid rgba(255,255,255,0.15);" alt="Showcase Preview" />
                            <div>
                                <div style="font-size: 14px; font-weight: 600; color: #ffffff;">1080p Full HD Video Tour</div>
                                <div style="font-size: 12px; color: #94a3b8; margin: 4px 0 8px 0;">30-second high-production walkthrough covering all 25+ apps, themes, and local AI.</div>
                                <a href="https://odoo-local.vercel.app" target="_blank" style="display: inline-block; padding: 6px 14px; border-radius: 6px; background: #6366f1; color: #fff; font-size: 12px; font-weight: 600; text-decoration: none;">Watch Live on Vercel &rarr;</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.appendChild(overlay);

            // Overlay click listeners
            overlay.addEventListener('click', function(e) {
                if (e.target === overlay || e.target.id === 'odoo-theme-modal-close') {
                    toggleModal();
                }
            });

            // Card click listeners
            overlay.querySelectorAll('.odoo-theme-card').forEach(card => {
                card.addEventListener('click', function() {
                    const selected = this.dataset.theme;
                    applyTheme(selected);
                    setTimeout(toggleModal, 180);
                });
            });
        }
    }

    function toggleModal() {
        const overlay = document.getElementById('odoo-theme-modal-overlay');
        if (overlay) {
            overlay.classList.toggle('active');
        }
    }

    // Keyboard shortcut: Ctrl + Alt + T opens theme switcher
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.altKey && (e.key === 't' || e.key === 'T')) {
            toggleModal();
        }
        if (e.key === 'Escape') {
            const overlay = document.getElementById('odoo-theme-modal-overlay');
            if (overlay && overlay.classList.contains('active')) {
                overlay.classList.remove('active');
            }
        }
    });

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initThemeSwitcher);
    } else {
        initThemeSwitcher();
    }
})();
