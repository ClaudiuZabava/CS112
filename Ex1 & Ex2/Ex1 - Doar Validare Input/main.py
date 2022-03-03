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


director=sys.argv[1] if len(sys.argv)>1 else "date.in" # atunci cand se doreste rularea din command line, director retine argumentul din CMD

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
            frecv=[0 for i in range(0,len(stari)+1)]
            cuv = f.readline().rstrip('\n')
            while cuv != "End": # verificam ca in interiorul tagului Transitions sa nu gasim un rand gol
                if cuv!='':
                    cuv = cuv.strip()
                    cuv = re.split('\W+', cuv) # separam starile si litera de alfabet de restul separatorilor, spatiilor
                    if cuv[1] not in sigma or cuv[0] not in stari or cuv[2] not in stari: # daca nu se citesc stari sau litere din alfabetul nostru, input devine invalid
                        t_valid=0 # daca tranzitia curenta nu are stari sau litere din alfabetul deja citit, sectiunea transitions e invalida
                    elif frecv[int(cuv[0])]>1: # mai avem o tranzitie ce pleaca din starea cuv[0] -> nu e bun
                        t_valid=0
                    elif cuv[1] in sigma and cuv[0] in stari and cuv[2] in stari: # creem un tuplu <i, k, j> doar daca k apartine alfabetului nostru
                        t = cuv[0], cuv[1], cuv[2]
                        transition.append(t) # memoram tuplul (muchia)
                        frecv[int(cuv[0])]+=1
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
    afd = 1  # inputul este valid -> afd poate rula.
    print("Input Valid")
    print()
    print("Alfabetul:", sigma, sep='\n')
    print("Starile:", stari, sep='\n')
    print("Stari finale:", s_final, sep='\n')
    print("Stare initiala:", s_start, sep='\n')
    print("Tranzitiile:", transition, sep='\n')


'''  AFD - acceptare cuvant -> vedeti cealalta arhiva trimisa   '''