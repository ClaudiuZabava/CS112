import sys
import re
start=[] #-> start symbol
epsilon=[] # aici o sa fie epsiolon
terminals=[]
n_terminals=[]
productions= {}
elemente=0 # cele 5 taguri ( states, sigma, transitions)
s_valid=0 #contor, tine minte nr de aparitii ale starii de start
t_valid=1 #contor, indica daca sectiunea Transitions este valida sua nu
nt_valid=1
p_valid=1
sectiuni_valide=1 #contor, indica daca cele 5 taguri sunt valide ( nu au fost introduse si alte taguri / cuvinte necunoscute)

director=sys.argv[1] if len(sys.argv)>1 else "date5.in" # atunci cand se doreste rularea din command line, director retine argumentul din CMD

with open(director) as f:
    cuv=f.readline().rstrip('\n')
    while elemente<5: # cat timp nu am citit toate cele 5 taguri (Start, teminals, non_terminals si productions)

        if cuv=='':
            pass

        elif cuv[0] == '#': #daca cuv citit este un rand gol sau comentariu, skip
            pass

        elif cuv == "Start:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='': # verificam ca in interiorul tagului Sigma sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam simbolul de start S de spatii, virgula etc..
                    start.append(cuv[0]) #salvam simbolul de start
                    s_valid+=1
                cuv = f.readline().rstrip('\n')

        elif cuv == "Epsilon:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='': # verificam ca in interiorul tagului sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam litera care il reprezinta pe epsilon de spatii, virgule, etc...
                    epsilon.append(cuv[0])
                cuv = f.readline().rstrip('\n')


        elif cuv == "Terminals:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='': # verificam ca in interiorul tagului sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam litera terminalului de spatii, virgula etc..
                    terminals.append(cuv[0]) #adaugam litera in lista de terminale
                    if cuv[0].isupper():
                        t_valid=0
                cuv = f.readline().rstrip('\n')

        elif cuv == "Nonterminals:":
            elemente+=1
            n_terminals.append(start[0])
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='': # verificam ca in interiorul tagului sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam litera nonterminalului de spatii, virgula etc..
                    n_terminals.append(cuv[0]) #adaugam litera in lista de nonterminale
                    if cuv[0].islower():
                        nt_valid=0
                cuv = f.readline().rstrip('\n')

        elif cuv == "Productions:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End": # verificam ca in interiorul tagului Productions sa nu gasim un rand gol
                if cuv!='':
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam terminalele si nonterminalele si combinatia cu epsilon ( daca avem) de restul separatorilor, spatiilor
                    if len(cuv)<=1:
                        p_valid=0
                    elif len(cuv[0])>1 and cuv[0] not in start and cuv[0] not in n_terminals:
                        p_valid=0
                    else:
                        productions[cuv[0]]=[]
                        for i in range(1,len(cuv)):
                            temp=[]
                            for j in cuv[i]:
                                if j not in terminals and j not in n_terminals and j not in epsilon and j not in start:
                                    p_valid=0
                                elif j in terminals or j in n_terminals or j in epsilon or j in start:
                                    temp.append(j)
                            productions[cuv[0]].append(temp)

                cuv = f.readline().rstrip('\n')

        elif cuv!="Start:" and cuv!="Epsilon:" and cuv!="Terminals:" and cuv!="Nonterminals:" and cuv!="Productions:" and cuv[0]!='#' and cuv!='':
            sectiuni_valide=0 # daca a fost detectata o sectiune necunoscuta / un cuvant care nu respecta tiparul , inputul e invalid
            break

        cuv = f.readline().rstrip('\n')



if s_valid!=1:
    print("CFG Input Invalid din s_valid")
    cfg=0 # daca inputul este invalid, acest contor idica faptul ca cfg nu poate rula

elif t_valid==0:
    print("CFG Input Invalid din t_valid")
    cfg=0

elif nt_valid==0:
    print("CFG Input Invalid din nt_valid")
    cfg=0
elif p_valid==0:
    print("CFG Input Invalid din p_valid")
    cfg=0

elif sectiuni_valide==0:
    print("CFG Input Invalid din sectiuni")
    cfg=0

