// Change the terms of a round and see the cap table and the exit waterfall recompute.
// The arithmetic is site/lib/round-maths.js, the same as the build's.

import { Base_Component } from '../base/base-component.js'
import { Round_Maths    } from '../../lib/round-maths.js'

const MONEY = new Intl.NumberFormat('en-GB', { style: 'currency', currency: 'GBP', maximumFractionDigits: 0 })
const COUNT = new Intl.NumberFormat('en-GB')

export class Round_Modeller extends Base_Component {

    static jsUrl = import.meta.url

    onReady() {
        this.maths = new Round_Maths()
        this.model = JSON.parse(this.dataset.model)
        const terms = this.model.terms
        this.$('#investment').value    = terms.investment
        this.$('#pre-money').value     = terms.pre_money
        this.$('#pool-pct').value      = terms.pool_pct * 100
        this.$('#pool-pre').checked    = terms.pool_in_pre_money
        this.$('#multiple').value      = terms.preference_multiple
        this.$('#participating').checked = terms.participating
        this.$('#exit').value          = 40000000
        this.$('form').addEventListener('input', () => this.render())
        this.$('form').addEventListener('submit', event => event.preventDefault())
        this.render()
    }

    read() {
        const number = id => Math.max(0, Number(this.$(id).value) || 0)
        return { investment   : number('#investment'),
                 preMoney     : Math.max(1, number('#pre-money')),
                 poolPct      : Math.min(0.5, number('#pool-pct') / 100),
                 poolInPre    : this.$('#pool-pre').checked,
                 multiple     : number('#multiple'),
                 participating: this.$('#participating').checked,
                 exitValue    : number('#exit') }
    }

    render() {
        const t      = this.read()
        const result = this.maths.pricedRound(this.model.holders, this.model.existing_pool, t.investment, t.preMoney, t.poolPct, t.poolInPre)
        const fall   = this.maths.waterfall(result, t.investment, t.multiple, t.participating, t.exitValue)
        this.$('#summary').textContent =
            `Price per share £${result.price.toFixed(4)} · ${COUNT.format(result.new_shares)} new Series A shares · ` +
            `${COUNT.format(result.new_pool)} new pool shares · post-money ${MONEY.format(result.post_money)}`
        const max  = Math.max(...result.rows.map(row => fall.payout[row.id]), 1)
        this.$('tbody').innerHTML = result.rows.map(row => `
            <tr>
                <th scope="row">${this.escape(row.name)}</th>
                <td>${COUNT.format(row.post)}</td>
                <td>${(row.post_pct * 100).toFixed(2)}%</td>
                <td>${MONEY.format(fall.payout[row.id])}</td>
                <td class="bar-cell"><span class="bar ${row.id === 'series-a' ? 'bar-pref' : ''}" style="width:${(fall.payout[row.id] / max * 100).toFixed(1)}%"></span></td>
            </tr>`).join('')
        this.$('#exit-note').textContent = t.participating
            ? `At a ${MONEY.format(t.exitValue)} exit, Series A takes its preference first and then shares in the rest.`
            : fall.converts
                ? `At a ${MONEY.format(t.exitValue)} exit, Series A does better converting to ordinary shares, so everyone is paid pro rata.`
                : `At a ${MONEY.format(t.exitValue)} exit, Series A takes its preference; the rest is shared by everyone else.`
    }
}

customElements.define('round-modeller', Round_Modeller)
