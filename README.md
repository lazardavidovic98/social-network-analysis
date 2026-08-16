# 📊 Scientific Collaboration Network – Faculty of Medicine, University of Belgrade

This project presents a comprehensive analysis of scientific output and collaboration among staff members from four departments of the Faculty of Medicine, University of Belgrade: **Immunology, Epidemiology, Infectious Diseases, and Microbiology**. The project was completed as part of the *Social Network Analysis* course at the School of Electrical Engineering, University of Belgrade.

The goal of the analysis is to model and analyze **co-authorship networks** and **journal networks** through graph metrics, centrality measures, community detection, and visualization, using real-world data collected from the **Scopus database** and institutional sources.

## Project Overview

The project includes the following steps:
- Cleaning and merging raw data from multiple Excel files (`epidemiology.xlsx`, `immunology.xlsx`, etc.)
- Filtering authors based on the official staff list (`authors.xlsx`)
- Constructing co-authorship and journal graphs using `NetworkX`
- Analyzing centrality (degree, closeness, eigenvector, betweenness)
- Community detection (Louvain method, spectral clustering)
- Comparing with random networks and measuring characteristics such as density, clustering, assortativity, etc.
- Visualizing networks and interpreting the results

## Project Structure


<!-- project-tree:start -->
<p>
<a href="https://github.com/LazarDavidovic98/social-network-analysis" title="social-network-analysis"><img src=".github/readme-tree/00.svg" alt="social-network-analysis" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/co-authorship-networks.ipynb" title="co-authorship-networks.ipynb"><img src=".github/readme-tree/01.svg" alt="co-authorship-networks.ipynb — co-authorship graph: centrality, communities" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/journal-networks.ipynb" title="journal-networks.ipynb"><img src=".github/readme-tree/02.svg" alt="journal-networks.ipynb — journal network analysis" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/data" title="data/"><img src=".github/readme-tree/03.svg" alt="data/ — Scopus exports per department" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/data/authors.xlsx" title="data/authors.xlsx"><img src=".github/readme-tree/04.svg" alt="data/authors.xlsx — official staff list used for filtering" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/data/epidemiology.xlsx" title="data/epidemiology.xlsx"><img src=".github/readme-tree/05.svg" alt="data/epidemiology.xlsx" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/data/immunology.xlsx" title="data/immunology.xlsx"><img src=".github/readme-tree/06.svg" alt="data/immunology.xlsx" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/data/infectious_diseases.xlsx" title="data/infectious_diseases.xlsx"><img src=".github/readme-tree/07.svg" alt="data/infectious_diseases.xlsx" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/data/microbiology.xlsx" title="data/microbiology.xlsx"><img src=".github/readme-tree/08.svg" alt="data/microbiology.xlsx" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/magazine" title="magazine/"><img src=".github/readme-tree/09.svg" alt="magazine/ — journal network inputs and results" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/magazine/data" title="magazine/data/"><img src=".github/readme-tree/10.svg" alt="magazine/data/ — authors and works per journal" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/magazine/images" title="magazine/images/"><img src=".github/readme-tree/11.svg" alt="magazine/images/ — assortativity and clustering plots" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/blob/main/magazine/models/journal-networks.gml" title="magazine/models/journal-networks.gml"><img src=".github/readme-tree/12.svg" alt="magazine/models/journal-networks.gml — saved journal graph" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/models" title="models/"><img src=".github/readme-tree/13.svg" alt="models/ — saved graphs (GML, Pajek, NET)" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/images" title="images/"><img src=".github/readme-tree/14.svg" alt="images/ — Louvain community detection plots" align="top"></a><br>
<a href="https://github.com/LazarDavidovic98/social-network-analysis/tree/main/docs" title="docs/"><img src=".github/readme-tree/15.svg" alt="docs/ — documentation and presentation" align="top"></a><br>
</p>

<sub>Every row is a link to that file or folder on GitHub. Purple: folders, green: source code, grey: configuration, data and docs.</sub>
<!-- project-tree:end -->

## Technologies Used

- `Python` (v3.9+)
- `pandas` – for data manipulation
- `networkX` – for network modeling and analysis
- `matplotlib` / `graphviz` – for visualization
- `Gephi` – for advanced visual analysis and Louvain community detection

## Key Analyses

- Number of publications per author (full and fractional counting)
- Author H-index
- Distribution by years and journals
- Network metrics: clustering, centrality, assortativity, diameter
- Detection of key individuals and communities within the scientific network

## Objective

Using social network analysis tools, the aim is to identify:
- the most influential scientific actors,
- the level of collaboration among authors and across departments,
- structural patterns of scientific production,
- potential recommendations for connecting isolated groups or individuals.

---

**Detailed documentation is available here**: [Documentation](docs/Documentation.md)

**You can also view the project presentation**: [Presentation](docs/Presentation.pdf)
