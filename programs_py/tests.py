import mariageStable

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