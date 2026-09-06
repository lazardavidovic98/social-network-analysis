"""Render the figures used in README.md from the results committed in this repository.

Inputs (all produced by the notebooks):
  models/network_one.gml              co-authorship network
  models/spectral_clustering.net      spectral clustering partition (3 clusters)
  magazine/data/authors_data.xlsx     staff list with departments
  magazine/data/authors_and_works.xlsx  staff member x publication table

Output: docs/figures/<name>-light.png and <name>-dark.png

Run from the repository root:  python scripts/make_readme_figures.py
"""
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "figures"

DEPARTMENTS = {
    "Katedra za epidemiologiju": "Epidemiology",
    "Katedra za mikrobiologiju": "Microbiology",
    "Infektivne bolesti": "Infectious Diseases",
    "Katedra za imunologiju": "Immunology",
}
DEPARTMENT_ORDER = ["Epidemiology", "Microbiology", "Infectious Diseases", "Immunology"]

# Categorical slots in fixed order (validated for adjacent pairs in both modes)
CATEGORICAL = ["#00876A", "#7B4FA0", "#C9773A", "#4E86C6"]
HIGHLIGHT = "#7B4FA0"  # single-hue highlight (purple family of #512D6D)
BAR = "#00876A"        # single-series bars (green family of #006B54)

THEMES = {
    "light": dict(bg="#FFFFFF", ink="#1F2328", muted="#59636E", grid="#E6E0F0",
                  node="#C9CDD2", edge="#AEB4BB", ref="#8C959F"),
    "dark": dict(bg="#0D1117", ink="#E6EDF3", muted="#9198A1", grid="#262C36",
                 node="#3D444D", edge="#4A525C", ref="#7D8590"),
}


def load():
    G = nx.read_gml(ROOT / "models" / "network_one.gml")
    staff = pd.read_excel(ROOT / "magazine" / "data" / "authors_data.xlsx")
    department = {r["Kratko ime"]: DEPARTMENTS[r["Katedra"]] for _, r in staff.iterrows()}
    partition = nx.read_pajek(ROOT / "models" / "spectral_clustering.net")
    cluster = {n: int(d["color"]) for n, d in partition.nodes(data=True)}
    works = pd.read_excel(ROOT / "magazine" / "data" / "authors_and_works.xlsx")
    works["Department"] = works["Katedra"].map(DEPARTMENTS)
    return G, department, cluster, works


def style(ax, t, grid_axis="y"):
    ax.set_facecolor(t["bg"])
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(t["grid"])
    ax.tick_params(colors=t["muted"], labelsize=8.5, length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=t["grid"], linewidth=0.8)
        ax.set_axisbelow(True)
    ax.xaxis.label.set_color(t["muted"])
    ax.yaxis.label.set_color(t["muted"])


def figure(t, w, h):
    fig = plt.figure(figsize=(w, h), dpi=200)
    fig.patch.set_facecolor(t["bg"])
    return fig


def save(fig, name, mode):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / f"{name}-{mode}.png", facecolor=fig.get_facecolor())
    plt.close(fig)


def draw_edges(ax, G, pos, t):
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=t["edge"], alpha=0.45,
                           width=[0.4 + 0.12 * min(w, 10) for _, _, w in G.edges(data="weight")])


def network_by_department(G, department, pos, t, mode):
    fig = figure(t, 8.3, 7.6)
    degree = dict(G.degree())
    for i, dep in enumerate(DEPARTMENT_ORDER):
        ax = fig.add_subplot(2, 2, i + 1)
        ax.set_facecolor(t["bg"])
        ax.axis("off")
        members = [n for n in G if department[n] == dep]
        others = [n for n in G if department[n] != dep]
        draw_edges(ax, G, pos, t)
        nx.draw_networkx_nodes(G, pos, nodelist=others, ax=ax, node_color=t["node"],
                               node_size=[14 + 3 * degree[n] for n in others], linewidths=0)
        nx.draw_networkx_nodes(G, pos, nodelist=members, ax=ax, node_color=HIGHLIGHT,
                               node_size=[20 + 6 * degree[n] for n in members],
                               edgecolors=t["bg"], linewidths=1.2)
        top = sorted(members, key=lambda n: -degree[n])[:2]
        for n in top:
            x, y = pos[n]
            ax.annotate(n, (x, y), xytext=(0, 10), textcoords="offset points", ha="center",
                        fontsize=7.5, color=t["ink"],
                        path_effects=[pe.withStroke(linewidth=2.5, foreground=t["bg"])])
        ax.set_title(f"{dep}  ·  {len(members)} staff in the network", fontsize=9.5,
                     color=t["ink"], loc="left")
    fig.suptitle("Where each department sits in the co-authorship network", x=0.02, ha="left",
                 fontsize=12, color=t["ink"], fontweight="bold")
    fig.text(0.02, 0.925, "Node size = degree (number of distinct co-authors among the staff). "
             "Labels: two best-connected members per department.", fontsize=8.5, color=t["muted"])
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.88, wspace=0.05, hspace=0.12)
    save(fig, "network-departments", mode)


