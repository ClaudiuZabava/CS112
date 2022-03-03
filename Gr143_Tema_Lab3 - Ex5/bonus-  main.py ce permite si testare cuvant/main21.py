import sys
import re
sigma=[] #alfabetul
stari=[] #starile{q1,q2...}
s_final=[] #stari finale
transition=[] #muchiile (i,k,j)
s_start=0 #starea initiala
elemente=0 # cele 3 taguri ( states, sigma, transitions)
s_valid=0 #contor, tine minte nr de aparitii ale starii de start
t_valid=1 #contor, indica daca sectiunea Transitions este valida sua nu
sectiuni_valide=1 #contor, indica daca cele 3 stari sunt valide ( nu au fost introduse si alte stari / cuvinte necunoscute)

director=sys.argv[1] if len(sys.argv)>1 else "date2.in" # atunci cand se doreste rularea din command line, director retine argumentul din CMD

with open(director) as f:
    cuv=f.readline().rstrip('\n')
    while elemente<3: # cat timp nu am citit toate cele 3 taguri

        if cuv=='':
            pass

        elif cuv[0] == '#': #daca cuv citit este un rand gol sau comentariu, skip
            pass

        elif cuv == "Sigma:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='': # verificam ca in interiorul tagului Sigma sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam litera de alfabet de spatii, virgula etc..
                    sigma.append(cuv[0]) #adaugam litera in alfabet
                cuv = f.readline().rstrip('\n')

        elif cuv == "States:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End":
                if cuv!='':  # verificam ca in interiorul tagului States sa nu gasim un rand gol
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam starea si , in unele cazuri, tipul acesteia de restul spatiilor, separatorilor
                    stari.append(cuv[0]) # memoram starea indiferent de tipul acesteia
                    if len(cuv) >= 2: # daca pe randul respectiv avem 2 obiecte citite
                        if cuv[1] == 'F' or (len(cuv)==3 and cuv[2] == 'F'):
                            s_final.append(cuv[0]) #daca este o stare finala, o adaugam in lista de stari finale
                        if cuv[1] == 'S':
                            s_valid+=1 #contorizam nr de aparitii ale acestei stari ( de regula, trebuie sa fie maxim 1)
                            s_start = cuv[0] # daca este starea initiala, o memoram alaturi dee nr ei de aparitii
                cuv = f.readline().rstrip('\n')

        elif cuv == "Transitions:":
            elemente+=1
            cuv = f.readline().rstrip('\n')
            while cuv != "End": # verificam ca in interiorul tagului Transitions sa nu gasim un rand gol
                if cuv!='':
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam starile si litera de alfabet de restul separatorilor, spatiilor
                    if cuv[1] not in sigma or cuv[0] not in stari or cuv[2] not in stari: # daca nu se citesc stari sau litere din alfabetul nostru, input devine invalid
                        t_valid=0 # daca tranzitia curenta nu are stari sau litere din alfabetul deja citit, sectiunea transitions e invalida
                    elif cuv[1] in sigma and cuv[0] in stari and cuv[2] in stari: # creem un tuplu <i, k, j> doar daca k apartine alfabetului nostru
                        t = cuv[0], cuv[1], cuv[2]
                        transition.append(t) # memoram tuplul (muchia)
                cuv = f.readline().rstrip('\n')

        elif cuv!="Sigma:" and cuv!="States:" and cuv!="Transitions:" and cuv!="End" and cuv[0]!='#' and cuv!='':
            sectiuni_valide=0 # daca a fost detectata o sectiune necunoscuta / un cuvant care nu respecta tiparul , inputul e invalid
            break;

        cuv = f.readline().rstrip('\n')

if s_valid!=1:
    print("Input Invalid")
    afd=0 # daca inputul este invalid, acest contor idica faptul ca afd nu poate rula

elif t_valid==0:
    print("Input Invalid")
    afd=0

elif sectiuni_valide==0:
    print("Input Invalid")
    afd=0

else:
    afd=1 # inputul este valid -> afd poate rula.
    print("Input Valid")
    print()
    print("Alfabetul:",sigma,sep='\n')
    print("Starile:",stari,sep='\n')
    print("Stari finale:",s_final,sep='\n')
    print("Stare initiala:", s_start, sep='\n')
    print("Tranzitiile:", transition, sep='\n')



