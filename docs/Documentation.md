# Project: Social Network Analysis of Scientific Collaboration

This documentation covers all technical and analytical aspects of the project developed as part of the *Social Network Analysis* course. The project's focus is the analysis of scientific collaboration among staff members at the Faculty of Medicine, University of Belgrade, using methods from the field of network analysis.

---

## Dataset

**Input files (`data/`):**
- `authors.xlsx` – list of relevant authors (department employees), with Serbian column headers (`Ime`, `Prezime`, `Katedra`, `H indeks`, `Broj radova`) that the notebook maps to English
- `epidemiology.xlsx`, `immunology.xlsx`, `infectious_diseases.xlsx`, `microbiology.xlsx` – raw Scopus publication data requiring preprocessing

**Derived files:**
- `output/*.xlsx` – cleaned tables written by `co-authorship-networks.ipynb` (git-ignored)
- `magazine/data/*.xlsx` – committed snapshot of those tables, the input of `journal-networks.ipynb`
- `models/*.gml`, `models/*.net`, `magazine/models/journal-networks.gml` – saved graphs

**Columns in the .xlsx files:**
- `Author`, `Authors`, `Title`, `Year`, `Source title`, `Volume`, `Issue`, `Art. No.`, `Page start`, `Page end`, `Page count`, `Cited by`, `Link`, `Document Type`, `Source`

**Filtering criteria:**
- Only the following types of documents were included: Article, Article in Press, Review, Book Chapter, Letter, Note
- Only authors from `authors.xlsx` were included

---

## Libraries and Tools Used

- `pandas` – table/data manipulation
- `networkX` – network creation and analysis
- `matplotlib`, `seaborn` – visualization
- `scipy` – Kendall τ correlation and the dendrogram
- `scikit-learn` – spectral clustering
- `Gephi` – advanced visual analysis and Louvain community detection

---

## 🧾 Key Analyses

### Statistical Analysis
- Number of publications per author (full counting)
- Average number of co-authors
- Computation of H-index per author and comparison with given values
- Productivity analysis by year and department
- Journal publication frequency

### Network Modeling
- Construction of an undirected weighted co-authorship network
- Construction of an undirected weighted journal network: two journals are linked when the same staff author published in both (saved as `magazine/models/journal-networks.gml`)

### Network Metrics
- Network density, diameter and average path length (computed in Gephi for the report)
- Connected components
- Clustering coefficients (global and local)
- Degree assortativity
- Rich-club phenomenon analysis (comparison with Havel-Hakimi graph)
- Degree distribution (log-scale histogram) and comparison with Erdős–Rényi, G(n, m) and scale-free random graphs

### Centrality
- Degree, closeness, betweenness, eigenvector
- Construction of a composite centrality score (heuristic)
- Identification of key authors and inter-departmental brokers

### Community Detection
- **Louvain method** (via Gephi) – visualization and resolution sensitivity analysis
- **Spectral clustering** – with comparison to the Girvan–Newman algorithm
- Analysis of community validity and identification of bridges between groups

---

## Conclusions and Recommendations

- Identified key network actors can serve as candidates for strengthening scientific team connections
- The network exhibits small-world properties: one connected component, an average path length of 2.08 and clustering about three times higher than in an Erdős–Rényi graph of the same density
- Degree assortativity is close to zero and slightly negative (−0.041), so there is no assortative mixing; the rich-club coefficient stays below the Havel–Hakimi reference
- Composite centrality helps rank authors with the most significant influence

---

## Technical Details

- Originally developed with Python 3.9; now tested with Python 3.12 and the versions pinned in `requirements.txt`
- `.ipynb` files executed in Jupyter (see the README for interactive and headless execution, and `tests/` for the automated checks)
- Network visualizations performed partly in Gephi and partly in Python
- The analyzed graphs are undirected and weighted: the co-authorship network by the number of joint publications, the journal network by the number of shared staff authors

---

<p style="color:#999999;">© 2024 Lazar Davidović — School of Electrical Engineering, University of Belgrade<br/>
© 2024 Luka Simić — School of Electrical Engineering, University of Belgrade</p>
