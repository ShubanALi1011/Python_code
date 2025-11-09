class Company:
    # Class Attribute (shared by all objects)
    company_name = "AlienXoft"   # public class attribute
    _industry = "Software"       # protected class attribute
    __headquarters = "Pakistan"  # private class attribute

    def __init__(self, id, revenue):
        # Instance Attributes
        self.id = id                # public
        self._revenue = revenue     # protected
        self.__secret_code = 12345  # private

    # ---------------- Instance Method ----------------
    def print_info(self):
        print(f"ID: {self.id}")
        print(f"Revenue: {self._revenue}")
        print(f"Company Name: {Company.company_name}")
        print(f"Industry: {Company._industry}")
        print(f"Headquarters: {Company._Company__headquarters}")  # access private class attr
        print(f"Secret Code: {self.__secret_code}")               # private instance attr

    # ---------------- Class Method ----------------
    @classmethod
    def set_company_name(cls, new_name):
        cls.company_name = new_name

    @classmethod
    def get_headquarters(cls):
        return cls.__headquarters  # access private class attr

    # ---------------- Static Method ----------------
    @staticmethod
    def calculate_profit(revenue, cost):
        return revenue - cost

    # ---------------- Property / Getter / Setter / Deleter ----------------
    # Protected revenue attribute
    @property
    def revenue(self):
        return self._revenue

    @revenue.setter
    def revenue(self, value):
        if value >= 0:
            self._revenue = value
        else:
            print("Revenue cannot be negative!")

    @revenue.deleter
    def revenue(self):
        print("Deleting revenue...")
        del self._revenue

    # Private secret code
    @property
    def secret_code(self):
        return self.__secret_code

    @secret_code.setter
    def secret_code(self, value):
        if isinstance(value, int):
            self.__secret_code = value
        else:
            print("Secret code must be an integer!")

    @secret_code.deleter
    def secret_code(self):
        print("Deleting secret code...")
        del self.__secret_code


# ---------------- Usage Example ----------------
# Creating Objects
c1 = Company(1, 100000)
c2 = Company(2, 250000)

# Access Instance Method
c1.print_info()
print("-----------")

# Access Class Method
Company.set_company_name("AlienXoft AI")
print(Company.company_name)

# Access Static Method
profit = Company.calculate_profit(50000, 15000)
print("Profit:", profit)

# Access Property (Getter / Setter)
print("Revenue before:", c1.revenue)
c1.revenue = 120000
print("Revenue after:", c1.revenue)

# Delete Revenue
del c1.revenue

# Access Private Attribute using Property
print("Secret Code:", c1.secret_code)
c1.secret_code = 99999
print("Secret Code updated:", c1.secret_code)
del c1.secret_code
