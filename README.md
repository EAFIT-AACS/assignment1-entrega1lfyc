**Student's full name:** Laura Indabur Garcia and Daniela Salazar Amaya   

**Student's class number:** 7308   

**Operating system:** Windows 11    

**Programming language:** python 3.12.7   

**Tools used:**
  - NumPy library
  - The combinations and zip_longest functions from the itertools module
    
**Instructions to run the code:** If you want to run our code, you just have to make sure you have already installed the NumPy library.

**Description of our algorithm:** Main function: Show you which states are equivalent in a DFA.

**Explanation of the algorithm:**
This algorithm, based on the DFA data provided by the user, creates a state matrix equivalent to the transition table of a DFA. The difference is that, in this matrix, the column corresponding to the states (q) is represented by the row index, storing only the columns of the alphabet.

Once the matrix is constructed, we generate all possible combinations of state pairs from the automaton and initially label them as unmarked. Then, we traverse this list and mark the tuples that contain one final state and one non-final state, as these cannot be equivalent.

After this initial filtering of unmarked, we analyze the remaining tuples to determine the states they transition to under the same input. If any of these tuples are in marked, then the tuple from which it can be reached (i.e., the initial tuple) must also be marked. This process is repeated iteratively until, in a complete traversal of the unmarked elements, no further modifications are made—that is, no more elements are marked.

At the end of the process, the tuples that remain in unmarked represent equivalent states.

In summary, this algorithm implements the minimization algorithm presented in Kozen 1997, Lecture 14

