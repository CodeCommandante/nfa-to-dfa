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
Created on Mon Feb 15 07:40:46 2021

@author: Jim Leon

This program takes as input a DOT (as ’.gv’) file, performs user requested modifications to it, and
outputs the modified DOT file. The incoming DOT file is expected to represent a Non-deterministic
Finite Accepter (NFA) and, based on the requested modifications given at the command line, will output
a Deterministic Finite Acceptor equivalent to the NFA. Further, the user may request a minimal DFA.
"""
import automata
import argparse

def main():
    """
    Main function that gathers command line args, and executes the program.

    Returns
    -------
    None.

    """
    parser = argparse.ArgumentParser(description='Program to convert an NFA represented by the DOT-language into an equivalent minimal DFA and view the corresponding results.')
    parser.add_argument('NFA',action='store',type=str,help='the NFA file (as a .gv filetype)')
    parser.add_argument('-f','--full',action='store_true',help='will write and display a fully connected DFA, including trap and NULL states')
    args = parser.parse_args()
    if args.full:
        N = automata.NFA(str(args.NFA))
        D = N.toDFA()
    else:
        N = automata.NFA(str(args.NFA))
        D = N.toDFA()
        D.reduce()
        
    N = automata.NFA('./testGraphs/nfa_8.gv')
    N.saveAndView()
    D = N.toDFA()
    D.reduce()
    D.saveAndView()
    
    del N
    del D
    
main()