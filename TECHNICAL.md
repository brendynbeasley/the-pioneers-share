# Technical notes

This is the technical companion to the [README](README.md). It covers the original study, the data, the method,
every test statistic and how to reproduce the results. All tables are in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

Jerry R. Green and Suzanne Scotchmer, "On the Division of Profit in Sequential Innovation," *RAND Journal of
Economics* 26(1), 1995, pp. 20–33. It is a theory paper. A first firm invents a product (quality $`x`$, cost $`c_1`$) that
makes possible a second-generation product (quality $`x + y`$, cost $`c_2`$) developed by another firm. With an ex ante
license and an even Nash split, the first firm earns its threat point plus half of the incremental surplus, so
(Proposition 1) its profit is never more than $`\pi_{x+y}(T) - (c_1 + c_2)`$ and is strictly less for some improvements.
Broad patents ($`y^* = \infty`$) are best when the improvement's value and cost are known before the second investment,
ex post licensing raises the first firm's share, and patents must last longer when the two generations are done
by different firms. The paper has no data and no headline estimate; its headline is the bound and the even split.

## Headline results

| Specification | b_S (% per own follow-on) | b_E (% per outside follow-on) | λ = b_E / b_S | 95% CI | N |
|---|---|---|---|---|---|
| Main: log value, firm + CPC-year FE | 0.195 (0.065) | 0.035 (0.010) | 0.181 | [0.056, 0.307] | 1,238,587 |
| Firm × five-year + CPC-year FE | 0.078 (0.025) | 0.017 (0.005) | 0.225 | [0.026, 0.424] | 1,238,587 |
| Firm × year FE | 0.006 (0.006) | 0.012 (0.003) | not defined | | 1,238,587 |
| Discrete technologies (drugs, chemicals) | | 0.151 (0.032) | 1.211 | | 783,277 pooled |
| Complex technologies (computing, semiconductors) | | 0.043 (0.011) | 0.154 | | 783,277 pooled |

Standard errors clustered by firm in parentheses. Under the main specification λ = 1 is rejected (p = 0.010) and
λ = ½ is rejected (p = 0.040). An outside follow-on patent is worth 0.11 percentage points less to the pioneer in
complex than in discrete technologies (p = 0.002), and the own-follow-on premium is 0.26 points larger (p = 0.034).
In discrete technologies the own premium is −0.026 points (p = 0.826), so λ = 1 cannot be rejected there.

## Data

| Source | File | What it gives | Downloaded |
|---|---|---|---|
| Kogan, Papanikolaou, Seru and Stoffman, extended data (GitHub `KPSS2017/Technological-Innovation-Resource-Allocation-and-Growth-Extended-Data`, release of September 9, 2026) | `KPSS_2025.zip`, `Match_patent_permco_permno_2025.zip`, `Match_patent_cpc_2025.zip` | Private value ξ of every patent granted to a CRSP-listed firm, 1926–2025; patent-to-permco match; CPC classes | November 1, 2026 |
| PatentsView final release of December 31, 2024 (USPTO), Zenodo record 15783125, CC-BY 4.0 | `g_us_patent_citation.tsv.zip` (2.16 GB), `g_patent.tsv.zip`, `g_assignee_disambiguated.tsv.zip` | 145.9 million US patent-to-patent citations; grant dates; disambiguated assignees | November 1, 2026 |
| FRED | `CPIAUCNS.csv` (committed) | CPI-U, to restate KPSS 1982–84 dollars in 2024 dollars | November 1, 2026 |

The raw files total about 2.8 GB and are fetched by `src/build_sample.py`; checksums match the Zenodo record.

## Method

Rules fixed before estimation:

- **Sample.** Utility patents granted 2000–2014 with a KPSS value and a CRSP firm (1,238,587 patents, 4,451 firms). 2014 is the last cohort with a full ten-year citation window inside the 2024 release.
- **Follow-on.** A later US utility patent citing the patent within 3,652 days of its grant. S counts citing patents owned by the same CRSP permco; E counts all others, including unlisted and foreign owners.
- **Outcome.** log ξ, where ξ is the KPSS value in 1982–84 dollars. The KPSS estimator is

```math
\xi_j = \frac{1}{1-\bar{\pi}}\,\frac{1}{N_j}\,\mathbb{E}[v_j \mid R_j]\,M_j
```

  with R the firm's three-day market-adjusted return from the grant date, v the part of that return due to the patent, M the market capitalization on the day before grant, N the number of patents the firm received that day, and π̄ the unconditional probability that an application succeeds.

- **Estimating equation.** Counts are top-coded at their 99.9th percentiles (S at 152, E at 317).

```math
\begin{aligned}
\log \xi_i &= \beta_S S_i + \beta_E E_i + \alpha_{f(i)} + \delta_{c(i),t(i)} + \varepsilon_i \\
\lambda &= \beta_E / \beta_S, \qquad H_0^{a}: \lambda = 1, \qquad H_0^{b}: \lambda = \tfrac{1}{2}
\end{aligned}
```

  where α is a firm effect, δ a CPC-subclass by grant-year effect, and errors are clustered by firm. The two nulls are tested as linear restrictions, β_E − β_S = 0 and β_E − ½β_S = 0; the interval for λ uses the delta method.
