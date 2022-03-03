import sys
import re
sigma=[] #alfabetul
stari=[] #starile{q1,q2...}
s_final=[] #stari finale
transition=[] #muchiile (i,k,j)
capete_epsilon=[] # retinem aici capetele tranzitiilor / starile din care se pleaca cu Epsilon spre alte stari diferite
transition_epsilon=[] # retinem aici starile intre care se afla mucie cu Epsilon.
s_start=0 #starea initiala
elemente=0 # cele 3 taguri ( states, sigma, transitions)
s_valid=0 #contor, tine minte nr de aparitii ale starii de start
t_valid=1 #contor, indica daca sectiunea Transitions este valida sua nu
epsilon_valid=0 # contor ce tine minte daca NFA-ul are tranzitii cu epsilon intre 2 stari diferite
sectiuni_valide=1 #contor, indica daca cele 3 stari sunt valide ( nu au fost introduse si alte stari / cuvinte necunoscute)

director=sys.argv[1] if len(sys.argv)>1 else "date3.in" # atunci cand se doreste rularea din command line, director retine argumentul din CMD

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

                    if cuv[0] != 'E':
                        sigma.append(cuv[0]) #adaugam litera in alfabet. E reprezinta Epsilon , se considera de la sine deja existent

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

                    if cuv[1] == 'E' and cuv[0] in stari and cuv[0] == cuv[2]:  #  daca intalnim o tranzitie de genul : q1 Epsilon q1, nu e nevoie sa o salvam, este de la sine existenta
                        pass

                    elif (cuv[1] not in sigma and cuv[1]!='E') or cuv[0] not in stari or cuv[2] not in stari: # daca nu se citesc stari sau litere din alfabetul nostru, input devine invalid
                        t_valid=0 # daca tranzitia curenta nu are stari sau litere din alfabetul deja citit, sectiunea transitions e invalida

                    elif (cuv[1] in sigma or cuv[1] == 'E') and cuv[0] in stari and cuv[2] in stari: # creem un tuplu <i, k, j> doar daca k apartine alfabetului nostru

                        if cuv[1] == 'E' :
                            epsilon_valid+=1
                            capete_epsilon.append(cuv[0])
                            t1 = cuv[0], cuv[2]
                            transition_epsilon.append(t1)


                        t = cuv[0], cuv[1], cuv[2]
                        transition.append(t) # memoram tuplul (muchia)

                cuv = f.readline().rstrip('\n')

        elif cuv!="Sigma:" and cuv!="States:" and cuv!="Transitions:" and cuv!="End" and cuv[0]!='#' and cuv!='':
            sectiuni_valide=0 # daca a fost detectata o sectiune necunoscuta / un cuvant care nu respecta tiparul , inputul e invalid
            break

        cuv = f.readline().rstrip('\n')

if s_valid!=1:
    print("Input Invalid")
    afn=0 # daca inputul este invalid, acest contor idica faptul ca afd nu poate rula

elif t_valid==0:
    print("Input Invalid")
    afn=0

elif sectiuni_valide==0:
    print("Input Invalid")
    afn=0

else:
    afn=1 # inputul este valid -> afn poate rula.
    print("Input Valid")
    print()
    print("Alfabetul:",sigma,sep='\n')
    print("Starile:",stari,sep='\n')
    print("Stari finale:",s_final,sep='\n')
    print("Stare initiala:", s_start, sep='\n')
    print("Tranzitiile:", transition, sep='\n')
    print("Prezenta tranzitii cu epsilon:", epsilon_valid, sep='\n')
    if epsilon_valid!=0:
        print("Starile care pleaca cu Epsilon:", capete_epsilon, sep='\n')




'''  Mai jos vom testa daca un cuvant introdus este Acceptat sau Respins de AFN ( testam asta direct pe AFN, fara sa convertim AFN-ul la un AFD)  '''


ok=0  # tinem minte daca am ajuns macar o data intr-o stare finala si cuvantul parsat complet
def functie(s_init,temp, i, c):  # functie recursiva ce parcurge concomitent cuvantul si tranzitiile si tine minte daca s-a putut ajunge intr-o stare finala

    global ok
    for t in transition:   # parcurgem tranzitiile si incercam sa gasim cea mai buna alegere pentru litera curenta din alfabet
        if i>=len(c):
            if s_init in s_final and ok != 1:
                ok=1    # Daca s_init ( starea curenta in cazul asta) este o stare finala si cuvantul s-a terminat, tinem minte ca am gasit un traseu bun
            break
        elif s_init == t[0] and i < len(c) and c[i] == t[1]:  # cautam o tranzitie care sa plece din starea curenta si sa foloseasca litera curenta
            if t[2] in capete_epsilon:  # In plus, verificam si transitiile cu Epsilon ( notat E in cazul nostru), deoarece acestea ne duc direct in alta stare
                for t1 in transition_epsilon:
                    if t1[0] == t[2]:
                        temp = s_init
                        s_init = t1[1]
                        break
            else:
                temp = s_init    # In temp tinem minte fosta stare actuala ( folosim temp in recursivitate, la pasul de intoarcere)
                s_init = t[2]   # reactualizam starea actuala
            functie(s_init,temp,i+1,c)  # apelam functia recursiv
            s_init=temp  # la iseire din recursivitate , in caz ca nu am selectat tranzitiile cele mai bune, reincercam cu altele


if afn==1: #daca inputul a fost valid, afd-ul ruleaza si se asteapta date de intrare.

    c=sys.argv[2] if len(sys.argv)>2 else input() # atunci cand se doreste rularea din command line, c retine argumentul din CMD

    s_init=str(s_start) #initializam starea initiala cu starea de inceput

    ok=0
    temp='0'
    functie(s_init,temp, 0, c)
    if ok==1:  # daca sunt respectate criteriile , cuvantul este acceptat
        print("ACCEPTED")
    else:
        print("REJECTED")


