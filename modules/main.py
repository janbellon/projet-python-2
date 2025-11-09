# main.py — Menu "Utilisateurs" central + sous-menus par rôles
from typing import Dict, Union
import sys



#==================== Imports principaux =========================

# ===== Cœur projet =====
from modules.bibliotheque import Bibliotheque
from modules.utilisateur import Lecteur, Bibliothecaire
from modules.recherche import exporter_csv, rechercher_texte, filtrer, trier, generer_statistiques
from modules.tri_filtrage import filtrer_livres, trier_livres, rechercher as rechercher_fulltext
from modules.statistiques import stats_depuis_bibliotheque

#==================== Imports autres =========================
# recherche.py 
try:
    from modules.recherche import exporter_csv, rechercher_texte, filtrer, trier, generer_statistiques
    HAS_RECHERCHE = True
except ImportError:
    try:
        from modules.recherche import exporter_csv, rechercher_texte, filtrer, trier, generer_statistiques
        HAS_RECHERCHE = True
    except ImportError:
        HAS_RECHERCHE = False

# tri_filtrage.py
try:
    from modules.tri_filtrage import filtrer_livres, trier_livres, rechercher as rechercher_fulltext
    HAS_TRI = True
except ImportError:
    try:
        from modules.tri_filtrage import filtrer_livres, trier_livres, rechercher as rechercher_fulltext
        HAS_TRI = True
    except ImportError:
        HAS_TRI = False

# statistiques.py
try:
    from modules.statistiques import stats_depuis_bibliotheque
    HAS_STATS = True
except ImportError:
    try:
        from modules.statistiques import stats_depuis_bibliotheque
        HAS_STATS = True
    except ImportError:
        HAS_STATS = False



class Admin:
    _id_counter = 1
    def __init__(self, nom: str, email: str):
        self.id = 10_000 + Admin._id_counter
        Admin._id_counter += 1
        self.nom = nom
        self.email = email
        self.role = 99  # Admin


# ===== État en mémoire =====
UserT = Union[Lecteur, Bibliothecaire, Admin]
utilisateurs: Dict[int, UserT] = {}   # id -> instance



