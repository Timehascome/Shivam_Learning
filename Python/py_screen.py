# Topics:
# List comprehension
# Enumerate
# Zip
# Counter
# defaultdict
# String slicing
# Join / split
# Sorted with key

# Practice problems:
# Reverse a string
# Check palindrome
# Find duplicates in array
# First non-repeating character
# Count frequency of characters

# Reverse a string
def reverse_string(s):
    for i in range(len(s) - 1, -1, -1):
        print(s[i], end="")
print(reverse_string("Hello, World!"))
# Check palindrome
def is_palindrome(s):
    return s == s[::-1]
print(is_palindrome("madam"))
print(is_palindrome("hello"))   
# Find duplicates in array
def find_duplicates(arr):
    from collections import Counter
    count = Counter(arr)
    return [item for item, freq in count.items() if freq > 1]
print(find_duplicates([1, 2, 3, 4, 2, 5, 1]))
# First non-repeating character
def first_non_repeating(s):
    from collections import Counter
    count = Counter(s)
    for char in s:
        if count[char] == 1:
            return char
print(first_non_repeating("sanjanashivaji")) 
# Count frequency of characters
def count_frequency(s):
    from collections import Counter
    return dict(Counter(s))     
print(count_frequency("hello world"))

# Problems using two pointers:
#============================#
# Two Sum (sorted array)
def two_sum_sorted(arr, target):
    n=len(arr)
    left, right = 0, n - 1
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return [arr[left], arr[right]]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
print(two_sum_sorted([1, 2, 2, 4, 5], 4))            
# Remove duplicates from sorted array
def remove_duplicates(arr):
    if not arr:
        return 0
    i, j = 0, 1
    while j < len(arr):
        if arr[i] != arr[j]:
            i =j
            j=i+1
        else:
            arr.remove(arr[j])    
    return arr        
print(remove_duplicates([1, 1, 2, 2, 3, 4, 4,5,5]))

# Reverse words in string without using [::-1]
def reverse_words(s):
    words = s.split()
    reversed_word = ""
    for word in words:
        reversed_word = word + " " + reversed_word
    return reversed_word
print(reverse_words("Hello World I am cool"))

# Valid palindrome ignoring symbols
def is_valid_palindrome(s):
    filtered_s = ''.join(char.lower() for char in s if char.isalnum())
    print(filtered_s)
    print(filtered_s[::-1])
    return filtered_s == filtered_s[::-1]   
print(is_valid_palindrome("A man5 , a plan, a canal: Pa5nama"))

# Move zeros to end
def move_zeros(arr):
    nz=0
    for i in range(len(arr)):
        if arr[i] != 0:
            arr[nz] = arr[i]
            nz += 1
    for i in range(nz, len(arr)):
        arr[i] = 0 
    return arr             
print(move_zeros([0, 1, 0, 3, 12]))



#problems using sliding window:
# Longest substring without repeating characters
# Maximum sum subarray of size k
# Minimum window substring
# Longest repeating character replacement
# Count substrings with k distinct characters

#problems using HashMap / Dictionary Pattern
# Problems:
# Two Sum
# Group anagrams
# Longest consecutive sequence
# Top K frequent elements
# Valid anagram
