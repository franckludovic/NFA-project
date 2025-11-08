# Project: Regular Expression to NFA Converter

This project is about creating a Python program that can take a regular expression as input, convert it into a Non-deterministic Finite Automaton (NFA), and then display that NFA visually as a graph.

Here you will find the documentation of each file in the project, why it exists, the output and input expected from every file, the methods and classes that should be present in the file, their data type and their return type, and some naming conventions we will use.



## 1. preprocessor.py

### Purpose of this File
This file acts as a translator. In a standard regular expression, the "and then" (concatenation) is implicit. When we write ab, we understand it means "an a followed by a b". Our parser, however, needs an explicit operator for every action. The job of this file is to take the raw regex and insert a dedicated character (we will use .) to represent "followed by". This makes the next step, parsing, much more straightforward.

### How It Works (The Core Logic)
The function will iterate through the input regex string, looking at the current character and the one immediately following it. A concatenation operator (.) needs to be inserted only if a specific set of conditions is met.

A . should be inserted between characters x and y (in the sequence ...xy...) if:
- x is a normal character and y is a normal character (e.g., ab -> a.b).
- x is a normal character and y is an opening parenthesis ( (e.g., a(b) -> a.(b)).
- x is a closing parenthesis ) and y is a normal character (e.g., (a)b -> (a).b).
- x is a Kleene star * and y is a normal character (e.g., a*b -> a*.b).
- x is a Kleene star * and y is an opening parenthesis ( (e.g., a*(b) -> a*.(b)).
- x is a closing parenthesis ) and y is an opening parenthesis ( (e.g. (a)(b) -> (a).(b)).

The logic must be careful not to insert a . in places where it would be incorrect, such as after a ( or before/after a |.

### Functions to Create
#### insert_concatenation_operator(regex_string)

**Function Signature:**
```python
def insert_concatenation_operator(regex_string: str) -> str:
```

**Input Parameter:**
- **regex_string:** Data Type: str (string). Description: The raw, original regular expression string exactly as the user typed it.
  - Example Input 1: "ab|c"
  - Example Input 2: "(a|b)*c"

**Output (Return Value):**
Data Type: str (string). Description: A new string containing the same regular expression, but with the explicit . concatenation operator added in all the correct places.
- Example Output 1 (for "ab|c"): "a.b|c" (Notice the . is only between a and b, not near the |).
- Example Output 2 (for "(a|b)*c"): "(a|b)*.c" (Notice the . is between the * and c).

### Naming Conventions for this File
- Variables: snake_case (e.g., processed_regex, current_char).
- Functions: snake_case (e.g., insert_concatenation_operator).





## 2. parser.py

### Purpose of this File
This file acts as a reorganizer. The regular expression we have after preprocessing (e.g., (a|b)*.c) is still in a "human-readable" format called infix notation. This format uses parentheses and operator precedence rules (* before ., . before |) which can be complex for a computer to handle directly during the construction phase. The purpose of this file is to convert that infix string into postfix notation (also known as Reverse Polish Notation).


### How It Works (The Core Logic)
This file will implement the Shunting-Yard Algorithm. You can visualize it as having two main areas: an output queue (where the final postfix string is built) and an operator_stack (a temporary holding area for operators like |, ., *).
The algorithm reads the preprocessed infix string one character at a time:
- If it sees an operand (a letter like a), it immediately adds it to the output.
- If it sees an operator (like . or |), it checks the operator_stack. It pops any operators from the stack that have a higher or equal precedence and moves them to the output, before finally pushing the new operator onto the stack.
- If it sees an opening parenthesis (, it pushes it onto the operator_stack.
- If it sees a closing parenthesis ), it pops operators from the operator_stack and moves them to the output until it finds the matching (.
By the end, the output will contain the perfectly ordered postfix string.

### Functions to Create
#### shunting_yard(infix_regex)

**Function Signature:**
```python
def shunting_yard(infix_regex: str) -> str:
```

**Input Parameter:**
- **infix_regex:** Data Type: str (string). Description: This is the string that has already been processed by insert_concatenation_operator. It will contain the explicit . for concatenation.
  - Example Input 1: "a.b|c"
  - Example Input 2: "(a|b)*.c"

**Output (Return Value):**
Data Type: str (string). Description: The final, reorganized postfix string that is now ready for the NFA construction phase.
- Example Output 1 (for "a.b|c"): "ab.c|"
- Example Output 2 (for "(a|b)*.c"): "ab|*c."

### Naming Conventions for this File
- Variables: snake_case (e.g., output_queue, operator_stack, precedence_map).
- Functions: snake_case (e.g., shunting_yard).







## 3. nfa_structure.py

### Purpose of this File
This file is the foundation of the entire project. It does not perform any actions or algorithms itself. Instead, it defines the custom data types that we will use to represent the automaton in memory.

Think of this file as creating the custom Lego bricks (State and NFA classes) that the converter.py file will later assemble. Every other part of the project that deals with the automaton will rely on the blueprints defined here.

### How It Works (The Core Logic)
This file will contain two class definitions:
- State: Represents a single node or "circle" in the automaton graph. Each state knows whether it's a final (accepting) state and holds a list of all its possible transitions to other states.
- NFA: Represents an entire Non-deterministic Finite Automaton, or a fragment of one. It is a simple "container" that only needs to keep track of the entry point (start_state) and the exit point (accept_state) of the automaton. This design is crucial for Thompson's algorithm, which works by linking the exit of one NFA fragment to the entry of another.

### Classes to Create
#### State Class

**Class Definition:**
```python
class State:
    def __init__(self, is_accepting: bool = False):
        # details below

    def add_transition(self, symbol: str, next_state: 'State'):
        # details below
```

**__init__(self, is_accepting: bool = False) constructor:**
- **is_accepting parameter:** Data Type: bool (True or False). Default is False. Description: Determines if this state is an accepting state (a double circle in diagrams).

**Internal Variables (Attributes):**
- **self.is_accepting:** Stores the boolean value passed in.
- **self.transitions:** Data Type: dict (dictionary). Description: This is the core of the state. It stores all outgoing transitions.
  - Keys: The symbol for the transition (str), e.g., 'a', 'b', or 'epsilon'.
  - Values: A set of State objects that can be reached on that symbol. We use a set because in an NFA, a single symbol can lead to multiple destination states.

**add_transition(self, symbol: str, next_state: 'State') method:**
- Purpose: A helper method to make it easy to add a new transition from this state to another.
- **symbol parameter:** The transition symbol (str).
- **next_state parameter:** The destination State object.

#### NFA Class

**Class Definition:**
```python
class NFA:
    def __init__(self, start_state: State, accept_state: State):
        # details below
```

**__init__(self, start_state: State, accept_state: State) constructor:**
- Parameters: It takes two State objects as input.

**Internal Variables (Attributes):**
- **self.start_state:** Stores the State object that serves as the entry point.
- **self.accept_state:** Stores the State object that serves as the exit point.

### Example Usage (How these classes will be used in other files)
```python
# This code will NOT be in this file, but in converter.py
# It shows how the classes are used.

# 1. Create two state objects
state1 = State()
state2 = State(is_accepting=True)

# 2. Add a transition from state1 to state2 on the character 'a'
state1.add_transition('a', state2)

# 3. Create an NFA fragment that represents this simple machine
nfa_for_a = NFA(start_state=state1, accept_state=state2)
```

### Naming Conventions for this File
- Classes: PascalCase (e.g., State, NFA).
- Methods & Variables: snake_case (e.g., add_transition, is_accepting, start_state).





## 4. converter.py

### Purpose of this File
This file is the construction engine of our entire project. Its job is to take the logical plan for the regular expression (the "postfix" string from the parser) and use it to build the actual NFA. It acts like a builder on a construction site who reads a blueprint (the postfix string) and uses the Lego bricks (State and NFA objects from nfa_structure.py) to construct the final building (our complete automaton).

### How It Works (The Core Logic)
This file will implement the famous Thompson's Construction algorithm. The logic works by reading the postfix string from left to right and using a "stack" (think of it as a stack of plates where you can only add or remove from the top).
The function will loop through each character of the postfix string:

- If the character is an operand (e.g., a, b):
  - Create a new, simple NFA fragment just for this character. This involves creating a new start state and a new accept state, with a single transition between them on that character.
  - Push this new NFA object onto the stack.

- If the character is the concatenation operator (.):
  - Pop the top two NFA objects off the stack (let's call them nfa2 and nfa1).
  - Combine them by linking the accept state of nfa1 to the start state of nfa2 (using an epsilon transition).
  - Create a new NFA object whose start state is nfa1's start state and whose accept state is nfa2's accept state.
  - Push this newly combined NFA onto the stack.

- If the character is the union operator (|):
  - Pop the top two NFA objects off the stack (nfa2 and nfa1).
  - Create a new start state and a new accept state.
  - Create epsilon transitions from the new start state to the start states of both nfa1 and nfa2.
  - Create epsilon transitions from the accept states of nfa1 and nfa2 to the new accept state.
  - Push the resulting NFA (with the new start/accept states) onto the stack.

- If the character is the Kleene star operator (*):
  - Pop one NFA object off the stack.
  - Create a new start state and a new accept state.
  - Add epsilon transitions to allow looping back, skipping the fragment entirely, or exiting.
  - Push the new NFA onto the stack.
After the loop finishes, there will be exactly one NFA left on the stack—this is our final, complete result.

### Functions to Create
#### postfix_to_nfa(postfix_regex)

**Function Signature:**
```python
from src.nfa_structure import NFA

def postfix_to_nfa(postfix_regex: str) -> NFA:
```

**Input Parameter:**
- **postfix_regex:** Data Type: str (string). Description: This is the postfix string generated by parser.py.
  - Example Input: For the original regex (a|b)*c, the input here would be "ab|*c.".

**Output (Return Value):**
Data Type: An NFA object (from nfa_structure.py).

Description: This function returns the single, final NFA object that represents the entire regular expression. This object contains the start and accept states of the complete graph.

- Example Output (Conceptual): For the input "ab|*c.", the function returns one NFA object. Internally, this object's start state will link to a complex web of other states that correctly model the "zero or more a's or b's, followed by a c" logic. This object is then passed to display.py to be visualized.

### Naming Conventions for this File
- Variables: snake_case (e.g., nfa_stack, nfa1, new_start_state).
- Functions: snake_case (e.g., postfix_to_nfa).

### Dependencies
This file is critically dependent on src.nfa_structure.py.
You must import the State and NFA classes at the top of this file:
```python
from src.nfa_structure import State, NFA
```

## 5. display.py

### Purpose of this File
This file is the visualizer. The NFA object created by converter.py is just a network of objects in the computer's memory. Humans can't see it. 

The purpose of this file is to traverse that network and generate a graphical representation of the automaton, saving it as an image file. 

This allows us to see the final result, verify it's correct, and understand the structure of the state machine. We will use the popular graphviz library to handle the drawing.

### How It Works (The Core Logic)
The main function in this file will perform a graph traversal (like a Breadth-First Search or Depth-First Search) starting from the NFA's start_state.

It will create a Digraph object from the graphviz library.
It will maintain a list of states it has already visited to avoid getting stuck in loops.
It will "crawl" from the start state, exploring every transition to find all reachable states.
For each state it discovers, it will add a "node" to the graph. Nodes for accepting states will be styled differently (e.g., a double circle).

For each transition it finds between two states, it will add a directed "edge" (an arrow) to the graph, labeling it with the transition symbol (e.g., 'a' or 'ε').
Once all states and transitions have been added, it will tell graphviz to render the graph and save it to a file (like nfa.png).

### Functions to Create
#### display_nfa(nfa, output_filename)

**Function Signature:**
```python
from src.nfa_structure import NFA

def display_nfa(nfa: NFA, output_filename: str = 'nfa_graph'):
```

**Input Parameters:**
- **nfa:** Data Type: NFA object (from nfa_structure.py). Description: This is the complete, final NFA object returned by the postfix_to_nfa function.
  - Example Input: The NFA object that represents the regex (a|b)*.

- **output_filename:** Data Type: str (string). Description: The name for the output image file, without the extension. The default can be 'nfa_graph'.

**Output (Return Value):**
This function does not return a value (None).

**Side Effect (what it does):** Its primary job is to create files on the disk. The graphviz library will typically generate two files:
- A source file (e.g., nfa_graph.gv).
- An image file (e.g., nfa_graph.png).

**Example Output (the generated nfa_graph.png file for (a|b)*):**
It would be a visual graph image showing the states as circles and transitions as labeled arrows, similar to this conceptual drawing:
![alt text](https://i.stack.imgur.com/G5T5s.png)

### External Library Required
This file requires the graphviz Python library. All team members will need to install it.
```bash
pip install graphviz
```
Important: The graphviz library also requires you to install the Graphviz command-line tools on your operating system. Instructions can be found on the official Graphviz website.

### Naming Conventions for this File
- Variables: snake_case (e.g., graph, visited_states, state_queue).
- Functions: snake_case (e.g., display_nfa).

### Dependencies
This file is dependent on src.nfa_structure.py for the definitions of NFA and State. You will need to import them.
```python
from src.nfa_structure import NFA, State
```