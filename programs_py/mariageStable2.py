from random import randint
from math import inf

def mariage_stable(capacites, pref_etudiants, pref_ecoles):

    # on fait une copie des préférences pour ne pas modifier l'original
    pref_etu = [list(prefs) for prefs in pref_etudiants]
    
    # on crée un dico pour chaque école: {etudiant: rang}
    rangs_ecoles = []
    for prefs in pref_ecoles:
        rangs = {}
        for rang, etudiant in enumerate(prefs):
            rangs[etudiant] = rang
        rangs_ecoles.append(rangs)
    
    # liste des étudiants pas encore placés
    etudiants_libres = list(range(len(pref_etu)))
    # liste des étudiants acceptés par chaque école
    affectations = [[] for i in range(len(pref_ecoles))]
    
    # tant qu'il reste des étudiants à placer
    while etudiants_libres:
        etudiant = etudiants_libres.pop(0)
        
        # si l'étudiant a épuisé ses préférences on passe au suivant 
        if not pref_etu[etudiant]:
            continue
        
        # l'étudiant propose à son école favorite actuelle
        ecole = pref_etu[etudiant].pop(0)
        
        # si l'école n'a pas classé cet étudiant on passe
        if etudiant not in rangs_ecoles[ecole]:
            continue
        
        # si l'école a de la place on accepte directement
        if len(affectations[ecole]) < capacites[ecole]:
            affectations[ecole].append(etudiant)
            continue
        
        # sinon on doit trouver l'étudiant le moins bien classé actuellement dans l'école
        pire = affectations[ecole][0]
        for etu in affectations[ecole]:
            if rangs_ecoles[ecole].get(etu, inf) > rangs_ecoles[ecole].get(pire, inf):
                pire = etu
        
        # si le nouvel étudiant est mieux classé on remplace
        if rangs_ecoles[ecole][etudiant] < rangs_ecoles[ecole][pire]:
            affectations[ecole].remove(pire)
            affectations[ecole].append(etudiant)
            # l'étudiant rejeté redevient libre
            if pref_etu[pire]:
                etudiants_libres.append(pire)
        else:
            # sinon le nouvel étudiant est rejeté
            etudiants_libres.append(etudiant)
    
    return affectations

def satisfaction_etudiants(affectations, pref_etudiants):
    nb_etudiants = len(pref_etudiants)
    satisfaction_totale = 0
    etudiants_places = 0
    
    # on crée un dico pour savoir quelle école a pris quel étudiant
    etudiant_vers_ecole = {}
    for ecole, etudiants in enumerate(affectations):
        for etudiant in etudiants:
            etudiant_vers_ecole[etudiant] = ecole
    
    rangs_obtenus = []
    
    for etudiant in range(nb_etudiants):
        # étudiant pas placé
        if etudiant not in etudiant_vers_ecole:
            rangs_obtenus.append(None)
            continue
        
        # on récupère l'école obtenue
        ecole_obtenue = etudiant_vers_ecole[etudiant]
        preferences = pref_etudiants[etudiant]
        
        # on trouve à quel rang était cette école dans ses préférences
        if ecole_obtenue in preferences:
            rang = preferences.index(ecole_obtenue)
            rangs_obtenus.append(rang)
            # plus le rang est bon (proche de 0), plus la satisfaction est haute
            satisfaction = 100 * (1 - rang / len(preferences))
            satisfaction_totale += satisfaction
            etudiants_places += 1
        else:
            rangs_obtenus.append(None)
    
    # calculs des stats
    satisfaction_moyenne = satisfaction_totale / nb_etudiants if nb_etudiants > 0 else 0
    taux_placement = 100 * etudiants_places / nb_etudiants if nb_etudiants > 0 else 0
    
    rangs_valides = [r for r in rangs_obtenus if r is not None]
    meilleur_rang = min(rangs_valides) if rangs_valides else None
    pire_rang = max(rangs_valides) if rangs_valides else None
    
    # affichage
    print("\nÉtudiants:")
    print(f"  Satisfaction moyenne: {satisfaction_moyenne:.2f}%")
    print(f"  Placés: {etudiants_places}/{nb_etudiants} ({taux_placement:.2f}%)")
    if meilleur_rang is not None:
        print(f"  Meilleur rang: {meilleur_rang}, Pire rang: {pire_rang}")
    
    return satisfaction_moyenne, taux_placement, etudiants_places, nb_etudiants, meilleur_rang, pire_rang

