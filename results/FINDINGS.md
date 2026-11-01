# Green and Scotchmer (1995) on modern data: findings

## In plain English

Green and Scotchmer showed in theory that when another firm builds on an inventor's patent, the inventor keeps
only part of the profit the improvement creates, half under the even bargaining split in their model. This study
measures that share on 1,238,587 US patents granted from 2000 to 2014 to listed companies, using the stock-market
value of each patent to its owner (Kogan, Papanikolaou, Seru and Stoffman) and the later patents that cite it.

- **Pioneers gain far less from others' improvements than from their own.** One more follow-on patent by the
  owner adds about 0.20% to a patent's value; one more by another firm adds about 0.035%. The ratio, 0.18, is
  well below full capture (1) and below Green and Scotchmer's even split (0.5).
- **Most follow-on work is done by someone else.** More than 80% of the patents citing IBM's, Intel's or Microsoft's
  patents within ten years belong to other companies, led by each other and by Apple and Micron. Micron is the
  exception, with about half of the follow-on to its patents coming from Micron.
- **Drugs and chemicals pay pioneers more for outside improvements.** In drugs, biotech and chemicals an outside
  follow-on patent is worth about 0.15% to the pioneer, against about 0.04% in computing, communications and
  semiconductors, where Microsoft, Intel and IBM patent. In the drug and chemical groups the data cannot tell
  outside follow-on from own follow-on (own premium p = 0.826), which is closer to full capture than to the even split.
- **One company built on the decade's most-cited patents.** Eight of the ten patents most built on by other firms
  are 2007–2008 oxide thin-film transistor patents held by HP, Canon, Kodak and Hitachi, and more than 97% of the
  outside citations to each came from Semiconductor Energy Laboratory.

A friendlier tour is in the [README](../README.md). Method and reproduction are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels below.** *ξ (xi)*: KPSS private value of a patent, in millions of 1982–84 dollars (restated in
2024 dollars where labeled). *S*: later patents owned by the same CRSP firm (permco) citing the patent within ten
years of grant. *E*: later patents owned by anyone else citing it within ten years. *b_S, b_E*: coefficients on S
and E, shown in percent of value per citing patent for the log outcome (`log_xi`) and in thousands of 1982–84
dollars per citing patent for the dollar outcome (`xi_w`, winsorized at the 99th percentile), with firm-clustered
standard errors in parentheses. *λ*: b_E / b_S, with a delta-method interval. *FE*: fixed effects; *CPC-year* is
a four-character CPC subclass by grant year. *Own share*: S / (S + E). *Discrete* groups are drugs and biotech plus
chemicals and materials; *complex* groups are computing and communications plus semiconductors and electronics.
*Own premium*: b_S − b_E. In the last row of `main_tests.csv` the Firms column counts PatentsView assignees, which replace the permco for S, E, the firm effect and the clusters. *Under main assignee* in `top_firms.csv` is the share of a permco's patents assigned to its most common PatentsView assignee. In `by_technology.csv`, λ is not meaningful where b_S is near zero (chemicals, medical
devices). In `binned_value.csv`, *pct_vs_zero* is the percent difference in value from patents with no follow-on
of that kind, net of firm and CPC-year effects.

## Tables

### sample_counts.csv

| step | count |
|---|---|
| KPSS patents granted 2000-2014 | 1,238,587 |
| with a firm (permco) and positive value | 1,238,587 |
| PatentsView citation rows read | 145,878,465 |
| unique citations pointing at sample patents | 24,183,980 |
| citations to sample patents within ten years | 13,537,728 |
|   of which from the same firm (permco) | 2,660,440 |
|   of which from the same assignee | 2,509,358 |
| sample patents with no CPC class | 359 |

### descriptives_by_year.csv

