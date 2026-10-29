// Score a company against the GenAI cybersecurity startup evaluation framework.
// Criteria, scores and bands come from data/framework.json; nothing entered leaves the browser.

import { Base_Component } from '../base/base-component.js'

export class Evaluation_Scorecard extends Base_Component {

    static jsUrl = import.meta.url

    async onReady() {
        this.framework = JSON.parse(await this.fetchText(new URL('../../data/framework.json', Evaluation_Scorecard.jsUrl)))
        const strongest = this.framework.strongest_predictors
        this.$('#criteria').innerHTML = this.framework.criteria.map(c => `
            <fieldset data-criterion="${this.escape(c.id)}">
                <legend><span class="num">${this.escape(c.number)}</span> ${this.escape(c.name)}${strongest.includes(c.id) ? ' <span class="tag">strong predictor</span>' : ''}</legend>
                <p class="question">${this.escape(c.question)}</p>
                <div class="flags"><span class="red">${this.escape(c.red)}</span><span class="green">${this.escape(c.green)}</span></div>
                <div class="scores" role="radiogroup" aria-label="${this.escape(c.name)}">
                    ${this.framework.scores.map(s => `
                        <label title="${this.escape(s.label)}: ${this.escape(s.meaning)}">
                            <input type="radio" name="${this.escape(c.id)}" value="${s.score}"><span>${s.score}</span>
                        </label>`).join('')}
                </div>
            </fieldset>`).join('')
        this.$('form').addEventListener('change', () => this.render())
        this.$('#reset').addEventListener('click', () => { this.$('form').reset(); this.render() })
        this.render()
    }

    render() {
        const picked = [...this.$$('input[type=radio]:checked')].map(input => Number(input.value))
        const total  = picked.reduce((sum, score) => sum + score, 0)
        const count  = this.framework.criteria.length
        const max    = count * 5
        this.$('#total').textContent = `${total} / ${max}`
        this.$('#meter').style.width = `${(total / max * 100).toFixed(1)}%`
        if (picked.length < count) {
            this.$('#band').textContent = `${picked.length} of ${count} criteria scored`
            this.$('#band').className   = 'band'
            return
        }
        const band = this.framework.bands.find(b => total >= b.min && total <= b.max)
        this.$('#band').textContent = band ? `${band.label}: ${band.meaning}` : ''
        this.$('#band').className   = `band band-${band ? band.label.toLowerCase().replace(/\s+/g, '-') : ''}`
        this.emit('scorecard-complete', { total })
    }
}

customElements.define('evaluation-scorecard', Evaluation_Scorecard)