# !!!!!! la satisfaction actuelle d'une école n'est pas parfaite : une école qui a une capacité de 2 et qui a obtenu ses 2 premiers choix devrait avoir une satisfaction de 100%
# demander à la prof...
def satisfaction_ecoles(affectations, pref_ecoles, capacites):
    nb_ecoles = len(pref_ecoles)
    satisfaction_totale = 0
    places_remplies = 0
    places_totales = sum(capacites)
    
    satisfactions_ecoles = []
    rangs_moyens = []
    meilleurs_rangs = []
    pires_rangs = []
    
    # pour chaque école
    for ecole in range(nb_ecoles):
        etudiants = affectations[ecole]
        preferences = pref_ecoles[ecole]
        
        # école vide (satisfaction à 0 pour le moment !)
        if not etudiants: 
            satisfactions_ecoles.append(0)
            rangs_moyens.append(None)
            meilleurs_rangs.append(None)
            pires_rangs.append(None)
            continue
        
        # on récupère le rang de chaque étudiant accepté
        rangs = []
        for etudiant in etudiants:
            if etudiant in preferences:
                rang = preferences.index(etudiant)
                rangs.append(rang)
        
        # stats sur les rangs
        rang_moyen = sum(rangs) / len(rangs)
        meilleur_rang = min(rangs)
        pire_rang = max(rangs)
        
        rangs_moyens.append(rang_moyen)
        meilleurs_rangs.append(meilleur_rang)
        pires_rangs.append(pire_rang)
        
        # satisfaction basée sur le rang moyen
        satisfaction_ecole = 100 * (1 - rang_moyen / len(preferences))
        
        satisfactions_ecoles.append(satisfaction_ecole)
        satisfaction_totale += satisfaction_ecole
        places_remplies += len(etudiants)
    
    satisfaction_moyenne = satisfaction_totale / nb_ecoles if nb_ecoles > 0 else 0
    taux_remplissage = 100 * places_remplies / places_totales if places_totales > 0 else 0
    
    # meilleur et pire rang parmi toutes les écoles
    meilleur_rang_global = min([r for r in meilleurs_rangs if r is not None]) if any(r is not None for r in meilleurs_rangs) else None
    pire_rang_global = max([r for r in pires_rangs if r is not None]) if any(r is not None for r in pires_rangs) else None
    
    # affichage
    print("\nÉcoles:")
    print(f"  Satisfaction moyenne: {satisfaction_moyenne:.2f}%")
    print(f"  Places remplies: {places_remplies}/{places_totales} ({taux_remplissage:.2f}%)")
    if meilleur_rang_global is not None:
        print(f"  Meilleur rang: {meilleur_rang_global}, Pire rang: {pire_rang_global}")
    
    print("\nDétail par école:")
    for ecole in range(len(affectations)):
        etudiants = affectations[ecole]
        if etudiants:
            print(f"  École {ecole}: {etudiants}")
            print(f"    -> satisfaction {satisfactions_ecoles[ecole]:.1f}%, "
                  f"rang moyen {rangs_moyens[ecole]:.2f} "
                  f"(min={meilleurs_rangs[ecole]}, max={pires_rangs[ecole]})")
        else:
            print(f"  École {ecole}: vide")
    
    return (satisfaction_moyenne, taux_remplissage, places_remplies, places_totales, 
            meilleur_rang_global, pire_rang_global, satisfactions_ecoles, 
            rangs_moyens, meilleurs_rangs, pires_rangs)