| Grant year | Patents | Citing patents within 10 years | Own share | Median value, $M 2024 | Mean value, $M 2024 |
|---|---|---|---|---|---|
| 2000 | 60,455 | 783,965 | 16.2% | 26.55 | 108.22 |
| 2001 | 66,747 | 865,538 | 16.9% | 16.51 | 77.43 |
| 2002 | 71,965 | 868,031 | 16.3% | 8.30 | 42.32 |
| 2003 | 75,652 | 922,257 | 16.4% | 8.17 | 35.25 |
| 2004 | 76,164 | 878,366 | 15.3% | 8.01 | 27.98 |
| 2005 | 69,110 | 760,767 | 16.6% | 8.20 | 28.34 |
| 2006 | 81,524 | 890,710 | 16.9% | 7.62 | 27.08 |
| 2007 | 69,746 | 729,415 | 17.6% | 9.63 | 32.35 |
| 2008 | 71,358 | 717,943 | 20.3% | 9.13 | 36.44 |
| 2009 | 75,088 | 730,418 | 21.4% | 9.35 | 40.14 |
| 2010 | 94,984 | 981,627 | 22.7% | 7.52 | 24.61 |
| 2011 | 96,464 | 978,513 | 21.3% | 7.22 | 22.24 |
| 2012 | 101,010 | 1,057,051 | 21.2% | 7.96 | 23.05 |
| 2013 | 109,181 | 1,142,080 | 24.1% | 8.99 | 23.71 |
| 2014 | 119,139 | 1,231,047 | 26.3% | 9.97 | 24.75 |
| all | 1,238,587 | 13,537,728 | 19.7% | 8.98 | 35.48 |

### main_tests.csv

| Specification | Outcome | b_S | b_E | λ | 95% CI | p (λ=1) | p (λ=½) | N | Firms |
|---|---|---|---|---|---|---|---|---|---|
| Main: firm + CPC-year FE | log_xi | 0.195 (0.065) | 0.035 (0.010) | 0.181 | [0.056, 0.307] | 0.010 | 0.040 | 1,238,587 | 4,451 |
| Dollar value ($M 1982), firm + CPC-year FE | xi_w | 24.501 (22.748) | 8.092 (3.425) | 0.330 | [-0.106, 0.766] | 0.419 | 0.648 | 1,238,587 | 4,451 |
| Firm x five-year period + CPC-year FE | log_xi | 0.078 (0.025) | 0.017 (0.005) | 0.225 | [0.026, 0.424] | 0.021 | 0.128 | 1,238,587 | 4,451 |
| Firm x year FE | log_xi | 0.006 (0.006) | 0.012 (0.003) | 2.042 | [-2.015, 6.098] | 0.351 | 0.028 | 1,238,587 | 4,451 |
| CPC-year FE only, across firms | log_xi | 2.282 (0.437) | 0.698 (0.136) | 0.306 | [0.196, 0.416] | 0.000 | 0.016 | 1,238,587 | 4,451 |
| Same firm = same PatentsView assignee | log_xi | 0.179 (0.057) | 0.033 (0.012) | 0.185 | [0.047, 0.322] | 0.006 | 0.030 | 1,238,587 | 4,451 |
| Citations within three years | log_xi | 0.542 (0.184) | 0.362 (0.073) | 0.668 | [0.112, 1.224] | 0.391 | 0.473 | 1,238,587 | 4,451 |
| Applicant citations only | log_xi | 0.112 (0.074) | 0.002 (0.012) | 0.018 | [-0.194, 0.229] | 0.137 | 0.152 | 1,238,587 | 4,451 |
| Counts top-coded at 99th percentile | log_xi | 0.512 (0.098) | 0.067 (0.013) | 0.131 | [0.064, 0.198] | 0.000 | 0.000 | 1,238,587 | 4,451 |
| Grants 2000-2007 | log_xi | 0.264 (0.058) | 0.043 (0.011) | 0.162 | [0.047, 0.276] | 0.000 | 0.006 | 571,363 | 3,605 |
| Grants 2008-2014 | log_xi | 0.030 (0.033) | 0.013 (0.006) | 0.435 | [-0.643, 1.513] | 0.624 | 0.916 | 667,224 | 2,645 |
| Assignee throughout: own, firm FE, clusters | log_xi | 0.199 (0.053) | 0.028 (0.010) | 0.143 | [0.038, 0.248] | 0.001 | 0.005 | 1,238,525 | 12,995 |

### headline.csv

| quantity | value |
|---|---|
| median patent value, $M 2024 | 8.9781 |
| mean own follow-on patents per patent (S) | 2.1480 |
| mean outside follow-on patents per patent (E) | 8.7820 |
| share of patents with any own follow-on | 0.3619 |
| share of patents with any outside follow-on | 0.7760 |
| top-code for S (99.9th percentile) | 152.0000 |
| top-code for E (99.9th percentile) | 317.0000 |
| percent value per own follow-on patent | 0.1952 |
| percent value per outside follow-on patent | 0.0354 |
| dollars per own follow-on patent at median, $ thousand 2024 | 17.5246 |
| dollars per outside follow-on patent at median, $ thousand 2024 | 3.1796 |
| lambda | 0.1814 |
| lambda 95% CI low | 0.0558 |
| lambda 95% CI high | 0.3071 |
| p-value, lambda = 1 | 0.0097 |
| p-value, lambda = 1/2 | 0.0399 |
| share of patents not under their KPSS firm's most common assignee | 0.2410 |

