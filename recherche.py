"""
recherche.py — Interface de recherche interactive (CLI) + Visualisation des statistiques + Export CSV.

Utilisation rapide:
    from recherche import menu_recherche
    menu_recherche()

Prérequis:
    - Module 'affichage' et 'tri_filtrage' disponibles
    - Module 'statistiques' pour pandas/matplotlib
    - Classe Livre avec attribut de classe `_livres` peuplé ailleurs
"""
from typing import List, Iterable
from affichage import afficher_livres
from tri_filtrage import filtrer_livres, trier_livres, rechercher
from statistiques import (
    dataframe_livres,
    stats_par_categorie,
    stats_disponibilite,
    tracer_bar,
    tracer_pie,
)
import os
import csv

def _input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""

def _to_rows(livres: Iterable):
    for lv in livres:
        yield {
            "id_livre": getattr(lv, "id_livre", getattr(lv, "id", "")),
            "titre": getattr(lv, "titre", ""),
            "auteur": getattr(lv, "auteur", ""),
            "categorie": getattr(lv, "categorie", ""),
            "statut": getattr(lv, "statut", ""),
        }

def exporter_vue_csv(livres_vue: Iterable, out_csv: str = "vue_courante.csv") -> str:
    """Exporte la vue courante en CSV (ID, Titre, Auteur, Catégorie, Statut)."""
    rows = list(_to_rows(livres_vue))
    if not rows:
        print("La vue courante est vide — rien à exporter.")
        return out_csv
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id_livre", "titre", "auteur", "categorie", "statut"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Vue courante exportée dans: {out_csv}")
    return out_csv

def visualiser_statistiques(output_dir: str = "graphs") -> None:
    """Génère les statistiques et enregistre les graphiques dans output_dir."""
    # Import tardif pour éviter les import circulaires
    from bibliotheque import Livre  # type: ignore

    livres = Livre._livres
    if not livres:
        print("Aucun livre dans le catalogue. Ajoutez des livres avant de générer des statistiques.")
        return

    # Préparer dossier de sortie
    os.makedirs(output_dir, exist_ok=True)

    # DataFrame
    df = dataframe_livres(livres)

    # Statistiques
    par_cat = stats_par_categorie(df)
    par_statut = stats_disponibilite(df)

    # Affichage console
    print("\n=== Statistiques ===")
    print("Livres par catégorie:")
    print(par_cat.to_string())
    print("\nRépartition par statut:")
    print(par_statut.to_string())

    # Graphiques
    path_cat = os.path.join(output_dir, "livres_par_categorie.png")
    path_statut = os.path.join(output_dir, "repartition_statut.png")
    tracer_bar(par_cat, path_cat)
    tracer_pie(par_statut, path_statut)

    print(f"\nGraphiques enregistrés:")
    print(f"- {path_cat}")
    print(f"- {path_statut}")

def menu_recherche():
    # Import tardif pour éviter les import circulaires
    from bibliotheque import Livre  # type: ignore

    livres = Livre._livres  # source de vérité
    courant: List = list(livres)  # vue courante

    while True:
        print("\n=== Recherche / Tri / Filtre ===")
        print("1. Afficher tous les livres")
        print("2. Rechercher (plein texte)")
        print("3. Filtrer")
        print("4. Trier")
        print("5. Réinitialiser la vue")
        print("6. Visualiser les statistiques (et générer les graphes)")
        print("7. Exporter la vue courante en CSV")
        print("8. Quitter le menu")

        choix = _input("Votre choix: ").strip()
        if choix == "1":
            afficher_livres(courant, header="Vue courante")
        elif choix == "2":
            q = _input("Terme à rechercher: ").strip()
            courant = list(rechercher(livres, q))
            afficher_livres(courant, header=f"Résultats pour: {q}")
        elif choix == "3":
            t = _input("Filtrer par titre (laisser vide pour ignorer): ").strip() or None
            a = _input("Filtrer par auteur (laisser vide): ").strip() or None
            c = _input("Filtrer par catégorie (laisser vide): ").strip() or None
            s = _input("Filtrer par statut [Disponible/Emprunté] (laisser vide): ").strip() or None
            disp_raw = _input("Disponibilité (o=Disponible, n=Emprunté, vide=ignore): ").strip().lower()
            disp = None
            if disp_raw in ("o", "oui", "y"):
                disp = True
            elif disp_raw in ("n", "non"):
                disp = False
            courant = list(filtrer_livres(livres, t, a, c, s, disp))
            afficher_livres(courant, header="Après filtres")
        elif choix == "4":
            print("Clés: id, titre, auteur, categorie, statut")
            cle = _input("Trier par: ").strip().lower() or "titre"
            inv = _input("Ordre décroissant ? (o/n): ").strip().lower() in ("o", "oui", "y")
            courant = trier_livres(courant, cle=cle, inverse=inv)
            afficher_livres(courant, header=f"Triage par {cle} ({'desc' if inv else 'asc'})")
        elif choix == "5":
            courant = list(livres)
            print("Vue réinitialisée.")
        elif choix == "6":
            out = _input("Dossier de sortie des graphes (défaut: graphs): ").strip() or "graphs"
            visualiser_statistiques(out)
        elif choix == "7":
            path = _input("Chemin du fichier CSV (défaut: vue_courante.csv): ").strip() or "vue_courante.csv"
            exporter_vue_csv(courant, path)
        elif choix == "8":
            print("Fermeture du menu recherche.")
            break
        else:
            print("Choix invalide.")
