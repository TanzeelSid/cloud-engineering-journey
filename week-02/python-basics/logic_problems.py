#1. fizzbuzz(n): Return list of strings 1..n
def fizzbuzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result

#2. sum_digits(n): Use a while loop
def sum_digits(n):
    total = 0
    n = abs(n)  # Ensure n is non-negative
    while n > 0:
        total += n % 10
        n //= 10
    return total

#3. reverse_string(s): Use a loop, not slicing
def reverse_string(s):
    reversed_str = ""
    for char in s:
        reversed_str = char + reversed_str
    return reversed_str

#4. is_palindrome(s): Reuse #3
def is_palindrome(s):
    return s == reverse_string(s)

#5. count_vowels(s): Case-insensitive
def count_vowels(s):
    vowels = set("aeiouAEIOU")
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

#6. factorial(n): loop
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

#7. is_prime(n): loop
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

#8. find_largest(lst): No max() 
def find_largest(lst):
    largest = lst[0]
    for num in lst[1:]:
        if num > largest:
            largest = num
    return largest

#9. word_count(text): Return a dictionary
def word_count(text):
    counts = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

#10. classify_numbers(lst): Return {"even": [...], "odd": [...]}
def classify_numbers(lst):
    classified = {"even": [], "odd": []}
    for num in lst:
        if num % 2 == 0:
            classified["even"].append(num)
        else:
            classified["odd"].append(num)
    return classified

# --- Tests ---
assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]
assert sum_digits(4821) == 15
assert reverse_string("cloud") == "duolc"
assert is_palindrome("level") and not is_palindrome("aws")
assert count_vowels("Cloud Engineer") == 6
assert factorial(5) == 120
assert is_prime(13) and not is_prime(15)
assert find_largest([3, 9, 2]) == 9
assert word_count("to be or not to be") == {"to": 2, "be": 2, "or": 1, "not": 1}
assert classify_numbers([1, 2, 3, 4]) == {"even": [2, 4], "odd": [1, 3]}
print("All 10 passed")