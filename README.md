## Vaishvik Brahmbhatt vbrahmb2@stevens.edu
## Venkata Santosh Gouranga Khande vkhande4@stevens.edu
#### GitHub URL: https://github.com/vaishvik24/CS515-Project2-BC-calculator

# CS 515: Project 2 - BC Calculator 🎮 

##  ⏰ Estimated hours: 33 hours

| Hours |                 Work                  |
|-------|:-------------------------------------:|
| 2     |    planning and managing the tasks    |
| 4     |    reading and understanding flow     |
| 12    |        implementing base flow         |
| 6     |       implementing 4 extensions       |
| 5     |    modification & refactoring code    |
| 2     |   testing code along with bug fixes   |
| 2     | creating README doc and GitHub set up |

##  🧪 Testing

- I started testing parallely while developing. Once, I write any function, I write `doctests` for the function and test the all possible outcomes. It helped me to fix runtime errors during coding phase.
- Once, the base flow was ready, I started testing with various of different arithmetics statements and fixed major of them. This was the overall base flow testing, not just a function or specific use-case. 
- The, I started implementing extensions. I did the testing for the extensions in a same way as base flow. Once, all the extensions were tested, I did base flow testing once again just to make sure it does not affect the original flow. 
- The code was tested for happy cases flow, then I added incomplete statements just to check that it does not fail for that.  I've covered major of corners cases and code was working with expectations of baseline as well as extensions too.

## 🐛 Bugs/Issues

- The latest code has no bugs or issues identified during overall testing.
- Future improvement: The if-else, loops, functions and many things can be added to current codebase.

## 💡 Example of issues/bugs and solution for it

- During testing, I found many of the issues/bugs which were difficult to solve. I've highlighted some below:
1. For unary operation, My code was failing if I've input with negative numbers (unary operation). The fix was a bit time-confusing for me. As the fix took me to change the code. The main issue was because of `-` can be used as subtraction operator as well as represent negative numbers too. Later, I found the fix for it and issue was resolved.
2. Another issue was with post and pre increment/decrement (`++` and `--`). The main reason behind failure was it has to attached with variable or number, not with any other operator or expression. In order to fix it, I need to keep track of prev parsed token. That was a bit difficult to fix when inputs are complex with parenthesis. But, with the help of TA, I found the fix and it worked in the end. 
3. The one issue was with boolean operator when the operator is `!` negate. We might've inputs like `!!!!!!1`. My code was failing for this case at the start. I brainstromed the idea because I was using 2 stacks and I forgot to add a conditions when stack is empty. Later, this fix worked and the inputs with multiple operators passed. 

## 🧩 Extensions:
I've implemented 4 extensions. 
Each extension is described as below:
### Op-equals:
- Op-equals extension helps us to evaluate the expressions containing  +=, -=, *=, /=, %= and ^= operators. In the bc_parser, each line is checked whether it contains the above mentioned operators. if yes, it is directed to operator parser function to strip the whitespaces and validate the string contains alphanumeric characters. It returns the processed string and passed into bc_calculator function as an input argument
- The next step is identifying the operator in the string and performing the operation accordingly and storing the updated variable name and its value in VARIABLES dictionary which created at the beginning. All operators are stored in stacks and validated using BODMAS rules. Error handling is done for this case when invalid operators such as '++' or '--' are present. it catches in excpetion it can be used only on variables.
- Test cases for this extension: 
1. x=1<br>
x+=10<br>
print x<br>
-> 11.0<br><br>
2. x=3<br>
y=4<br>
z=x*y<br>
print x,y,z<br>
z*=2<br>
print z<br>
-> 3.0 4.0 12.0<br>
24.0<br><br>
3. x=12<br>
x^=2<br>
print x<br>
x/=3<br>
print x<br>
x%=5<br>
print x<br>
-> 144.0<br>
48.0<br>
3.0<br><br>
4. x=13<br>
x=*2<br>
print x<br>
-> parse error<br><br>
5. x=-4<br>
x*=-4<br>
print x<br>
-> 16.0<br><br>
6. a=12<br>
b=-4<br>
b-+=5<br>
print b<br>
-> parse error


### Binary Operators:
- Binary operations extension evaluates the input statements which contain mathematical expressions having ['&', '|', '!'] this operators. in each input line, the operators are recognized and stored in operators stacks, the line passed into bc_parser and then the variables are recognized and the experssion is evaluated using apply_operation(a,b,op) function which return the value.
- In the bc_evaluator() function, the input is validated by checking whether the constant is present in variables dict and then access its value and perform the operation and then update the variable value in the dictionary. Error handling is done for this extension by catching error when input line contains '&&&' or '|||' in the expression since its valid only for binary and logic operations. For an expression to be evaluated, variable values stored in stacks are popped out and even the operator and then those are passed into apply_operation() function. 
- In this way, the extension works and no errors have been found since every possibility is tried and the errors are caught and displayed when given invalid inputs
- Test cases for this extension:
1. x=5<br>
y=0<br>
print x&&y, x||y, !x<br>
-> 0 1 0<br><br>
2. x=20<br>
y=5<br>
print x&y, x&&&y, x|||y<br>
-> parse error<br><br>
3. print 1 && 2, 2 && 1, -5 && 1, 0 && -100<br>
-> 1 1 1 0

### Comments:
- Comments extension helps us to identify whether the input given is markdown or not. Using is_commented(statement) function, it returns whether it starts with '/*' or # and it passed to new_commented_line(i, statements) function where it returns the current index of input statements. 
- Till the line contains "*/" the i index increments making the parser to ignore the lines whatever given in between /* and /*. In this way the extension works and ignores the commented input lines. The comment is recognized even with '#' symbol. One or more symbols can be considered as the comment and the commands won't execute post the symbol. In this way, this extension works
- Test cases for this extension:
1. a=20<br>
/*<br>
a+=3<br>
a*=4<br>
b=6<br>
*/<br>
print a,b<br>
-> 20.0 0.0<br><br>
2. x=5<br>
\/*<br>
x+=4<br>
print x<br>
\/*<br>
print x<br>
-> No output since the comment is not closed with '*/'<br><br>
3. x=6<br>
\# x+=9<br>
\## x+=8<br>
print x<br>
-> 6.0<br><br>


### Relational Operations:
- Relational operations extension evaluates the input statements which contain ['==', '<=', '>=', '!=', '<', '>'] this operators. Every operation returns the boolean value and is checked between two variables. The input line is checked whether it contains any of the above operators using the is_relational_cond() condition which is used in the bc_parser() function. Then, it is checked whether it contains any variables which are not defined. 
- It is then passed into relational_cond_var() function to collect variable and the value present in the relation. After processing the input and then getting the variable and the value from the function, these two are passed into bc_evaluator function and it is evaluated inside the function. 
- Error handling is done for this Extension catching Zero division error and Parsing error. In this way this extension is implemented. 
- Test cases for this extension:
1. x=10<br>
y=4<br>
print x==y<br>
-> 0.0<br><br>
2. x=5<br>
y=6<br>
print y>x<br>
-> 1.0<br><br>
3. x=12<br>
y=43<br>
print x==>y<br>
-> parse error<br><br>
4. x=12<br>
y=43<br>
print x!=y<br>
-> 1.0<br><br>

## 🏃‍Run Guide

- Install python 3 in your machine
- Read README.md file to get more context of the project
- Inputs to the code is given by stdin
   ```shell
   $ python3 bc.py < input_statements.txt
   ```
  Here, input_statements.txt consists bunch of arthemtic statements which is passed to the BC calculator code.