### elasticities.csv

| fixed_effects | term | coef | se | n |
|---|---|---|---|---|
| firm + CPC-year | log(1+S) | 0.0272 | 0.0055 | 1,238,587 |
| firm + CPC-year | log(1+E) | 0.0086 | 0.0018 | 1,238,587 |
| firm + CPC-year | log(1+S+E) | 0.0166 | 0.0020 | 1,238,587 |
| firm x year | log(1+S+E) | 0.0030 | 0.0004 | 1,238,587 |

### by_technology.csv

| Group | Kind | Patents | Firms | Own share of follow-on | b_S | b_E | λ | 95% CI |
|---|---|---|---|---|---|---|---|---|
| Drugs and biotech | discrete | 43,319 | 1,005 | 23.6% | 0.434 (0.174) | 0.131 (0.053) | 0.301 | [-0.065, 0.666] |
| Chemicals and materials | discrete | 104,831 | 1,351 | 28.6% | 0.025 (0.093) | 0.133 (0.036) | 5.395 | [-34.739, 45.528] |
| Medical devices | other | 49,860 | 857 | 24.2% | 0.008 (0.081) | 0.009 (0.015) | 1.142 | [-21.068, 23.353] |
| Computing and communications | complex | 395,118 | 2,068 | 13.4% | 0.337 (0.118) | 0.037 (0.012) | 0.110 | [0.008, 0.213] |
| Semiconductors and electronics | complex | 240,009 | 1,258 | 22.2% | 0.228 (0.071) | 0.060 (0.018) | 0.261 | [0.015, 0.508] |
| Mechanical and other | other | 405,091 | 2,773 | 21.8% | 0.325 (0.065) | 0.045 (0.020) | 0.137 | [0.003, 0.272] |

### discrete_vs_complex.csv

| Contrast | Estimate | SE | p | N |
|---|---|---|---|---|
| b_E, discrete | 0.151 | 0.032 | 0.000 | 783,277 |
| b_E, complex | 0.043 | 0.011 | 0.000 | 783,277 |
| b_E, complex minus discrete | -0.108 | 0.034 | 0.002 | 783,277 |
| own premium b_S - b_E, discrete | -0.026 | 0.120 | 0.826 | 783,277 |
| own premium b_S - b_E, complex | 0.238 | 0.074 | 0.001 | 783,277 |
| own premium, complex minus discrete | 0.264 | 0.125 | 0.034 | 783,277 |
| lambda, discrete | 1.211 |  |  | 783,277 |
| lambda, complex | 0.154 |  |  | 783,277 |

### top_firms.csv