''' AFD to Min-AFD'''

if afd==1:         #daca inputul a fost valid, ne apucam sa il transformam intr-un afd minimal
    zero = []
    matrice = [[0 for i in range(0, j)] for j in range(0, len(stari))]         # construim matricea triunghiulara, initial cu 0
    for i in range(0, len(stari)):
        for j in range(i + 1, len(stari)):         # ne deplasam doar in partea de jos a matricei ( in triunghi)
            if (stari[i] in s_final and stari[j] not in s_final) or (stari[i] not in s_final and stari[j] in s_final):
                matrice[j][i] = 1          # marcam doar daca avem o pereche de stare finala si nefinala, conform teoriei.
            else:
                zero.append((str(i), str(j)))         # memoram perechile de stari ce au ramas 0. Astfel le putem accesa mai repede la urmatoarea verificare


    print()
    print("Initial Nemarcate in matrice:",zero,sep='\n')

    def tranzitie(x, c):
        ok3 = 0
        for s in stari:
            if (x, c, s) in transition:      # in aceasta functie verificam daca gasim o tranzitie care sa plece din starea X cu caracterul C
                ok3 = 1
                return s
        if ok3 == 0:      # daca am gasit ce cautam, returnam celalalt capat al tranzitie (muchiei). Daca nu, returnam 0.
            return 0


    ok = 1
    while ok:
        op = 0
        t = 0
        while t < len(zero):
            if matrice[int(zero[t][1])][int(zero[t][0])] == 0:     # reverificam matricea, in special pe pozitiile care initial au ramas 0 (cele salvate in lista zero[])
                for c in sigma:
                    ok1=0                            # zero[t][0] si zero[t][1] reprezinta elementele tuplului de pe pozitia t din lista zero[]
                    t1 = tranzitie(zero[t][0], c)    # t1 retine starea in care se ajunge plecand din starea z[t][0] cu o litera C
                    t2 = tranzitie(zero[t][1], c)    # t2 retine starea in care se ajunge plecand din starea z[t][1] cu o litera C
                    if int(t1) < int(t2):
                        t1, t2 = t2, t1              # intrucat matricea noastra este triunghiulara , ne asiguram ca ordinea 'indicilor' este cea corecta
                    if t1 != 0 and t2 != 0 and t1 != t2:
                        if matrice[int(t1)][int(t2)] == 1:        # ne asiguram ca starile in care se ajunge sunt diferite, si verificam daca pozitia formata din starile destinatie este deja marcata in matrice
                            matrice[int(zero[t][1])][int(zero[t][0])] = 1
                            op+=1      # tine minte daca in matrice au intervenit schimbari.
                            ok1=1
                            zero.remove(zero[t])        # daca conditiile au fost respectate inseamna ca pozitia formata din starile din care am plecat cu o litera C poate fi si ea marcata cu 1.
                            t = t - 1       # dupa ce o marcam, respectiva pereche de stari este stearsa din lista zero[]
                    if ok1==1:      # ok=1 indica faptul ca am gasit o litera C din alfabet pentru care conditiile au fost respectate. Nu este nevoie sa cautam alta asa ca forul se opreste aici.
                        break
            t += 1      #avansam in lista de perechi de stari nemarcate
        if op == 0:     # daca in matrice nu au intervenit shcimbari -> putem sa ne oprin din reverificare.
            ok = 0



    print()
    print("Matricea:")    # cum arata acum matricea :
    for i in range(1, len(stari)):
        for j in range(0, i):
            print(matrice[i][j], sep=" ", end=" ")
        print()



    perechi = []        # Acum, cel mai probabil, in matrice inca au ramas positii egale cu 0 ce nu pot fi modificate. Le vom pastra in lista de liste numita perechi.
    perechi.append(list(zero[0][0]))
    for t in zero:
        ok = 0
        p = 0
        while p<len(perechi):
            if t[0] in perechi[p]:
                perechi[p].append(t[1])
                ok = 1
                break
            elif t[1] in perechi[p]:
                perechi[p].append(t[0])
                ok = 1
                break
            elif t[0] not in perechi[p] and t[1] not in perechi[p]:
                perechi.append(list(t[0]))
            p+=1

    print()     # pastram in perechi[] toate starile care au ramas 0 si care sunt unite prin indici: ex: in matirce pe pozitia 1-2 este 0 dar si pe pozitia 3-2 -> in perechi vom avea [ [1,2,3] , [alta lista..] ..etc ]
    print("Perechile reprezentand noile stari:", perechi, sep='\n')       # pastram aceste stari deoarece le vom uni si vom crea sari noi



    for i in range(0, len(perechi)):
        stari.append(str(int(stari[len(stari) - 1]) + 1))      # adaugam stari noi reprezentand perechile de stari mentionate mai sus, unite. ex: starile din lista [1,2] se unesc si se adauga o stare noua, starea 7.
    # aici id-ul starile adaugate pot sa difere fata de cele din exemplu, dar au aceeasi functionalitate !( de ex. starea 7 din exemplul de la lab se poate numi aici starea 6, dar functionalitatea ei este corecta)

    for i in range(0, len(perechi)):
        j = 0
        ok1 = 0
        while (j < len(transition)):
            if transition[j][0] in perechi[i] and transition[j][2] in perechi[i]:
                new_t=(stari[len(stari) - len(perechi) + i], transition[j][1], stari[len(stari) - len(perechi) + i])
                if new_t not in transition:
                    transition.append(new_t)              # in urmatoarele linii de cod, ne asiguram ca legam noile stari cu tranzitiile corespunzatoare starilor din care au fost compuse.
                transition.remove(transition[j])         # unele tranzitii pot sa nu mai fie necesare (reprezinta dubluri).
                j -= 1
            elif transition[j][0] in perechi[i] and transition[j][2] not in perechi[i]:
                new_t = (stari[len(stari) - len(perechi) + i], transition[j][1], transition[j][2])
                if new_t not in transition:
                    transition.append(new_t)
                transition.remove(transition[j])
                j -= 1
            elif transition[j][0] not in perechi[i] and transition[j][2] in perechi[i]:
                new_t=(transition[j][0], transition[j][1], stari[len(stari) - len(perechi) + i])
                if new_t not in transition:
                    transition.append(new_t)
                transition.remove(transition[j])
                j -= 1
            j += 1
        if str(s_start) in perechi[i]:
            s_start = int(stari[len(stari) - len(perechi) + i])      # redefinim starea de start
        st = 0
        while st < len(s_final):
            if s_final[st] in perechi[i]:
                if ok1 == 0:
                    s_final.append(stari[len(stari) - len(perechi) + i])       # redefinim starile finale
                    ok1 = 1
                s_final.remove(s_final[st])
                st -= 1
            st += 1



    print()    # iata aici noul AFD-minimal, cu noile stari si tranzitiile reinoite:
    print("Noul AFD-Minimal:")
    print()
    print("Alfabetul:", sigma, sep='\n')
    print("Starile:", stari, sep='\n')
    print("Stari finale:", s_final, sep='\n')
    print("Stare initiala:", s_start, sep='\n')
    print("Tranzitiile:", transition, sep='\n')



'''  Test cuvant - AFD minimal   '''

if afd==1: #daca inputul a fost valid, afd-ul ruleaza si se asteapta date de intrare.

    c=sys.argv[2] if len(sys.argv)>2 else input() # atunci cand se doreste rularea din command line, c retine argumentul din CMD

    s_init=str(s_start) #initializam starea initiala cu starea de inceput

    ok=1 # contor pentru a determina daca un cuvant citit are doar litere din alfabetul sigma

    for i in c:

        gasit=0 # contor pentru a determina daca gasim o muchie si o stare corespunzatoare

        for t in transition:
            if s_init==t[0] and i==t[1]:  # daca am gasit o muchie corespunzatoare actualizam starea initiala
                s_init=t[2]
                gasit=1
                break

        if gasit==0:  # daca nu gasim o muchie corespunzatoare initializam contorul pentru cuvant cu 0
            ok=0
            break

    if ok==1 and s_init in s_final:  # daca sunt respectate criteriile , cuvantul este acceptat
        print("ACCEPTED")
    else:
        print("REJECTED")