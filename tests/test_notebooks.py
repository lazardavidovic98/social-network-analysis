"""Execute both notebooks headlessly in a temporary copy of the project.

The notebooks write tables, plots and graphs relative to the working directory,
so they run in tmp_path and the working tree is never modified.
"""
import shutil

import nbformat
import networkx as nx
import pytest
from nbclient import NotebookClient

pytestmark = pytest.mark.slow

INPUT_DIRS = ["data", "magazine/data"]
OUTPUT_DIRS = ["images", "models", "magazine/images", "magazine/models"]


@pytest.fixture
def workdir(tmp_path, repo_root, monkeypatch):
    for d in INPUT_DIRS:
        shutil.copytree(repo_root / d, tmp_path / d)
    for d in OUTPUT_DIRS:
        (tmp_path / d).mkdir(parents=True, exist_ok=True)
    # The kernel inherits this environment; a non-interactive backend would keep
    # figures open after plt.show() and draw later plots on top of them.
    monkeypatch.delenv("MPLBACKEND", raising=False)
    return tmp_path


def run_notebook(repo_root, workdir, name):
    nb = nbformat.read(repo_root / name, as_version=4)
    client = NotebookClient(
        nb, timeout=600, kernel_name="python3", resources={"metadata": {"path": str(workdir)}}
    )
    client.execute()  # raises CellExecutionError on the first failing cell
    return nb


def weighted_edges(G):
    return {(frozenset((u, v)), w) for u, v, w in G.edges(data="weight")}


def test_co_authorship_notebook(repo_root, workdir):
    run_notebook(repo_root, workdir, "co-authorship-networks.ipynb")

    for table in ["authors_data", "combined_works", "works_per_authors", "authors_and_works"]:
        assert (workdir / "output" / f"{table}.xlsx").is_file()
    for plot in ["local_cc_main_network", "local_cc_er_network", "local_cc_random_scale_free_network"]:
        assert (workdir / "images" / f"{plot}.png").is_file()

    # The regenerated graph must be the one committed in models/
    produced = nx.read_gml(workdir / "models" / "network_one.gml")
    committed = nx.read_gml(repo_root / "models" / "network_one.gml")
    assert list(produced.nodes) == list(committed.nodes)
    assert weighted_edges(produced) == weighted_edges(committed)

    partition = nx.read_pajek(workdir / "models" / "spectral_clustering.net")
    assert partition.number_of_nodes() == 58


def test_journal_network_notebook(repo_root, workdir):
    run_notebook(repo_root, workdir, "journal-networks.ipynb")

    produced = nx.read_gml(workdir / "magazine" / "models" / "journal-networks.gml")
    committed = nx.read_gml(repo_root / "magazine" / "models" / "journal-networks.gml")
    assert not produced.is_directed()
    assert weighted_edges(produced) == weighted_edges(committed)
    assert (workdir / "magazine" / "images" / "local_cc_magazine_network.png").is_file()
