"""
affichage.py — Affichage formaté des livres de la bibliothèque.

Dépendances internes:
    - Suppose l'existence d'une classe Livre avec un attribut de classe `_livres` (liste d'instances).
    - Les instances de Livre doivent exposer: id_livre, titre, auteur, categorie, statut.

Aucune modification n'est requise dans la classe Livre (l'autre équipe corrige __init__).

Fonctions principales:
    - afficher_livres(livres, ...): tableau lisible en console.
    - afficher_catalogue(): affiche tout le catalogue Livre._livres
    - apercu(livres, n): aperçu limité (utile après un tri/filtre).
    - to_rows(livres): convertit en lignes (liste de tuples) — pratique pour d'autres modules.
"""
from typing import Iterable, List, Tuple, Optional

COLS = ("ID", "Titre", "Auteur", "Catégorie", "Statut")

def _fmt_cell(val, width):
    s = "" if val is None else str(val)
    if len(s) > width:
        return s[: max(0, width - 1)] + "…"
    return s.ljust(width)

def _widths(rows: List[Tuple], minw=(4, 18, 16, 14, 12)) -> Tuple[int, ...]:
    w = list(minw)
    for row in rows:
        for i, cell in enumerate(row):
            w[i] = max(w[i], len("" if cell is None else str(cell)))
    return tuple(w)

def to_rows(livres: Iterable) -> List[Tuple]:
    rows: List[Tuple] = []
    for lv in livres:
        # On reste tolérant si certains attributs manquent temporairement
        idv = getattr(lv, "id_livre", getattr(lv, "id", "?"))
        rows.append((
            idv,
            getattr(lv, "titre", ""),
            getattr(lv, "auteur", ""),
            getattr(lv, "categorie", ""),
            getattr(lv, "statut", ""),
        ))
    return rows

def afficher_livres(livres: Iterable, header: str = "Catalogue", limit: Optional[int] = None) -> None:
    data = list(livres)
    if limit is not None:
        data = data[: max(0, int(limit))]
    rows = to_rows(data)
    widths = _widths(rows)
    line = " | ".join(_fmt_cell(c, w) for c, w in zip(COLS, widths))
    sep = "-+-".join("-" * w for w in widths)
    print(f"\n{header}")
    print(sep)
    print(line)
    print(sep)
    for r in rows:
        print(" | ".join(_fmt_cell(c, w) for c, w in zip(r, widths)))
    print(sep)
    print(f"{len(rows)} ligne(s).")

def apercu(livres: Iterable, n: int = 10) -> None:
    afficher_livres(list(livres)[:n], header=f"Aperçu (n={n})", limit=None)

def afficher_catalogue() -> None:
    # Import tardif pour éviter les dépendances circulaires au chargement
    from bibliotheque import Livre  # type: ignore
    afficher_livres(Livre._livres, header="Catalogue complet")
