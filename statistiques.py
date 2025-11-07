"""
statistiques.py — Statistiques et visualisations (pandas + matplotlib).

Fonctions:
    - dataframe_livres(livres): DataFrame à partir d'instances Livre
    - stats_par_categorie(df): Series du nombre de livres par catégorie
    - stats_disponibilite(df): Series du nombre de livres par statut
    - tracer_bar(series, out_png): Barres simples
    - tracer_pie(series, out_png): Camembert simple
    - compter_utilisateurs_par_type(utilisateurs): dict {type: nombre}

Remarques:
    - Aucune donnée factice n'est créée ici. Les fonctions acceptent vos listes actuelles.
    - Si vous utilisez des CSV, chargez-les côté projet puis passez les données ici.
"""
from typing import Iterable, Dict
import pandas as pd
import matplotlib.pyplot as plt
from modules.bibliotheque import Bibliotheque 
def dataframe_livres(livres: Iterable) -> pd.DataFrame:
    rows = []
    for lv in livres:
        rows.append({
            "id_livre": getattr(lv, "id_livre", getattr(lv, "id", None)),
            "titre": getattr(lv, "titre", None),
            "auteur": getattr(lv, "auteur", None),
            "categorie": getattr(lv, "categorie", None),
            "statut": getattr(lv, "statut", None),
        })
    return pd.DataFrame(rows)

def stats_par_categorie(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=int)
    return df["categorie"].fillna("Inconnu").value_counts().sort_values(ascending=False)

def stats_disponibilite(df: pd.DataFrame) -> pd.Series:
    if df.empty:
        return pd.Series(dtype=int)
    return df["statut"].fillna("Inconnu").value_counts().sort_values(ascending=False)

def tracer_bar(series: pd.Series, out_png: str) -> None:
    plt.figure()
    series.plot(kind="bar")  # ne pas fixer de couleurs/styles
    plt.title("Répartition")
    plt.xlabel(series.name if series.name else "")
    plt.ylabel("Nombre")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def tracer_pie(series: pd.Series, out_png: str) -> None:
    plt.figure()
    series.plot(kind="pie", autopct="%1.0f%%")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(out_png)
    plt.close()

def compter_utilisateurs_par_type(utilisateurs: Iterable) -> Dict[str, int]:
    """Compter sans imposer une structure stricte.
    On regarde, dans l'ordre:
        - attribut 'type_utilisateur' s'il existe
        - sinon, le nom de classe (Lecteur/Bibliothecaire/etc.)
    """
    res: Dict[str, int] = {}
    for u in utilisateurs:
        t = getattr(u, "type_utilisateur", None)
        if not t:
            t = u.__class__.__name__
        res[t] = res.get(t, 0) + 1
    return res
