class Employee:
    language = "urdu"  # class variable
    
    def __init__(self, name, pos, salary):
        self.name = name
        self._pos = pos          # protected variable
        self.__salary = salary   # private variable

    # Getter for private salary
    def get_salary(self):
        return self.__salary


shuban = Employee("Shuban Ali", "Graphic Designer", 30000)
nazish = Employee("Nazish Jabbar", "HR Manager", 40000)
zaid = Employee("Zaid Khan", "IT Manager", 100000)

print("Shuban :-", shuban.name, "--", shuban._pos, "-", shuban.get_salary(), "-", shuban.language)
