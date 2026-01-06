// i18n client-side support

const I18N = {
    texts: [],
    currentLang: 'English',
    keys: [],
    
    async load(lang) {
        try {
            const res = await API.get(`/api/i18n/${lang}`);
            // backwards compatible: API may return either an array (old)
            // or an object {texts: [...], overrides: {...}}
            if (Array.isArray(res)) {
                this.texts = res;
                this.overrides = {};
            } else if (res && res.texts) {
                this.texts = res.texts || [];
                this.overrides = res.overrides || {};
            } else {
                this.texts = [];
                this.overrides = {};
            }
            this.currentLang = lang;

            // Ensure we have the English keys mapping for string->index lookup
            if (!this.keys || this.keys.length === 0) {
                try {
                    const en = await API.get('/api/i18n/English');
                    if (Array.isArray(en)) {
                        this.keys = en;
                    } else if (en && en.texts) {
                        this.keys = en.texts;
                    } else {
                        this.keys = [];
                    }
                } catch (e) {
                    console.warn('Failed to load English keys for i18n:', e);
                    this.keys = [];
                }
            }
        } catch (error) {
            console.error('Failed to load translations:', error);
        }
    },

    t(key) {
        // If numeric index provided
        if (typeof key === 'number') {
            const idx = key;
            if (idx >= 0 && idx < this.texts.length) return this.texts[idx];
            return `[Missing: ${idx}]`;
        }

        // If a string is provided, try to map it using English keys
        if (typeof key === 'string') {
            try {
                const idx = this.keys.indexOf(key);
                if (idx >= 0 && idx < this.texts.length) return this.texts[idx];
            } catch (e) {
                // fallthrough
            }
            // If not found in keys, check overrides (string-keyed) and then fallback
            try {
                if (this.overrides && key in this.overrides) return this.overrides[key];
            } catch (e) {
                // ignore
            }
            return key;
        }

        return String(key);
    }
};

// Expose as global function
window._ = (index) => I18N.t(index);

// Load on page load
$(document).ready(() => {
    const lang = $('html').attr('lang') || 'English';
    I18N.load(lang);
});
