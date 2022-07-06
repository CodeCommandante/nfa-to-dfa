"""    
    Program for converting NFAs to DFAs.
    Copyright (C) 2021  Jim Leon

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 10:07:22 2021

@author: jimleon
"""
import networkx as nx
import graphviz as gv

class NFA:
    """Class representing an NFA."""    
    __NFA = ()
    __States = []
    __Alphabet = []
    __Deltas = []
    __Finals = []
    
    def __init__(self, file):
        """
        Constructor for the NFA.      

        Parameters
        ----------
        file : str
            The name of the .gv (DOT) file describing an NFA.  This file name 
            should include a relative or absolute path.

        Returns
        -------
        None.

        """
        self.__NFA = nx.DiGraph(nx.drawing.nx_agraph.read_dot(file))
        self.__populateStates()
        self.__populateFinalStates()
        self.__populateDeltas()
        self.__populateAlphabet()
        
    def __del__(self):
        """
        Destructor for the DFA.  Clears private member lists.

        Returns
        -------
        None.

        """
        self.__Alphabet.clear()
        self.__States.clear()
        self.__Deltas.clear()
        self.__Finals.clear()
        
    def getAlphabet(self):
        """
        Standard getter for the private Alphabet member.

        Returns
        -------
        List
            Copy of the Alphabet list.

        """
        return self.__Alphabet.copy()

    def getDeltas(self):
        """
        Standard getter for the private Delta member.

        Returns
        -------
        List (2D)
            Copy of the Deltas list.

        """
        return self.__Deltas.copy()
    
    def getEdgeLabel(self,stateA,stateB):
        """
        Standard getter for an edge label between two nodes/states.

        Parameters
        ----------
        stateA : str
            The stored name of the first node/state.  On the form 'q_0','q_1',etc.
        stateB : str
            The stored name of the second node/state.  On the form 'q_0','q_1',etc.

        Returns
        -------
        str
            The edge label (all symbols, separated by commas if needed).

        """
        SymSet = []
        for i in self.__Deltas:
            if i[0] == stateA and i[2] == stateB:
                SymSet.append(i[1])
        return self.__groupedSymbols(SymSet)
    
    def getFinalStates(self):
        """
        Standard getter for the private Finals member.

        Returns
        -------
        List.
            Copy of the Finals list.

        """
        return self.__Finals.copy()

    def getStates(self):
        """
        Standard getter for the private States member.

        Returns
        -------
        List.
            Copy of the States list.

        """
        return self.__States.copy()
    
    def isFinalState(self,state):
        """
        Declares if given state is a final state (true or false).

        Parameters
        ----------
        state : str
            The name of the state in question.

        Returns
        -------
        bool
            True if given state is a final state.  False otherwise.

        """
        for i in self.__Finals:
            if state == i:
                return True
        return False

    def saveAndView(self,name='./myNFA.gv'):
        """
        Saves a copy of the constructed NFA and opens a PDF version for viewing.

        Parameters
        ----------
        name : str, optional
            The name AND relative (or absolute) path for your saved NFA copy.
            The default is './myNFA.gv'.

        Returns
        -------
        None.

        """
        nx.drawing.nx_agraph.write_dot(self.__NFA,name)
        gv.render('dot','pdf',name)
        ViewName = name + '.pdf'
        gv.view(ViewName)
        
    def toDFA(self):
        """
        Uses the data from this NFA to construct a new DFA class object.

        Returns
        -------
        D : DFA
            A new DFA class instantiation.

        """
        #self.__reduce()
        D = DFA(self)
        return D
    
    def __build(self):
        """
        Constructs the Networkx NFA object using the wrapper class characteristics.

        Returns
        -------
        None.

        """
        self.__NFA = nx.DiGraph(rankdir='LR')
        for i in self.__Deltas:
            self.__NFA.add_node(i[0],shape='circle')
            self.__NFA.add_node(i[2],shape='circle')
            Label = self.getEdgeLabel(i[0],i[2])
            self.__NFA.add_edge(i[0],i[2],label=Label)
        for j in self.__Finals:
            nx.set_node_attributes(self.__NFA,{j:{'shape':'doublecircle'}})
        self.__NFA.add_node('q_i',shape='point')
        self.__NFA.add_edge('q_i','q_0')
    
    def __aggregateCSEdges(self):
        """
        Aggregate/separate Comma Separated Edges and build the delta-transitions 
        for each separated character.

        Returns
        -------
        None.

        """
        index = 0
        ListLen = len(self.__Deltas)
        while index < ListLen:
            Edge = self.__Deltas[index][1]
            if len(Edge) > 1:
                indey = 0
                while indey < len(Edge):
                    Entry = []
                    if indey%2 == 0:
                        Entry.append(self.__Deltas[index][0])
                        Entry.append(Edge[indey])
                        Entry.append(self.__Deltas[index][2])
                        self.__Deltas.append(Entry.copy())
                        Entry.clear()
                    indey = indey + 1
            index = index + 1
        #Remove any copies that may have shown up.
        indez = 0
        while indez < len(self.__Deltas):
            Edge = self.__Deltas[indez][1]
            if len(Edge) > 1:
                self.__Deltas.remove(self.__Deltas[indez])
                indez = indez - 1
            indez = indez + 1
        TempDelta = []
        for i in self.__States:
            for j in self.__Deltas:
                if i == j[0]:
                    TempDelta.append(j.copy())
        self.__Deltas.clear()
        self.__Deltas = TempDelta.copy()
        
    def __findMatchedPairFrom(self,state,symbol,rev=""):
        """
        Determines if two states are indistinguishable relative to the given state 
        on the given symbol.

        Parameters
        ----------
        state : str
            The name of the state.
        symbol : str
            The symbol/edge on which to transition.

        Returns
        -------
        List
            Returns a pair of states that are considered indistinguishable.

        """
        Match = []
        for i in self.__Deltas:
            if (rev == "") and (state == i[0]) and (symbol == i[1]) and (state != i[2]):
                Match.append(i[2])
            elif (rev != "") and (state == i[2]) and (symbol == i[1]) and (state != i[0]):
                Match.append(i[0])
        if len(Match) == 2:
            return Match
        else:
            return []
        
    def __mergeStates(self,keepState,mergeState):
        """
        Merges two states.

        Parameters
        ----------
        keepState : str
            The name of the state which will remain and inherit edges from mergeState.
        mergeState : str
            The name of the state which will disappear.

        Returns
        -------
        None.

        """
        #Never phase out the q_0 state      
        if mergeState == 'q_0':
            return
        i = 0
        while i < len(self.__Deltas):
            if self.__Deltas[i][0] == mergeState:
                self.__Deltas[i][0] = keepState
            if self.__Deltas[i][2] == mergeState:
                self.__Deltas[i][2] = keepState
            i = i + 1
        self.__pruneDeltaCopies()
        
    def __groupedSymbols(self,symSet):
        """
        Creates labels for combined symbol transitions.  On the form "a,b,c", etc.

        Parameters
        ----------
        symSet : List
            The symbols to combine.

        Returns
        -------
        str
            The comma-separated symbol/edge label.

        """
        if not symSet:
            return ""
        Group = symSet[0]
        index = 1
        while index < len(symSet):
            Group = Group + ","
            Group = Group + symSet[index]
            index = index + 1
        return Group
    
    def __populateAlphabet(self):
        """
        Populates the Alphabet for the machine language from the characteristics 
        given in the .gv file.

        Returns
        -------
        None.

        """
        Deltas = nx.get_edge_attributes(self.__NFA,'label')
        for i in Deltas:
            value = Deltas[i]
            #if edge is made up of more than one character...
            if len(value) > 1:
                for j in range(len(value)):
                    S = value[j]
                    if j % 2 == 0:
                        self.__Alphabet.append(S)
            else:
                self.__Alphabet.append(value)
        #"Prune" and sort the Alphabet
        Pruned = set(self.__Alphabet)
        self.__Alphabet.clear()
        for k in Pruned:
            self.__Alphabet.append(k)
        self.__Alphabet.sort()
            
    def __populateDeltas(self):
        """
        Populates the Delta-transitions for the automaton from the characteristics 
        given in the .gv file.

        Returns
        -------
        None.

        """
        DDict = nx.get_edge_attributes(self.__NFA,'label')
        #Get separate components for the delta-transition from DDict
        #https://www.geeksforgeeks.org/python-get-all-tuple-keys-from-dictionary/
        States = [state for key in DDict for state in key]
        TempDelta = []
        index = 0
        for key in DDict:
            Entry = []
            Entry.append(States[index])
            index = index + 1
            Entry.append(DDict[key])
            Entry.append(States[index])
            index = index + 1
            TempDelta.append(Entry)
        for i in self.__States:
            for j in range(len(TempDelta)):
                if i == TempDelta[j][0]:
                    self.__Deltas.append(TempDelta[j])
        self.__aggregateCSEdges()
            
    def __populateFinalStates(self):
        """
        Populates the Final States for the automaton from the characteristics 
        given in the .gv file.

        Returns
        -------
        None.

        """
        NodeAtts = nx.get_node_attributes(self.__NFA,'shape')
        for i in NodeAtts:
            if NodeAtts[i] == 'doublecircle':
                self.__Finals.append(i)
        self.__Finals.sort()
        
    def __populateStates(self):
        """
        Populates the States for the automaton from the characteristics 
        given in the .gv file.

        Returns
        -------
        None.

        """
        for i in nx.nodes(self.__NFA):
            if i != 'qi':
                self.__States.append(i)
        self.__States.sort()
        
    def __pruneDeltaCopies(self):
        """
        Removes duplicated Delta-transitions from Deltas member.

        Returns
        -------
        None.

        """
        index = 0
        while index < (len(self.__Deltas)-1):
            indey = index + 1
            First = self.__Deltas[index].copy()
            while indey < len(self.__Deltas):
                Second = self.__Deltas[indey].copy()
                if (First[0]==Second[0]) and (First[1]==Second[1]) and (First[2]==Second[2]):
                    self.__Deltas.remove(self.__Deltas[indey])
                    indey = indey - 1
                indey = indey + 1
            index = index + 1
            
    def __pruneStates(self):
        """
        Removes states from States list if they are no longer found in the Deltas 
        member list.

        Returns
        -------
        None.

        """
        index = 0
        while index < len(self.__States):
            Defunct = True
            for j in self.__Deltas:
                if (self.__States[index] == j[0]) or (self.__States[index] == j[2]):
                    Defunct = False
            if Defunct:
                self.__States.remove(self.__States[index])
                index = index - 1
            index = index + 1
        
    def __reduce(self):
        """
        Reduces the NFA to the extent possible.

        Returns
        -------
        None.

        """
        #Merge identical successors
        for i in self.__States:
            for j in self.__Alphabet:
                Match = self.__findMatchedPairFrom(i,j)
                if Match and self.isFinalState(Match[0]):
                    self.__mergeStates(Match[0],Match[1])
                elif Match and self.isFinalState(Match[1]):
                    self.__mergeStates(Match[1],Match[0]) 
                elif Match and not self.isFinalState(Match[0]) and not self.isFinalState(Match[1]):
                    self.__mergeStates(Match[0],Match[1])
        #Merge identical predecessors
        for k in self.__Finals:
            for l in self.__Alphabet:
                Match = self.__findMatchedPairFrom(k,l,'r')
                if Match and self.isFinalState(Match[0]):
                    self.__mergeStates(Match[0],Match[1])
                elif Match and self.isFinalState(Match[1]):
                    self.__mergeStates(Match[1],Match[0]) 
                elif Match and not self.isFinalState(Match[0]) and not self.isFinalState(Match[1]):
                    self.__mergeStates(Match[0],Match[1]) 
        #self.__removeLambdaTransitions()
        self.__pruneStates()
        self.__build()
        
    def __removeLambdaTransitions(self):
        i = 0
        while i < len(self.__Deltas):
            if self.__Deltas[i][1] == '\u03BB':
                if self.isFinalState(self.__Deltas[i][0]):
                    self.__mergeStates(self.__Deltas[i][0],self.__Deltas[i][2])
                elif self.isFinalState(self.__Deltas[i][1]):
                    self.__mergeStates(self.__Deltas[i][1],self.__Deltas[i][0]) 
                elif not self.isFinalState(self.__Deltas[i][0]) and not self.isFinalState(self.__Deltas[i][1]):
                    self.__mergeStates(self.__Deltas[i][0],self.__Deltas[i][1])  
                i = -1
            i = i + 1
            
