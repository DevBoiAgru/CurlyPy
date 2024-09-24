# This code was translated to Python from Brython
true = True
false = False
# Sample file
# Simple function
def HelloWorld(name: str) :
   if name :
      print (f"Hello {name}!") 		# f-strings support semicolons
   else :
      print ("Hello World!")
name: str=input("What is your name?: ")
HelloWorld(name)
# For loop
for n in range(10):
   if n % 3 == 0 and n % 5 == 0 :
      print("FizzBuzz")
   elif n % 3 == 0 :
      print("Fizz")
   elif n % 5 == 0 :
      print("Buzz")
   else:
      print(n)
# Dictionary is defined using type hints
dictionary_test: dict[str, str] = {"foo":"bar", "baz":"qux"}
print(dictionary_test["foo"])