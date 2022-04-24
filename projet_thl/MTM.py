from os import name
import sys
from typing import List, final 

class Transition:
    """classe simulant une transition pour une mt"""

    def __init__(self,caralu,caraecri,mouv,etatsuivant):
        self.caracterlu=caralu
        self.caracteraecrire=caraecri
        self.mouvement=mouv
        self.nextetat=etatsuivant

    def get_mouv(self)->str:
        return self.mouvement

    def get_caracterlu(self)->str:
        return self.caracterlu
    
    def get_caracteraecrire(self)->str:
        return self.caracteraecrire
    
    def get_nexetat(self)->str:
        return self.nextetat
    
    def set_caractlu(self,mot):
        self.caracterlu=mot

    def set_caracterecrire(self,mot):
        self.caracteraecrire=mot

    def set_nextetat(self,mot):
        self.nextetat=mot
    
    def aff_transi(self):
        print("caractere lu: "+self.caracterlu)
        print("caractere a écrire: "+self.caracteraecrire)
        print("mouvement: "+self.mouvement)
        print("état suivant "+self.nextetat)

class Etat:
    """Classe simulant un ETAT d'une mt et stockant toutes les transitions liées a cette état"""
    def __init__(self,nometat,tabtransi) -> None:
        self.name=nometat
        self.stocktransi=tabtransi

    def get_etat_name(self)->str:
        return self.name

    def verif_transi(self,T)->bool:
        for x in self.stocktransi:
            if T.get_caracterlu() == x.get_caracterlu() and T.get_caracteraecrire()==x.get_caracteraecrire() and T.get_mouv()==x.get_mouv() and T.get_nexetat==x.get_nexetat():
                return True
        return False
    
    def aff_etat(self):
        print("nom de l'etat: "+str(self.get_etat_name()))
        print()
        for x in self.stocktransi:
            x.aff_transi()
            print()
    
class MT:
    """Classe simulant la définition d'une machine de turing"""
    def __init__(self,name,alphabet,alphatravail,tabetat,etatinit,etatfinal,bande,positontete):
        self.nmt=name
        self.alpha=alphabet
        self.alphat=alphatravail
        self.init=etatinit
        self.final=etatfinal
        self.etatbande=bande
        self.etatactuel=etatinit
        self.positete=positontete
        self.tableauetat=tabetat

    def get_name_mt(self)->str:
        return self.nmt
    
    def get_etat_actuel(self)->str:
        return self.etatactuel
    
    def get_etat_init(self)->str:
        return self.init
    
    def get_etat_final(self)->str:
        return self.final

    def get_bande(self)->str:
        tmp=""
        for x in self.etatbande:
            tmp=tmp+x
        return(tmp)
    
    def get_position(self)->int:
        return(self.positete)
    
    def get_alpha(self)->str:
        return(self.alpha)
    
    def get_alphat(self)->str:
        return(self.alphat)
    
    def get_taillealpha(self)->int:
        buf=self.get_alpha()
        tmp=0
        for k in buf.split(","):
            if len(k)!=tmp and tmp!=0:
                return(-1)

            tmp=len(k)
        return(tmp)
            
        
    def set_init(self,init):
        self.init=init
    
    def set_final(self,final):
        self.final=final

    def set_bande(self,bande):
        self.etatbande=bande
    
    def set_position(self,posi):
        self.positete=posi
    
    def set_etatactuel(self,etat):
        self.etatactuel=etat
    
    def print_bande(self):
        print(self.get_bande())
        i=0
        buf=""
        taille=self.get_taillealpha()
        while i < self.get_position():
            buf=(" "*taille)+buf
            i=i+1
        print(buf+"^")

    def aff_mt(self):
        print("nom de la mt: "+self.get_name_mt())
        print("alphabet: "+str(self.alpha))
        print("alphabet de travail: "+str(self.alphat))
        print("etat initial: "+self.get_etat_init())
        print("etat final: "+self.get_etat_final())
        print("bande :"+self.get_bande())
        print("état actuel: "+self.etatactuel)
        print("position :"+str(self.get_position())+"\n")
        for x in self.tableauetat:
            x.aff_etat()