def network_by_cluster(G, department, cluster, pos, t, mode):
    fig = figure(t, 8.3, 5.2)
    ax = fig.add_axes([0.0, 0.0, 0.66, 0.86])
    ax.set_facecolor(t["bg"])
    ax.axis("off")
    degree = dict(G.degree())
    draw_edges(ax, G, pos, t)
    shapes = ["o", "s", "^"]
    colors = CATEGORICAL[:3]
    for c in range(3):
        nodes = [n for n in G if cluster[n] == c]
        nx.draw_networkx_nodes(G, pos, nodelist=nodes, ax=ax, node_color=colors[c],
                               node_shape=shapes[c], node_size=[24 + 6 * degree[n] for n in nodes],
                               edgecolors=t["bg"], linewidths=1.2, label=f"Cluster {c + 1}")

    # Composition table: which departments end up in which cluster
    tab = fig.add_axes([0.67, 0.12, 0.31, 0.62])
    tab.axis("off")
    counts = Counter((cluster[n], department[n]) for n in G)
    y = 1.0
    tab.text(0.0, y, "Members per cluster", fontsize=9.5, color=t["ink"], fontweight="bold",
             transform=tab.transAxes)
    for c in range(3):
        y -= 0.13
        tab.scatter([0.03], [y + 0.012], marker=shapes[c], s=46, color=colors[c],
                    transform=tab.transAxes, clip_on=False)
        size = sum(v for (cc, _), v in counts.items() if cc == c)
        tab.text(0.09, y, f"Cluster {c + 1}  ({size})", fontsize=9, color=t["ink"],
                 transform=tab.transAxes)
        for dep in DEPARTMENT_ORDER:
            if counts[(c, dep)]:
                y -= 0.075
                tab.text(0.09, y, f"{counts[(c, dep)]:>2}  {dep}", fontsize=8.5, color=t["muted"],
                         transform=tab.transAxes, family="monospace")
    fig.suptitle("Spectral clustering (k = 3) of the co-authorship network", x=0.02, ha="left",
                 fontsize=12, color=t["ink"], fontweight="bold")
    fig.text(0.02, 0.9, "Clusters found from co-authorship alone, compared with official departments.",
             fontsize=8.5, color=t["muted"])
    save(fig, "spectral-clusters", mode)


def publications_per_year(works, t, mode):
    fig = figure(t, 8.3, 4.2)
    ax = fig.add_axes([0.07, 0.13, 0.74, 0.68])
    style(ax, t)
    counts = works.groupby(["Year", "Department"]).size().unstack(fill_value=0)
    earlier = int(counts.loc[counts.index < 1996].to_numpy().sum())
    first_year = int(counts.index.min())
    counts = counts.loc[counts.index >= 1996]  # earlier years have only a handful of records
    for i, dep in enumerate(DEPARTMENT_ORDER):
        s = counts[dep]
        ax.plot(s.index, s.values, color=CATEGORICAL[i], linewidth=2, solid_capstyle="round")
        ax.annotate(dep, (s.index[-1], s.values[-1]), xytext=(6, 0), textcoords="offset points",
                    va="center", fontsize=8.5, color=t["ink"])
    # Keep the end labels apart when two series finish close together
    ax.set_xlim(counts.index.min(), counts.index.max())
    ax.set_ylim(0, None)
    ax.set_ylabel("Publications (counted once per staff author)", fontsize=8.5)
    fig.suptitle("Publication output by department and year", x=0.07, ha="left", fontsize=12,
                 color=t["ink"], fontweight="bold")
    fig.text(0.07, 0.86, f"Scopus exports after filtering and deduplication. Not shown: {earlier} "
             f"records from {first_year}–1995.", fontsize=8.5, color=t["muted"])
    save(fig, "publications-per-year", mode)


