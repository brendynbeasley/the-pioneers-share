"""How much of the follow-on value does a pioneer keep? Green & Scotchmer (1995) on 2000-2014 patents.

Green and Scotchmer show that when a second firm builds on a first firm's invention, the first firm
cannot collect all the profit the improvement creates. Under their ex ante licensing with an even
(Nash) split, it keeps its threat point plus half of the incremental surplus; when it makes the
improvement itself, it keeps all of it.

The test: regress the log stock-market value of each patent to its owner (KPSS xi) on the number
of later patents that build on it, split into the owner's own follow-on patents (S) and other
firms' follow-on patents (E), comparing patents of the same firm, and patents in the same CPC
subclass granted in the same year:

    log xi_i = b_S * S_i + b_E * E_i + a_firm + d_(CPC x year) + e_i,      lambda = b_E / b_S

lambda is the value the pioneer gets from an outside follow-on invention as a fraction of what it
gets from one of its own. Green-Scotchmer predict lambda < 1, and 1/2 under their symmetric split.

The extension repeats the estimate by technology, where patent breadth and the habit of licensing
differ (Cohen, Nelson & Walsh's "discrete" and "complex" product industries).

Run src/build_sample.py first. Usage (from the repository root):
    python src/division_of_profit.py
"""

import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyhdfe
from linearmodels.iv.absorbing import AbsorbingLS
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
OUT = ROOT / "results"

WINSOR_XI = 0.99        # value winsorized at the 99th percentile (KPSS values are heavily right-skewed)
WINSOR_CITES = 0.999    # citation counts top-coded at the 99.9th percentile of each count
NASH_SHARE = 0.5        # Green-Scotchmer's even split of the incremental surplus
TOP_FIRMS = 15          # firms in the names table, ranked by number of sample patents
CPI_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS"  # CPI-U, 1982-84 = 100
CPI_YEAR = 2024         # KPSS real values (1982-84 dollars) are restated in 2024 dollars

# Technology groups by first-listed CPC subclass. "Discrete" and "complex" follow Cohen, Nelson &
# Walsh (2000): chemicals and drugs versus telecommunications, computing and semiconductors.
TECH_GROUPS = [
    ("Drugs and biotech", "discrete", ("A61K", "A61P", "C07K", "C12N", "C12P", "C12Q")),
    ("Chemicals and materials", "discrete", ("C0", "C1", "C2", "C3", "C4", "B01")),
    ("Medical devices", "other", ("A61B", "A61F", "A61M", "A61N", "A61L")),
    ("Computing and communications", "complex", ("G06", "H04", "G09", "G10L")),
    ("Semiconductors and electronics", "complex", ("H01", "H02", "H03", "H05", "H10", "G11")),
]


def tech_group(cpc4):
    if not isinstance(cpc4, str):
        return "No CPC class"
    for name, _, prefixes in TECH_GROUPS:
        if cpc4.startswith(prefixes):
            return name
    return "Mechanical and other"


def cpi_2024():
    path = RAW / "CPIAUCNS.csv"
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(CPI_URL, path)
    c = pd.read_csv(path)
    c["year"] = pd.to_datetime(c.iloc[:, 0]).dt.year
    return c[c.year.eq(CPI_YEAR)].iloc[:, 1].astype(float).mean()


