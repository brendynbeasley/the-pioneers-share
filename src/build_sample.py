"""Build the patent-level sample: stock-market value of each patent and who built on it.

For every US utility patent granted 2000-2014 to a firm listed on a US stock exchange, this script
joins three public sources:

    KPSS (Kogan, Papanikolaou, Seru & Stoffman 2017, data updated to 2025): the patent's private
        value to its owner, xi, estimated from the owner's stock return around the grant date,
        plus the patent-to-CRSP firm match and CPC technology classes.
    PatentsView (USPTO, final release of 12/31/2024, Zenodo mirror): every citation from one US
        patent to another, grant dates, and disambiguated assignees.

and counts, for each patent, the later patents that cite it within ten years of its grant, split
into citations from the same firm (self follow-on) and from everyone else (external follow-on).

The raw files are about 2.8 GB, so they are not committed. The script downloads any that are
missing into data/raw/ (this takes a while) and writes data/processed/patents.parquet,
data/processed/firm_names.csv, data/processed/top_external_citers.csv, results/sample_counts.csv
and results/most_built_on_citers.csv.

Usage (from the repository root):
    python src/build_sample.py
"""

import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROC = ROOT / "data" / "processed"
OUT = ROOT / "results"

KPSS_URL = ("https://raw.githubusercontent.com/KPSS2017/"
            "Technological-Innovation-Resource-Allocation-and-Growth-Extended-Data/master/")
PV_URL = "https://zenodo.org/api/records/15783125/files/{}/content"  # PatentsView 12/31/2024, CC-BY 4.0
FILES = {
    "KPSS_2025.zip": KPSS_URL + "KPSS_2025.zip",
    "Match_patent_permco_permno_2025.zip": KPSS_URL + "Match_patent_permco_permno_2025.zip",
    "Match_patent_cpc_2025.zip": KPSS_URL + "Match_patent_cpc_2025.zip",
    "g_patent.tsv.zip": PV_URL.format("g_patent.tsv.zip"),
    "g_assignee_disambiguated.tsv.zip": PV_URL.format("g_assignee_disambiguated.tsv.zip"),
    "g_us_patent_citation.tsv.zip": PV_URL.format("g_us_patent_citation.tsv.zip"),
}

FIRST_GRANT_YEAR = 2000   # first cohort; earlier grants lack the citation_category field
LAST_GRANT_YEAR = 2014    # last cohort with a full ten-year citation window inside the 2024 data
WINDOW_DAYS = 3652        # forward citations counted within ten years of the cited patent's grant
EARLY_DAYS = 1096         # a three-year window, used as a robustness check
CHUNK = 5_000_000         # rows per chunk when streaming the 146-million-row citation file


def fetch(name):
    """Return the local path of a raw file, downloading it first if it is missing."""
    path = RAW / name
    if not path.exists():
        RAW.mkdir(parents=True, exist_ok=True)
        print(f"  downloading {name} ...")
        tmp = path.with_suffix(path.suffix + ".part")
        urllib.request.urlretrieve(FILES[name], tmp)
        tmp.rename(path)
    return path


def load_kpss():
    k = pd.read_csv(fetch("KPSS_2025.zip"), usecols=["patent_num", "issue_date", "xi_real", "xi_nominal"])
    m = pd.read_csv(fetch("Match_patent_permco_permno_2025.zip"), usecols=["patent_num", "permco"])
    print(f"KPSS: {len(k):,} patents matched to listed firms, 1926-2025; firm match rows {len(m):,}")
    k = k.merge(m.drop_duplicates("patent_num"), on="patent_num", how="left")
    k["grant"] = pd.to_datetime(k.issue_date.astype(str), format="%Y%m%d")
    return k.drop(columns="issue_date")


def primary_cpc(sample_ids):
    """First-listed CPC subclass (four characters, e.g. A61K) for each sample patent."""
    c = pd.read_csv(fetch("Match_patent_cpc_2025.zip"))
    c = c[c.patent_num.isin(sample_ids)]
    c["cpc4"] = c.cpc.astype(str).str.split(";").str[0].str[:4]
    c.loc[c.cpc.isna(), "cpc4"] = np.nan
    return c.set_index("patent_num").cpc4