- **Extension.** Technology groups by first-listed CPC subclass. Discrete: drugs and biotech (A61K, A61P, C07K, C12N, C12P, C12Q) and chemicals and materials (other C, B01). Complex: computing and communications (G06, H04, G09, G10L) and semiconductors and electronics (H01–H03, H05, H10, G11). Following Cohen, Nelson and Walsh (2000). The pooled test interacts S and E with a complex indicator under the same fixed effects.

The KPSS patent-to-permco match is imperfect. 24% of sample patents are not assigned to their permco's most
common PatentsView assignee; many are subsidiaries, but some are unrelated (the permco labeled Robert Bosch also
holds Stanford and BMW patents). The last robustness row uses the PatentsView assignee for S, E, the fixed effect
and the clusters; 62 patents without an assignee drop out. `results/top_firms.csv` shows the match for the 15
largest permcos. Patents with no CPC class (359) form their own class.

I first planned firm × year fixed effects as the main comparison. Because KPSS assign the same ξ to every patent a firm receives on the same day, within a firm-year ξ varies only across grant Tuesdays, and citations explain almost none of that variation (elasticity of value to total citations 0.003). I report that version but use firm plus CPC-year effects, the specification KPSS themselves use to validate ξ against citations, as the main one.

## Full test statistics

| Specification | b_S | b_E | λ | 95% CI | p (λ = 1) | p (λ = ½) |
|---|---|---|---|---|---|---|
| Main | 0.195 (0.065) | 0.035 (0.010) | 0.181 | [0.056, 0.307] | 0.010 | 0.040 |
| Dollar value, $M 1982 | 24.5 (22.7) | 8.09 (3.43) | 0.330 | [−0.106, 0.766] | 0.419 | 0.648 |
| Firm × five-year period | 0.078 (0.025) | 0.017 (0.005) | 0.225 | [0.026, 0.424] | 0.021 | 0.128 |
| Firm × year | 0.006 (0.006) | 0.012 (0.003) | 2.04 | [−2.01, 6.10] | 0.351 | 0.028 |
| CPC-year only, across firms | 2.282 (0.437) | 0.698 (0.136) | 0.306 | [0.196, 0.416] | < 0.001 | 0.016 |
| Same assignee instead of same permco | 0.179 (0.057) | 0.033 (0.012) | 0.185 | [0.047, 0.322] | 0.006 | 0.030 |
| Citations within three years | 0.542 (0.184) | 0.362 (0.073) | 0.668 | [0.112, 1.224] | 0.391 | 0.473 |
| Applicant citations only | 0.112 (0.074) | 0.002 (0.012) | 0.018 | [−0.194, 0.229] | 0.137 | 0.152 |
| Counts top-coded at 99th percentile | 0.512 (0.098) | 0.067 (0.013) | 0.131 | [0.064, 0.198] | < 0.001 | < 0.001 |
| Grants 2000–2007 | 0.264 (0.058) | 0.043 (0.011) | 0.162 | [0.047, 0.276] | < 0.001 | 0.006 |
| Grants 2008–2014 | 0.030 (0.033) | 0.013 (0.006) | 0.435 | [−0.643, 1.513] | 0.624 | 0.916 |
| Assignee for S/E, firm effects and clusters (12,995 assignees, N = 1,238,525) | 0.199 (0.053) | 0.028 (0.010) | 0.143 | [0.038, 0.248] | < 0.001 | 0.005 |

b in percent of value per citing patent; in the dollar row, thousands of 1982–84 dollars per citing patent.
Elasticities under the main fixed effects are 0.027 (0.006) for log(1 + S), 0.009 (0.002) for log(1 + E) and
0.017 (0.002) for log(1 + S + E); under firm × year effects the last is 0.003 (0.0004).

## Reproducing the results

```bash
pip install -r requirements.txt
python src/build_sample.py        # downloads about 2.8 GB on first run, then builds data/processed/
python src/division_of_profit.py  # regressions, tables and figures in results/
```

The build takes about eleven minutes on a laptop once the files are downloaded; the analysis takes about two.

## Repository layout

| Path | What it is |
|---|---|
| [src/build_sample.py](src/build_sample.py) | Joins KPSS values to PatentsView citations; counts own and outside follow-on |
| [src/division_of_profit.py](src/division_of_profit.py) | Main test, robustness, technology extension, names tables, figures |
| [results/FINDINGS.md](results/FINDINGS.md) | Plain-English summary and every table |
| [METHODS_REVIEW.md](METHODS_REVIEW.md) | Methods review of the original paper |

## References

- Chou, T. & Haller, H. (1995). The division of profit in sequential innovation reconsidered. CentER Discussion Paper 1995-64, Tilburg University.
- Cohen, W. M., Nelson, R. R. & Walsh, J. P. (2000). Protecting their intellectual assets. NBER Working Paper 7552.
- Green, J. R. & Scotchmer, S. (1995). On the division of profit in sequential innovation. *RAND Journal of Economics* 26(1): 20–33.
- Hall, B. H., Jaffe, A. & Trajtenberg, M. (2005). Market value and patent citations. *RAND Journal of Economics* 36(1): 16–38.
- Kogan, L., Papanikolaou, D., Seru, A. & Stoffman, N. (2017). Technological innovation, resource allocation, and growth. *Quarterly Journal of Economics* 132(2): 665–712.
- Scotchmer, S. (1991). Standing on the shoulders of giants. *Journal of Economic Perspectives* 5(1): 29–41.