def load():
    p = pd.read_parquet(PROC / "patents.parquet")
    print(f"Loaded {len(p):,} patents, {p.permco.nunique():,} firms, granted {p.year.min()}-{p.year.max()}")
    p["fy"] = p.permco.astype(str) + "_" + p.year.astype(str)
    p["f5"] = p.permco.astype(str) + "_" + (p.year // 5).astype(str)
    p["xi_w"] = p.xi_real.clip(upper=p.xi_real.quantile(WINSOR_XI))
    p["log_xi"] = np.log(p.xi_real)
    for c in ["self", "ext", "self_asg", "ext_asg", "self_early", "ext_early", "self_app", "ext_app"]:
        p[c + "_w"] = p[c].clip(upper=p[c].quantile(WINSOR_CITES))
    p["self_w99"] = p.self.clip(upper=p.self.quantile(0.99))
    p["ext_w99"] = p.ext.clip(upper=p.ext.quantile(0.99))
    p["tech"] = p.cpc4.map(tech_group)
    p["cpc_year"] = p.cpc4.fillna("none") + "_" + p.year.astype(str)
    return p


MAIN_FE = ("permco", "cpc_year")


def estimate(p, y, s, e, absorb=MAIN_FE, label="", cluster="permco"):
    """Regression of y on S and E with absorbed fixed effects; returns b_S, b_E, lambda and tests."""
    d = p[list(dict.fromkeys([y, s, e, "permco", cluster, *absorb]))].dropna()
    if len(d) < len(p):
        print(f"  ({label}: dropped {len(p) - len(d):,} patents with a missing variable)")
    fe = pd.DataFrame({a: pd.Categorical(d[a]) for a in absorb}, index=d.index)
    clusters = pd.Series(pd.factorize(d[cluster])[0], index=d.index)
    res = AbsorbingLS(d[y], d[[s, e]], absorb=fe).fit(cov_type="clustered", clusters=clusters)
    b, v = res.params, res.cov
    lam = b[e] / b[s]
    grad = np.array([-b[e] / b[s] ** 2, 1 / b[s]])  # delta method for b_E / b_S
    se_lam = float(np.sqrt(grad @ v.loc[[s, e], [s, e]].values @ grad))
    out = {"spec": label, "outcome": y, "b_self": b[s], "se_self": res.std_errors[s],
           "b_ext": b[e], "se_ext": res.std_errors[e], "lambda": lam, "se_lambda": se_lam,
           "lam_lo": lam - 1.96 * se_lam, "lam_hi": lam + 1.96 * se_lam,
           "n": int(res.nobs), "firms": d[cluster].nunique()}
    for name, c in (("p_equal", 1.0), ("p_half", NASH_SHARE)):  # H0: b_E = c * b_S
        g = np.array([-c, 1.0])
        t = (b[e] - c * b[s]) / np.sqrt(g @ v.loc[[s, e], [s, e]].values @ g)
        out[name] = 2 * stats.norm.sf(abs(t))
    print(f"  {label:<46} b_S={b[s]:.4f} ({res.std_errors[s]:.4f})  b_E={b[e]:.4f} "
          f"({res.std_errors[e]:.4f})  lambda={lam:.3f} [{out['lam_lo']:.3f}, {out['lam_hi']:.3f}]  N={out['n']:,}")
    return out


def descriptives(p, cpi):
    rows = []
    for yr, d in p.groupby("year"):
        rows.append({"year": yr, "patents": len(d), "cites_10yr": int(d.n_cites.sum()),
                     "self_share": d.self.sum() / d.n_cites.sum(),
                     "median_value_2024usd_m": d.xi_real.median() * cpi / 100,
                     "mean_value_2024usd_m": d.xi_real.mean() * cpi / 100})
    t = pd.DataFrame(rows)
    tot = {"year": "all", "patents": len(p), "cites_10yr": int(p.n_cites.sum()),
           "self_share": p.self.sum() / p.n_cites.sum(),
           "median_value_2024usd_m": p.xi_real.median() * cpi / 100,
           "mean_value_2024usd_m": p.xi_real.mean() * cpi / 100}
    t = pd.concat([t, pd.DataFrame([tot])], ignore_index=True)
    t.to_csv(OUT / "descriptives_by_year.csv", index=False)
    print(f"  self share of ten-year citations {tot['self_share']:.3f}; median value ${tot['median_value_2024usd_m']:.2f}M")
    return t


def main_tests(p):
    print("Main test: log value on own and outside follow-on")
    y = "log_xi"
    specs = [
        estimate(p, y, "self_w", "ext_w", label="Main: firm + CPC-year FE"),
        estimate(p, "xi_w", "self_w", "ext_w", label="Dollar value ($M 1982), firm + CPC-year FE"),
        estimate(p, y, "self_w", "ext_w", absorb=("f5", "cpc_year"), label="Firm x five-year period + CPC-year FE"),
        estimate(p, y, "self_w", "ext_w", absorb=("fy",), label="Firm x year FE"),
        estimate(p, y, "self_w", "ext_w", absorb=("cpc_year",), label="CPC-year FE only, across firms"),
        estimate(p, y, "self_asg_w", "ext_asg_w", label="Same firm = same PatentsView assignee"),
        estimate(p, y, "self_early_w", "ext_early_w", label="Citations within three years"),
        estimate(p, y, "self_app_w", "ext_app_w", label="Applicant citations only"),
        estimate(p, y, "self_w99", "ext_w99", label="Counts top-coded at 99th percentile"),
        estimate(p[p.year <= 2007], y, "self_w", "ext_w", label="Grants 2000-2007"),
        estimate(p[p.year >= 2008], y, "self_w", "ext_w", label="Grants 2008-2014"),
        estimate(p, y, "self_asg_w", "ext_asg_w", absorb=("assignee_id", "cpc_year"), cluster="assignee_id",
                 label="Assignee throughout: own, firm FE, clusters"),
    ]
    t = pd.DataFrame(specs)
    t.to_csv(OUT / "main_tests.csv", index=False)
    return t


def off_main_assignee(p):
    """Share of patents whose PatentsView assignee differs from the most common assignee of their KPSS firm.
    Subsidiaries count as different, so this is an upper bound on mismatched patents."""
    main = p.dropna(subset=["assignee"]).groupby("permco").assignee.agg(lambda s: s.value_counts().index[0])
    return p.assignee.ne(p.permco.map(main)).mean()


def headline(p, tests, cpi):
    """Translate the main estimate into dollars at the median patent."""
    m = tests.iloc[0]
    med = p.xi_real.median() * cpi / 100
    rows = [
        ("median patent value, $M 2024", med),
        ("mean own follow-on patents per patent (S)", p.self.mean()),
        ("mean outside follow-on patents per patent (E)", p.ext.mean()),
        ("share of patents with any own follow-on", p.self.gt(0).mean()),
        ("share of patents with any outside follow-on", p.ext.gt(0).mean()),
        ("top-code for S (99.9th percentile)", p.self.quantile(WINSOR_CITES)),
        ("top-code for E (99.9th percentile)", p.ext.quantile(WINSOR_CITES)),
        ("percent value per own follow-on patent", 100 * m.b_self),
        ("percent value per outside follow-on patent", 100 * m.b_ext),
        ("dollars per own follow-on patent at median, $ thousand 2024", 1000 * med * m.b_self),
        ("dollars per outside follow-on patent at median, $ thousand 2024", 1000 * med * m.b_ext),
        ("lambda", m["lambda"]),
        ("lambda 95% CI low", m.lam_lo),
        ("lambda 95% CI high", m.lam_hi),
        ("p-value, lambda = 1", m.p_equal),
        ("p-value, lambda = 1/2", m.p_half),
        ("share of patents not under their KPSS firm's most common assignee", off_main_assignee(p)),
    ]
    pd.DataFrame(rows, columns=["quantity", "value"]).to_csv(OUT / "headline.csv", index=False)


def elasticity(p):
    """Elasticities in logs of counts (the KPSS-style form), under several sets of fixed effects."""
    p = p.assign(ls=np.log1p(p.self), le=np.log1p(p.ext), ln=np.log1p(p.n_cites))
    rows = []
    for fe_name, absorb, X in (("firm + CPC-year", MAIN_FE, ["ls", "le"]),
                               ("firm + CPC-year", MAIN_FE, ["ln"]),
                               ("firm x year", ("fy",), ["ln"])):
        d = p[list(dict.fromkeys(["log_xi", *X, "permco", *absorb]))]
        fe = pd.DataFrame({a: pd.Categorical(d[a]) for a in absorb}, index=d.index)
        r = AbsorbingLS(d.log_xi, d[X], absorb=fe).fit(cov_type="clustered", clusters=d.permco)
        for x in X:
            rows.append({"fixed_effects": fe_name, "term": {"ls": "log(1+S)", "le": "log(1+E)", "ln": "log(1+S+E)"}[x],
                         "coef": r.params[x], "se": r.std_errors[x], "n": int(r.nobs)})
            print(f"  {fe_name:<16} {rows[-1]['term']:<11} {r.params[x]:.4f} ({r.std_errors[x]:.4f})")
    pd.DataFrame(rows).to_csv(OUT / "elasticities.csv", index=False)


def by_technology(p):
    print("Extension: lambda by technology group")
    rows = []
    for name in [g[0] for g in TECH_GROUPS] + ["Mechanical and other"]:
        d = p[p.tech.eq(name)]
        r = estimate(d, "log_xi", "self_w", "ext_w", label=name)
        r["group"] = name
        r["kind"] = {g[0]: g[1] for g in TECH_GROUPS}.get(name, "other")
        r["self_share"] = d.self.sum() / d.n_cites.sum()
        r["patents"] = len(d)
        rows.append(r)
    # Pooled discrete vs complex groups in one interacted regression, compared by linear contrasts.
    kind = p.tech.map({g[0]: g[1] for g in TECH_GROUPS}).fillna("other")
    d = p[kind.isin(["discrete", "complex"])].copy()
    d["cx"] = kind[d.index].eq("complex").astype(float)
    d["s_c"], d["e_c"] = d.self_w * d.cx, d.ext_w * d.cx
    fe = pd.DataFrame({a: pd.Categorical(d[a]) for a in MAIN_FE}, index=d.index)
    X = d[["self_w", "ext_w", "s_c", "e_c"]]
    r = AbsorbingLS(d.log_xi, X, absorb=fe).fit(cov_type="clustered", clusters=d.permco)
    b, v = r.params.values, r.cov.values
    contrasts = {  # weights on (b_S, b_E, extra b_S if complex, extra b_E if complex)
        "b_E, discrete": [0, 1, 0, 0],
        "b_E, complex": [0, 1, 0, 1],
        "b_E, complex minus discrete": [0, 0, 0, 1],
        "own premium b_S - b_E, discrete": [1, -1, 0, 0],
        "own premium b_S - b_E, complex": [1, -1, 1, -1],
        "own premium, complex minus discrete": [0, 0, 1, -1],
    }
    pooled = []
    for name, w in contrasts.items():
        w = np.array(w, dtype=float)
        est, se = w @ b, float(np.sqrt(w @ v @ w))
        pooled.append({"contrast": name, "estimate": est, "se": se, "lo": est - 1.96 * se, "hi": est + 1.96 * se,
                       "p": 2 * stats.norm.sf(abs(est / se)), "n": int(r.nobs)})
    pooled.append({"contrast": "lambda, discrete", "estimate": b[1] / b[0], "n": int(r.nobs)})
    pooled.append({"contrast": "lambda, complex", "estimate": (b[1] + b[3]) / (b[0] + b[2]), "n": int(r.nobs)})
    pooled = pd.DataFrame(pooled)
    pooled.to_csv(OUT / "discrete_vs_complex.csv", index=False)
    for _, row in pooled.iterrows():
        print(f"  {row.contrast:<40} {row.estimate:.4f}" + (f" ({row.se:.4f}) p={row.p:.3f}" if row.notna().se else ""))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "by_technology.csv", index=False)
    return t


