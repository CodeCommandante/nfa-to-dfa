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

#! /usr/bin/python3

"""
Created on Fri Feb 26 19:34:34 2021

@author: jimleon
"""
import unittest
import automata

class Test_Automatons_NFA_getStates(unittest.TestCase):
    
    def test_nfa1(self):
        NFA = automata.NFA('./testGraphs/nfa_1.gv')
        States = NFA.getStates()
        ActStates = ['q_0','q_1','q_2','q_3','q_4','q_5']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
      
    def test_nfa2(self):
        NFA = automata.NFA('./testGraphs/nfa_2.gv')
        States = NFA.getStates()
        ActStates = ['q_0','q_1','q_2']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
     
    def test_nfa3(self):
        NFA = automata.NFA('./testGraphs/nfa_3.gv')
        States = NFA.getStates()
        ActStates = ['q_0','q_1','q_2']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
    def test_nfa4(self):
        NFA = automata.NFA('./testGraphs/nfa_4.gv')
        States = NFA.getStates()
        ActStates = ['q_0','q_1','q_2']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
    def test_nfa5(self):
        NFA = automata.NFA('./testGraphs/nfa_5.gv')
        States = NFA.getStates()
        ActStates = ['q_0','q_1','q_2']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
class Test_Automatons_NFA_getFinalStates(unittest.TestCase):
        
    def test_nfa1(self):
        NFA = automata.NFA('./testGraphs/nfa_1.gv')
        States = NFA.getFinalStates()
        ActStates = ['q_3','q_5']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
      
    def test_nfa2(self):
        NFA = automata.NFA('./testGraphs/nfa_2.gv')
        States = NFA.getFinalStates()
        ActStates = ['q_0']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
     
    def test_nfa3(self):
        NFA = automata.NFA('./testGraphs/nfa_3.gv')
        States = NFA.getFinalStates()
        ActStates = ['q_1']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
    def test_nfa4(self):
        NFA = automata.NFA('./testGraphs/nfa_4.gv')
        States = NFA.getFinalStates()
        ActStates = ['q_1']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
    def test_nfa5(self):
        NFA = automata.NFA('./testGraphs/nfa_5.gv')
        States = NFA.getFinalStates()
        ActStates = ['q_1']
        for i in range(len(ActStates)):
            self.assertEqual(States[i],ActStates[i])
        del NFA
        
class Test_Automatons_NFA_getAlphabet(unittest.TestCase):
        
    def test_nfa1(self):
        NFA = automata.NFA('./testGraphs/nfa_1.gv')
        Syms = NFA.getAlphabet()
        ActSyms = ['a']
        for i in range(len(ActSyms)):
            self.assertEqual(Syms[i],ActSyms[i])
        del NFA
      
    def test_nfa2(self):
        NFA = automata.NFA('./testGraphs/nfa_2.gv')
        Syms = NFA.getAlphabet()
        ActSyms = ['0','1','\u03BB']
        for i in range(len(ActSyms)):
            self.assertEqual(Syms[i],ActSyms[i])
        del NFA
     
    def test_nfa3(self):
        NFA = automata.NFA('./testGraphs/nfa_3.gv')
        Syms = NFA.getAlphabet()
        ActSyms = ['a','\u03BB']
        for i in range(len(ActSyms)):
            self.assertEqual(Syms[i],ActSyms[i])
        del NFA
        
    def test_nfa4(self):
        NFA = automata.NFA('./testGraphs/nfa_4.gv')
        Syms = NFA.getAlphabet()
        ActSyms = ['a','b','\u03BB']
        for i in range(len(ActSyms)):
            self.assertEqual(Syms[i],ActSyms[i])
        del NFA
        
    def test_nfa5(self):
        NFA = automata.NFA('./testGraphs/nfa_5.gv')
        Syms = NFA.getAlphabet()
        ActSyms = ['0','1']
        for i in range(len(ActSyms)):
            self.assertEqual(Syms[i],ActSyms[i])
        del NFA

class Test_Automatons_NFA_getDeltas(unittest.TestCase):
        
    def test_nfa1(self):
        NFA = automata.NFA('./testGraphs/nfa_1.gv')
        self.assertEqual(len(NFA.getDeltas()),6)
        del NFA
      
    def test_nfa2(self):
        NFA = automata.NFA('./testGraphs/nfa_2.gv')
        self.assertEqual(len(NFA.getDeltas()),5)
        del NFA
     
    def test_nfa3(self):
        NFA = automata.NFA('./testGraphs/nfa_3.gv')
        self.assertEqual(len(NFA.getDeltas()),3)
        del NFA
        
    def test_nfa4(self):
        NFA = automata.NFA('./testGraphs/nfa_4.gv')
        self.assertEqual(len(NFA.getDeltas()),4)
        del NFA
        
    def test_nfa5(self):
        NFA = automata.NFA('./testGraphs/nfa_5.gv')
        self.assertEqual(len(NFA.getDeltas()),6)
        del NFA
        
class Test_Automatons_DFA_getAlphabet(unittest.TestCase):
        
    def test_nfa1_todfa(self):
        NFA = automata.NFA('./testGraphs/nfa_1.gv')
        DFA = NFA.toDFA()
        Alpha = DFA.getAlphabet()
        ActAlpha = ['a']
        for i in range(len(Alpha)):
            self.assertEqual(Alpha[i],ActAlpha[i])
        del NFA
        del DFA
      
    def test_nfa2_todfa(self):
        NFA = automata.NFA('./testGraphs/nfa_2.gv')
        DFA = NFA.toDFA()
        Alpha = DFA.getAlphabet()
        ActAlpha = ['0','1']
        for i in range(len(Alpha)):
            self.assertEqual(Alpha[i],ActAlpha[i])
        del NFA
        del DFA
     
    def test_nfa3_todfa(self):
        NFA = automata.NFA('./testGraphs/nfa_3.gv')
        DFA = NFA.toDFA()
        Alpha = DFA.getAlphabet()
        ActAlpha = ['a']
        for i in range(len(Alpha)):
            self.assertEqual(Alpha[i],ActAlpha[i])
        del NFA
        del DFA
        
    def test_nfa4(self):
        NFA = automata.NFA('./testGraphs/nfa_4.gv')
        DFA = NFA.toDFA()
        Alpha = DFA.getAlphabet()
        ActAlpha = ['a','b']
        for i in range(len(Alpha)):
            self.assertEqual(Alpha[i],ActAlpha[i])
        del NFA
        del DFA
        
    def test_nfa5(self):
        NFA = automata.NFA('./testGraphs/nfa_5.gv')
        DFA = NFA.toDFA()
        Alpha = DFA.getAlphabet()
        ActAlpha = ['0','1']
        for i in range(len(Alpha)):
            self.assertEqual(Alpha[i],ActAlpha[i])
        del NFA
        del DFA
        


if __name__ == '__main__':
    unittest.main()
