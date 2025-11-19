import mariageStable
import mariageStable2
import statistics

def sort_affectation(to_sort,order):
    result = []
    for i in order:
        if i in to_sort:
            result.append(i)
    return result


def compute_sat_scores(pref_E,pref_S,affectation):
    #Note : Le programme implose si on lui donne qu'une seule école ou qu'un seul étudiant
    L_students, L_schools = [-1]*len(pref_E), []
    for l in range(len(affectation)):
        affectation_length = len(affectation[l])
        if affectation_length != 0:
            sum_of_position = 0
            #sorted_list = sort_affectation(affectation[l],pref_S[l])
            for i in range(affectation_length):
                student_id = affectation[l][i]
                temp_school_pref = []#liste des préférences de l'école l moins les valeurs affectées a l'école l + la valeur i
                for x in pref_S[l]:#Il y a une optimisation a faire içi juste le fait pas faite parceque la prof a dit que ça l'interessait pas et ca rend le code moins clair
                    if not(x in affectation[l]) or x == student_id:
                        temp_school_pref.append(x)
                sum_of_position += ((len(temp_school_pref)-1) - temp_school_pref.index(student_id)) / float(len(temp_school_pref)-1) #Il est aussi possible de faire nb tot élèves - position
                stud_score = (len(pref_E[student_id])-1) - pref_E[student_id].index(l)#nombre d'école dans la liste de préférence de l'étudiant e - position de l'école choisie
                if(L_students[student_id] == -1):
                    L_students[student_id] = stud_score/float(len(pref_E[student_id])-1)
                else :
                    print("Il semblerait qu'un étudiant soit affecté deux fois dans la liste finale")
            L_schools.append((sum_of_position/float(affectation_length)))#On enlève 1 a la taille de la liste a chaque fois pour que le score le plus bas possible soit 0 et pas (n-1)/n
        else :
            L_schools.append("L'étudiant n'avait sélectionner aucune école")
    return {"Avg_schools" : sum(L_schools)/float(len(L_schools)), "Median_schools" : statistics.median(L_schools), "Avg_students" : sum(L_students)/float(len(L_students)), "Median_students" : statistics.median(L_students)}