
def computeAvgSkill(set):
    return sum(x.skill for x in set)/len(set)

def computeAvgSalary(set):
    return int(sum(x.salary for x in set)/len(set))

def computeAvgGradeDist(set):
    gradeDist = {}
    for x in set:
        if x.average_grade not in gradeDist:
            gradeDist.update({x.average_grade : 1})
        else:
            gradeDist.update({x.average_grade : gradeDist.get(x.average_grade)+1})
    for grade, amt in gradeDist.items():
        gradeDist.update({grade : int((amt/len(set))*100)})
    return gradeDist