def load_citations(sample_ids):
    """Stream the citation file and keep only citations that point at a sample patent."""
    keep = []
    cols = ["patent_id", "citation_patent_id", "citation_category"]
    reader = pd.read_csv(fetch("g_us_patent_citation.tsv.zip"), sep="\t", usecols=cols, dtype=str,
                         chunksize=CHUNK)
    total = 0
    for chunk in reader:
        total += len(chunk)
        cited = pd.to_numeric(chunk.citation_patent_id, errors="coerce")
        citing = pd.to_numeric(chunk.patent_id, errors="coerce")
        ok = cited.isin(sample_ids) & citing.notna()
        keep.append(pd.DataFrame({"citing": citing[ok].astype("int64"), "cited": cited[ok].astype("int64"),
                                  "applicant": chunk.citation_category[ok].eq("cited by applicant")}))
        print(f"  read {total:,} citation rows", end="\r")
    cites = pd.concat(keep, ignore_index=True).drop_duplicates(["citing", "cited"])
    print(f"\nCitations: {total:,} rows read; {len(cites):,} unique citations point at sample patents")
    return cites, total


def load_grants(sample_ids):
    """Grant date of every utility patent, and the title of each sample patent."""
    g = pd.read_csv(fetch("g_patent.tsv.zip"), sep="\t", dtype=str,
                    usecols=["patent_id", "patent_type", "patent_date", "patent_title"])
    g = g[g.patent_type.eq("utility")]
    g["patent_id"] = pd.to_numeric(g.patent_id, errors="coerce")
    g = g.dropna(subset=["patent_id"]).astype({"patent_id": "int64"}).set_index("patent_id")
    print(f"PatentsView grants: {len(g):,} utility patents with dates")
    titles = g.patent_title[g.index.isin(sample_ids)]
    return pd.to_datetime(g.patent_date), titles


def load_assignees():
    a = pd.read_csv(fetch("g_assignee_disambiguated.tsv.zip"), sep="\t", dtype=str,
                    usecols=["patent_id", "assignee_sequence", "assignee_id", "disambig_assignee_organization"])
    a = a[a.assignee_sequence.eq("0")]
    a["patent_id"] = pd.to_numeric(a.patent_id, errors="coerce")
    a = a.dropna(subset=["patent_id"]).astype({"patent_id": "int64"})
    print(f"PatentsView assignees: {len(a):,} patents with a first-listed assignee")
    return a.set_index("patent_id")[["assignee_id", "disambig_assignee_organization"]]


