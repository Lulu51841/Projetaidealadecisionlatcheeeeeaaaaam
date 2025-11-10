from random import randint

def Mariage_stable(capacity,pref_E,pref_S):
    #est-ce que on doit avoir tout les étudiants qui classent toutes écoles et vis-versa ?
    #préférences_E (resp. préférence_pref_S) est une liste de liste tq la sous_liste i contient les préférences de l'étudiant (resp. l'école) i
    #capacité est la capacité des écoles, c'est une liste
    #Le résultat est une liste de liste correspondant a la liste des étudiants choisis par chaque école
    if(len(pref_E)-1 < max([max(p) for p in pref_S])):
        raise Exception("Mauvaise entrée, taille de l'attribut Pref_E incohérente avec les nombres présents dans l'attributs pref_S")
    if(len(pref_S)-1 < max([max(p) for p in pref_E])):
        raise Exception("Mauvaise entrée, taille de l'attribut Pref_S incohérente avec les nombres présents dans l'attributs pref_E")
    currently_choosen = [False]*len(pref_E) #vaut vrai si les étudiants sont choisis ou si ils ont épuisé leurs préférences
    current_student_in_school = [[] for i in range(len(pref_S))]#On veut garder chaque sous liste triée par préférence de l'école
    while (currently_choosen != [True]*len(pref_E)): #Tant que tout le monde n'est pas choisi et que les préférences ne sont pas épuisées
        demandes = [ [] for i in range(len(pref_S))]
        for i in range(len(pref_E)):
            if( not(currently_choosen[i])):
                choosen_school = pref_E[i][0]
                #print("pref : "+str(pref_E[i][0])+" , liste correspondante : "+str(demandes[(pref_E[i][0])]))
                demandes[choosen_school].append(i)
                pref_E[i].pop(0)#On retire l'école de la liste des préférences car elle ne sera jamais réutilisé
                if(pref_E[i] ==[]):
                    currently_choosen[i]=True
        #Check if i is accepted somewhere
        #print("les demandes des étudiants sont : "+str(demandes))
        for i in range(len(pref_S)):
            for j in range(len(demandes[i])):
                etu = demandes[i][j]
                if(len(current_student_in_school[i]) < capacity[i]):
                    current_student_in_school[i].append(etu)
                    currently_choosen[etu] = True
                else :
                    #comparaison de préférence des écoles
                    if(etu in pref_S[i] and pref_S[i].index(current_student_in_school[i][-1]) > pref_S[i].index(etu)):
                        #on supprime le dernier element et on place le nouveau a sa place en fonction des préférences de l'école
                        dropped_stud = current_student_in_school[i].pop(-1)
                        if(pref_E[dropped_stud] != []):
                            currently_choosen[dropped_stud] = False
                        currently_choosen[etu] = True
                        for e in range(len(current_student_in_school[i])-1,-1,-1):
                            if(pref_S[i].index(e) < pref_S[i].index(etu)):
                                current_student_in_school[i].insert(e-1,etu)
                            elif(e==0):
                                current_student_in_school[i].insert(0,etu)
                        if(len(current_student_in_school[i]) == 0):
                            current_student_in_school[i].append(etu)
                        #print("étudiants classé : "+str(currently_choosen))

        #print("choix des écoles : "+str(current_student_in_school))
        #print("préférences des étudiants : "+str(pref_E))
    return current_student_in_school

def generate_instance(capacity,etu_size):
    school_size = len(capacity)
    pref_S = []
    for s in range(school_size):
        pref_size = randint(1,etu_size)
        pref_S.append([])
        for e in range(pref_size):
            r = randint(0,etu_size-1)
            while r in pref_S[s]:
                r = randint(0,etu_size-1)
            pref_S[s].append(r)
    pref_E = []
    for e in range(etu_size):
        pref_size = randint(1,school_size)
        pref_E.append([])
        for s in range(pref_size):
            r = randint(0,school_size-1)
            while r in pref_E[e]:
                r = randint(0,school_size-1)
            pref_E[e].append(r)
    return capacity,pref_E,pref_S