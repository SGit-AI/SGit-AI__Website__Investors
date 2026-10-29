// The base every component on this site extends. A component is three files with one basename
// (name.js, name.html, name.css); the base finds the other two from the subclass's own URL,
// renders them into a shadow root, and calls onReady(). Subclasses never use connectedCallback.

export class Base_Component extends HTMLElement {

    static jsUrl = import.meta.url

    async connectedCallback() {
        if (this.shadowRoot) return
        const jsUrl = this.constructor.jsUrl
        const name  = jsUrl.split('/').pop().replace(/\.js$/, '')
        try {
            const [markup, css] = await Promise.all([this.fetchText(new URL(`${name}.html`, jsUrl)),
                                                     this.fetchText(new URL(`${name}.css` , jsUrl))])
            this.attachShadow({ mode: 'open' }).innerHTML = `<style>${css}</style>${markup}`
            this.onReady()
        } catch (error) {
            console.error(`${name}: could not start`, error)                 // the fallback markup inside the element stays visible
        }
    }

    async fetchText(url) {
        const response = await fetch(url)
        if (!response.ok) throw new Error(`${url} returned ${response.status}`)
        return response.text()
    }

    onReady() {}

    $(selector)  { return this.shadowRoot.querySelector(selector)    }
    $$(selector) { return this.shadowRoot.querySelectorAll(selector) }

    escape(text) {
        return String(text).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[ch]))
    }

    emit(name, detail) {
        document.dispatchEvent(new CustomEvent(`investor:${name}`, { detail, bubbles: true, composed: true }))
    }
}
