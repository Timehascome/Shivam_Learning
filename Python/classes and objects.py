#we practice classes and objects in python**********
class Dog:
    #class attribute
    species = "Canis familiaris"

    #initializer / instance attributes
    def __init__(self, name, age):
        self.name = name
        self.age = age

    #instance method
    def description(self):
        return f"{self.name} is {self.age} years old"

    #another instance method
    def speak(self, sound):
        return f"{self.name} says {sound}"  
#creating instances of the Dog class
mikey = Dog("Mikey", 6)         
print(mikey.description())  # Output: Mikey is 6 years old
print(mikey.speak("Woof Woof"))         # Output: Mikey says Woof Woof
jane = Dog("Jane", 4)
print(jane.description())   # Output: Jane is 4 years old   
print(jane.speak("Bark Bark"))         # Output: Jane says Bark Bark
#accessing class attribute
print(f"{mikey.name} is a {mikey.species}")  # Output: Mikey is a Canis familiaris
print(f"{jane.name} is a {jane.species}")      # Output: Jane is a Canis familiaris 

#now we learn about inheritance****************
class Bulldog(Dog):
    def run(self, speed):
        return f"{self.name} runs {speed}"      
#creating an instance of the Bulldog class
jim = Bulldog("Jim", 5)     
print(jim.description())  # Output: Jim is 5 years old
print(jim.speak("Woof"))         # Output: Jim says Woof        
print(jim.run("slowly"))        # Output: Jim runs slowly
print(f"{jim.name} is a {jim.species}")  # Output: Jim is a Canis familiaris

 #we practice encapsulation**************
class Cat:
    def __init__(self, name, age):
        self.__name = name  # private attribute
        self.__age = age    # private attribute

    # getter method for name
    def get_name(self):
        return self.__name

    # getter method for age
    def get_age(self):
        return self.__age

    # setter method for age
    def set_age(self, age):
        if age > 0:
            self.__age = age
        else:
            print("Please enter a valid age")       


#creating an instance of the Cat class 
whiskers = Cat("Whiskers", 3)
print(whiskers.get_name())  # Output: Whiskers      
print(whiskers.get_age())   # Output: 3
whiskers.set_age(4)
print(whiskers.get_age())   # Output: 4
whiskers.set_age(-1)        # Output: Please enter a valid age

#we practice polymorphism******************
class Bird:
    def speak(self):
        return "Chirp Chirp"    
class Fish:
    def speak(self):
        return "Blub Blub"  
#function that takes an object and calls its speak method
def animal_sound(animal):
    print(animal.speak())       
#creating instances of Bird and Fish
parrot = Bird()     
goldfish = Fish()  
animal_sound(parrot)    # Output: Chirp Chirp   
animal_sound(goldfish)  # Output: Blub Blub

#we practice abstraction
from abc import ABC, abstractmethod 
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass        
class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)           
#creating an instance of Rectangle
rect = Rectangle(5, 10) 
print(f"Area: {rect.area()}")          # Output: Area: 50
print(f"Perimeter: {rect.perimeter()}")  # Output: Perimeter: 30

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

    def perimeter(self):
        return 2 * 3.14 * self.radius       
#creating an instance of Circle
circ = Circle(7)        
print(f"Area: {circ.area()}")          # Output: Area: 153.86
print(f"Perimeter: {circ.perimeter()}")  # Output: Perimeter: 43.96     