def resoudre(capacites, pref_etudiants, pref_ecoles):
    
    affectations = mariage_stable(capacites, pref_etudiants, pref_ecoles)
    
    stats_etu = satisfaction_etudiants(affectations, pref_etudiants)
    stats_ecoles = satisfaction_ecoles(affectations, pref_ecoles, capacites)
    
    return affectations, stats_etu, stats_ecoles


def generer_instance(capacites, nb_etudiants):
    nb_ecoles = len(capacites)
    
    # préférences des écoles
    pref_ecoles = []
    for ecole in range(nb_ecoles):
        taille_pref = randint(1, nb_etudiants)
        pref_ecoles.append([])
        for i in range(taille_pref):
            etudiant = randint(0, nb_etudiants - 1)
            while etudiant in pref_ecoles[ecole]:
                etudiant = randint(0, nb_etudiants - 1)
            pref_ecoles[ecole].append(etudiant)
    
    # préférences des étudiants
    pref_etudiants = []
    for etudiant in range(nb_etudiants):
        taille_pref = randint(1, nb_ecoles)
        pref_etudiants.append([])
        for i in range(taille_pref):
            ecole = randint(0, nb_ecoles - 1)
            while ecole in pref_etudiants[etudiant]:
                ecole = randint(0, nb_ecoles - 1)
            pref_etudiants[etudiant].append(ecole)
    
    return capacites, pref_etudiants, pref_ecoles


def exercice_cm():
    capacites = [1, 1, 1]
    pref_etudiants = [[1, 0, 2], [0, 1, 2], [0, 1, 2]]
    pref_ecoles = [[0, 2, 1], [1, 0, 2], [1, 0, 2]]
    return capacites, pref_etudiants, pref_ecoles


def exercice_cc():
    capacites = [1, 1, 1, 1, 1]
    pref_etudiants = [[1, 0, 2, 4, 3], [0, 2, 1, 4, 3], [2, 0, 4, 1, 3], [2, 1, 4, 3, 0], [0, 1, 2, 3, 4]]
    pref_ecoles = [[2, 0, 4, 3, 1], [1, 0, 4, 3, 2], [4, 1, 2, 3, 0], [1, 0, 4, 3, 2], [2, 1, 4, 3, 0]]
    return capacites, pref_etudiants, pref_ecoles


def test_capacity_up():
    capacites = [2, 2, 2]
    pref_etudiants = [[1, 0, 2], [0, 1, 2], [0, 1, 2], [1, 0, 2], [0, 1, 2], [0, 1, 2]]
    pref_ecoles = [[0, 2, 1, 3, 5, 4], [1, 0, 2, 4, 3, 5], [1, 0, 2, 4, 3, 5]]
    return capacites, pref_etudiants, pref_ecoles

def test_incoherence():
    capacites = [2]
    pref_etudiants = [[0], [0]]
    pref_ecoles = [[0, 1]]
    return capacites, pref_etudiants, pref_ecoles


# test
if __name__ == "__main__":
    
    # Test 1
    print("\n" + "─"*60)
    print("TEST 1 : Exercice CM")
    print("─"*60)
    
    capacites, pref_etudiants, pref_ecoles = exercice_cm()
    affectations = resoudre(capacites, pref_etudiants, pref_ecoles)
    
    
    # Test 2
    print("\n" + "─"*60)
    print("TEST 2 : Exercice CC")
    print("─"*60)
    
    capacites, pref_etudiants, pref_ecoles = exercice_cc()
    affectations = resoudre(capacites, pref_etudiants, pref_ecoles)
    
    
    # Test 3
    print("\n" + "─"*60)
    print("TEST 3 : Test capacités augmentées")
    print("─"*60)

    capacites, pref_etudiants, pref_ecoles = test_capacity_up()
    affectations = resoudre(capacites, pref_etudiants, pref_ecoles)

    # Test simple incohérence satisfaction école
    print("\n" + "─"*60)
    print("TEST 4 : ")
    print("─"*60)
    
    capacites, pref_etudiants, pref_ecoles = test_incoherence()
    affectations = resoudre(capacites, pref_etudiants, pref_ecoles)