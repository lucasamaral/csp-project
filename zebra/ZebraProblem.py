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
        # print state.assigned
        if self.solution:
            # print('ret1')
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
            zi = ZebraVar(zebra_var.name, var_value) #maybe this is not neccessary
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
            if house['nation'] == None or house['cigar'] == None or house['animal'] == None or \
                house['color'] == None or house['drink'] == None:
                return False
        return True

    """Every constraint checking function returns the answer to: Was there a failure?"""

    def ingles_vermelha(self, assigneds):
        for house in assigneds:
            if house['nation'] and house['nation'] == 'ingles' and \
                house['color'] and house['color'] != 'vermelha':
                return True
            if house['color'] and house['color'] == 'vermelha' and \
                house['nation'] and house['nation'] != 'ingles':
                return True
        return False


    def espanhol_cachorro(self, assigneds):
        for house in assigneds:
            if house['nation'] and house['nation'] == 'espanhol' and \
                house['animal'] and house['animal'] != 'cachorro':
                return True
            if house['nation'] and house['nation'] != 'espanhol' and \
                house['animal'] and house['animal'] == 'cachorro':
                return True
        return False

    def noruegues_primeira(self, assigneds):
        for house in assigneds:
            if house['nation'] and house['nation'] == 'noruegues' and assigneds.index(house) != 0:
                return True
            if house['nation'] and house['nation'] != 'noruegues' and assigneds.index(house) == 0:
                return True
        return False

    def kool_amarela(self, assigneds):
        for house in assigneds:
            if house['cigar'] and house['cigar'] == 'kool' and \
                house['color'] and house['color'] != 'amarela':
                return True
            if house['cigar'] and house['cigar'] != 'kool' and \
                house['color'] and house['color'] == 'amarela':
                return True
        return False

    def chester_lado_raposa(self, assigneds):
        for idx in xrange(5):
            if assigneds[idx]['cigar'] and assigneds[idx]['cigar'] == 'chester':
                if idx > 0 and idx < 4:
                    if assigneds[idx-1]['animal'] and assigneds[idx-1]['animal'] != 'raposa' and \
                        assigneds[idx+1]['animal'] and assigneds[idx+1]['animal'] != 'raposa':
                        return True
                elif idx == 0:
                    if assigneds[idx+1]['animal'] and assigneds[idx+1]['animal'] != 'raposa':
                        return True
                elif idx == 4:
                    if assigneds[idx-1]['animal'] and assigneds[idx-1]['animal'] != 'raposa':
                        return True
        return False

    def noruegues_lado_casa_azul(self, assigneds):
        for idx in xrange(5):
            if assigneds[idx]['nation'] and assigneds[idx]['nation'] == 'noruegues':
                if idx > 0 and idx < 4:
                    if assigneds[idx-1]['color'] and assigneds[idx-1]['color'] != 'azul' and \
                        assigneds[idx+1]['color'] and assigneds[idx+1]['color'] != 'azul':
                        return True
                elif idx == 0:
                    if assigneds[idx+1]['color'] and assigneds[idx+1]['color'] != 'azul':
                        return True
                elif idx == 4:
                    if assigneds[idx-1]['color'] and assigneds[idx-1]['color'] != 'azul':
                        return True
        return False

    def winston_caramujos(self, assigneds):
        for house in assigneds:
            if house['cigar'] and house['cigar'] == 'winston' and \
                house['animal'] and house['animal'] != 'caramujos':
                return True
            if house['cigar'] and house['cigar'] != 'winston' and \
                house['animal'] and house['animal'] == 'caramujos':
                return True
        return False

    def lucky_suco_laranja(self, assigneds):
        for house in assigneds:
            if house['cigar'] and house['cigar'] == 'lucky' and \
                house['drink'] and house['drink'] != 'laranja':
                return True
            if house['cigar'] and house['cigar'] != 'lucky' and \
                house['drink'] and house['drink'] == 'laranja':
                return True
        return False

    def ucraniano_cha(self, assigneds):
        for house in assigneds:
            if house['nation'] and house['nation'] == 'ucraniano' and \
                house['drink'] and house['drink'] != 'cha':
                return True
            if house['nation'] and house['nation'] != 'ucraniano' and \
                house['drink'] and house['drink'] == 'cha':
                return True
        return False

    def japones_fuma_parliament(self, assigneds):
        for house in assigneds:
            if house['nation'] and house['nation'] == 'japones' and \
                house['cigar'] and house['cigar'] != 'parliament':
                return True
            if house['nation'] and house['nation'] != 'japones' and \
                house['cigar'] and house['cigar'] == 'parliament':
                return True
        return False

    def kool_lado_cavalo(self, assigneds):
        for idx in xrange(5):
            if assigneds[idx]['cigar'] and assigneds[idx]['cigar'] == 'kool':
                if idx > 0 and idx < 4:
                    if assigneds[idx-1]['animal'] and assigneds[idx-1]['animal'] != 'cavalo' and \
                        assigneds[idx+1]['animal'] and assigneds[idx+1]['animal'] != 'cavalo':
                        return True
                elif idx == 0:
                    if assigneds[idx+1]['animal'] and assigneds[idx+1]['animal'] != 'cavalo':
                        return True
                elif idx == 4:
                    if assigneds[idx-1]['animal'] and assigneds[idx-1]['animal'] != 'cavalo':
                        return True
        return False

    def cafe_casa_verde(self, assigneds):
        for house in assigneds:
            if house['drink'] and house['drink'] == 'cafe' and \
                house['color'] and house['color'] != 'verde':
                return True
            if house['drink'] and house['drink'] != 'cafe' and \
                house['color'] and house['color'] == 'verde':
                return True
        return False

    def verde_a_direita_marfim(self, assigneds):
        for idx in xrange(5):
            if assigneds[idx]['color'] and assigneds[idx]['color'] == 'marfim':
                if idx == 4:
                    return True
                if assigneds[idx+1]['color'] and assigneds[idx+1]['color'] != 'verde':
                    return True
        return False

    def leite_casa_meio(self, assigneds):
        if assigneds[2]['drink'] and assigneds[2]['drink'] != 'leite':
            return True
        else:
            return False

    def check_constraints(self, assigneds):
        better_dict = {}
        for index, house in enumerate(assigneds):
            for v in house.values():
                better_dict[v] = index

        if self.noruegues_primeira(assigneds, better_dict):
            return True
        if self.espanhol_cachorro(assigneds, better_dict):
            return True
        if self.kool_amarela(assigneds, better_dict):
            return True
        if self.chester_lado_raposa(assigneds, better_dict):
            return True
        if self.noruegues_lado_casa_azul(assigneds, better_dict):
            return True
        if self.winston_caramujos(assigneds, better_dict):
            return True
        if self.lucky_suco_laranja(assigneds, better_dict):
            return True
        if self.ucraniano_cha(assigneds, better_dict):
            return True
        if self.japones_fuma_parliament(assigneds, better_dict):
            return True
        if self.kool_lado_cavalo(assigneds, better_dict):
            return True
        if self.cafe_casa_verde(assigneds, better_dict):
            return True        
        if self.verde_a_direita_marfim(assigneds, better_dict):
            return True        
        if self.leite_casa_meio(assigneds, better_dict):
            return True
        # return False
        if self.ingles_vermelha(assigneds, better_dict):
            return True
        return False
        

zebra = Zebra()
zebra.run_zebra()
for elt in zebra.solution.assigned:
    print elt
# print(zebra.solution.assigned)