| Firm | Patents | Median value, $M 2024 | Citing patents per patent | Own share | Top outside citers | Under main assignee | Next assignees in the same permco |
|---|---|---|---|---|---|---|---|
| International Business Machines Corporation | 67,578 | 9.03 | 10.3 | 19.0% | Microsoft Corporation; Intel Corporation | 98.2% | Fujikura Ltd.; FUJI ELECTRIC SYSTEMS CO. LTD.; National Institute for Materials Science |
| HITACHI, LTD. | 45,679 | 0.15 | 6.6 | 9.6% | International Business Machines Corporation; Semiconductor Energy Laboratory Co., Ltd. | 38.0% | Renesas Technology Corporation; Hitachi Global Storage Technologies Netherlands B.V.; FUJI XEROX CO., LTD. |
| Sumitomo Electric Industries, Ltd. | 42,042 | 0.27 | 5.9 | 8.5% | SAMSUNG ELECTRONICS CO., LTD.; LG ELECTRONICS INC. | 34.8% | PANASONIC HOLDINGS CORPORATION; Mitsubishi Electric Corporation; NGK INSULATORS, LTD. |
| Sony Group Corporation | 40,261 | 0.65 | 6.3 | 10.8% | Apple Inc.; SAMSUNG ELECTRONICS CO., LTD. | 68.0% | ALPS ELECTRIC CO., LTD.; Sony Ericsson Mobile Communications AB; SONY COMPUTER ENTERTAINMENT INC. |
| Canon Kabushiki Kaisha | 37,015 | 0.27 | 6.3 | 36.4% | Semiconductor Energy Laboratory Co., Ltd.; Ricoh Company, Ltd. | 96.3% | Japan Display Inc.; TOKUYAMA CORPORATION; Canon Anelva Corporation |
| HONDA MOTOR CO., LTD. | 34,388 | 0.30 | 5.1 | 17.8% | Ford Global Technologies, LLC; TOYOTA JIDOSHA KABUSHIKI KAISHA | 33.4% | YAZAKI CORPORATION; OMRON Corporation; SHOWA DENKO K.K. |
| Intel Corporation | 26,860 | 23.67 | 9.4 | 15.1% | International Business Machines Corporation; Micron Technology, Inc. | 79.7% | NITTO DENKO CORPORATION; Dai Nippon Printing Co., Ltd.; Intel Mobile Communications GmbH |
| Microsoft Corporation | 24,503 | 36.81 | 16.0 | 17.7% | International Business Machines Corporation; Apple Inc. | 99.2% | SKYPE; MICROSOFT INTERNATIONAL HOLDINGS B.V.; Mircosoft Corporation |
| LG ELECTRONICS INC. | 23,418 | 0.11 | 4.4 | 18.6% | SAMSUNG ELECTRONICS CO., LTD.; Apple Inc. | 52.4% | SK hynix Inc.; LG DISPLAY CO., LTD.; LG Philips LCD Co., Ltd. |
| Hewlett-Packard Development Company, L.P. | 21,613 | 21.50 | 9.8 | 9.1% | International Business Machines Corporation; Semiconductor Energy Laboratory Co., Ltd. | 83.2% | Hewlett-Packard Company, L.P.; COMPAQ Information Technologies Group, L.P.; Hewlett-Packard Indigo B.V. |
| Micron Technology, Inc. | 21,328 | 4.70 | 10.7 | 49.2% | International Business Machines Corporation; SAMSUNG ELECTRONICS CO., LTD. | 92.2% | ELPIDA MEMORY, INC.; BTG International Limited; Micron Technologies, Inc. |
| SIEMENS AKTIENGESELLSCHAFT | 20,093 | 0.76 | 6.0 | 7.6% | General Electric Company; ALLISON TRANSMISSION, INC. | 51.3% | Siemens Medical Solutions USA, Inc.; ZF FRIEDRICHSHAFEN AG; BSH Bosch und Siemens Hausgeräte GmbH |
| General Electric Company | 20,075 | 58.59 | 8.2 | 26.1% | UNITED TECHNOLOGIES CORPORATION; SIEMENS AKTIENGESELLSCHAFT | 88.8% | GE Medical Systems Global Technology Company, LLC; GE Healthcare Bio-Science AB; GE Medical Systems Information Technologies, Inc. |
| Robert Bosch GmbH | 13,652 | 3.46 | 6.2 | 10.4% | Ford Global Technologies, LLC; Pylon Manufacturing Corporation | 73.7% | THE BOARD OF TRUSTEES OF THE LELAND STANFORD JUNIOR UNIVERSITY; Bayerische Motoren Werke Aktiengesellschaft; Parker-Hannifin Corporation |
| NEC CORPORATION | 12,348 | 0.05 | 7.7 | 2.5% | Micron Technology, Inc.; International Business Machines Corporation | 76.0% | NEC Electronics Corporation; NEC LCD Technologies, Ltd.; NEC TOKIN CORPORATION |

### most_built_on_patents.csv

| Patent | Owner | Granted | Title | Value, $M 2024 | Citing patents | Own | Outside |
|---|---|---|---|---|---|---|---|
| 7468304 | Canon Kabushiki Kaisha | 2008-12-23 | Method of fabricating oxide semiconductor device | 0.64 | 2904 | 3 | 2901 |
| 7462862 | Hewlett-Packard Development Company, L.P. | 2008-12-09 | Transistor using an isovalent semiconductor oxide as the active channel layer | 36.29 | 2891 | 0 | 2891 |
| 7453087 | Canon Kabushiki Kaisha | 2008-11-18 | Thin-film transistor and thin-film diode having amorphous-oxide semiconductor layer | 0.43 | 2872 | 7 | 2865 |
| 7411209 | Canon Kabushiki Kaisha | 2008-08-12 | Field-effect transistor and method for manufacturing the same | 0.72 | 2795 | 19 | 2776 |
| 7402506 | EASTMAN KODAK COMPANY | 2008-07-22 | Methods of making thin film transistors comprising zinc-oxide-based semiconductor materials and transistors made thereby | 4.16 | 2770 | 1 | 2769 |
| 7385224 | HITACHI, LTD. | 2008-06-10 | Thin film transistor having an etching protection film and manufacturing method thereof | 0.26 | 2688 | 0 | 2688 |
| 7297977 | Hewlett-Packard Development Company, L.P. | 2007-11-20 | Semiconductor device | 19.08 | 2498 | 1 | 2497 |
| 7282782 | Hewlett-Packard Development Company, L.P. | 2007-10-16 | Combined binary oxide semiconductor device | 26.03 | 2393 | 0 | 2393 |
| 8657177 | COVIDIEN LP | 2014-02-25 | Surgical apparatus and method for endoscopic surgery | 27.41 | 1737 | 1 | 1736 |
| 8672206 | COVIDIEN LP | 2014-03-18 | Apparatus for endoscopic procedures | 9.31 | 1656 | 1 | 1655 |