def names_table(p, cpi):
    names = pd.read_csv(PROC / "firm_names.csv").set_index("permco").assignee
    citers = pd.read_csv(PROC / "top_external_citers.csv")
    top = p.permco.value_counts().head(TOP_FIRMS).index
    rows = []
    for f in top:
        d = p[p.permco.eq(f)]
        c = citers[citers.permco.eq(f)]
        c = c[c.citing_org.ne(names.get(f))].head(2)
        orgs = d.assignee.value_counts()
        rows.append({"permco": f, "firm": names.get(f, str(f)), "patents": len(d),
                     "median_value_2024usd_m": d.xi_real.median() * cpi / 100,
                     "cites_per_patent": d.n_cites.mean(), "self_share": d.self.sum() / d.n_cites.sum(),
                     "top_outside_citers": "; ".join(c.citing_org),
                     "share_under_main_assignee": orgs.iloc[0] / len(d),
                     "next_assignees": "; ".join(orgs.index[1:4])})
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "top_firms.csv", index=False)
    best = p.sort_values("ext", ascending=False).head(10)
    best = best.assign(firm=best.permco.map(names), value_2024usd_m=best.xi_real * cpi / 100,
                       grant_date=best.grant.dt.date)
    best[["patent_num", "firm", "grant_date", "title", "xi_real", "value_2024usd_m", "n_cites", "self",
          "ext"]].to_csv(
        OUT / "most_built_on_patents.csv", index=False)
    return t


