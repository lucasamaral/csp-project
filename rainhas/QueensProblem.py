import sys

class QueenState(object):
    """docstring for QueenState"""
    def __init__(self, unassigned = [], assigned = []):
        self.unassigned = unassigned
        self.assigned = assigned

    def __repr__(self):
        return self.unassigned.__repr__() + self.assigned.__repr__()

class QueenVar(object):
    """docstring for QueenVar"""
    def __init__(self, position, domain, val = None):
        self.name = 'Queen' + str(position)
        self.domain = domain
        self.position = position
        self.value = val

    def __repr__(self):
        repr_string = self.name
        repr_string += 'D: ' + self.domain.__repr__()
        repr_string += 'Pos: ' + str(self.position)
        repr_string += 'Val: ' + str(self.value)
        return repr_string

class NnQueens(object):
    """docstring for NnQueens"""
    def __init__(self, number):
        self.number = number
        self.solutions = []
        self.queens = []
        for x in xrange(1,self.number+1):
            self.queens.append(QueenVar(x, range(1,self.number+1)))
        
        self.initial = QueenState(self.queens)

    def runNnQueens(self):
        self.explore(self.initial)

    def find_one_solution(self):
        self.explore_one_solution(self.initial)

    def explore(self,state):
        if len(state.assigned) > 1:
            failure = self.check_constraints(state.assigned)
            if failure:
                return

        if len(state.unassigned) > 0:
            queen_var = state.unassigned.pop()
            for x in queen_var.domain:
                q = QueenVar(queen_var.position, queen_var.domain, x)
                new_unass = list(state.unassigned)
                new_ass = list(state.assigned)
                new_ass.append(q)
                self.explore(QueenState(new_unass, new_ass))
        else:
            self.solutions.append(state)

    def check_constraints(self, assigneds):
        for var_queen in assigneds:
            for sec_queen in assigneds[(assigneds.index(var_queen)+1):]:
                if var_queen.value == sec_queen.value:
                    return True
                if abs(var_queen.value-sec_queen.value) == abs(var_queen.position-sec_queen.position):
                    return True
        return False

    def explore_one_solution(self, state):
        if len(self.solutions) > 0:
            return

        if len(state.assigned) > 1:
            failure = self.check_constraints(state.assigned)
            if failure:
                return

        if len(state.unassigned) > 0:
            queen_var = state.unassigned.pop()
            for x in queen_var.domain:
                q = QueenVar(queen_var.position, queen_var.domain, x)
                new_unass = list(state.unassigned)
                new_ass = list(state.assigned)
                new_ass.append(q)
                self.explore_one_solution(QueenState(new_unass, new_ass))
        else:
            self.solutions.append(state)

    def print_queens(self, quens_list):
        sys.stdout.write('-')
        for i in xrange(1,self.number+1):
            sys.stdout.write('--')
        sys.stdout.write('\n')
        for d_val in xrange(1,self.number+1):
            for Q in quens_list:
                if(Q.value==d_val):
                    x = 1
                    while x <= len(quens_list) :
                        if x == Q.position :
                            sys.stdout.write('|Q')
                        else:
                            sys.stdout.write('| ')
                        x = x+1
            print('|')
        sys.stdout.write('-')
        for i in xrange(1,self.number+1):
            sys.stdout.write('--')
        sys.stdout.write('\n')
    def print_all_solutions(self):
        for solution in self.solutions:
            self.print_queens(solution.assigned)
        
# print 'Digite o numero de rainhas: '
# n = input()
Nqueens = NnQueens(20)
# Nqueens.runNnQueens()
Nqueens.find_one_solution()
# print('Numero de solucoes: ' + str(len(Nqueens.solutions)))
Nqueens.print_all_solutions()