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

# !observate: Programul transofrma  un AFN normal intr-un AFD. Programul nu transforma un AFN-Epsilon intr-un AFD, dar verifica config-ul in conditiile de epsilon

director=sys.argv[1] if len(sys.argv)>1 else "date4.in" # atunci cand se doreste rularea din command line, director retine argumentul din CMD

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

                    if cuv[0] != 'E':  # Acest 'E' reprezinta notatia lui Epsilon din config
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




'''  Mai jos vom converti AFN -ul (daca este valid) intr-un AFD  '''

# Pentru a converti AFN in AFD vom folosi o matriec a carei linii au ca indice stari iar coloanele au ca indice literele din alfabet
# Continutul matricei ( matrice[i][j] ) va reprezenta starea ( fie ea deja existenta, fie alta noua ) in care se ajunge plecand din starea i cu litera j
# Daca apar noi stari, matricea se extinde , cuprinzandu-le si pe acelea
# Matricea va trece prin mai multe transformari pana in stadiul in care vor ramane doar starile ce intra in alcatuirea noului AFD



def perechi(i, row1):  # creeaza linia 'i' a matricei ( este creata o lista de noi stari, stari in care se ajunge plecand din starea 'i' cu cate o litera din alfabet)

    for j in sigma:    # aceasta functie perechi(..) este apelata in construirea matricei, mai jos
        pack = []
        ok1 = 0
        for t in transition:
            if t[0] == i and t[1] == j:
                ok1 = 1
                pack.append(t[2])
        if ok1 == 0:
            pack.append('Q')  # intrucat exista posibilitatea ca in matrice sa avem si elemente 'multime vida' , acestea sunt notate cu Q
        pack.sort()
        row1.append(pack)