### most_built_on_citers.csv

| patent_num | citing_org | cites | share |
|---|---|---|---|
| 7282782 | Semiconductor Energy Laboratory Co., Ltd. | 2374 | 99.2% |
| 7282782 | Canon Kabushiki Kaisha | 10 | 0.4% |
| 7282782 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7297977 | Semiconductor Energy Laboratory Co., Ltd. | 2434 | 97.5% |
| 7297977 | Applied Materials, Inc. | 15 | 0.6% |
| 7297977 | Canon Kabushiki Kaisha | 14 | 0.6% |
| 7385224 | Semiconductor Energy Laboratory Co., Ltd. | 2667 | 99.2% |
| 7385224 | Arizona Board of Regents, a body corporate of the State of Arizona acting for and on behalf of | 6 | 0.2% |
| 7385224 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7402506 | Semiconductor Energy Laboratory Co., Ltd. | 2742 | 99.0% |
| 7402506 | PANASONIC HOLDINGS CORPORATION | 3 | 0.1% |
| 7402506 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7411209 | Semiconductor Energy Laboratory Co., Ltd. | 2759 | 99.4% |
| 7411209 | SAMSUNG ELECTRONICS CO., LTD. | 8 | 0.3% |
| 7411209 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7453087 | Semiconductor Energy Laboratory Co., Ltd. | 2848 | 99.4% |
| 7453087 | SAMSUNG ELECTRONICS CO., LTD. | 7 | 0.2% |
| 7453087 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7462862 | Semiconductor Energy Laboratory Co., Ltd. | 2880 | 99.6% |
| 7462862 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 7462862 | (no assignee) | 2 | 0.1% |
| 7468304 | Semiconductor Energy Laboratory Co., Ltd. | 2886 | 99.5% |
| 7468304 | NLT TECHNOLOGIES, LTD. | 3 | 0.1% |
| 7468304 | Semiconductor Energy Laboratories Co., Ltd. | 3 | 0.1% |
| 8657177 | Cilag GmbH International | 634 | 36.5% |
| 8657177 | Ethicon, Inc. | 593 | 34.2% |
| 8657177 | COVIDIEN LP | 375 | 21.6% |
| 8672206 | Ethicon, Inc. | 605 | 36.6% |
| 8672206 | Cilag GmbH International | 495 | 29.9% |
| 8672206 | COVIDIEN LP | 384 | 23.2% |

### binned_value.csv

| series | bin | pct_vs_zero | se_log | patents |
|---|---|---|---|---|
| self | 0 | 0.00 | 0.0007 | 790,288 |
| self | 1 | 1.22 | 0.0015 | 180,640 |
| self | 2 | 2.16 | 0.0022 | 83,674 |
| self | 3-4 | 2.95 | 0.0023 | 76,482 |
| self | 5-7 | 4.37 | 0.0031 | 44,891 |
| self | 8-12 | 6.13 | 0.0040 | 27,818 |
| self | 13-20 | 8.09 | 0.0053 | 15,679 |
| self | 21-33 | 9.74 | 0.0074 | 8,881 |
| self | 34+ | 11.58 | 0.0066 | 10,234 |
| ext | 0 | 0.00 | 0.0012 | 277,500 |
| ext | 1 | 0.65 | 0.0015 | 181,974 |
| ext | 2 | 0.81 | 0.0017 | 132,717 |
| ext | 3-4 | 1.08 | 0.0015 | 176,728 |
| ext | 5-7 | 1.10 | 0.0017 | 148,494 |
| ext | 8-12 | 1.62 | 0.0019 | 121,475 |
| ext | 13-20 | 2.63 | 0.0023 | 83,438 |
| ext | 21-33 | 3.75 | 0.0030 | 53,826 |
| ext | 34+ | 5.15 | 0.0028 | 62,435 |

