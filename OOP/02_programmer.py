class Programmer:
    company = "Devsinc"
    def __init__(self, dep, name, salary):
        self.dep = dep
        self.name = name
        self.__salary = salary

    @staticmethod
    def getSalary():
        # return self.__salary
        print('Printing Salary')

shuban = Programmer("AI/ML", "Shuban Ali",'250k')
print("Company : ",shuban.company," | " "Department : ",shuban.dep,"  |   ","\nName : ",shuban.name,"   |   ","Salary : ",shuban.getSalary() )
shuban.getSalary()