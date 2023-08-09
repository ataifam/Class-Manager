
def computeAvgSkill(set):
    return round(sum(x.skill for x in set)/len(set), 1)

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
        gradeDist.update({grade : round((amt/len(set))*100, 1)})
    return gradeDist