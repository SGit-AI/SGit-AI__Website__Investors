# The arithmetic of a priced round and of an exit waterfall.
# site/lib/round-maths.js is the same arithmetic for the browser, line for line;
# tests/test_round_maths.py runs both on the same inputs and requires the same numbers.

import math


class Round_Maths:

    def half_up(self, value):
        return math.floor(value + 0.5)

    def priced_round(self, holders, existing_pool, investment, pre_money, pool_pct, pool_in_pre_money):
        existing = sum(holder['shares'] for holder in holders) + existing_pool
        if pool_in_pre_money:
            ratio      = investment / pre_money
            pre_shares = (existing - existing_pool) / (1 - pool_pct * (1 + ratio))
            new_pool   = max(0, self.half_up(pre_shares - existing))
            price      = pre_money / (existing + new_pool)
            new_shares = math.floor(investment / price)
        else:
            price      = pre_money / existing
            new_shares = math.floor(investment / price)
            new_pool   = max(0, self.half_up((pool_pct * (existing + new_shares) - existing_pool) / (1 - pool_pct)))
        post_shares = existing + new_pool + new_shares
        rows  = [{ 'id': h['id'], 'name': h['name'], 'class': h['class'], 'pre': h['shares'], 'post': h['shares'] } for h in holders]
        rows += [{ 'id': 'pool'    , 'name': 'Option pool', 'class': 'Options'   , 'pre': existing_pool, 'post': existing_pool + new_pool },
                 { 'id': 'series-a', 'name': 'Series A'   , 'class': 'Preferred' , 'pre': 0            , 'post': new_shares            }]
        pre_total = existing
        for row in rows:
            row['pre_pct' ] = row['pre' ] / pre_total
            row['post_pct'] = row['post'] / post_shares
        return { 'price'       : price      ,
                 'new_shares'  : new_shares ,
                 'new_pool'    : new_pool   ,
                 'pre_shares'  : pre_total  ,
                 'post_shares' : post_shares,
                 'post_money'  : price * post_shares,
                 'rows'        : rows       }

    def waterfall(self, round_result, investment, preference_multiple, participating, exit_value):
        rows       = round_result['rows']
        post       = round_result['post_shares']
        preferred  = next(row for row in rows if row['id'] == 'series-a')
        others     = post - preferred['post']
        preference = min(exit_value, investment * preference_multiple)
        payout     = {}
        converts   = False
        if participating:
            remainder = exit_value - preference
            for row in rows:
                payout[row['id']] = remainder * row['post'] / post
            payout['series-a'] += preference
        else:
            as_converted = exit_value * preferred['post'] / post
            converts     = as_converted > preference
            if converts:
                for row in rows:
                    payout[row['id']] = exit_value * row['post'] / post
            else:
                remainder = exit_value - preference
                for row in rows:
                    payout[row['id']] = remainder * row['post'] / others
                payout['series-a'] = preference
        return { 'exit_value': exit_value, 'converts': converts, 'payout': payout }