#fonction coupant le mot et l'initialisant
def motbande(MtM)->List:
        i=True
        tab=[" "," "]
        taille=MtM.get_taillealpha()
        buf=""
        if taille==-1:
            print("\n problème de taille entre différent de caractère compris dans l'alphabet \n")
            return(tab)
        
        while(i):
            tmp=input("mot a rentrer dans la bande:")
            for x in tmp:
                for k in MtM.alpha:
                        if k.count(",")<1:
                            if k==x:
                                i=False
                                break
                            else:
                                i=True
            if i==True:
                print("le mot entré n'est pas compris dans l'alphabet de la MT \n")
                tmp=""
            else:
                print("mot enregistré \n")
            for x in tmp:
                buf=buf+x
                if len(buf)==taille:
                    tab.insert(len(tab)-1,buf)
                    buf=""

        return(tab)

#fonction lisant une mt dans un fichier .txt
def lecture_init(numero)->MT:
    filin = open(sys.argv[numero],"r")
    transi=[]
    etattab=[]
    nextetat="NULL"
    etat=nextetat
    buf =filin.readlines()
    for x in buf:
        if x[0]!="\n":

            if x.count("name "):
                name=x[5:len(x)-1]
            elif x.count("alpha "):
                alphabet=x[6:len(x)-2]
            elif x.count(":\n"):
                etat=x[0:len(x)-2]
                if nextetat=="NULL":
                    nextetat=etat
            elif x.count(",")>3:
                j=0
                for k in x.split(","):
                    if k!="\n":
                        if j==0:
                            buflu=k
                            j=j+1
                        elif j==1:
                            bufecri=k
                            j=j+1
                        elif j==2:
                            bufmouv=k
                            j=j+1
                        elif j==3:
                            bufnext=k

                d=Transition(buflu,bufecri,bufmouv,bufnext)
                transi.append(d)
            if etat!=nextetat or x.count("end"):
                E=Etat(nextetat,transi)
                etattab.append(E)
                transi=[]
                nextetat=etat

    filin.close()
    alphat=alphabet
    alphat= alphat+" "
    MtM=MT(name,alphabet,alphat,etattab,"A","QA",[" ","n","u","l","l"," "],1)

    return(MtM)

#fonction de pas de calcul
def calcul(MT)->bool:
    for x in MT.tableauetat:
        if x.get_etat_name()==MT.etatactuel:
            for k in x.stocktransi:
                if k.get_caracterlu()==MT.etatbande[MT.get_position()]:
                    if k.get_mouv()==">":
                        MT.set_position(MT.get_position()+1)
                        if MT.positete==len(MT.etatbande):
                            tmp=MT.etatbande
                            tmp.append(" ")
                            MT.set_bande([])
                            MT.set_bande(tmp)
                        MT.etatbande[MT.get_position()-1]=k.get_caracteraecrire()

                    if k.get_mouv()=="<":
                        MT.set_position(MT.get_position()-1)
                        if MT.positete<0:
                            tmp=MT.etatbande
                            tmp.insert(0," ")
                            MT.set_bande([])
                            MT.set_bande(tmp)
                            MT.set_position(0)
                        MT.etatbande[MT.get_position()+1]=k.get_caracteraecrire()
                    if k.get_mouv()=="-":
                        MT.etatbande[MT.get_position()]=k.get_caracteraecrire()

                    MT.set_etatactuel(k.get_nexetat())
                    return(True)             
    return(False)

#fonction disant si lemot est accepté
def accept_or_reject(MT,mot):
    MT.set_bande(mot)
    i=bool
    MT.print_bande()
    while i:
        input()
        i=calcul(MT)
        MT.print_bande()
    if MT.get_etat_actuel()==MT.get_etat_final():
        print(" ACCEPT ")
    else:
        print(" REJECT")
    MT.set_position(1)
    MT.set_etatactuel(MT.get_etat_init())

#fonction regroupant toutes les fonctions de la partie 1
def partie_1(max):
    tabmt=[]
    i=1
    while i<max:
        m=lecture_init(i)
        tabmt.append(m)
        m=[]
        i=i+1
    while(1):
        print("voici les machines de turings enregistrées :")
        i=0
        for x in tabmt:
            print(str(i)+"."+x.get_name_mt())
            i=i+1

        tmp=input("Pour quitter les MT taper -1 \n \n tapez un chiffre pour sélectionner la MT voulu : \n")
        if len(tmp)==1 and (ord(tmp)<58 and ord(tmp)>47):
            tmp=int(tmp)
            if tmp>=0 and tmp<len(tabmt):
                print("mt sélectionnée :"+tabmt[tmp].get_name_mt()+"\n")
                accept_or_reject(tabmt[tmp],motbande(tabmt[tmp]))
            else:
                print("aucune MT ne correspond au chiffre rentré \n veuillez rentrer un chiffre valide \n")
        elif tmp=="-1":
            break
        else:
            print("aucune MT ne correspond au chiffre rentré \n veuillez rentrer un chiffre valide \n")
        tmp=""
        
