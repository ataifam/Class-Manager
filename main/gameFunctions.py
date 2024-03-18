from .models import Student, Teacher

def computeAvgSkill(set):
    if len(set) == 0: 
        return 0
    return round(sum(x.skill for x in set)/len(set), 1)

def computeAvgSalary(set):
    if len(set) == 0: 
        return 0
    return int(sum(x.salary for x in set)/len(set))

def computeAvgGradeDist(set):
    gradeDist = {}
    if not len(set) == 0: 
        for x in set:
            if x.getLetterGrade() not in gradeDist:
                gradeDist.update({x.getLetterGrade() : 1})
            else:
                gradeDist.update({x.getLetterGrade() : gradeDist.get(x.getLetterGrade())+1})
        for grade, amt in gradeDist.items():
            gradeDist.update({grade : round((amt/len(set))*100, 1)})
    return gradeDist

def computeFinancials(school):
    teachers = Teacher.objects.filter(school_id=school.id)
    studentCount = Student.objects.filter(school_id=school.id).count()
    tuition = school.tuition

    profit = tuition*studentCount
    losses = sum(teacher.salary for teacher in teachers)

    return profit-losses