class DFA:
    """Class representing a DFA."""
    __DFA = ()
    __States = []
    __Alphabet = []
    __Deltas = []
    __Finals = []
    
    def __init__(self,NFAObj=()):  
        """
        Constructor for the DFA.

        Parameters
        ----------
        NFAObj : NFA, optional
            An NFA class object. The default is ().

        Returns
        -------
        None.

        """
        #if no NFA provided, construct a simple one-state DFA.
        if NFAObj == ():
            self.__DFA = nx.DiGraph(rankdir='LR')
            self.__DFA.add_node('q_i',shape='point')
            self.__DFA.add_node('q_0',shape='doublecircle')
            self.__DFA.add_edge('q_i','q_0')
        else:
            self.__Alphabet = NFAObj.getAlphabet()
            self.__trimInheritedAlphabet()
            self.__Deltas = NFAObj.getDeltas()
            self.__Finals = NFAObj.getFinalStates()
            self.__States = NFAObj.getStates()
            self.__buildDeltasFromInherited()
            self.__build()
      
    def __del__(self):
        """
        Destructor for the DFA.  Clears private member lists.

        Returns
        -------
        None.

        """
        self.__Alphabet.clear()
        self.__States.clear()
        self.__Deltas.clear()
        self.__Finals.clear()
        
    def getAlphabet(self):
        """
        Standard getter for the private Alphabet member.

        Returns
        -------
        List
            Copy of the Alphabet list.

        """
        return self.__Alphabet.copy()
        
    def getDeltas(self):
        """
        Standard getter for the private Deltas member.

        Returns
        -------
        List (2D)
            Copy of the Deltas list.

        """
        return self.__Deltas.copy()
    
    def getEdgeLabel(self,stateA,stateB):
        """
        Standard getter for an edge label between two nodes/states.

        Parameters
        ----------
        stateA : str
            The stored name of the first node/state.  On the form 'q_0','q_1',etc.
        stateB : str
            The stored name of the second node/state.  On the form 'q_0','q_1',etc.

        Returns
        -------
        str
            The edge label (all symbols, separated by commas if needed).

        """
        SymSet = []
        for i in self.__Deltas:
            if i[0] == stateA and i[2] == stateB:
                SymSet.append(i[1])
        return self.__groupedSymbols(SymSet)
        
    def getFinalStates(self):
        """
        Standard getter for the private Finals member.

        Returns
        -------
        List
            Copy of the Finals list.

        """
        return self.__Finals.copy()
    
    def getNextStateOn(self,initState,symbol):
        """
        Getter that returns the succeeding state on a given edge (symbol).

        Parameters
        ----------
        initState : str
            The starting node/state.  On the form 'q_0','q_1',etc.
        symbol : str
            The outgoing symbol/edge.

        Returns
        -------
        str
            The name of the destination node/state.  Returns empty string if 
            invalid.

        """
        for i in self.__Deltas:
            if (i[0] == initState) and (i[1] == symbol):
                return i[2]
        return ""
         
    def getStates(self):
        """
        Standard getter for the private States member.

        Returns
        -------
        List
            Copy of the States list.

        """
        return self.__States.copy()  

    def inDegreeOn(self,state):
        """
        Returns the number of incoming edges/symbols on the given node/state.

        Parameters
        ----------
        state : str
            The name of the state.

        Returns
        -------
        Degree : int
            The number of incoming edges/symbols.

        """
        Degree = 0
        for i in self.__Deltas:
            if i[2] == state:
                Degree = Degree + 1
        return Degree
    
    def isFinalState(self,state):
        """
        Declares if given state is a final state (true or false).

        Parameters
        ----------
        state : str
            The name of the state in question.

        Returns
        -------
        bool
            True if given state is a final state.  False otherwise.

        """
        for i in self.__Finals:
            if state == i:
                return True
        return False
    
    def hasOutEdgeOn(self,state,symbol):
        """
        Declares if the given state has an outgoing edge on the given symbol.

        Parameters
        ----------
        state : str
            The name of the state in question.
        symbol : str
            The symbol in question.

        Returns
        -------
        bool
            True if outgoing edge exists on given state. False otherwise.

        """
        for i in self.__Deltas:
            if state == i[0] and symbol == i[1]:
                return True
        return False
    
    def hasSelfLoopOn(self,state):
        """
        Declares if given state has a self-loop.

        Parameters
        ----------
        state : str
            The name of the state in question.

        Returns
        -------
        bool
            True if the given state has a self-loop.  False otherwise.

        """
        for i in self.__Deltas:
            if (state == i[0]) and (state == i[2]):
                return True
        return False
    
    def reduce(self):
        """
        Reduces the DFA to the extent possible.

        Returns
        -------
        None.

        """
        self.__removeNullStates()
        #self.__removeTrapStates()
        for i in self.__States:
            for j in self.__Alphabet:
                Match = self.__findMatchedPairFrom(i,j)
                if Match and self.isFinalState(Match[0]):
                    self.__mergeStates(Match[0],Match[1])
                elif Match and self.isFinalState(Match[1]):
                    self.__mergeStates(Match[1],Match[0]) 
        self.__pruneStates()
        self.__build()
          
    def numberOfSelfLoopsOn(self,state):
        """
        Returns the number of self-loops on the given state.

        Parameters
        ----------
        state : str
            The name of the state in question.

        Returns
        -------
        Num : int
            The number of self-loops on the given state.

        """
        Num = 0
        for i in self.__Deltas:
            if (state == i[0]) and (state == i[2]):
               Num = Num + 1
        return Num
        
    def outDegreeOn(self,state):
        """
        Returns the number of outgoing edges/symbols on the given node/state.

        Parameters
        ----------
        state : str
            The name of the given state.

        Returns
        -------
        Degree : int
            The number of outgoing edges on the given state.

        """
        Degree = 0
        for i in self.__Deltas:
            if i[0] == state:
                Degree = Degree + 1
        return Degree

    def saveAndView(self,name='./myDFA.gv'):
        """
        Saves a copy of the constructed DFA and opens a PDF version for viewing.

        Parameters
        ----------
        name : str, optional
            The name AND relative (or absolute) path for your saved DFA.
            The default is './myDFA.gv'.

        Returns
        -------
        None.

        """
        nx.drawing.nx_agraph.write_dot(self.__DFA,name)
        gv.render('dot','pdf',name)
        ViewName = name + '.pdf'
        gv.view(ViewName)
        
    def __allPairsFinalAndNon(self):
        """
        Returns all pairs of Final and Non-Final states (unordered).

        Returns
        -------
        AllPairs : List (2D)
            All pairs of non-final and final state.

        """
        NonFinals = []
        AllPairs = []
        for i in self.__States:
            if not self.isFinalState(i):
                NonFinals.append(i)
        for i in self.__Finals:
            for j in NonFinals:
                AllPairs.append([i,j])
                AllPairs.append([j,i])
        return AllPairs
                
    def __build(self):
        """
        Constructs the Networkx DFA object using the wrapper class characteristics.

        Returns
        -------
        None.

        """
        self.__DFA = nx.DiGraph(rankdir='LR')
        for i in self.__Deltas:
            self.__DFA.add_node(i[0],shape='circle')
            self.__DFA.add_node(i[2],shape='circle')
            Label = self.getEdgeLabel(i[0],i[2])
            self.__DFA.add_edge(i[0],i[2],label=Label)
        for j in self.__Finals:
            nx.set_node_attributes(self.__DFA,{j:{'shape':'doublecircle'}})
        self.__DFA.add_node('q_i',shape='point')
        self.__DFA.add_edge('q_i','q_0')
    
    def __buildDeltasFromInherited(self):
        """
        Constructs the 2-D list of delta-transitions from the incoming NFA class 
        object.

        Returns
        -------
        None.

        """
        NewDeltas = []
        NullState = False
        for i in self.__States:
            for j in self.__Alphabet:
                Grouped = self.__groupWalksFromStateOnSymbol(i,j)
                #if returns group is an empty list, edges transition to NULL state.
                if not Grouped:
                    NewDeltas.append([i,j,'\u2205'])
                    NullState = True  #flag means add NULL state to States member.
                else:
                    for k in Grouped:
                        NewDeltas.append([i,j,k])
        if NullState:
            self.__States.append('\u2205')
            Label = self.__groupedSymbols(self.__Alphabet.copy())
            NewDeltas.append(['\u2205',Label,'\u2205'])
        self.__Deltas.clear()
        self.__Deltas = NewDeltas.copy()
        self.__pruneDeltaCopies()
        
    def __findMatchedPairFrom(self,state,symbol):
        """
        Determines if two states are indistinguishable relative to the given state 
        on the given symbol.

        Parameters
        ----------
        state : str
            The name of the state.
        symbol : str
            The symbol/edge on which to transition.

        Returns
        -------
        List
            Returns a pair of states that are considered indistinguishable.

        """
        Match = []
        for i in self.__Deltas:
            if (state == i[0]) and (symbol == i[1]) and (state != i[2]):
                Match.append(i[2])
        if len(Match) == 2:
            return Match
        else:
            return []
        
    def __groupedSymbols(self,symSet):
        """
        Creates labels for combined symbol transitions.  On the form "a,b,c", etc.

        Parameters
        ----------
        symSet : List
            The symbols to combine.

        Returns
        -------
        str
            The comma-separated symbol/edge label.

        """
        if not symSet:
            return ""
        Group = symSet[0]
        index = 1
        while index < len(symSet):
            Group = Group + ","
            Group = Group + symSet[index]
            index = index + 1
        return Group
    
    def __groupWalksFromStateOnSymbol(self,initState,symbol):
        """
        Given a symbol in the alphabet and an initial state, determines a destination 
        state when empty-strings (lambdas) are removed from the DFA.

        Parameters
        ----------
        initState : str
            The name of the state to start 'walking' from.
        symbol : str
            The alphabet symbol/edge.

        Returns
        -------
        List
            States reached after removal of lambda edges.

        """
        Group = []
        state = initState
        #Case:  No edge on symbol from initial state; follow the lambdas first.
        if not self.hasOutEdgeOn(state,symbol):
            index = 0
            while index < len(self.__Deltas):
                if (self.__Deltas[index][0] == state) and (self.__Deltas[index][1] == '\u03BB') and not (self.__Deltas[index][2] == state):
                    state = self.__Deltas[index][2]
                    index = -1
                index = index + 1
            initState = state
            if self.isFinalState(initState):
                Group.append(initState)
            for j in self.__Deltas:
                if (j[0] == initState) and (j[1] == symbol):
                    state = j[2]
                    Group.append(state)
        #Case:  Follow alphabet symbol first, then follow lambdas.
        else:
            for i in self.__Deltas:
                if (i[0] == initState) and (i[1] == symbol):
                    state = i[2]
                    Group.append(state)
            index = 0
            while index < len(self.__Deltas):
                if (self.__Deltas[index][0] == state) and (self.__Deltas[index][1] == '\u03BB') and not (self.__Deltas[index][2] == state):
                    state = self.__Deltas[index][2]
                    Group.append(state)
                    index = -1
                index = index + 1
        return Group.copy()
    
    def __mark(self):
        """
        Marks all non-final and final state pairs as distinguishable or indistinguishable.

        Returns
        -------
        Distinguishable : List (2D)
            All pairs of distinguishable states (unordered pairs).

        """
        Distinguishable = []
        Marked = self.__allPairsFinalAndNon()
        for i in Marked:
            for j in self.__Alphabet:
                State1 = self.getNextStateOn(i[0],j)
                State2 = self.getNextStateOn(i[1],j)
                for k in Marked:
                    if State1==k[0] and State2==k[1]:
                        Distinguishable.append(k)
        return Distinguishable      

    def __mergeStates(self,keepState,mergeState):
        """
        Merges two states.

        Parameters
        ----------
        keepState : str
            The name of the state which will remain and inherit edges from mergeState.
        mergeState : str
            The name of the state which will disappear.

        Returns
        -------
        None.

        """
        #Never phase out the q_0 state      
        if mergeState == 'q_0':
            return
        i = 0
        while i < len(self.__Deltas):
            if self.__Deltas[i][0] == mergeState:
                self.__Deltas[i][0] = keepState
            if self.__Deltas[i][2] == mergeState:
                self.__Deltas[i][2] = keepState
            i = i + 1
        self.__pruneDeltaCopies()
    
    def __pruneDeltaCopies(self):
        """
        Removes duplicated Delta-transitions from Deltas member.

        Returns
        -------
        None.

        """
        index = 0
        while index < (len(self.__Deltas)-1):
            indey = index + 1
            First = self.__Deltas[index].copy()
            while indey < len(self.__Deltas):
                Second = self.__Deltas[indey].copy()
                if (First[0]==Second[0]) and (First[1]==Second[1]) and (First[2]==Second[2]):
                    self.__Deltas.remove(self.__Deltas[indey])
                    indey = indey - 1
                indey = indey + 1
            index = index + 1
            
    def __pruneStates(self):
        """
        Removes states from States list if they are no longer found in the Deltas 
        member list.

        Returns
        -------
        None.

        """
        index = 0
        while index < len(self.__States):
            Defunct = True
            for j in self.__Deltas:
                if (self.__States[index] == j[0]) or (self.__States[index] == j[2]):
                    Defunct = False
            if Defunct:
                self.__States.remove(self.__States[index])
                index = index - 1
            index = index + 1
            
    def __removeNullStates(self):
        """
        Removes all Delta-Transitions with NULL states in them.  Also removes the 
        NULL state from the States list (see pruneStates() method)

        Returns
        -------
        None.

        """
        index = 0
        while index < len(self.__Deltas):
            if self.__Deltas[index][2] == '\u2205':
                self.__Deltas.remove(self.__Deltas[index])
                index = index - 1
            index = index + 1
        index = 0
        while index < len(self.__Deltas):
            if not self.isFinalState(self.__Deltas[index][0]) and (self.inDegreeOn(self.__Deltas[index][0]) == self.numberOfSelfLoopsOn(self.__Deltas[index][0])) and (self.__Deltas[index][0] != 'q_0'):
                self.__Deltas.remove(self.__Deltas[index])
                index = index - 1
            index = index + 1
        self.__pruneStates()
        
    def __removeTrapStates(self):
        """
        Removes all Delta-transitions with trap states in them.  Also removes the 
        trap state from the States list (see pruneStates() method).

        Returns
        -------
        None.

        """
        index = 0
        while index < len(self.__Deltas):
            if not self.isFinalState(self.__Deltas[index][2]) and (self.outDegreeOn(self.__Deltas[index][2]) == 0):
                self.__Deltas.remove(self.__Deltas[index])
                index = index - 1
            index = index + 1
        index = 0
        while index < len(self.__Deltas):
            if not self.isFinalState(self.__Deltas[index][2]) and (self.outDegreeOn(self.__Deltas[index][2]) == self.numberOfSelfLoopsOn(self.__Deltas[index][2])) and (self.__Deltas[index][2] != 'q_0'):
                self.__Deltas.remove(self.__Deltas[index])
                index = index - 1
            index = index + 1   
        self.__pruneStates()
            
    def __trimInheritedAlphabet(self):
        """
        Removes lambda characters in the Alphabet inherited from the NFA 
        class object.

        Returns
        -------
        None.

        """
        index = 0
        AlphaLen = len(self.__Alphabet)
        while index < AlphaLen:
            if self.__Alphabet[index] == '\u03BB':
                self.__Alphabet.remove(self.__Alphabet[index])
                index = index - 1
                AlphaLen = AlphaLen - 1
            index = index + 1