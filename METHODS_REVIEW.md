# Methods review: Green and Scotchmer (1995)

- **Paper:** Jerry R. Green and Suzanne Scotchmer, "On the Division of Profit in Sequential Innovation," *RAND Journal of Economics* 26(1), Spring 1995, pp. 20–33. An earlier version circulated as Harvard Institute of Economic Research Working Paper 1638 (1993).
- **Statistical focus:** the paper's Proposition 1 (the first innovator's profit is never more than the joint profit of both generations net of both research costs, and is strictly less for some second-generation products), the even Nash split of the incremental surplus in an ex ante licensing agreement that drives it, and the policy conclusion that patents must last longer when the two generations of research are done by different firms.
- **Review standard:** internal consistency of the formal results, explicit statement of assumptions, and whether the predictions can be tested. There is no data in the paper, so the AEA Data and Code Availability Policy does not apply.
- **What was read:** the published abstract on IDEAS/RePEc and EconPapers; a seminar presentation that restates the model's notation, the ex ante bargaining payoffs and Propositions 1 to 5 with the authors' conclusions (slides by Dane Richard Franchi, hosted on Felix Munoz-Garcia's course page at felixmunozgarcia.com); a summary of the model in a research blog (A Fine Theorem, 2012); and the abstract of Chou and Haller's 1995 reply (CentER Discussion Paper 1995-64). I did not read the full published text, so page numbers below are not given and everything extracted comes from the restatement and the abstract. Where the restatement and the blog summary disagree on details (for example the blog describes ex post sales of patents where the slides describe ex ante licenses), I follow the slides, which quote the propositions directly.

## Methods summary

The paper is a theory paper with no data. It builds a two-stage model of cumulative innovation. A first firm can invent a product of quality x at cost c1. That invention makes possible a second-generation product of quality x + y, which a second firm can develop at cost c2. Both patents are assumed to start and end together and last T periods. Profit over the patent life depends on market structure: the first product alone sold by a monopolist earns π_x(T); the improved product sold by a monopolist earns π_{x+y}(T); if the two products compete, they earn π_x^c(T) and π_y^c(T), with π_x^c ≤ π_x and π_{x+y} ≥ π_x^c + π_y^c. Patent breadth is a threshold y*: a second product with y ≥ y* does not infringe the first patent. The firms may sign an ex ante license after the second firm has its idea but before it sinks c2, or an ex post license after c2 is sunk and the product infringes. Agreements before the first invention are ruled out on the grounds that the first firm cannot identify future improvers. Bargaining in an agreement splits the surplus above each side's threat point evenly. The analysis compares the first innovator's profit under different breadths and antitrust rules, and derives the minimum patent life that makes the first investment worthwhile.

### Research design

A two-firm bargaining model of sequential innovation, solved analytically. Results are propositions about the first innovator's profit under different patent breadths and licensing rules.

### Sampling strategy, sample size, and inclusion and exclusion criteria

Do not apply. The paper uses no data, so there is no sample, no sample size and no inclusion rule. The closest analogue is the set of cases the model covers (infringing and non-infringing improvements, ex ante and ex post licensing), which the propositions treat one at a time.

### Independent and dependent variables

In the model, the inputs are patent breadth y*, patent life T, the quality steps x and y, and the research costs c1 and c2; the outcome is the first innovator's profit and the minimum patent life that makes the first investment worthwhile.

### Statistical methods

Do not apply. The results are derived, not estimated.

### Reported effect sizes, confidence intervals and p-values

Do not apply. The paper reports no estimates, intervals or tests. Its formal results, listed in the table below, stand in for statistics.

### Missing data treatment

Does not apply.

### Stated limitations

As restated in the sources read, the authors assume both patents start and end together, that breadth can be expressed in units of value, that agreements before the first invention are impossible, and that bargaining splits surplus evenly. Whether the paper states further limitations could not be checked without the full text.

## Statistics extraction table

| Statistic | Value and unit | Source location | What it measures | What it does not establish |
|---|---|---|---|---|
| Proposition 1 bound | Firm 1's profit ≤ π_{x+y}(T) − (c1 + c2), strictly less for some second-generation products | Proposition 1 (as restated in the seminar slides) | The most the first innovator can earn when the second generation is developed by another firm | How large the shortfall is in any real industry, or how often the strict case occurs |
| Ex ante agreement payoffs, non-infringing case | Firm 1: π_x^c − c1 + ½[π_{x+y} − (π_x^c + π_y^c)]; firm 2: π_y^c − c2 + ½[π_{x+y} − (π_x^c + π_y^c)] | Division-of-profit section (as restated) | Each firm's profit when the competitive outcome is the threat point and the gain from merging the two products is split evenly | That real negotiations split surplus evenly; the ½ is an assumption of symmetric Nash bargaining, not an estimate |
| Even split share | ½ of the incremental surplus to each firm | Same | The bargaining weight assumed throughout | Any measured share of profit |
| Proposition 2 | Optimal breadth y* = ∞ when all uncertainty about y and c2 is resolved before the second investment | Proposition 2 (as restated) | That broad patents maximize the first innovator's profit under full information | That broad patents are optimal when value remains uncertain |
| Proposition 3 | Optimal breadth finite, y* < ∞, when only c2 is known before the second investment and an expected-profit condition holds | Proposition 3 (as restated) | A case where a narrower patent removes the second firm's credible threat not to invest | How common that case is |
| Proposition 4 | With ex ante licensing legal, firm 1 earns more for any breadth if ex post licensing is also permitted | Proposition 4 (as restated) | Ex post licensing as a shift in the threat points of the ex ante deal | Effects on total profit, which the restatement says are unchanged |
| Proposition 5 | If the first technology has no stand-alone value (π_{x+y}(T) = π_y^c(T)), ex ante licensing raises social welfare for any breadth | Proposition 5 (as restated) | A welfare ranking of antitrust rules for research tools | Welfare effects when the first product sells on its own |
| Patent-life conclusion | Patents must last longer when cumulative research is done by different firms than by one firm | Abstract; conclusion (as restated) | The policy implication of Proposition 1 | A specific length in years |

## Interpretation notes

- The paper's numbers are bounds and comparative statics, not estimates. Proposition 1 is close to an accounting identity once one accepts that the second firm must cover its own cost and has some bargaining power; the substantive content is in why the second firm keeps a positive share (non-infringement, credible refusal to invest, or exclusive ability to develop).
- The even split is a modeling convenience. The qualitative results (firm 1 cannot collect everything; breadth and ex post licensing matter only through threat points) hold for any interior bargaining weight, but any quantitative reading of "half" depends on it.
- The assumption that both patents begin and end at the same time removes the timing question that later work (for example on patent life when improvements arrive years later) treats as central. The restatement says the authors judged that relaxing it would not change the conclusions; the paper does not test that claim.
- Breadth is defined in economic units (the value increment y), while courts judge infringement on technical claims. The authors acknowledge this proxy, so the breadth results speak to the economic reach of a patent rather than to claim language.
- Chou and Haller (1995) argue that when patents are probabilistic and the patentee offers a licensing contract, the basic researcher can extract essentially all the profit facilitated by the basic innovation across a wide range of parameters. That is a disagreement about the bargaining protocol and threat points, not an identified error in Green and Scotchmer's derivations.

## Unanswered questions

- How large is the share of follow-on value that pioneers actually collect, and does it vary with patent breadth as Propositions 2 and 3 suggest?
- How sensitive is the patent-life conclusion to unequal bargaining power, to many potential second innovators competing for the same improvement, or to asymmetric information about c2?
- When the first innovator can also develop the improvement itself, does integration replace licensing, and does that change the policy prescription?
- How should breadth be measured in practice so that the model's y* can be mapped to examined claims?

## Items requiring expert verification

- Exact wording and page locations of Propositions 1 to 5 in the published version, since this review relied on a faithful-looking restatement rather than the article itself.
- Whether the published paper contains numerical examples or calibrations not mentioned in the restatement or the abstract.
- Whether the ex ante payoff formula in the restatement applies only to the non-infringing case or is stated more generally in the paper.
- The extent to which Chou and Haller's full-extraction result depends on take-it-or-leave-it offers by the patentee, which would make it a change in bargaining power rather than a contradiction.

The modern data in this repository do not reproduce anything in the paper, which has no data. They take its sharpest prediction, that a pioneer keeps less of the value of an improvement made by another firm than of one it makes itself, and measure that gap on 2000–2014 US patents using stock-market patent values and forward citations.
