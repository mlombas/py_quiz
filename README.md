# Py Quiz Server

A server that runs and lets people create accounts, and
then use that accounts to solve problems about
python and earn points with them.

The problems are described using a mini-language described
below

## The problem mini-language

The problem code is divided in several _sections_. To use
these sections, you first write the section name and
then, indented, the section code. For more information,
see the examples below.
Any line starting with a # is considered a comment
Current supported _sections_ are:
* `statment`:

   The text that the user can read and will need in 
   order to solve the problem.

   For example:
   ```
   statment:
      Write a line of code that calculates the average of a and b
   ```

* `variables':

   This section holds variables that are defined beforehand
   and are needed to solve the problem. Variables are defined
   by python expressions. If some module were needed (like
   random) specify it in the `initialization` section.
   If you add a comment after a variable definition, then
   the variable will have that as its description. If not,
   it will have its type.

   For example:
   ```
   variables:
      #These are fixed-value variables
      s = "I am a string variable"
      #You can have booleans too
      #Also, this will appear as "b: A boolean" in the description
      b = True #A boolean
      #You can use modules too!
      a = random.uniform(-100, 10023)
      #You can also use variables defined in initialization
      s2 = answer_to_the_universe / 2
   ```

* `initialization`:
   
   Simply a python code snippet that will run before
   the variables in `variables` are defined and, of
   course, before the user code is run. Use it to 
   import modules or define extra variables you
   dont want the user to be aware of.
   
   For example:
   ```
   initialization:
      import random
      from math import pi
      answer = 42 #User wont be aware of this
   ```

* `check`:

   This section is what the problem should output. This must contain
   a single python expression that returns either True or False.
   There is a special variable defined, result, which holds
   the result of the evaluation of the code submitted by the user

   For example:
   ```
   check:
      abs(a - result) == abs(b - result)
   ```

So, a full example would be:
```
#Note that the sections need not to be in any specific order
statment:
   Write a line of code that calculates the average of a and b
variables:
   a = random.uniform(-1e6, 1e6) #A random number
   b = random.uniform(-1e6, 1e6) #A random number
initialization:
   import random
check:
   abs(a - result) == abs(b - result)
```