if afn==1: #Daca inputul a fost valid, AFN-ul poate fi convertit la un AFD.
    matrice=[]  # Matricea mentionata mai sus
    for i in stari:
        row=[]
        perechi(i,row)
        matrice.append(row)    # Pentru inceput, completam matricea folosindu-ne de starile obisnuite ale AFN. In matrice vor aparea si stari noi (formate prin perechi din starile vechi)

    zero=[]  # In aceasta lista vom tine minte ce stari noi ( perechi formate din starile vechi) sunt la un moment dat
    istoric=[] # In aceasta lista vom tine minte TOATE starile noi aparute in matrice, dar si unele vechi, in functie de necesitatea lor.
    for i in matrice:
        for j in i:
            if len(j)>1 and j not in zero and j not in istoric:
                zero.append(j)    # In aceasta prima parcurgere a matricei, retinem starile noi ce s-au format prin grupare din 2 sau mai multe stari vechi
                istoric.append(j)   # Orice stare nou aparuta este salvata si in istoric


    while len(zero)>0:     # Acum ca avem la momentul actual un nr de stari noi, pentru fiecare dintre acestea creem alte linii in matrice care vor contine alte noi stari
        for i in range(0,len(zero)):   # Acest proces repetitiv se opreste atunci cand nu vom mai avea stari noi aparute
            final = []
            ok2=0
            for k in zero[i]:
                row = []
                perechi(k, row)

                if len(final) < 1: # Intrucat noile stari mentionate mai sus sunt defapt grupari de 2 sau mai multe stari vechi,
                    final = row    # pentru a afla unde ajungem plecand din aceasta stare compusa ( adica ce cu ce vom completa matricea ),
                else:              # o sa aflam pe rand unde ajungem plecand din fiecare stare din care este alcatuita cea noua
                    for j in range(0, len(final)):
                        if final[j][0] == 'Q' and row[j][0] == 'Q':
                            pass
                        elif final[j][0] != 'Q' and row[j][0] != 'Q':
                            for l in row[j]:
                                if l not in final[j]:
                                    final[j].append(l)  # Rezultatul final reprezinta linia corespunzatoare starii actuale in matrice
                            final[j].sort()
                        elif final[j][0] == 'Q' and row[j][0] != 'Q':
                            final[j] = row[j]
                        else:
                            pass
            for j in matrice:  # Pentru a evita cazurile de loop infinit, ne asiguram ca nu vom insera aceeasi linia cu aceleasi stari noi de mai multe ori
                if j == final:
                    ok2+=1
            if ok2<=1:
                matrice.append(final)
            nr = 0
            for j in final:
                if len(j) > 1 and j not in zero and j not in istoric:
                    nr += 1
                    zero.append(j)  # Asa cum am mentionat mai sus, zero retine starile noi (actuale) create prin matrice,
                    istoric.append(j)
            for j in range(0,len(zero)-nr):
                zero.pop(j)   # si le elimina pe cele ce au fost deja folosite pentru crearea unei linii in matrice
                i-=1


        # Mai departe vom verifica matricea pe coloane pentru a verifica daca
        # o stare creata anterior poate / trebuie refolosita pentru crearea altei linii in matrice

        for j in range(0,len(sigma)):
            for i in range(0,len(matrice)-1):
                nre=0
                for k in range(i+1,len(matrice)):
                    if matrice[i][j] == matrice [k][j] and matrice[i][j][0]!='Q':
                        nre+=1
                if nre == 1 and matrice[i][j] not in istoric:
                    zero.append(matrice[i][j])
                    istoric.append(matrice[i][j])
        # Toate aceste procese se repeta pana cand nu vom mai avea stari noi.


    print('\n')
    print("Matricea in raport cu starea corespunzatoare: ")
    for i in range(0,len(matrice)):  # Aruncam o privire sa vedem cum arata matricea in raport cu fiecare stare corespunzatoare
        if i<len(stari):
            print("starea ", i, " are: ", matrice[i])
        else:
            print("starea ", istoric[i-len(istoric)-1], " are: ", matrice[i])
    # Observam ca pot exista si dubluri la sfarsitul matricei. Acestea nu influenteaza noul AFD intrucat se iau din matrice doar anumite stari distince


    t_state=[] # Aici vom retine doar starile eligibile, starile pe baza carora se va construi noul AFD
    for i in range(0,len(matrice)):
        if i<len(stari):
            t_state.append(list(str(i)))
        else:
            if istoric[i-len(istoric)-1] not in t_state:
                t_state.append(istoric[i-len(istoric)-1])

    i=0
    nr_sters=0
    while i<len(matrice):  # Scapam din matrice de liniile corespunzatoare starilor ce nu intra in alcatuirea noului AFD
        if i<len(stari):
            ok3=0
            for j in matrice[i]:
                if j in istoric and len(j)>=1:
                    ok3=1
                    break
            temp=[]
            temp.append(str(i))
            if str(i) != s_start and ok3==0:
                t_state.pop(i-nr_sters)
                matrice[i]=[['Q']]  # Prima data le marcam, pentru a sti unde sa cautam la stergere
                nr_sters+=1
        i+=1
    i=0
    while i<len(matrice):
        if len(matrice[i])<len(sigma):
            matrice.pop(i)  # Apoi are loc stergerea efectiva
            i-=1
        i+=1


    ok4=0
    s_start1=[]  # Datorita noilor stari, trebuie sa regasim starea de start si starile finale
    s_final1=[]  # Asa cum am zis , o parte din noile stari sunt compuse din stari vechi.
                 # Astfel, daca o stare veche din compozitia unei stari noi a fost s_finala sau s_initiala, atunci si noua stare va fi
    for i in t_state:
        for j in i:
            if j in s_final:
                s_final1.append(i)
                break
    for i in t_state:
        for j in i:
            if ok4==0 and j== s_start:
                s_start1 = i
                ok4=1
                break
    s_final=s_final1 # Inlocuim starile finale si cea de start cu cele actuale
    s_start=s_start1
    stari=t_state  # Inlocuim starile vechi cu cele actuale.
                   # ! observatie : noile stari nu vor mai fi o lista de elemente, vor fi o lista de liste intrucat o stare acum poate fi compusa din alte 2 stari vehci


    i=0
    transition=[]  # Recreem tranzitiile ghidandu-ne de noile stari si de matrice. Se va lucra acum cu o lista de tupluri ce contine alte mici liste
    for i in range(0,len(stari)):
        for j in range(0,len(sigma)):
            if matrice[i][j][0]!='Q':
                t= stari[i], sigma[j], matrice[i][j]
                transition.append(t)

    # Iata AFD - ul obtinut din vechiul AFN!!!

    print('\n')
    print("AFD-ul obtinut din fostul AFN :")
    print()
    print("Alfabetul:", sigma, sep='\n')
    print("Starile:", stari, sep='\n')
    print("Stari finale:", s_final, sep='\n')
    print("Stare initiala:", s_start, sep='\n')
    print("Tranzitiile:", transition, sep='\n')
    print('\n')
    print("! Pentru a testa si un cuvant -> vezi folderul ||AFN to AFD + testarea unui cuvant|| ")




# Acest cod a fost realizat de: Zabava Claudiu Alexandru
# Ajutoare: Elena Adania Miu, Rinu Alexandru Ionut
