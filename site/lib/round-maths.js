// The arithmetic of a priced round and of an exit waterfall.
// admin/build/round_maths.py is the same arithmetic for the build, line for line;
// tests/test_round_maths.py runs both on the same inputs and requires the same numbers.

export class Round_Maths {

    halfUp(value) {
        return Math.floor(value + 0.5)
    }

    pricedRound(holders, existingPool, investment, preMoney, poolPct, poolInPreMoney) {
        const existing = holders.reduce((sum, holder) => sum + holder.shares, 0) + existingPool
        let price, newShares, newPool
        if (poolInPreMoney) {
            const ratio     = investment / preMoney
            const preShares = (existing - existingPool) / (1 - poolPct * (1 + ratio))
            newPool         = Math.max(0, this.halfUp(preShares - existing))
            price           = preMoney / (existing + newPool)
            newShares       = Math.floor(investment / price)
        } else {
            price           = preMoney / existing
            newShares       = Math.floor(investment / price)
            newPool         = Math.max(0, this.halfUp((poolPct * (existing + newShares) - existingPool) / (1 - poolPct)))
        }
        const postShares = existing + newPool + newShares
        const rows = holders.map(h => ({ id: h.id, name: h.name, class: h.class, pre: h.shares, post: h.shares }))
        rows.push({ id: 'pool'    , name: 'Option pool', class: 'Options'  , pre: existingPool, post: existingPool + newPool },
                  { id: 'series-a', name: 'Series A'   , class: 'Preferred', pre: 0           , post: newShares              })
        for (const row of rows) {
            row.pre_pct  = row.pre  / existing
            row.post_pct = row.post / postShares
        }
        return { price, new_shares: newShares, new_pool: newPool, pre_shares: existing,
                 post_shares: postShares, post_money: price * postShares, rows }
    }

    waterfall(roundResult, investment, preferenceMultiple, participating, exitValue) {
        const rows       = roundResult.rows
        const post       = roundResult.post_shares
        const preferred  = rows.find(row => row.id === 'series-a')
        const others     = post - preferred.post
        const preference = Math.min(exitValue, investment * preferenceMultiple)
        const payout     = {}
        let   converts   = false
        if (participating) {
            const remainder = exitValue - preference
            for (const row of rows) payout[row.id] = remainder * row.post / post
            payout['series-a'] += preference
        } else {
            const asConverted = exitValue * preferred.post / post
            converts          = asConverted > preference
            if (converts) {
                for (const row of rows) payout[row.id] = exitValue * row.post / post
            } else {
                const remainder = exitValue - preference
                for (const row of rows) payout[row.id] = remainder * row.post / others
                payout['series-a'] = preference
            }
        }
        return { exit_value: exitValue, converts, payout }
    }
}