def main():
    OUT.mkdir(exist_ok=True)
    PROC.mkdir(parents=True, exist_ok=True)
    counts = []

    k = load_kpss()
    s = k[k.grant.dt.year.between(FIRST_GRANT_YEAR, LAST_GRANT_YEAR)].copy()
    counts.append(("KPSS patents granted 2000-2014", len(s)))
    s = s[s.permco.notna() & s.xi_real.gt(0)]
    counts.append(("with a firm (permco) and positive value", len(s)))
    s["permco"] = s.permco.astype("int64")
    s["cpc4"] = s.patent_num.map(primary_cpc(set(s.patent_num)))
    print(f"Sample patents: {len(s):,} (2000-2014 grants, firm matched, xi > 0); "
          f"{s.cpc4.isna().sum():,} lack a CPC class")

    cites, total_rows = load_citations(set(s.patent_num))
    counts.append(("PatentsView citation rows read", total_rows))
    counts.append(("unique citations pointing at sample patents", len(cites)))
    dates, titles = load_grants(set(s.patent_num))
    assignee = load_assignees()
    firm_of = k.dropna(subset=["permco"]).set_index("patent_num").permco.astype("int64")

    cites["citing_date"] = cites.citing.map(dates)
    cites["cited_date"] = cites.cited.map(s.set_index("patent_num").grant)
    n0 = len(cites)
    cites = cites.dropna(subset=["citing_date"])
    lag = (cites.citing_date - cites.cited_date).dt.days
    print(f"  dropped {n0 - len(cites):,} citations from patents without a utility grant date")
    n1 = len(cites)
    cites = cites[(lag >= 0) & (lag <= WINDOW_DAYS)].copy()
    print(f"  dropped {n1 - len(cites):,} citations made before the grant or more than ten years after it")
    lag = lag.loc[cites.index]
    print(f"  kept {len(cites):,} citations made within ten years of the cited patent's grant")

    # Same firm, first definition: both patents matched to the same CRSP permco.
    cites["self_firm"] = cites.citing.map(firm_of).eq(cites.cited.map(firm_of))
    # Same firm, second definition: same PatentsView disambiguated assignee.
    a_id = assignee.assignee_id
    cites["self_asg"] = cites.citing.map(a_id).eq(cites.cited.map(a_id)) & cites.cited.map(a_id).notna()
    cites["n_early"] = lag <= EARLY_DAYS
    cites["self_early"] = cites.self_firm & cites.n_early
    cites["self_app"] = cites.self_firm & cites.applicant

    flags = cites[["cited", "self_firm", "self_asg", "self_early", "n_early", "self_app", "applicant"]]
    agg = flags.groupby("cited").sum().rename(columns={"self_firm": "self", "applicant": "n_app"})
    agg["n_cites"] = cites.groupby("cited").size()
    s = s.merge(agg, left_on="patent_num", right_index=True, how="left")
    fill = ["n_cites", "self", "self_asg", "self_early", "n_early", "self_app", "n_app"]
    s[fill] = s[fill].fillna(0).astype("int32")
    s["ext"] = s.n_cites - s.self
    s["ext_asg"] = s.n_cites - s.self_asg
    s["ext_early"] = s.n_early - s.self_early
    s["ext_app"] = s.n_app - s.self_app
    s["year"] = s.grant.dt.year.astype("int16")
    s["assignee"] = s.patent_num.map(assignee.disambig_assignee_organization)
    s["assignee_id"] = s.patent_num.map(assignee.assignee_id)
    s["title"] = s.patent_num.map(titles)

    # Who builds on whom: the outside organizations that cite each firm's patents most often.
    ext = cites[~cites.self_firm]
    ext = pd.DataFrame({"permco": ext.cited.map(firm_of).values,
                        "citing_org": ext.citing.map(assignee.disambig_assignee_organization).values})
    top = (ext.dropna().groupby(["permco", "citing_org"]).size().rename("cites").reset_index()
           .sort_values(["permco", "cites"], ascending=[True, False]).groupby("permco").head(5))
    top.to_csv(PROC / "top_external_citers.csv", index=False)

    # For the ten patents most built on by other firms, who did the building.
    most = s.nlargest(10, "ext").patent_num
    c = cites[cites.cited.isin(most) & ~cites.self_firm]
    c = pd.DataFrame({"patent_num": c.cited.values,
                      "citing_org": c.citing.map(assignee.disambig_assignee_organization).fillna("(no assignee)").values})
    c = c.groupby(["patent_num", "citing_org"]).size().rename("cites").reset_index()
    c["share"] = c.cites / c.groupby("patent_num").cites.transform("sum")
    c = c.sort_values(["patent_num", "cites"], ascending=[True, False]).groupby("patent_num").head(3)
    c.to_csv(OUT / "most_built_on_citers.csv", index=False)
    counts.append(("citations to sample patents within ten years", int(s.n_cites.sum())))
    counts.append(("  of which from the same firm (permco)", int(s.self.sum())))
    counts.append(("  of which from the same assignee", int(s.self_asg.sum())))
    counts.append(("sample patents with no CPC class", int(s.cpc4.isna().sum())))

    # A display name for each firm: its most common assignee organization in the sample.
    names = (s.dropna(subset=["assignee"]).groupby(["permco", "assignee"]).size()
             .rename("n").reset_index().sort_values(["permco", "n"], ascending=[True, False])
             .drop_duplicates("permco")[["permco", "assignee"]])
    names.to_csv(PROC / "firm_names.csv", index=False)

    s.to_parquet(PROC / "patents.parquet", index=False)
    pd.DataFrame(counts, columns=["step", "count"]).to_csv(OUT / "sample_counts.csv", index=False)
    print(f"Wrote {len(s):,} patents from {s.permco.nunique():,} firms to data/processed/patents.parquet")
    for step, n in counts:
        print(f"  {step}: {n:,}")


if __name__ == "__main__":
    main()
