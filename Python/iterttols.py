        # we learn itertools module
        
import itertools    
# Example: Using itertools to create a Cartesian product of two lists
list1 = [1, 2]  
list2 = ['a', 'b']  
cartesian_product = list(itertools.product(list1, list2))   
print("Cartesian Product:", cartesian_product)
#we do tuple packing and unpacking using cartesian product
a, b = cartesian_product[0]  # Unpacking the first tuple    
print("Unpacked values:", a, b)