def figures(p, tech, cpi):
    # Figure 1: log value net of firm and CPC-year effects, by bins of own and outside follow-on.
    d = p.copy()
    ids = np.column_stack([pd.factorize(d[a])[0] for a in MAIN_FE])
    d["resid"] = pyhdfe.create(ids, drop_singletons=False).residualize(d[["log_xi"]].values)[:, 0]
    bins = [0, 1, 2, 3, 5, 8, 13, 21, 34, 1e9]
    labels = ["0", "1", "2", "3-4", "5-7", "8-12", "13-20", "21-33", "34+"]
    fig, ax = plt.subplots(figsize=(8, 4.6))
    rows = []
    for col, name, color in (("self", "Own follow-on patents (S)", "#1f5f8b"),
                             ("ext", "Other firms' follow-on patents (E)", "#c4622d")):
        cut = pd.cut(d[col], bins=bins, right=False, labels=labels)
        m = d.groupby(cut, observed=True).resid.agg(["mean", "sem", "size"])
        m["mean"] -= m["mean"].iloc[0]  # relative to patents with no follow-on of that kind
        m["pct"] = 100 * np.expm1(m["mean"])
        ax.errorbar(range(len(m)), m["pct"], yerr=196 * m["sem"], marker="o",
                    capsize=3, color=color, label=name)
        rows += [{"series": col, "bin": b, "log_points_vs_zero": r["mean"], "pct_vs_zero": r["pct"],
                  "se_log": r["sem"], "patents": int(r["size"])} for b, r in m.iterrows()]
    pd.DataFrame(rows).to_csv(OUT / "binned_value.csv", index=False)
    ax.set_xticks(range(len(labels)), labels)
    ax.set_xlabel("Later patents citing it within ten years")
    ax.set_ylabel("Value to owner, % above patents\nwith none (firm and class-year adjusted)")
    ax.set_title("A patent is worth more to its owner when the owner builds on it")
    ax.legend(frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "value_by_follow_on.png", dpi=150)
    plt.close(fig)

    # Figure 2: value per own and per outside follow-on patent, by technology group.
    t = tech.sort_values("b_self")
    fig, ax = plt.subplots(figsize=(8, 4.4))
    y = np.arange(len(t))
    for col, se, off, name, color in (("b_self", "se_self", 0.15, "Own follow-on patent", "#1f5f8b"),
                                      ("b_ext", "se_ext", -0.15, "Other firm's follow-on patent", "#c4622d")):
        ax.errorbar(100 * t[col], y + off, xerr=196 * t[se], fmt="o", capsize=3, color=color, label=name)
    ax.axvline(0, color="#444444", lw=0.8)
    ax.set_yticks(y, t.group)
    ax.set_xlabel("Percent added to the patent's value per citing patent (95% interval)")
    ax.set_title("What one more follow-on patent is worth to the pioneer")
    ax.legend(frameon=False, loc="lower right")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(OUT / "follow_on_value_by_technology.png", dpi=150)
    plt.close(fig)


def main():
    OUT.mkdir(exist_ok=True)
    cpi = cpi_2024()
    print(f"CPI-U {CPI_YEAR} annual average: {cpi:.3f} (1982-84 = 100)")
    p = load()
    descriptives(p, cpi)
    tests = main_tests(p)
    headline(p, tests, cpi)
    elasticity(p)
    tech = by_technology(p)
    names_table(p, cpi)
    figures(p, tech, cpi)
    print("Wrote results/*.csv and results/*.png")


if __name__ == "__main__":
    main()