#créé une mt de recopiage
def creatmtr(number,etat,tabalpha)->List:
    tmp=[]
    i=number
    tmp.append("QR"+str(i)+":\n")
    for x in tabalpha:
        tmp.append(str(x+","+x+","+">,QR"+str(i)+",\n"))
        
    i=i+1
    y=0+i
    tmp.append(str(" , ,<,QR"+str(i)+",\n \n"))
    tmp.append(str("QR"+str(i)+":\n"))
    for x in tabalpha:
        i=i+1
        tmp.append(str(x+", ,>,QR"+str(i)+",\n"))
    tmp.append(str("£,£,>,QR"+str((i+2))+",\n \n"))
    i=i+1

    for x in tabalpha:
        y=y+1
        tmp.append(str("QR"+str(y)+":\n"))
        tmp.append(str(" ,"+x+",<,QR"+str(i)+",\n \n"))
    
    tmp.append(str("QR"+str(i)+":\n"))
    tmp.append(str(" , ,<,QR"+str(number+1)+",\n \n"))
    i=i+1
    tmp.append(str("QR"+str(i)+":\n"))
    tmp.append(str(" , ,>,"+etat+",\n \n"))

    return(tmp)

#fonction regroupant les fonctions pour simuler une bande infini droite
def bande_infini_droite(number):
    filin = open(sys.argv[number],"r")
    buf =filin.readlines()
    buf2=[]
    tabalpha=[]
    name=""
    bufalph=""
    etatactuel=""
    etatplus=[]
    i=0
    for x in buf:
        if x.count("name "):
            name=x[5:len(x)-1]
        if x.count("alpha ")==1:
            bufalph=x[6:len(x)-2]
            for y in bufalph.split(","):
                if(y!="\n"):
                    tabalpha.append(y)
        if x.count(":\n"):
            etatactuel=x[0:len(x)-2]
            fait=True
        if x.count("<") and fait:
            buf2.append("£,£,>,QR"+str(i)+",\n")
            etatplus.append(creatmtr(i,etatactuel,tabalpha))
            fait=False
            i=i+4+(len(tabalpha))
        
        if x.count("end\n"):
            for z in etatplus:
                for k in z:
                    buf2.append(k)

        buf2.append(x)


    filin.close()

    name=name+"_question6.txt"
    file=open(name[len(name)-13:len(name)],"w+")
    file.write("name "+name[0:len(name)-13]+"infini_droite \n")
    file.write("alpha "+bufalph+",£,\n")
    for x in buf2[2:len(buf2)]:
        file.write(x)
    filin.close()

#fonction pour ecrire dans une mt
def ecriture_MT(MT,name) -> bool :

    f = open(name+".txt","w")

    f.write("name " + MT.nmt + "\n" + "alpha " + MT.alpha+",\n \n")

    for u in MT.tableauetat:
        
        f.write(u.get_etat_name() + ":\n")
           

        for v in u.stocktransi:

            f.write( v.get_caracterlu() + ","+v.get_caracteraecrire() + ","+v.get_mouv() + ","+v.get_nexetat() + ",\n")
        f.write("\n")

    f.write("\n\n")
    f.write("end")
    
    f.close()

