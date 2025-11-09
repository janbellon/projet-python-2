"""
recherche.py — Fonctions de recherche, filtrage, tri et statistiques
adaptées à la classe Bibliotheque.

"""

import os
import csv
from typing import Iterable, List

from modules.bibliotheque import Bibliotheque
from modules.livre import Livre

# Si ces modules existent, on les importe
try:
    from modules.statistiques import (
        dataframe_livres,
        stats_par_categorie,
        stats_disponibilite,
        tracer_bar,
        tracer_pie,
    )
except ImportError:
    dataframe_livres = stats_par_categorie = stats_disponibilite = tracer_bar = tracer_pie = None


# ------------------ Export CSV ------------------
def _to_rows(livres: Iterable[Livre]):
    """Transforme les objets Livre en lignes CSV."""
    for lv in livres:
        yield {
            "id_livre": getattr(lv, "id_livre", ""),
            "titre": getattr(lv, "titre", ""),
            "auteur": getattr(lv, "auteur", ""),
            "categorie": getattr(lv, "categorie", ""),
            "statut": getattr(lv, "statut", ""),
        }


def exporter_csv(out_csv: str = "catalogue.csv") -> str:
    """Exporte tout le catalogue en CSV."""
    livres = Bibliotheque.livres
    if not livres:
        print("Aucun livre à exporter.")
        return out_csv

    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id_livre", "titre", "auteur", "categorie", "statut"])
        writer.writeheader()
        writer.writerows(_to_rows(livres))
    print(f"Catalogue exporté dans: {out_csv}")
    return out_csv


# ------------------ Recherche et filtrage ------------------
def rechercher_texte(terme: str) -> List[Livre]:
    """Recherche un livre par mot-clé (titre ou auteur)."""
    terme = terme.lower().strip()
    return [l for l in Bibliotheque.livres if terme in l.titre.lower() or terme in l.auteur.lower()]


def filtrer(categorie: str = None, statut: str = None) -> List[Livre]:
    """Filtre les livres selon la catégorie ou le statut."""
    res = Bibliotheque.livres
    if categorie:
        res = [l for l in res if l.categorie.lower() == categorie.lower()]
    if statut:
        res = [l for l in res if l.statut.lower() == statut.lower()]
    return res


def trier(cle: str = "titre", inverse: bool = False) -> List[Livre]:
    """Trie les livres selon une clé (titre, auteur, catégorie, statut, id_livre)."""
    if not Bibliotheque.livres:
        return []
    return sorted(Bibliotheque.livres, key=lambda l: getattr(l, cle), reverse=inverse)


# ------------------ Statistiques ------------------
def generer_statistiques(output_dir: str = "graphs") -> None:
    """Crée les statistiques si pandas/matplotlib sont disponibles."""
    if dataframe_livres is None:
        print("Les fonctions statistiques ne sont pas disponibles (module manquant).")
        return

    livres = Bibliotheque.livres
    if not livres:
        print("Aucun livre dans la bibliothèque.")
        return

    os.makedirs(output_dir, exist_ok=True)
    df = dataframe_livres(livres)
    par_cat = stats_par_categorie(df)
    par_statut = stats_disponibilite(df)

    print("\n=== Statistiques ===")
    print("Livres par catégorie:\n", par_cat.to_string())
    print("\nRépartition par statut:\n", par_statut.to_string())

    tracer_bar(par_cat, os.path.join(output_dir, "livres_par_categorie.png"))
    tracer_pie(par_statut, os.path.join(output_dir, "repartition_statut.png"))
    print(f"\nGraphiques enregistrés dans '{output_dir}/'")


