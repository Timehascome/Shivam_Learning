#list manipulations 
my_list = [1, 2, 3, 4, 5]
my_list.append(6)  # Add an element to the end  
my_list.remove(3)  # Remove an element by value
print("List:", my_list)
print("List Length:", len(my_list))  # Get the length of the list
print("List Slicing:", my_list[1:4])  # Slicing the list
my_list.sort(reverse=True)  # Sort the list in descending order
print("Sorted List:", my_list)  
my_list.pop()  # Remove and return the last element
print("List after pop:", my_list)
sorted_list = sorted(my_list)  # Return a new sorted list
print("New Sorted List:", sorted_list)

#tuple manipulations
my_tuple = (10, 20, 30, 40, 50) 
print("Tuple:", my_tuple)
print("Tuple Length:", len(my_tuple))  # Get the length of the tuple
print("Tuple Slicing:", my_tuple[1:4])  # Slicing the tuple 
print("Tuple Index of 30:", my_tuple.index(30))  # Get the index of an element
print("Tuple Count of 20:", my_tuple.count(20))  # Count occurrences of an element
#my_tuple.remove(20) and pop  # This will raise an error as tuples are immutable

# Dictionaries manipulations
my_dict = {'a': 1, 'b': 2, 'c': 3}
my_dict['d'] = 4  # Add a new key-value pair        
print("Dictionary:", my_dict)
print("Dictionary Length:", len(my_dict))  # Get the length of the dictionary           
del my_dict['b']  # Remove a key-value pair by key
print("Dictionary after deletion:", my_dict)        
print("Dictionary Keys:", my_dict.keys())  # Get all keys
print("Dictionary Values:", my_dict.values())  # Get all values
print("Dictionary Items:", my_dict.items())  # Get all key-value pairs   
   
# Set manipulations
my_set = {1, 2, 3, 4, 5}        
my_set.add(6)  # Add an element to the set  
print("Set:", my_set)
print("Set Length:", len(my_set))  # Get the length of the set
my_set.remove(3)  # Remove an element from the set  
print("Set after removal:", my_set) 
my_set.update({7, 8, 9})  # Add multiple elements to the set
print("Set after update:", my_set)  
print("Set Contains 4:", 4 in my_set)  # Check if an element is in the set
print("Set Contains 10:", 10 in my_set)  # Check if an element is in the set
print("Set as List:", list(my_set))  # Convert set to list
print("Set as Tuple:", tuple(my_set))  # Convert set to tuple       
print("Set as Dictionary Keys:", dict.fromkeys(my_set, 0))  # Convert set to dictionary keys with default value 0       
print("Frozen Set:", frozenset(my_set))  # Create a frozenset from the set

