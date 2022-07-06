# NFA to DFA

## Author
Jim Leon

## Program Description
This program takes as input a DOT (as ’.gv’) file, performs user requested modifications to it, and
outputs the modified DOT file. The incoming DOT file is expected to represent a Non-deterministic
Finite Accepter (NFA) and, based on the requested modifications given at the command line, will output
a Deterministic Finite Acceptor equivalent to the NFA. Further, the user may request a minimal DFA.
The program is written in Python 3.8; which means that no separate compilation should be required
to run the program. The only prerequisites needed is a Python 3.8 code base, and the Graphviz and
Networkx libraries. The Graphviz and Networkx libraries form the basis of the graph manipulation
and visualization procedures. To download these libraries on a Linux machine, the user must issue the
following commands at the command line:

$ sudo pip install graphviz
$ sudo pip install networkx

For further information/details on installing the needed libraries, refer to the following links: 

https://pypi.org/project/graphviz/
https://networkx.org/documentation/networkx-2.5/install.html

These links will provide additional information/details on Windows installations as well.

## Running the application
The application can be run right from the command line. Navigate to a directory in which you want
your output .gv and .gv.pdf files to be saved and enter commands with the following usage:

$ ./NFAtoDFA.py [-h] [-f,--full] NFA

...where the ”-h” and ”-f” flags are optional and ”NFA” is a .gv (DOT) file describing the NFA you
want to convert to a DFA. You must include the relative or absolute file path for your .gv file (example:
./myFiles/myNFA.gv) or you will get an error. If no optional flags are specified, the NFA is converted to
an equivalent minimal DFA, and both the original NFA and DFA are saved and displayed to the screen
as PDF files. The newly constructed NFA (copy) and DFA files are saved to your current directory as
”myNFA.gv” and ”myDFA.gv”, respectively. Their PDF renderings are saved as ”myNFA.gv.pdf” and
”myDFA.gv.pdf”, respectively.

If you include the ”-h” flag, you will see a help and usage menu printed to the console.
1By including the ”-f” or ”–full” flag, the NFA will be transformed into an equivalent fully-connected
DFA, which includes all trap and NULL states in the graph.

## Code Structure and Primary Functions
The program relies on two constructed classes, ”NFA” and ”DFA”. These classes are wrappers that
use some of the functionality of the Graphviz and Networkx libraries to construct NFA and DFA Graph
objects. By constructing wrapper classes, I was able to create member functions and member data
that was easier to internally manipulate and transform. For example, delta-transitions are represented
within the two classes as a 2D array with 3 columns (starting node, edge symbol, ending node) and n
rows corresponding to the Graph edges. (NOTE: The node ’q i’ and the single edge entering ’q 0’ are
not represented in the delta-transition table). Other member data include: the Language alphabet (as
a list/array), the states (as a list/array), and the final states (as a list/array) of the automata.

## Program Limitations, Bugs, and To-Do’s
The implementation of the reduce portion of the algorithm proved somewhat difficult. This along with
some limitations on voluminous test candidates means that I expect for some NFA’s, the corresponding
DFA may not be truly minimal. Minimized, for certain - but, perhaps not minimal.
There is no built in exception or type handling (outside of what Python offers under the hood) for
this program. Passing parameters or data to functions expecting a certain type or form may result in
buggy behavior or, at worst, program failure/crash. I have drastically limited the API and public class
access in order to miminize the possiblity of these types of errors/failures; however, if exploring the
code and application deeper, expect to find bugs and other vulnerabilities throughout.
There is a small test suite included in this application package. This test suite was the beginning
of an attempt to diligently practice my TDD. However, as a novice, I quickly found a barrier to my
diligence when building the classes and their corresponding private member methods - which do the
majority of the heavy-lifting in this program. I did discover late in the project (with the help of Dr.
Paul Hinker) that Python allows developers to call private member methods without the use of ”friend”
functions or other work-arounds. By the time of this discovery, the faithful execution of my TDD skills
had gone to the wind. Despite this, I’ve included the tests I managed to get written (mostly for the
NFA class and it’s methods).


