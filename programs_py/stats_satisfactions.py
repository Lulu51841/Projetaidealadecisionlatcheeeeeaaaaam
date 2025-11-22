import matplotlib.pyplot as plt
import numpy as np
import random
from mariageStable2 import mariage_stable
from calcul_satisfaction import compute_sat_scores

N_INSTANCES = 500  # nombre d'instances par tranche

def generer_preferences_incompletes(n_etudiants, n_ecoles, taux_completion=0.5):
    pref_etudiants = []
    pref_ecoles = []
    
    for _ in range(n_etudiants):
        toutes_ecoles = list(range(n_ecoles))
        random.shuffle(toutes_ecoles)
        n_choix = max(1, int(n_ecoles * taux_completion))
        pref_etudiants.append(toutes_ecoles[:n_choix])
    
    for _ in range(n_ecoles):
        tous_etudiants = list(range(n_etudiants))
        random.shuffle(tous_etudiants)
        n_choix = max(1, int(n_etudiants * taux_completion))
        pref_ecoles.append(tous_etudiants[:n_choix])
    
    return pref_etudiants, pref_ecoles


def generer_tests():
    tests = []
    tailles = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    
    groupes_config = [
        ("Groupe 1: Restrictif", 0.3, 0.5),
        ("Groupe 2: Flexible", 0.6, 0.8),
        ("Groupe 3: Complet", 1.0, 1.0)
    ]
    
    for n in tailles:
        for groupe_nom, taux_min, taux_max in groupes_config:
            for instance in range(N_INSTANCES):
                n_eco = n
                taux = taux_min if taux_min == taux_max else random.uniform(taux_min, taux_max)
                pref_etu, pref_eco = generer_preferences_incompletes(n, n_eco, taux)
                capacites = [1] * n_eco
                
                tests.append({
                    "groupe": groupe_nom,
                    "capacites": capacites,
                    "pref_etudiants": pref_etu,
                    "pref_ecoles": pref_eco,
                    "n_etudiants": n,
                    "n_ecoles": n_eco,
                    "instance": instance
                })
    
    return tests


def executer_tests(tests):
    resultats = []
    
    for test in tests:
        affectation = mariage_stable(test['capacites'], test['pref_etudiants'], test['pref_ecoles'])
        stats = compute_sat_scores(test['pref_etudiants'], test['pref_ecoles'], affectation)
        
        ecoles_vides = sum(1 for aff in affectation if len(aff) == 0)
        taux_ecoles_vides = ecoles_vides / len(affectation) if len(affectation) > 0 else 0
        
        resultats.append({
            "groupe": test['groupe'],
            "n_etudiants": test['n_etudiants'],
            "n_ecoles": test['n_ecoles'],
            "taux_affectation": stats['Taux_affectation'],
            "avg_students": stats['Avg_students'],
            "median_students": stats['Median_students'],
            "variance_students": stats['Variance_students'],
            "avg_schools": stats['Avg_schools'],
            "median_schools": stats['Median_schools'],
            "variance_schools": stats['Variance_schools'],
            "taux_ecoles_vides": taux_ecoles_vides
        })
    
    return resultats


def agreger_resultats(resultats):
    """Agrège les résultats par (groupe, taille) en faisant la moyenne des N_INSTANCES"""
    agregats = {}
    
    for r in resultats:
        cle = (r['groupe'], r['n_etudiants'])
        if cle not in agregats:
            agregats[cle] = []
        agregats[cle].append(r)
    
    resultats_agreges = []
    for (groupe, n), instances in agregats.items():
        resultats_agreges.append({
            "groupe": groupe,
            "n_etudiants": n,
            "n_ecoles": n,
            "taux_affectation": np.mean([r['taux_affectation'] for r in instances]),
            "avg_students": np.mean([r['avg_students'] for r in instances]),
            "median_students": np.mean([r['median_students'] for r in instances]),
            "variance_students": np.mean([r['variance_students'] for r in instances]),
            "avg_schools": np.mean([r['avg_schools'] for r in instances]),
            "median_schools": np.mean([r['median_schools'] for r in instances]),
            "variance_schools": np.mean([r['variance_schools'] for r in instances]),
            "taux_ecoles_vides": np.mean([r['taux_ecoles_vides'] for r in instances])
        })
    
    return resultats_agreges


