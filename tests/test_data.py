"""Fast checks of the input data and the saved graphs the README reports on."""
import networkx as nx
import pandas as pd
import pytest

DEPARTMENT_FILES = [
    "epidemiology.xlsx",
    "immunology.xlsx",
    "infectious_diseases.xlsx",
    "microbiology.xlsx",
]

SCOPUS_COLUMNS = [
    "Author", "Authors", "Title", "Year", "Source title", "Volume", "Issue", "Art. No.",
    "Page start", "Page end", "Page count", "Cited by", "Link", "Document Type", "Source",
]


@pytest.mark.parametrize("file_name", DEPARTMENT_FILES)
def test_department_exports_have_scopus_columns(repo_root, file_name):
    df = pd.read_excel(repo_root / "data" / file_name)
    assert list(df.columns) == SCOPUS_COLUMNS
    assert len(df) > 0


def test_staff_list_has_the_headers_the_notebook_maps(repo_root):
    # co-authorship-networks.ipynb renames exactly these columns to English
    df = pd.read_excel(repo_root / "data" / "authors.xlsx")
    assert list(df.columns) == ["Ime", "Prezime", "Katedra", "H indeks", "Broj radova"]
    assert len(df) == 59
    assert df["Katedra"].nunique() == 4


@pytest.mark.parametrize(
    "file_name",
    ["authors_data.xlsx", "combined_works.xlsx", "works_per_authors.xlsx", "authors_and_works.xlsx"],
)
def test_journal_network_inputs_exist(repo_root, file_name):
    assert (repo_root / "magazine" / "data" / file_name).is_file()


def test_journal_network_input_has_required_columns(repo_root):
    df = pd.read_excel(repo_root / "magazine" / "data" / "authors_and_works.xlsx")
    assert {"Author", "Source title"} <= set(df.columns)


def test_saved_co_authorship_network(repo_root):
    G = nx.read_gml(repo_root / "models" / "network_one.gml")
    assert not G.is_directed()
    assert G.number_of_nodes() == 58
    assert G.number_of_edges() == 307
    assert nx.is_connected(G)
    assert not any(u == v for u, v in G.edges())
    weights = [w for _, _, w in G.edges(data="weight")]
    assert all(isinstance(w, int) and w >= 1 for w in weights)


def test_saved_journal_network_is_undirected(repo_root):
    G = nx.read_gml(repo_root / "magazine" / "models" / "journal-networks.gml")
    assert not G.is_directed()
    assert G.number_of_nodes() == 536
    assert nx.is_connected(G)
