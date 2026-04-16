# Iterators vs generators
"""Iterators are objects that implement the iterator protocol, which consists of the methods __iter__() and __next__(). 
They allow you to traverse through all the elements of a collection, such as a list or a tuple. 
Generators, on the other hand, are a special type of iterator that can be created using generator functions or generator expressions. 
They use the yield keyword to produce a sequence of values lazily, meaning they generate values on-the-fly as needed, rather than storing them all in memory at once."""

class iterator_example:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            result = self.data[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration
iterator = iterator_example([1, 2, 3])
for item in iterator:
    print(item)  

# Generator example
def generator_example(n):
    for i in range(n):
        yield i * i 

for value in generator_example(5):
    print(value)    

#when reading a large file, using a generator can be more memory efficient than reading the entire file into memory at once.
def read_large_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()  # Yield one line at a time, stripping whitespace



# Decorators
"""Decorators are a powerful and flexible way to modify the behavior of functions or classes in Python.
They allow you to wrap another function or class, adding functionality before and after the wrapped function is called, without modifying the original function's code.""" 


def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        print("Wrapper executed before {}".format(original_function.__name__))
        args = list(args)
        print(args)
        if len(args)>=2:
            args[0],args[1] = args[1],args[0]
        return original_function(*args, **kwargs)
    return wrapper_function
@decorator_function
def display(a,b,c):
    print(f"Display function executed : {a,b,c}")  
display(1,2,{"a":1})

# Context managers

"""Context managers are a way to manage resources in Python, such as file handling, database connections, or network connections.
They allow you to set up a context for a block of code, ensuring that resources are properly acquired and released, even if an error occurs within the block.
The most common way to create a context manager is by using the with statement, which ensures that the __enter__() and __exit__() methods of the context manager 
are called appropriately."""

with open('example.txt', 'w') as file:
    file.write("Hello, World!")

#more examples of context managers
import contextlib
@contextlib.contextmanager
def open_file(file_path, mode='r'):  
    file = None
    try:
        file = open(file_path, mode)
        yield file  # Yield the file object to the block of code using the context manager
    finally:
        if file:
            file.close()  # Ensure the file is closed after the block of code is executed
with open_file('example.txt', 'w') as file:
    file.write("Hello, World!")



# Multithreading vs multiprocessing vs asyncio
"""Multithreading allows multiple threads to run concurrently within a single process, sharing the same memory space. 
It is suitable for I/O-bound tasks, where the program spends a lot of time waiting for external resources, 
such as file I/O or network requests. However, due to the Global Interpreter Lock (GIL) in Python, 
multithreading may not be effective for CPU-bound tasks, as only one thread can execute Python bytecode at a time.

Multiprocessing, on the other hand, allows multiple processes to run concurrently, each with its own memory space.
It is suitable for CPU-bound tasks, as it can take advantage of multiple CPU cores. 
However, it can be more resource-intensive than multithreading, 
as each process requires its own memory and resources.

Asyncio is a library for writing asynchronous code in Python. It allows you to write concurrent code using the async/await syntax,
which is particularly useful for I/O-bound tasks. Asyncio uses an event loop to manage and schedule tasks, 
allowing you to write code that can handle multiple tasks concurrently without blocking the main thread."""

# Memory optimization
"""Memory optimization in Python can be achieved through various techniques, such as using generators instead of lists 
to generate values on-the-fly, using the __slots__ attribute in classes to reduce memory overhead, and using built-in data 
structures like sets and dictionaries efficiently. Additionally, you can use the sys.getsizeof() function to check the memory
usage of objects and optimize your code accordingly."""
#example of using __slots__ to reduce memory overhead in a class
#how __slots__ works
"""When you define a class in Python, it creates a default __dict__ for each instance, 
which is a dictionary that stores the instance's attributes. This allows for dynamic attribute assignment but can consume more memory.
By using __slots__, you can tell Python to use a more compact internal structure for instances of the class, 
which can save memory by eliminating the need for the __dict__. 
However, this also means that you cannot add attributes to instances of the class that are not defined in __slots__, 
and you cannot use features like weak references or multiple inheritance with classes that use __slots__."""  
class MyClass:
    __slots__ = ['attribute1', 'attribute2']  # Define only the attributes that will be used

    def __init__(self, attribute1, attribute2):
        self.attribute1 = attribute1
        self.attribute2 = attribute2
#example of using sys.getsizeof() to check memory usage of objects in bytes
import sys  
my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] 
my_tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
my_set = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}  
print(sys.getsizeof(my_list))  # Get memory usage of the list object
print(sys.getsizeof(my_set))  # Get memory usage of the list object
print(sys.getsizeof(my_tuple))  # Get memory usage of the list object
#why set is taking more memory than list and tuple
"""A set in Python is implemented as a hash table, which allows for fast membership testing and unique elements. 
However, this implementation can lead to higher memory usage compared to lists and tuples, which are implemented as arrays."""
#why list is taking more memory than tuple
"""A list in Python is a mutable data structure, which means it can be modified after creation
and it can grow or shrink in size. To accommodate this mutability, lists require additional memory 
to store information about the current size, capacity, and other metadata.
On the other hand, a tuple is an immutable data structure, which means it cannot be modified after creation. Since tuples are fixed in size and do not require additional 
memory for metadata, they typically consume less memory than lists."""        

# Logging frameworks
#Logging frameworks in Python, such as the built-in logging module, provide a flexible and configurable way to log messages from your application.
import logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.info("This is an informational message.")
#log into a file
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logging.info("This message will be logged to the file.") 


# Writing REST APIs (FastAPI / Flask)   
#small example of writing a REST API using FastAPI
from fastapi import FastAPI
app = FastAPI()
@app.get("/hello")
def read_root():
    return {"message": "Hello, World!"} 


#small example of writing a REST API using Flask
from flask import Flask, jsonify    
app = Flask(__name__)
@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})