def generer_graphiques(resultats):
    
    groupes = {
        "Groupe 1: Restrictif": [r for r in resultats if r['groupe'] == "Groupe 1: Restrictif"],
        "Groupe 2: Flexible": [r for r in resultats if r['groupe'] == "Groupe 2: Flexible"],
        "Groupe 3: Complet": [r for r in resultats if r['groupe'] == "Groupe 3: Complet"]
    }
    
    couleurs = {
        "Groupe 1: Restrictif": '#e74c3c',
        "Groupe 2: Flexible": '#3498db',
        "Groupe 3: Complet": '#2ecc71'
    }
    
    noms_courts = ['Restrictif (30-50%)', 'Flexible (60-80%)', 'Complet (100%)']
    noms_groupes = list(groupes.keys())
    
    # etudiants
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, :])
    
    x = np.arange(len(noms_courts))
    width = 0.2
    
    taux_moy = [np.mean([r['taux_affectation'] for r in groupes[g]]) * 100 for g in noms_groupes]
    avg_moy = [np.mean([r['avg_students'] for r in groupes[g]]) for g in noms_groupes]
    med_moy = [np.mean([r['median_students'] for r in groupes[g]]) for g in noms_groupes]
    var_moy = [np.mean([r['variance_students'] for r in groupes[g]]) for g in noms_groupes]
    
    bars1 = ax1.bar(x - 1.5*width, taux_moy, width, label='Taux affectation (%)', color='#3498db', alpha=0.8)
    bars2 = ax1.bar(x - 0.5*width, [s*100 for s in avg_moy], width, label='Moyenne (×100)', color='#2ecc71', alpha=0.8)
    bars3 = ax1.bar(x + 0.5*width, [m*100 for m in med_moy], width, label='Médiane (×100)', color='#f39c12', alpha=0.8)
    bars4 = ax1.bar(x + 1.5*width, [v*1000 for v in var_moy], width, label='Variance (×1000)', color='#e74c3c', alpha=0.8)
    
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
    
    ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Valeurs (normalisées)', fontsize=12)
    ax1.set_title(f'Satisfaction des ÉTUDIANTS (n=m, capacité=1, moyenne sur {N_INSTANCES} instances)', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(noms_courts)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    metriques = [
        ('taux_affectation', 'Taux d\'affectation (%)', gs[1, 0], 100),
        ('avg_students', 'Satisfaction moyenne', gs[1, 1], 1),
    ]
    
    for metrique, titre, position, multiplicateur in metriques:
        ax = fig.add_subplot(position)
        
        for nom_groupe, data in groupes.items():
            data_sorted = sorted(data, key=lambda r: r['n_etudiants'])
            x_data = [r['n_etudiants'] for r in data_sorted]
            y_data = [r[metrique] * multiplicateur for r in data_sorted]
            ax.plot(x_data, y_data, 'o-', label=nom_groupe, color=couleurs[nom_groupe], 
                   linewidth=2, markersize=6)
        
        ax.set_xlabel('Nombre d\'étudiants', fontsize=10)
        ax.set_ylabel(titre, fontsize=10)
        ax.set_title(titre, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.savefig('analyse_etudiants.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # etablissements
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
    
    ax1 = fig.add_subplot(gs[0, :])
    
    x = np.arange(len(noms_courts))
    width = 0.2
    
    avg_moy_schools = [np.mean([r['avg_schools'] for r in groupes[g]]) for g in noms_groupes]
    med_moy_schools = [np.mean([r['median_schools'] for r in groupes[g]]) for g in noms_groupes]
    var_moy_schools = [np.mean([r['variance_schools'] for r in groupes[g]]) for g in noms_groupes]
    taux_vides_moy = [np.mean([r['taux_ecoles_vides'] for r in groupes[g]]) * 100 for g in noms_groupes]
    
    bars1 = ax1.bar(x - 1.5*width, [s*100 for s in avg_moy_schools], width, label='Moyenne (×100)', color='#2ecc71', alpha=0.8)
    bars2 = ax1.bar(x - 0.5*width, [m*100 for m in med_moy_schools], width, label='Médiane (×100)', color='#f39c12', alpha=0.8)
    bars3 = ax1.bar(x + 0.5*width, [v*1000 for v in var_moy_schools], width, label='Variance (×1000)', color='#e74c3c', alpha=0.8)
    bars4 = ax1.bar(x + 1.5*width, taux_vides_moy, width, label='Établissements vides (%)', color='#95a5a6', alpha=0.8)
    
    for bars in [bars1, bars2, bars3, bars4]:
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
    
    ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Valeurs (normalisées)', fontsize=12)
    ax1.set_title(f'Satisfaction des ÉTABLISSEMENTS (n=m, capacité=1, moyenne sur {N_INSTANCES} instances)', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(noms_courts)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    metriques = [
        ('avg_schools', 'Satisfaction moyenne', gs[1, 0], 1),
        ('taux_ecoles_vides', 'Taux établissements vides (%)', gs[1, 1], 100),
    ]
    
    for metrique, titre, position, multiplicateur in metriques:
        ax = fig.add_subplot(position)
        
        for nom_groupe, data in groupes.items():
            data_sorted = sorted(data, key=lambda r: r['n_ecoles'])
            x_data = [r['n_ecoles'] for r in data_sorted]
            y_data = [r[metrique] * multiplicateur for r in data_sorted]
            ax.plot(x_data, y_data, 'o-', label=nom_groupe, color=couleurs[nom_groupe], 
                   linewidth=2, markersize=6)
        
        ax.set_xlabel('Nombre d\'établissements', fontsize=10)
        ax.set_ylabel(titre, fontsize=10)
        ax.set_title(titre, fontsize=11, fontweight='bold')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)
    
    plt.savefig('analyse_etablissements.png', dpi=300, bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    
    tests = generer_tests()
    resultats = executer_tests(tests)
    resultats_agreges = agreger_resultats(resultats)
    generer_graphiques(resultats_agreges)
    
    print(f"Fichiers générés : analyse_etudiants.png, analyse_etablissements.png ({N_INSTANCES} instances par configuration)")