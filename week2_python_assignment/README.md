### ***Task 2 - File Handling, Problem Solving and OOP in Python***

______________
### File Handling:
  * #### A file `data.txt` is created using the `open()` function with the second parameter as `"w"`.
  * #### Usind the `write()` function, we write various lines of text into the file - `data.txt1`.
  * #### We close this file using `close()`.
  * #### To read the newly created file we use `"r"` as the 2nd paraemter in the open function (since we want a read-only mode) and then using the `read()` function we print out all the content into the console. 

### Problem Solving:
   * #### The user is asked for the no. of reqd elements in the list using the `input()` function. A for loop is then used to take that many inputs from the user and append it to an empty list in each of its iteration.
   * #### For finding the max/min, we set the max/min to the first element and then iterate through the list, updating their value if a number satisfies the given condition. These values are printed at the end of both iterations. 
   * #### For finding the sum of all numbers as well as their squares we initialise variables `sum = 0, sum-squares = 0`, and then keep adding each element of the list/its square in each iteration. These values are printed at the end of both iterations. 
   * #### We check the condition for prime for each element and append it to a new list of primes if it satisfies the condition. (A `break` function could be used after flag is set to 1 instead of continuing the iterations).
   * #### Any duplicates are removed and the final primes list is printed. 

### OOP:
* #### A student class is made with all the specified attributes, and an object function to check if the student has passed acc to marks is defined in the class. 
* #### Variables asking for inputs are defined and passed as the attrbiutes of a student object.
* #### The object function is called to check if passed. 
