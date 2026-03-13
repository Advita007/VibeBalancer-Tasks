from math import *
n = int(input("Enter the no. of elements you want to input: "))
my_list = []
primes_list = []
for index in range(n):
    my_list.append(int(input()))
max = 0
min = 0
sum = 0
sum_squares = 0
for index in range(n):
    flag = 0
    if(my_list[index]>my_list[max]):
        max = index
print("The largest number is",my_list[max])
for index in range(n):
    if(my_list[index]<my_list[min]):
        min = index
print("The smallest number is",my_list[min])
for index in range(n):
    sum += my_list[index]
print("Sum of the numbers is",sum)
for index in range(n):
    sum_squares += pow(my_list[index],2)
print("Sum of the squares of all numbers is",sum_squares)
 
for index in range(n):
    flag = 0
    for value in range(2,int(sqrt(my_list[index]))+1):
        if my_list[index]%value == 0:
            flag = 1
    if my_list[index]!=1 and flag != 1:
            primes_list.append(my_list[index])

unique_primes = list(set(primes_list))
print(unique_primes)
