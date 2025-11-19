import mariageStable
import calcul_satisfaction
import mariageStable2
from random import randint

def exerciceCM():
    capacity = [1,1,1]
    pref_eleves = [[1,0,2],[0,1,2],[0,1,2]]
    pref_ecoles = [[0,2,1],[1,0,2],[1,0,2]]
    solution = [[0],[1],[2]]
    result = mariageStable.Mariage_stable(capacity=capacity,pref_E=pref_eleves,pref_S=pref_ecoles)
    return result == solution

def exerciceCC():
    pref_eleves = [[1,0,2,4,3],[0,2,1,4,3],[2,0,4,1,3],[2,1,4,3,0],[0,1,2,3,4]]
    pref_ecoles = [[2,0,4,3,1],[1,0,4,3,2],[4,1,2,3,0],[1,0,4,3,2],[2,1,4,3,0]]
    capacity = [1]*len(pref_ecoles)
    solution = [[2],[1],[4],[0],[3]]
    result = mariageStable.Mariage_stable(capacity=capacity,pref_E=pref_eleves,pref_S=pref_ecoles)
    return result == solution


def testCapacityUp():
    capacity = [2,2,2]
    pref_eleves = [[1,0,2],[0,1,2,],[0,1,2],[1,0,2],[0,1,2,],[0,1,2]]
    pref_ecoles = [[0,2,1,3,5,4],[1,0,2,4,3,5],[1,0,2,4,3,5]]
    solution = [{1,2},{4,0},{5,3}]
    result = mariageStable.Mariage_stable(capacity=capacity,pref_E=pref_eleves,pref_S=pref_ecoles)
    set_result = [set(e) for e in result]
    return set_result == solution

def trivial_case_1():
    capacity,pref_E,pref_S = mariageStable.generate_instance([1,1,1,1],etu_size=3)
    result = mariageStable.Mariage_stable(capacity,pref_E=pref_E,pref_S=pref_S)
    return [] in result

def calcul_sat_test_trivial_min_sat():
    scores = calcul_satisfaction.compute_sat_scores([[1,0],[0,1]],[[1,0],[0,1]],[[0],[1]])
    return scores["Avg_schools"] == 0. and scores["Avg_students"] == 0.

def calcul_sat_test_trivial_max_sat():
    scores = calcul_satisfaction.compute_sat_scores([[1,0],[0,1]],[[1,0],[0,1]],[[1],[0]])
    return scores["Avg_schools"] == 1. and scores["Avg_students"] == 1.

def calcul_sat_test_random_val_capacity_1_1():
    scores = calcul_satisfaction.compute_sat_scores([[0, 2, 1], [0, 2, 1], [1, 0, 2]],[[0, 1, 2], [1, 2, 0], [1, 0, 2]],[[0], [2], [1]])
    return scores["Avg_schools"] == 2.5/3. and scores["Avg_students"] == 2.5/3. and scores["Median_schools"] == 1. and scores["Median_students"] == 1.

def calcul_sat_test_random_val_capacity_1_2():
    scores = calcul_satisfaction.compute_sat_scores([[0, 2, 1], [1, 0, 2], [1, 0, 2]],[[1, 0, 2], [2, 0, 1], [2, 1, 0]],[[1], [2], [0]])
    return scores["Avg_schools"] == 2./3. and scores["Avg_students"] == 2./3. and scores["Median_schools"] == 1 and scores["Median_students"] == .5

def calcul_sat_test_random_val_capacity_1_3():
    scores = calcul_satisfaction.compute_sat_scores([[1, 2, 0], [1, 0, 2], [0, 1, 2]],[[1, 0, 2], [1, 2, 0], [0, 2, 1]],[[2], [1], [0]])
    print(scores)
    return scores["Avg_schools"] == 2./3. and scores["Avg_students"] == 2.5/3. and scores["Median_schools"] == 1 and scores["Median_students"] == 1

def calcul_sat_test_random_val_capacity_2():
    scores = calcul_satisfaction.compute_sat_scores([[0, 2, 1], [0, 1, 2], [2, 0, 1], [0, 1, 2], [2, 1, 0], [2, 1, 0]],[[3, 2, 4, 1, 0, 5], [5, 0, 2, 1, 3, 4], [5, 1, 2, 0, 4, 3]],[[1, 3], [4, 0], [2, 5]])
    print(scores)
    return scores["Avg_schools"] == 4./6. and scores["Avg_students"] == 4.5/6. and scores["Median_schools"] == 0.75 and scores["Median_students"] == 1

def sat_test():
    return [calcul_sat_test_random_val_capacity_1_1(),calcul_sat_test_random_val_capacity_1_2(),calcul_sat_test_random_val_capacity_1_3(),calcul_sat_test_random_val_capacity_2(),calcul_sat_test_trivial_max_sat(),calcul_sat_test_trivial_min_sat()]


print(sat_test())
#print(calcul_sat_test_on_random_entry_cap1())
#print(calcul_sat_test_on_random_entry_cap_over1())