import copy

class ZebraState(object):
    """docstring for ZebraState"""
    def __init__(self, unassigned = [],
        assigned = [{'nation':None, 'cigar':None, 'color':None, 'animal':None, 'drink':None},
                    {'nation':None, 'cigar':None, 'color':None, 'animal':None, 'drink':None},
                    {'nation':None, 'cigar':None, 'color':None, 'animal':None, 'drink':None},
                    {'nation':None, 'cigar':None, 'color':None, 'animal':None, 'drink':None},
                    {'nation':None, 'cigar':None, 'color':None, 'animal':None, 'drink':None}
                ]):
        self.unassigned = unassigned
        self.assigned = assigned

class ZebraVar(object):
    """docstring for ZebraVar"""
    def __init__(self, name, value = None):
        self.name = name
        self.value = value

    def __repr__(self):
        repr_string = self.name
        repr_string += ' Val: ' + str(self.value)
        return repr_string

class Zebra(object):
    """docstring for Zebra"""
    def __init__(self):
        self.variables = []
        self.domains = {'nation': ['noruegues', 'ingles', 'espanhol', 'japones', 'ucraniano'],
                        'cigar' : ['kool', 'chester', 'winston', 'lucky', 'parliament'],
                        'color' : ['vermelha', 'amarela', 'azul', 'verde', 'marfim'],
                        'animal': ['zebra', 'cachorro', 'raposa', 'caramujos', 'cavalo'],
                        'drink' : ['agua', 'laranja', 'cha', 'cafe', 'leite']}
        self.solution = None
        self.recursion_length = 0

        for x in xrange(5):
            self.variables.append(ZebraVar('nation'))
        for x in xrange(5):
            self.variables.append(ZebraVar('cigar'))
        for x in xrange(5):
            self.variables.append(ZebraVar('color'))
        for x in xrange(5):
            self.variables.append(ZebraVar('animal'))
        for x in xrange(5):
            self.variables.append(ZebraVar('drink'))
        
        self.initial = ZebraState(self.variables)

    def run_zebra(self):
        self.explore(self.initial, self.domains)

    def explore(self, state, domain):
        if self.solution:
            return

        if len(state.unassigned) < 25:
            failure = self.check_constraints(state.assigned)
            if failure:
                return

        if len(state.unassigned) > 0:
            zebra_var = state.unassigned.pop()
            
            if domain[zebra_var.name]:
                var_value = domain[zebra_var.name][0]
            else:
                return
            zi = ZebraVar(zebra_var.name, var_value)
            domain[zebra_var.name].remove(var_value)
            for idx in xrange(5):
                if state.assigned[idx][zi.name] is None:
                    new_unass = copy.deepcopy(state.unassigned)
                    state.assigned[idx][zi.name] = zi.value
                    self.explore(ZebraState(new_unass, state.assigned), domain)
                    if self.solution:
                        return
                    state.assigned[idx][zi.name] = None
            domain[zebra_var.name].append(var_value)
        else:
            if self.all_filled(state.assigned):
                self.solution = state

    def all_filled(self, assigneds):
        for house in assigneds:
            if None in house.values():
                return False
        return True

    """Every constraint checking function returns the answer to: Was there a failure?"""

    def ingles_vermelha(self, better_dict):
        if 'ingles' in better_dict and 'vermelha' in better_dict and better_dict['ingles'] != better_dict['vermelha']:
            return True  
        return False


    def espanhol_cachorro(self, better_dict):
        if 'espanhol' in better_dict and 'cachorro' in better_dict and better_dict['espanhol'] != better_dict['cachorro']:
            return True  
        return False

    def noruegues_primeira(self, better_dict):
        if 'noruegues' in better_dict and better_dict['noruegues'] != 0:
            return True  
        return False

    def kool_amarela(self, better_dict):
        if 'kool' in better_dict and 'amarela' in better_dict and better_dict['kool'] != better_dict['amarela']:
            return True  
        return False

    def chester_lado_raposa(self, better_dict):
        if 'chester' in better_dict and 'raposa' in better_dict and abs(better_dict['chester']-better_dict['raposa'])!=1:
            return True  
        return False

    def noruegues_lado_casa_azul(self, better_dict):
        if 'noruegues' in better_dict and 'azul' in better_dict and abs(better_dict['noruegues']-better_dict['azul'])!=1:
            return True  
        return False

    def winston_caramujos(self, better_dict):
        if 'winston' in better_dict and 'caramujos' in better_dict and better_dict['winston'] != better_dict['caramujos']:
            return True  
        return False

    def lucky_suco_laranja(self, better_dict):
        if 'lucky' in better_dict and 'laranja' in better_dict and better_dict['lucky'] != better_dict['laranja']:
            return True  
        return False

    def ucraniano_cha(self, better_dict):
        if 'ucraniano' in better_dict and 'cha' in better_dict and better_dict['ucraniano'] != better_dict['cha']:
            return True  
        return False

    def japones_fuma_parliament(self, better_dict):
        if 'japones' in better_dict and 'parliament' in better_dict and better_dict['japones'] != better_dict['parliament']:
            return True  
        return False

    def kool_lado_cavalo(self, better_dict):
        if 'kool' in better_dict and 'cavalo' in better_dict and abs(better_dict['kool']-better_dict['cavalo'])!=1:
            return True  
        return False


    def cafe_casa_verde(self, better_dict):
        if 'cafe' in better_dict and 'verde' in better_dict and better_dict['cafe'] != better_dict['verde']:
            return True  
        return False

    def verde_a_direita_marfim(self, better_dict):
        if 'verde' in better_dict and 'marfim' in better_dict and better_dict['verde']-better_dict['marfim']!=1:
            return True  
        return False

    def leite_casa_meio(self, better_dict):
        if 'leite' in better_dict and better_dict['leite'] != 2:
            return True
        else:
            return False

    def check_constraints(self, assigneds):
        better_dict = {}
        for index, house in enumerate(assigneds):
            for v in house.values():
                better_dict[v] = index

        if self.noruegues_primeira(better_dict):
            return True
        if self.espanhol_cachorro(better_dict):
            return True
        if self.kool_amarela(better_dict):
            return True
        if self.chester_lado_raposa(better_dict):
            return True
        if self.noruegues_lado_casa_azul(better_dict):
            return True
        if self.winston_caramujos(better_dict):
            return True
        if self.lucky_suco_laranja(better_dict):
            return True
        if self.ucraniano_cha(better_dict):
            return True
        if self.japones_fuma_parliament(better_dict):
            return True
        if self.kool_lado_cavalo(better_dict):
            return True
        if self.cafe_casa_verde(better_dict):
            return True        
        if self.verde_a_direita_marfim(better_dict):
            return True        
        if self.leite_casa_meio(better_dict):
            return True
        if self.ingles_vermelha(better_dict):
            return True
        return False
        

zebra = Zebra()
zebra.run_zebra()
for elt in zebra.solution.assigned:
    print elt