#fonction répondant a la question 7 de manière très simple en changeant juste la valeur de a,b,c,d sans rajouter de transition
#ça fonction presque parfaitement, il n'y a que l'affichage qui pose problème
"""
def binary_translate(numero):
    
    new_MT = lecture_init(numero)
    
    new_MT.alpha = "00,01,10,11"

    new_MT.nmt = new_MT.nmt + "_binary"

    for i in new_MT.etatbande:
        i.lower()

        if i == "a":
            i = "00"
        elif i == "b":
            i = "01"
        elif i == "c":
            i = "10"
        elif i == "d":
            i = "11"

    for u in new_MT.tableauetat:
        for v in u.stocktransi:
            
            if v.caracterlu == "a":
                v.caracterlu = "00"
            
            elif v.caracterlu == "b":
                v.caracterlu = "01"
            
            elif v.caracterlu == "c":
                v.caracterlu = "10"
            
            elif v.caracterlu == "d":
                v.caracterlu = "11"   

            if v.caracteraecrire == "a":
                v.caracteraecrire = "00"
            
            elif v.caracteraecrire == "b":
                v.caracteraecrire = "01"
            
            elif v.caracteraecrire == "c":
                v.caracteraecrire = "10"
            
            elif v.caracteraecrire == "d":
                v.caracteraecrire = "11" 

    ecriture_MT(new_MT) 

"""
#fonction de simplification
def opti_double(MT):
    buf_tabetat=MT.tableauetat
    buf_stock=[]
    for x in MT.tableauetat:
        buf_stock=x.stocktransi
        for k in x.stocktransi:
            for y in buf_stock:
                if k.caracterlu == y.caracterlu and k.caracteraecrire==y.caracteraecrire and k.mouvement==y.mouvement and k.get_nexetat().count("BI") and k.get_nexetat()!=y.get_nexetat():
                    bufnextetat=y.get_nexetat()
                    for w in buf_tabetat:
                        if w.get_etat_name()==bufnextetat:
                            bufetatsuppr=w
                    for w in buf_tabetat:
                        if w.get_etat_name()==k.get_nexetat():
                            w.stocktransi.append(bufetatsuppr.stocktransi[0])
                    y.set_caractlu("/")
                    y.set_caracterecrire("/")
                    y.set_nextetat(" ")

