from typing import Iterable, Callable, Optional, List

# ===================== Coeur (inchangé) =====================

def _norm(s: Optional[str]) -> str:
    return "" if s is None else str(s).strip().casefold()

def _match_field(value: str, needle: Optional[str]) -> bool:
    if needle is None:
        return True
    return _norm(needle) in _norm(value)

def filtrer_livres(
    livres: Iterable,
    titre: Optional[str] = None,
    auteur: Optional[str] = None,
    categorie: Optional[str] = None,
    statut: Optional[str] = None,
    disponibilite: Optional[bool] = None,  # True=Disponible, False=Emprunté
):
    for lv in livres:
        t = getattr(lv, "titre", "")
        a = getattr(lv, "auteur", "")
        c = getattr(lv, "categorie", "")
        s = getattr(lv, "statut", "")

        if not _match_field(t, titre):
            continue
        if not _match_field(a, auteur):
            continue
        if not _match_field(c, categorie):
            continue
        if statut is not None and _norm(s) != _norm(statut):
            continue
        if disponibilite is not None:
            # tolère "emprunté", "emprunte", "emprunté" (accents)
            dispo_txt = (_norm(s) == "disponible")
            if dispo_txt != disponibilite:
                continue
        yield lv

def trier_livres(livres: Iterable, cle: str = "titre", inverse: bool = False):
    key_map: dict[str, Callable] = {
        "id": lambda x: getattr(x, "id_livre", getattr(x, "id", 0)),
        "titre": lambda x: getattr(x, "titre", ""),
        "auteur": lambda x: getattr(x, "auteur", ""),
        "categorie": lambda x: getattr(x, "categorie", ""),
        "statut": lambda x: getattr(x, "statut", ""),
    }
    key_func = key_map.get(cle, key_map["titre"])
    return sorted(list(livres), key=key_func, reverse=inverse)

def rechercher(livres: Iterable, texte: str):
    q = _norm(texte)
    for lv in livres:
        blob = " ".join([
            _norm(getattr(lv, "titre", "")),
            _norm(getattr(lv, "auteur", "")),
            _norm(getattr(lv, "categorie", "")),
            _norm(getattr(lv, "statut", "")),
        ])
        if q in blob:
            yield lv

# ===================== Helpers optionnels =====================

def _get_bibliotheque():
    """Import paresseux pour éviter les imports circulaires et gérer les chemins."""
    try:
        from modules.bibliotheque import Bibliotheque  # type: ignore
    except ImportError:
        from bibliotheque import Bibliotheque  # type: ignore
    return Bibliotheque

def filtrer_catalogue(
    titre: Optional[str] = None,
    auteur: Optional[str] = None,
    categorie: Optional[str] = None,
    statut: Optional[str] = None,
    disponibilite: Optional[bool] = None,
):
    """Filtre directement dans Bibliotheque.livres."""
    Bibliotheque = _get_bibliotheque()
    return list(filtrer_livres(Bibliotheque.livres, titre, auteur, categorie, statut, disponibilite))

def trier_catalogue(cle: str = "titre", inverse: bool = False):
    """Trie directement Bibliotheque.livres (renvoie une nouvelle liste)."""
    Bibliotheque = _get_bibliotheque()
    return trier_livres(Bibliotheque.livres, cle=cle, inverse=inverse)

def rechercher_catalogue(texte: str):
    """Recherche plein-texte directement dans Bibliotheque.livres."""
    Bibliotheque = _get_bibliotheque()
    return list(rechercher(Bibliotheque.livres, texte))