def _input(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return ""


# ======================= MENUS =======================

def menu_principal():
    while True:
        print("\n=== BIBLIOTHÈQUE — Accueil ===")
        print("1. Menu utilisateurs ")
        print("2. Catalogue (vue seule)")
        print("3. Quitter")
        ch = _input("Votre choix: ").strip()
        if ch == "1":
            menu_utilisateurs()
        elif ch == "2":
            Bibliotheque.historique()
        elif ch == "3":
            print("Au revoir.")
            sys.exit(0)
        else:
            print("Choix invalide.")


def menu_utilisateurs():
    while True:
     
        print("\n--- Menu Utilisateurs ---")
        print("1. Créer un Lecteur")
        print("2. Créer un Bibliothécaire")
        print("3. Créer un Admin")
        print("4. Lister les utilisateurs")
        print("5. Se connecter (ID)")
        print("6. Retour")
        ch = _input("Votre choix: ").strip()

        if ch == "1":
            nom = _input("Nom: ").strip()
            email = _input("Email: ").strip()
            pwd = _input("Mot de passe: ")
            u = Lecteur(nom, email, pwd)
            utilisateurs[u.id] = u
            print(f"Lecteur créé → ID {u.id} | {u.nom} <{u.email}> (role=Lecteur)")

        elif ch == "2":
            nom = _input("Nom: ").strip()
            email = _input("Email: ").strip()
            pwd = _input("Mot de passe: ")
            u = Bibliothecaire(nom, email, pwd)
            utilisateurs[u.id] = u
            print(f"Bibliothécaire créé → ID {u.id} | {u.nom} <{u.email}> (role=Bibliothécaire)")

        elif ch == "3":
            nom = _input("Nom: ").strip()
            email = _input("Email: ").strip()
            u = Admin(nom, email)
            utilisateurs[u.id] = u
            print(f"Admin créé → ID {u.id} | {u.nom} <{u.email}> (role=Admin)")

        elif ch == "4":
            if not utilisateurs:
                print("Aucun utilisateur.")
            else:
                for uid, u in utilisateurs.items():
                    r = "Lecteur" if getattr(u, "role", 0) == 1 else "Bibliothécaire" if getattr(u, "role", 0) == 2 else "Admin" if getattr(u, "role", 0) == 99 else "?"
                    print(f"- ID {uid} | {r} | {u.nom} <{u.email}>")

        elif ch == "5":
            try:
                uid = int(_input("ID utilisateur: ").strip())
            except ValueError:
                print("ID invalide.")
                continue
            u = utilisateurs.get(uid)
            if not u:
                print("Utilisateur introuvable.")
                continue
            demarrer_session(u)

        elif ch == "6":
            break
        else:
            print("Choix invalide.")


def demarrer_session(user: UserT):
    role = getattr(user, "role", 0)
    if role == 1:
        menu_session_lecteur(user)           # type: ignore
    elif role == 2:
        menu_session_bibliothecaire(user)    # type: ignore
    elif role == 99:
        menu_session_admin(user)             # type: ignore
    else:
        print("Rôle inconnu.")


# ---------- Session LECTEUR ----------
def menu_session_lecteur(u: Lecteur):
    while True:
        print(f"\n=== Session Lecteur — {u.nom} (ID {u.id}) ===")
        print("1. Emprunter un livre")
        print("2. Rendre un livre")
        print("3. Voir le catalogue")
        print("4. Rechercher (plein texte)")
        print("5. Déconnexion")
        ch = _input("Votre choix: ").strip()

        if ch == "1":
            u.emprunter()  
        elif ch == "2":
            u.rendre()
        elif ch == "3":
            Bibliotheque.historique()
        elif ch == "4":
            q = _input("Terme: ").strip()
            livres = Bibliotheque.livres
            if HAS_RECHERCHE:
                res = rechercher_texte(q)
            elif HAS_TRI:
                res = list(rechercher_fulltext(livres, q))
            else:
                qlc = q.lower()
                res = [l for l in livres if qlc in l.titre.lower() or qlc in l.auteur.lower() or qlc in l.categorie.lower()]
            _afficher_res(res)
        elif ch == "5":
            print("Déconnexion.")
            break
        else:
            print("Choix invalide.")


# ---------- Session BIBLIOTHÉCAIRE ----------
def menu_session_bibliothecaire(u: Bibliothecaire):
    while True:
        print(f"\n=== Session Bibliothécaire — {u.nom} (ID {u.id}) ===")
        print("1. Ajouter un livre")
        print("2. Modifier un livre")
        print("3. Supprimer un livre")
        print("4. Voir le catalogue")
        print("5. Rechercher / Filtrer / Trier")
        print("6. Déconnexion")
        ch = _input("Votre choix: ").strip()

        if ch == "1":
            u.ajouter()
        elif ch == "2":
            u.modifier()
        elif ch == "3":
            u.supprimer()
        elif ch == "4":
            Bibliotheque.historique()
        elif ch == "5":
            _outils_recherche_tri()  # outils communs
        elif ch == "6":
            print("Déconnexion.")
            break
        else:
            print("Choix invalide.")


# ---------- Session ADMIN ----------
def menu_session_admin(u: Admin):
    while True:
        print(f"\n=== Session Admin — {u.nom} (ID {u.id}) ===")
        print("1. Statistiques / Graphes")
        print("2. Exporter catalogue (CSV)")
        print("3. Sauvegarder / Charger (JSON)")
        print("4. Résumé global")
        print("5. Outils Rechercher / Filtrer / Trier")
        print("6. Voir le catalogue")
        print("7. Déconnexion")
        ch = _input("Votre choix: ").strip()
        livres = Bibliotheque.livres

        if ch == "1":
            if HAS_RECHERCHE:
                out = _input("Dossier graphes (défaut: graphs): ").strip() or "graphs"
                generer_statistiques(out)
            elif HAS_STATS:
                stats_depuis_bibliotheque("graphs")
            else:
                print("Module statistiques indisponible.")

        elif ch == "2":
            path = _input("Chemin CSV (défaut: catalogue.csv): ").strip() or "catalogue.csv"
            if HAS_RECHERCHE:
                exporter_csv(path)
            else:
                _fallback_export_csv(livres, path)

        elif ch == "3":
            _menu_persistance()

        elif ch == "4":
            Bibliotheque.save_resume_json("bibliotheque_resume.json", print_resume=True)

        elif ch == "5":
            _outils_recherche_tri()

        elif ch == "6":
            Bibliotheque.historique()

        elif ch == "7":
            print("Déconnexion.")
            break
        else:
            print("Choix invalide.")


# ---------- Outils communs (recherche / filtre / tri) ----------
def _outils_recherche_tri():
    while True:
        print("\n--- Outils Recherche / Filtre / Tri ---")
        print("1. Rechercher plein texte")
        print("2. Filtrer")
        print("3. Trier")
        print("4. Retour")
        ch = _input("Votre choix: ").strip()
        livres = Bibliotheque.livres

        if ch == "1":
            q = _input("Terme: ").strip()
            if HAS_RECHERCHE:
                res = rechercher_texte(q)
            elif HAS_TRI:
                res = list(rechercher_fulltext(livres, q))
            else:
                qlc = q.lower()
                res = [l for l in livres if qlc in l.titre.lower() or qlc in l.auteur.lower() or qlc in l.categorie.lower()]
            _afficher_res(res)

        elif ch == "2":
            t = _input("Titre (vide=ignore): ").strip() or None
            a = _input("Auteur (vide=ignore): ").strip() or None
            c = _input("Catégorie (vide=ignore): ").strip() or None
            s = _input("Statut [Disponible/Emprunté] (vide=ignore): ").strip() or None
            dr = _input("Disponibilité (o=Disponible, n=Emprunté, vide=ignore): ").strip().lower()
            dispo = True if dr in ("o", "oui", "y") else False if dr in ("n", "non") else None

            if HAS_TRI:
                res = list(filtrer_livres(livres, t, a, c, s, dispo))
            else:
                res = _fallback_filtrer(livres, t, a, c, s, dispo)
            _afficher_res(res)

        elif ch == "3":
            print("Clés: id, titre, auteur, categorie, statut")
            cle = _input("Trier par: ").strip().lower() or "titre"
            inv = _input("Ordre décroissant ? (o/n): ").strip().lower() in ("o", "oui", "y")
            if HAS_TRI:
                res = trier_livres(livres, cle=cle, inverse=inv)
            else:
                res = _fallback_trier(livres, cle, inv)
            _afficher_res(res)

        elif ch == "4":
            break
        else:
            print("Choix invalide.")


# ---------- Persistance (JSON) ----------
def _menu_persistance():
    while True:
        print("\n--- Sauvegarder / Charger ---")
        print("1. Sauvegarder CATALOGUE (JSON)")
        print("2. Charger CATALOGUE (JSON)")
        print("3. Retour")
        ch = _input("Votre choix: ").strip()
        if ch == "1":
            fn = _input("Nom fichier (défaut: bibliotheque_catalogue.json): ").strip() or "bibliotheque_catalogue.json"
            Bibliotheque.save_catalog_json(fn)
        elif ch == "2":
            fn = _input("Nom fichier (défaut: bibliotheque_catalogue.json): ").strip() or "bibliotheque_catalogue.json"
            Bibliotheque.load_catalog_json(fn, reset=True)
        elif ch == "3":
            break
        else:
            print("Choix invalide.")


# ======================= FallBacks =======================
def _afficher_res(livres):
    if not livres:
        print("(aucun résultat)")
        return
    for l in livres:
        print(f"[{getattr(l, 'id_livre', '?')}] {getattr(l, 'titre', '')} — {getattr(l, 'auteur', '')} ({getattr(l, 'categorie', '')}) [{getattr(l, 'statut', '')}]")

def _fallback_filtrer(livres, titre, auteur, categorie, statut, disponibilite):
    def norm(s): return "" if s is None else s.strip().lower()
    res = []
    for l in livres:
        t = getattr(l, "titre", "")
        a = getattr(l, "auteur", "")
        c = getattr(l, "categorie", "")
        s = getattr(l, "statut", "")
        if titre and norm(titre) not in norm(t): continue
        if auteur and norm(auteur) not in norm(a): continue
        if categorie and norm(categorie) not in norm(c): continue
        if statut and norm(statut) != norm(s): continue
        if disponibilite is not None:
            dispo_txt = norm(s) == "disponible"
            if dispo_txt != disponibilite: continue
        res.append(l)
    return res

def _fallback_trier(livres, cle, inverse):
    key_map = {
        "id": lambda x: getattr(x, "id_livre", getattr(x, "id", 0)),
        "titre": lambda x: getattr(x, "titre", ""),
        "auteur": lambda x: getattr(x, "auteur", ""),
        "categorie": lambda x: getattr(x, "categorie", ""),
        "statut": lambda x: getattr(x, "statut", ""),
    }
    key_func = key_map.get(cle, key_map["titre"])
    return sorted(list(livres), key=key_func, reverse=inverse)

def _fallback_export_csv(livres, out_csv):
    import csv, os
    os.makedirs(os.path.dirname(out_csv) or ".", exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id_livre", "titre", "auteur", "categorie", "statut"])
        for l in livres:
            w.writerow([getattr(l, "id_livre", ""), getattr(l, "titre", ""), getattr(l, "auteur", ""), getattr(l, "categorie", ""), getattr(l, "statut", "")])
    print(f"Catalogue exporté dans: {out_csv}")


# ======================= Entrée =======================
if __name__ == "__main__":
    menu_principal()