#fonction transformant une mt a,b,c,d en 0,1
def binary_translate(numero):
      
    new_MT = lecture_init(numero)
    new_MT.alpha = "0,1"
    new_MT.nmt = new_MT.nmt + "_binary"
    binaryname="BI"
    transi=[]
    i=0
    for x in new_MT.tableauetat:
        for k in x.stocktransi:
            
            if (k.get_caracterlu()== "a" or k.get_caracterlu()=="b" or  k.get_caracterlu()=="c" or k.get_caracterlu()=="d"):
                buf=k.get_caracterlu()
                bufecri=k.get_caracteraecrire()
                bufnextetat=k.get_nexetat()
                bufmouv=k.get_mouv()
                if buf=="a":
                    k.set_caractlu("0")
                    if bufecri=="a":
                        k.set_caracterecrire("0")
                        d=Transition("0","0",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition("0",bufecri,bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="b":
                    k.set_caractlu("0")
                    if bufecri=="b":
                        k.set_caracterecrire("0")
                        d=Transition("1","1",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition("1",bufecri,bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="c":
                    k.set_caractlu("1")
                    if bufecri=="c":
                        k.set_caracterecrire("1")
                        d=Transition("0","0",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition("0",bufecri,bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="d":
                    k.set_caractlu("1")
                    if bufecri=="d":
                        k.set_caracterecrire("1")
                        d=Transition("1","1",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition("1",bufecri,bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
            elif k.get_caracterlu()== "a" or k.get_caracterlu()=="b" or  k.get_caracterlu()=="c" or k.get_caracterlu()=="d":
                buf=k.get_caracteraecrire()
                bufecri=k.get_caracterlu()
                bufnextetat=k.get_nexetat()
                bufmouv=k.get_mouv()
                if buf=="a":
                    k.set_caractlu("0")
                    if bufecri=="a":
                        k.set_caracterecrire("0")
                        d=Transition("0","0",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition(bufecri,"0",bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="b":
                    k.set_caractlu("0")
                    if bufecri=="b":
                        k.set_caracterecrire("0")
                        d=Transition("1","1",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition(bufecri,"1",bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="c":
                    k.set_caractlu("1")
                    if bufecri=="c":
                        k.set_caracterecrire("1")
                        d=Transition("0","0",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition(bufecri,"0",bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
                elif buf=="d":
                    k.set_caractlu("1")
                    if bufecri=="d":
                        k.set_caracterecrire("1")
                        d=Transition("1","1",bufmouv,bufnextetat)
                    else:
                        k.set_caracterecrire(bufecri)
                        d=Transition(bufecri,"1",bufmouv,bufnextetat)
                        
                    transi.append(d)
                    k.set_nextetat(binaryname+str(i))
                    E=Etat(binaryname+str(i),transi)
                    (new_MT.tableauetat).append(E)
                    transi=[]
                    i=i+1
            
    opti_double(new_MT)
    ecriture_MT(new_MT,"question7") 


#fonction pour aller plus vite, parcourir moins d'état
def quetion9(numero):
    new_MT=lecture_init(numero)

    for u in new_MT.tableauetat:
        for v in u.stocktransi:

            if v.get_mouv()=="-":

                for k in new_MT.tableauetat:
                    if k.get_etat_name()==v.get_nexetat():
                        a=k

                b=v.get_caracteraecrire()

                for w in a.stocktransi:
                    if w.get_caracterlu()==b:
                        v.caracteraecrire = w.get_caracteraecrire()
                        v.nextetat= w.get_nexetat()
                        v.mouvement=w.get_mouv()

    ecriture_MT(new_MT,"question9")



#fonction verifiant si la mt contien l'état concerné
def verif_si_etat(MT,etat)->bool:
    for x in MT.tableauetat:
        if x.get_etat_name()==etat:
            return(True)
    return(False)
#fonction fesant une mt n'utilisant que les etat utile pour le mot en entré
def calcul_opti(MT,copie)->bool:
    buf_transi=[]
    for x in MT.tableauetat:
        if x.get_etat_name()==MT.etatactuel:
            for k in x.stocktransi:
                if k.get_caracterlu()==MT.etatbande[MT.get_position()]:
                    if k.get_mouv()==">":
                        MT.set_position(MT.get_position()+1)
                        if MT.positete==len(MT.etatbande):
                            tmp=MT.etatbande
                            tmp.append(" ")
                            MT.set_bande([])
                            MT.set_bande(tmp)
                        MT.etatbande[MT.get_position()-1]=k.get_caracteraecrire()
                    
                    if k.get_mouv()=="<":
                        MT.set_position(MT.get_position()-1)
                        if MT.positete<0:
                            tmp=MT.etatbande
                            tmp.insert(0," ")
                            MT.set_bande([])
                            MT.set_bande(tmp)
                            MT.set_position(0)
                        MT.etatbande[MT.get_position()+1]=k.get_caracteraecrire()
                    if k.get_mouv()=="-":
                        MT.etatbande[MT.get_position()]=k.get_caracteraecrire()
                    if verif_si_etat(copie,MT.get_etat_actuel):
                        for x in copie.tableauetat:
                            if x==MT.get_etat_actuel():
                                if x.verif_transi(k)==False:
                                    (x.stocktransi).append(k)
                    else:
                        buf_transi.append(k)
                        (copie.tableauetat).append(Etat(MT.get_etat_actuel(),buf_transi))
                    MT.set_etatactuel(k.get_nexetat())
                    buf_transi=[]
                    return(True)             
    return(False)

#pareil que l'accept_or_reject de base mais épuré
def accept_or_reject_opti(MTM,mot)->MT:
    MTM.set_bande(mot)
    copie=MT("copie_opti_"+MTM.get_name_mt(),MTM.get_alpha(),MTM.get_alphat(),[],MTM.get_etat_init(),MTM.get_etat_final(),"",1)
    i=bool
    while i:
        i=calcul_opti(MTM,copie)

    MTM.set_position(1)
    MTM.set_etatactuel(MTM.get_etat_init())
    return(copie)

#fonction rassemblant toutes les fonctions pour avoir une mt optimisé pour un mot 
def opti_question10(max):
    tabmt=[]
    i=1
    while i<max:
        m=lecture_init(i)
        tabmt.append(m)
        m=[]
        i=i+1
    while(1):
        print("voici les machines de turings enregistrées que vous pouvez optimiser :")
        i=0
        for x in tabmt:
            print(str(i)+"."+x.get_name_mt())
            i=i+1

        tmp=input("Pour quitter les MT taper -1 \n \n tapez un chiffre pour sélectionner la MT voulu : \n")
        if len(tmp)==1 and (ord(tmp)<58 and ord(tmp)>47):
            tmp=int(tmp)
            if tmp>=0 and tmp<len(tabmt):
                print("mt sélectionnée :"+tabmt[tmp].get_name_mt()+"\n")
                copie=accept_or_reject_opti(tabmt[tmp],motbande(tabmt[tmp]))
                ecriture_MT(copie,"question10")
            else:
                print("aucune MT ne correspond au chiffre rentré \n veuillez rentrer un chiffre valide \n")
        elif tmp=="-1":
            break
        else:
            print("aucune MT ne correspond au chiffre rentré \n veuillez rentrer un chiffre valide \n")
        tmp=""


def main():
    bande_infini_droite(4)
    binary_translate(5)
    partie_1(8)
    opti_question10(8)
    quetion9(8)


main()



