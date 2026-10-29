import json
import os
import subprocess
import unittest

from admin.build.round_maths import Round_Maths

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOLDERS = [{ 'id': 'founder-a', 'name': 'Founder A', 'class': 'Ordinary', 'shares': 5000000 },
           { 'id': 'founder-b', 'name': 'Founder B', 'class': 'Ordinary', 'shares': 4000000 },
           { 'id': 'seed'     , 'name': 'Seed'     , 'class': 'Ordinary', 'shares': 1000000 }]
CASES   = [(3000000, 12000000, 0.10, True , 1  , True , 40000000),
           (3000000, 12000000, 0.08, True , 1  , False, 15000000),
           (3000000, 12000000, 0.08, True , 1  , False, 40000000),
           (2000000,  6000000, 0.15, False, 1.5, False,  5000000),
           (1000000,  9000000, 0.00, True , 2  , True ,  1000000)]


class test_Round_Maths(unittest.TestCase):

    def setUp(self):
        self.maths = Round_Maths()

    def test_pool_is_the_agreed_share_after_the_round(self):
        for investment, pre, pct, in_pre, *_ in CASES:
            result = self.maths.priced_round(HOLDERS, 0, investment, pre, pct, in_pre)
            pool   = next(row for row in result['rows'] if row['id'] == 'pool')
            self.assertAlmostEqual(pool['post_pct'], pct, places=5)

    def test_pool_in_pre_money_keeps_the_investor_share(self):                 # the investor buys investment / post-money of the company
        result = self.maths.priced_round(HOLDERS, 0, 3000000, 12000000, 0.10, True)
        series = next(row for row in result['rows'] if row['id'] == 'series-a')
        self.assertAlmostEqual(series['post_pct'], 0.20, places=5)
        self.assertAlmostEqual(result['price'], 1.05, places=5)

    def test_waterfall_pays_out_the_exit(self):
        for investment, pre, pct, in_pre, multiple, participating, exit_value in CASES:
            result = self.maths.priced_round(HOLDERS, 0, investment, pre, pct, in_pre)
            fall   = self.maths.waterfall(result, investment, multiple, participating, exit_value)
            self.assertAlmostEqual(sum(fall['payout'].values()), exit_value, delta=1)

    def test_non_participating_converts_only_when_it_pays(self):
        result = self.maths.priced_round(HOLDERS, 0, 3000000, 12000000, 0.08, True)
        self.assertFalse(self.maths.waterfall(result, 3000000, 1, False, 15000000)['converts'])
        self.assertTrue (self.maths.waterfall(result, 3000000, 1, False, 40000000)['converts'])

    def test_javascript_gives_the_same_numbers(self):                          # the browser's arithmetic against the build's
        script = ("import { Round_Maths } from './site/lib/round-maths.js';"
                  "const m = new Round_Maths(); const input = JSON.parse(process.argv[1]); const out = [];"
                  "for (const [inv, pre, pct, inPre, mult, part, exit] of input.cases) {"
                  "  const r = m.pricedRound(input.holders, 0, inv, pre, pct, inPre);"
                  "  out.push({ round: r, fall: m.waterfall(r, inv, mult, part, exit) }) }"
                  "console.log(JSON.stringify(out))")
        run = subprocess.run(['node', '--input-type=module', '-e', script, json.dumps({ 'holders': HOLDERS, 'cases': CASES })],
                             cwd=ROOT, capture_output=True, text=True, check=True)
        for case, js in zip(CASES, json.loads(run.stdout)):
            investment, pre, pct, in_pre, multiple, participating, exit_value = case
            py   = self.maths.priced_round(HOLDERS, 0, investment, pre, pct, in_pre)
            fall = self.maths.waterfall(py, investment, multiple, participating, exit_value)
            for key in ('new_shares', 'new_pool', 'post_shares'):
                self.assertEqual(py[key], js['round'][key], key)
            self.assertEqual(py['price'], js['round']['price'])
            self.assertEqual(fall['converts'], js['fall']['converts'])
            for holder, value in fall['payout'].items():
                self.assertAlmostEqual(value, js['fall']['payout'][holder], places=6)
