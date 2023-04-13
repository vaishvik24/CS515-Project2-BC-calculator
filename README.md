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

### Binary Operators:
- todo

### Comments:
- todo

### Relational Operations:
- todo

## 🏃‍Run Guide

- Install python 3 in your machine
- Read README.md file to get more context of the project
- Inputs to the code is given by stdin
   ```shell
   $ python3 bc.py < input_statements.txt
   ```
  Here, input_statements.txt consists bunch of arthemtic statements which is passed to the BC calculator code.
