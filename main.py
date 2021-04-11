import sys
import string

E_one_state = []

# Functia determina epsilon pentru starea s
# Rezultatul este salvat in E_one_state
def det_epsilon(delta_nfa,s):
    # Daca starea a fost deja vizitata
    if s in E_one_state:
        return None
    
    # Se adauga starea
    E_one_state.append(s)
    
    # Daca starea nu are "drumuri" catre alte
    # stari, cautarea nu isi mai are sens
    if s not in delta_nfa.keys():
        return None

    # Se parcurg toate drumurile starii respective
    for symbol,nex_st in delta_nfa[s].items():
        
        # Daca exista o epsilon tranzitie
        if symbol == "eps":

            # Se aplica recursiv functia pentru fiecare epsilon tranzitie
            for nxt in nex_st:
                det_epsilon(delta_nfa,nxt)
        
    return None

if __name__ == "__main__":
    # Se deschide fisierul
    f = open(sys.argv[1], "r")
    
    # Se citeste numarul de stari
    states = f.readline().replace('\n','')
    
    # Se citesc starile finale
    finals = f.readline().replace('\n','').split(' ')
    
    delta_nfa = {}
    sigma = []

    while True: 
    
        # Se citeste linia
        line = f.readline()

        # Daca este goala, inseamna ca s-a terminat fisierul
        if not line: 
            break
        
        line = line.replace('\n','').split(' ')

        # Starea curenta
        current_state = line[0]

        # Simbol
        symbol = line[1]

        # Se actualizeaza alfabetul
        if (symbol not in sigma) and symbol != 'eps':
            sigma.append(symbol)

        # Starea urmatoare
        next_states = line[2:len(line)]

        # Se verifica daca exista starea curenta in delta_nfa
        if current_state not in delta_nfa.keys():
        
            # Daca nu exista, este adaugat un dictionar nou,
            # reprezentand "salturile" pentru starea respectiva
            next_step = {}
            next_step[symbol] = next_states
            delta_nfa[current_state] = next_step
        else:
            # Daca exista, se adauga noul simbol cu starile in care
            # se duce acesta
            delta_nfa[current_state][symbol] = next_states

    # Se inchide fisierul
    f.close()

    epsilon = {}

    # Se creaza dictionarul epsilon, care memoreaza epsilon
    # tranzitiile pentru fiecare stare din nfa
    for elem in range(0,int(states)):
        E_one_state.clear()
        det_epsilon(delta_nfa,str(elem))
        epsilon[str(elem)] = E_one_state.copy()

    delta_dfa = {}

    # In dfa_states se adauga starile noi descoperite,
    # urmand ca apoi sa se extraga cate o stare
    dfa_states = []

    # In selected_states se momoreaza starile care au
    # fost deja prelucrate
    selected_states = []

    # Se prelucreaza epsilon de 0, pentru a avea starile compuse
    # formate in aceeasi ordine
    aux = list(map(int, epsilon['0']))
    aux.sort()
    aux = list(map(str, aux))

    # Se incepe cu starea formata de epsilon aplicat pe starea initiala 
    # (Starile compuse se noteza cu . intre ele, pentru a putea
    # deosebi starea 12 de starea compusa 1.2
    dfa_states.append('.'.join(aux))

    while dfa_states:
        
        # Se extrage cate o stare 
        current_state = dfa_states.pop()
        
        # Se verifica daca aceasta nu a fost deja prelucrata
        if current_state not in selected_states:
            selected_states.append(current_state)
        else:
            continue
        
        next_s = {}
        # Se ia fiecare simbol din alfabet
        for elem in sigma:
            sink = 0
            nxt = []
            # Se selecteaza fiecare stare, din cea curenta
            # Pentru starea compusa 0.1 , se ia prima data
            # starea 0 dupa starea 1.
            for state in current_state.split('.'):
                
                # Se verifica daca starea are drumuri care pleaca din ea
                if state not in delta_nfa.keys():
                    continue
                
                # Se extrage dictionarul cu drumuri pentru starea respectiva
                new_states = delta_nfa[state]

                # Se concateneaza epsilonul starilor in care se ajunge
                if elem in new_states.keys():
                    for i in new_states[elem]:
                        nxt = nxt + epsilon[i]
            
            # Se elimina duplicatele
            nxt = list(set(nxt))

            # Se convertesc in int si se sorteaza
            nxt = list(map(int, nxt))
            nxt.sort()

            # Se converteste la loc in string
            nxt = list(map(str, nxt))

            # Se adauga starea la care se ajunge
            next_s[elem] = '.'.join(nxt)

            # Se verifica daca starea nu a mai fost selectata
            if next_s[elem] not in selected_states:
                dfa_states.append(next_s[elem])

        # Se declara drumurile pentru noua stare in dfa
        delta_dfa[current_state] = next_s
    
    final_states_dfa = []

    # Se genereaza starile finale dfa
    # Se ia fiecare stare din noul dfa creat si se verifica
    # daca ea contine cel putin o stare finala a nfa
    for elem in selected_states:
        for i in elem.split('.'):
            if i in finals:
                if elem not in final_states_dfa:
                    final_states_dfa.append(elem)

    # Se deschide fisierul pentru scriere
    f2 = open(sys.argv[2], "w")

    # Se scriu numarul total de stari a dfa
    f2.write(str(len(selected_states)) +'\n')
    
    # Se scriu starile finale a dfa
    for elem in final_states_dfa:
        f2.write(str(selected_states.index(elem)) + ' ')
    
    f2.write('\n')

    # Se scriu drumurile intre starile dfa
    for stare,next_step in delta_dfa.items():
        for symbol,next_states in next_step.items():
            
            f2.write(str(selected_states.index(stare)) +' '+ 
            str(symbol) + ' '+ str(selected_states.index(next_states)) +'\n')

    # Se inchide fisierul
    f2.close()
            


            
        

            
    
    