else:
    cfg=1 # inputul este valid -> cfg poate rula.
    print("CFG input Valid")
    print()
    print("Start:",start,sep='\n')
    print("Epsilon:",epsilon,sep='\n')
    print("Terminals",terminals,sep='\n')
    print("Nonterminals:", n_terminals, sep='\n')
    print("Productions:", productions, sep='\n')


if cfg==1:

    def scoate_element(deriv):
        for x in n_terminals:
            if x not in deriv:

                if x in productions:
                    del productions[x]
                    for i in productions:
                        for j in range(0, len(productions[i])):
                            if x in productions[i][j]:
                                productions[i][j].remove(x)
                            if len(productions[i][j]) < 1:
                                productions[i].remove([])
                elif x not in productions:
                    for i in productions:
                        for j in range(0, len(productions[i])):
                            if x in productions[i][j]:
                                productions[i][j]=[]
                            if len(productions[i][j]) < 1:
                                productions[i].remove([])


    '''SIMPLIFICAREA UNUI CFG:'''


    ''' CFG Reduction '''
    # Eliminam productiile care nu ajung in terminals, productiile care blocheaza stringul nostru. Aceasta operatie se realizeaza in 2 etape
    #In prima faza retinem simbolurile nonterminale care conduc stringul spre simboluri terminale.

    '''Faza 1:'''
    deriv=[]
    for x in productions:
        okt=0
        for i in terminals:
            for j in productions[x]:
                if i in j:
                    okt=1
        if okt==1:
            deriv.append(x)
    deriv.sort()


    ok = 0
    while ok == 0:
        deriv_t = deriv.copy()
        for x in n_terminals:
            if x not in productions or x in deriv_t:
                pass
            elif x in productions and x not in deriv_t:
                for i in range(0,len(productions[x])):
                    for j in productions[x][i]:
                        if j in deriv_t:
                            deriv.append(x)
                            i = len(productions[x])
                            break
            else:
                pass
        deriv.sort()
        if deriv_t == deriv:
            ok = 1
        else:
            deriv_t = deriv.copy()


    scoate_element(deriv)


    # In faza 2, plecand din Start si folosind modificarile din faza 1, gasim si eliminam simbolurile tranzitive sau inaccesibile din start
    ''' Faza 2 '''

    deriv=[]
    deriv.append(start[0])

    ok2=0

    while ok2==0:
        deriv_t=deriv.copy()

        for x in deriv_t:

            for i in productions[x]:
                for j in i:
                    if j not in deriv and j in n_terminals:
                        deriv.append(j)

        if deriv_t == deriv:
            ok2=1
        else:
            deriv_t=deriv.copy()

    scoate_element(deriv)

    tempr=terminals.copy()
    for i in range(0,len(terminals)):
        nr=0
        for x in productions:
            for j in productions[x]:
                if terminals[i] in j:
                    nr+=1
        if nr == 0:
            tempr.remove(terminals[i])
    terminals=tempr.copy()

    tempr=n_terminals.copy()
    for i in range(0,len(n_terminals)):
        nr=0
        for x in productions:
            if n_terminals[i] == x:
                nr+=1
        if nr == 0:
            tempr.remove(n_terminals[i])
    n_terminals=tempr.copy()

    print()
    print("Dupa Cfg Reduction:")
    print("Terminals", terminals, sep='\n')
    print("Nonterminals:", n_terminals, sep='\n')
    print("Productions:", productions, sep='\n')




    ''' Removing epsilon / null productions'''
   # Aici ne vom ocupa de productiile care contin epsilon. Vom elimina si inlocui fiecare 'epsilon' cu productii mai bune astfel incat sa pastram regulile de functionare ale cfg ului.

    eps = []

    for i in productions:
        for j in productions[i]:
            if len(j) == 1 and j[0] in epsilon:
                eps.append(i)


    temp_n={}
    for i in eps:
        temp_n[i]=[]
        for j in productions[i]:
            if len(j)==1 and j[0] not in epsilon:
                temp_n[i].append(j)
            elif len(j)>1:
                temp=[]
                for k in j:
                    if k !=i:
                        temp.append(k)
                temp_n[i].append(temp)
        productions[i].remove(['0'])
        for j in temp_n[i]:
            productions[i].append(j)

    for i in productions:
        temp=[]
        if i not in eps:
            for j in productions[i]:
                if len(j) == 1 and j[0] in eps:
                    for k in temp_n[j[0]]:
                        productions[i].append(k)
                elif len(j) > 1:
                    for k in range(0, len(j)):
                        if j[k] in eps:
                            t1 = j[0:k]
                            t2 = j[k + 1:len(j)]
                            t1 = t1 + t2
                            temp.append(t1)
            for j in temp:
                productions[i].append(j)
    print()
    print("Dupa eliminarea null productions:")
    print("Terminals", terminals, sep='\n')
    print("Nonterminals:", n_terminals, sep='\n')
    print("Productions:", productions, sep='\n')


    '''Remove unit productions'''
    # In final ne vom ocupa de productiile unitare. Acest tip de productii nu conduc spre terminali ci doar spre nonterminals asa ca vor fii inlocuite sau sterse.
    # Vom modifica productiile care pleaca si din starea de start pentru a pastra regulile de functionare a cfg ului.
    ok3=0
    while ok3 == 0:
        temp_d = {}
        nr = 0
        for x in productions:
            for i in range(0, len(productions[x])):
                temp = []
                if len(productions[x][i]) == 1 and productions[x][i][0] in n_terminals:
                    nr += 1
                    temp.append(productions[x][i])
                    temp_d[x] = temp
        if nr == 0:
            ok3 = 1
            break

        for i in temp_d:
            if i not in start:
                for j in productions[temp_d[i][0][0]]:
                    if len(j) == 1 and j[0] == i:
                        pass
                    elif j not in temp_d[i]:
                        temp_d[i].append(j)



        for i in temp_d:
            if i not in start:
                for j in range(0, len(productions[i])):
                    if productions[i][j] == temp_d[i][0]:
                        productions[i][j] = temp_d[i][1].copy()
                        if len(temp_d[i])>2:
                            for k in range(2,len(temp_d[i])):
                                if temp_d[i][k] not in productions[i]:
                                    productions[i].append(temp_d[i][k])

        # gasim productiile si simbolurile inaccesibile si le stergem
        to_delete = []
        for i in productions:
            if i not in to_delete:
                for j in productions:
                    if productions[i] == productions[j] and i != j:
                        to_delete.append(j)


        # aici stergem ce se afla in to_delete
        for k in to_delete:
            productions.pop(k)
            n_terminals.remove(k)
            temp_d.pop(k)
            for i in productions:
                if list(k) in productions[i]:
                    productions[i].remove(list(k))
                for j in range(0, len(productions[i])):
                    if len(productions[i][j]) > 1:
                        if k in productions[i][j]:
                            productions[i][j].remove(k)

        # executam operatiile de mai sus din nou, de data asta pe simbolul de start:
        for i in temp_d:
            if i in start:
                if temp_d[i][0][0] in n_terminals:
                    for j in productions[temp_d[i][0][0]]:
                        if len(j) == 1 and j[0] == i:
                            pass
                        elif j not in temp_d[i]:
                            temp_d[i].append(j)
        for i in temp_d:
            if i in start:
                for j in range(0, len(productions[i])):
                    if productions[i][j] == temp_d[i][0]:
                        productions[i][j] = temp_d[i][1].copy()
                        for k in range(2, len(temp_d[i])):
                            if temp_d[i][k] not in productions[i]:
                                productions[i].append(temp_d[i][k])
        temp_d.clear()
        to_delete.clear()
        temp.clear()

    print()
    print("Dupa eliminarea unit productions:")
    print("Terminals", terminals, sep='\n')
    print("Nonterminals:", n_terminals, sep='\n')
    print("Productions:", productions, sep='\n')


    #Afisare:
    print()
    print("Afisare CFG simplificat:")
    for i in productions:
        print(i,end="->")
        for j in range(0,len(productions[i])-1):
            for k in productions[i][j]:
                print(k,end="")
            print("|",end="")
        for k in productions[i][len(productions[i])-1]:
            print(k,end="")
        print()





