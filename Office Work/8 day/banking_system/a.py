class Person:
    def greet(self, name):
        print(f"Hello, {name}. I'm {self}")

p = Person()

Person.greet(p, "Alex")