def top_degree(G, t, mode):
    dc = nx.degree_centrality(G)
    top = sorted(dc.items(), key=lambda kv: kv[1], reverse=True)[:10][::-1]
    fig = figure(t, 8.3, 3.9)
    ax = fig.add_axes([0.2, 0.12, 0.72, 0.76])
    style(ax, t, grid_axis="x")
    names = [n for n, _ in top]
    vals = [v for _, v in top]
    ax.barh(names, vals, color=BAR, height=0.62)
    for i, v in enumerate(vals):
        ax.text(v + 0.006, i, f"{v:.2f}", va="center", fontsize=8, color=t["muted"])
    ax.tick_params(axis="y", colors=t["ink"], labelsize=8.5)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_xlabel("Degree centrality (share of the other 57 staff members co-authored with)",
                  fontsize=8.5)
    fig.suptitle("Ten best-connected staff members", x=0.02, ha="left", fontsize=12,
                 color=t["ink"], fontweight="bold")
    save(fig, "top-degree-centrality", mode)


def reference_models(G, t, mode):
    n, m = G.number_of_nodes(), G.number_of_edges()
    p = 2 * m / (n * (n - 1))
    er = nx.erdos_renyi_graph(n, p, seed=42)  # same call and seed as the notebook
    _, deg_list = zip(*G.degree())
    hh = nx.havel_hakimi_graph(deg_list)
    rc = nx.rich_club_coefficient(G, normalized=False)
    rc_hh = nx.rich_club_coefficient(hh, normalized=False)

    fig = figure(t, 8.3, 3.9)
    ax1 = fig.add_axes([0.07, 0.15, 0.40, 0.62])
    ax2 = fig.add_axes([0.57, 0.15, 0.40, 0.62])
    for ax in (ax1, ax2):
        style(ax, t)

    real = Counter(d for _, d in G.degree())
    rand = Counter(d for _, d in er.degree())
    xs = range(0, max(max(real), max(rand)) + 1)
    ax1.plot(xs, [rand.get(x, 0) for x in xs], color=t["ref"], linewidth=1.6, linestyle=(0, (4, 3)))
    ax1.plot(xs, [real.get(x, 0) for x in xs], color=HIGHLIGHT, linewidth=2)
    ax1.set_xlabel("Degree", fontsize=8.5)
    ax1.set_ylabel("Number of staff members", fontsize=8.5)
    ax1.set_title("Degree distribution", fontsize=9.5, color=t["ink"], loc="left")

    ks = sorted(rc)
    ax2.plot(ks, [rc_hh[k] for k in ks], color=t["ref"], linewidth=1.6, linestyle=(0, (4, 3)))
    ax2.plot(ks, [rc[k] for k in ks], color=HIGHLIGHT, linewidth=2)
    ax2.set_xlabel("Degree threshold k", fontsize=8.5)
    ax2.set_ylabel("Rich-club coefficient", fontsize=8.5)
    ax2.set_title("Rich-club coefficient", fontsize=9.5, color=t["ink"], loc="left")
    ax2.set_ylim(0, 1.05)

    from matplotlib.lines import Line2D
    handles = [Line2D([], [], color=HIGHLIGHT, linewidth=2, label="Co-authorship network"),
               Line2D([], [], color=t["ref"], linewidth=1.6, linestyle=(0, (4, 3)),
                      label="Reference: Erdős–Rényi (left) · Havel–Hakimi, same degrees (right)")]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.06, 0.92), ncol=2, frameon=False,
               fontsize=8.5, labelcolor=t["ink"])
    fig.suptitle("The network compared with random reference graphs", x=0.07, ha="left", fontsize=12,
                 color=t["ink"], fontweight="bold")
    save(fig, "reference-models", mode)


def main():
    G, department, cluster, works = load()
    pos = nx.spring_layout(G, seed=7, k=0.42, iterations=300)  # fixed seed: same layout every run
    for mode, t in THEMES.items():
        plt.rcParams["font.family"] = "DejaVu Sans"
        network_by_department(G, department, pos, t, mode)
        network_by_cluster(G, department, cluster, pos, t, mode)
        publications_per_year(works, t, mode)
        top_degree(G, t, mode)
        reference_models(G, t, mode)
    print(f"Figures written to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
