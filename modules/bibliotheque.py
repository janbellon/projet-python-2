
import json
from modules.livre import Livre

class Bibliotheque:
    """
    Classe centrale qui gère la collection : ajout/suppression/recherche,
    résumé global, sauvegarde & chargement JSON.
    """
    livres = []
    id_counter = 1  # géré ici, pas dans Livre

    # ------------------ CRUD collection ------------------
    @classmethod
    def ajouter_livre(cls, titre, auteur, categorie, statut="Disponible"):
        """Crée un Livre, assigne un ID, l'ajoute à la collection."""
        livre = Livre(cls.id_counter, titre, auteur, categorie, statut)
        cls.id_counter += 1
        cls.livres.append(livre)
        print(f"Livre ajouté : {livre.titre} (ID {livre.id_livre})")
        return livre

    @classmethod
    def supprimer_livre(cls, id_livre):
        for i, l in enumerate(cls.livres):
            if l.id_livre == id_livre:
                del cls.livres[i]
                print(f"🗑️  Livre supprimé : ID {id_livre}")
                return True
        print(f"Aucun livre trouvé avec l'ID {id_livre}.")
        return False

    @classmethod
    def modifier_livre(cls, id_livre, **kwargs):
        """Trouve un livre par ID et applique Livre.modifier(...)."""
        livre = cls.trouver_par_id(id_livre)
        if not livre:
            print(f"Aucun livre trouvé avec l'ID {id_livre}.")
            return None
        livre.modifier(**kwargs)
        print(f"✏️  Livre {id_livre} mis à jour.")
        return livre

    # ------------------ Recherche / Filtrage ------------------
    @classmethod
    def trouver_par_id(cls, id_livre):
        return next((l for l in cls.livres if l.id_livre == id_livre), None)

    @classmethod
    def rechercher_par_titre(cls, mot_cle):
        return [l for l in cls.livres if mot_cle.lower() in l.titre.lower()]

    @classmethod
    def rechercher_par_auteur(cls, mot_cle):
        return [l for l in cls.livres if mot_cle.lower() in l.auteur.lower()]

    @classmethod
    def rechercher(cls, *, titre=None, auteur=None, categorie=None, statut=None):
        """Filtrage combiné."""
        res = cls.livres
        if titre is not None:
            res = [l for l in res if titre.lower() in l.titre.lower()]
        if auteur is not None:
            res = [l for l in res if auteur.lower() in l.auteur.lower()]
        if categorie is not None:
            res = [l for l in res if l.categorie.lower() == categorie.lower()]
        if statut is not None:
            res = [l for l in res if l.statut.lower() == statut.lower()]
        return res

    # ------------------ Affichages utiles ------------------
    @classmethod
    def historique(cls):
        """Affiche tous les livres (style proche de ton code)."""
        for l in cls.livres:
            print(f"ID : {l.id_livre}")
            print(f"Titre       : {l.titre}")
            print(f"Auteur      : {l.auteur}")
            print(f"Catégorie   : {l.categorie}")
            print(f"Statut      : {l.statut}")
            print("-" * 50)

    @classmethod
    def resume_global(cls, *, as_print=True):
        """
        Résumé par titre (comme ton implémentation initiale),
        sérialisable en JSON (sets -> listes).
        """
        resume = {}
        for l in cls.livres:
            key = l.titre.strip().lower()
            bloc = resume.setdefault(key, {
                "titre": l.titre,
                "auteurs": set(),
                "nb_total": 0,
                "nb_disponible": 0,
                "nb_emprunte": 0,
            })
            bloc["nb_total"] += 1
            bloc["auteurs"].add(l.auteur)

            s = l.statut.strip().lower()
            if s == "disponible":
                bloc["nb_disponible"] += 1
            elif s in ("emprunté", "emprunte", "emprunté"):
                bloc["nb_emprunte"] += 1

        # sets -> listes triées
        for k in list(resume.keys()):
            resume[k]["auteurs"] = sorted(resume[k]["auteurs"])

        if as_print:
            print("\nRésumé global de la bibliothèque :")
            for _, infos in resume.items():
                print(f"\n{infos['titre']}")
                print(f"   Auteurs       : {', '.join(infos['auteurs'])}")
                print(f"   Total         : {infos['nb_total']}")
                print(f"   Disponibles   : {infos['nb_disponible']}")
                print(f"   Empruntés     : {infos['nb_emprunte']}")

        return resume

    # ------------------ Persistance ------------------
    @classmethod
    def save_resume_json(cls, filename="bibliotheque_resume.json", *, print_resume=False):
        """Sauvegarde le RÉSUMÉ (lisible)."""
        data = cls.resume_global(as_print=print_resume)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Résumé sauvegardé : {filename}")

    @classmethod
    def save_catalog_json(cls, filename="bibliotheque_catalogue.json"):
        """Sauvegarde le CATALOGUE COMPLET (rechargeable)."""
        payload = {
            "id_counter": cls.id_counter,
            "livres": [l.to_dict() for l in cls.livres],
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=4)
        print(f"Catalogue sauvegardé : {filename}")

    @classmethod
    def load_catalog_json(cls, filename="bibliotheque_catalogue.json", *, reset=True):
        """Recharge le CATALOGUE COMPLET (garde les IDs cohérents)."""
        with open(filename, "r", encoding="utf-8") as f:
            payload = json.load(f)

        if reset:
            cls.livres.clear()
            cls.id_counter = 1

        for d in payload.get("livres", []):
            livre = Livre.from_dict(d)
            cls.livres.append(livre)

        if "id_counter" in payload:
            cls.id_counter = max(cls.id_counter, payload["id_counter"])
        else:
            # fallback si le champ manque : reprend max ID + 1
            if cls.livres:
                cls.id_counter = max(l.id_livre for l in cls.livres) + 1

        print(f"Catalogue chargé depuis : {filename} ({len(cls.livres)} livres)")
