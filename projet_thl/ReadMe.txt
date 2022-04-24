pour lancer le projet on tape "make" dans le terminal

pour écrire une mt dans un fichier texte on l'écrit de la manière suivante:
on ecrit d'abort le nom de la mt puis l'alphabet de travail(le caractère blanc est " " et est déja compris dans l'alphabet du programme) dans un troisième temps les états avec deux points 
puis les transition qui vont avec les états.
les transitions sont décrites de la manière suivante
le caractère lu, le caractère a écrire,trois mouvement possible >(right),<(left),-(stay),l'état suivant,
l'état initial sera toujours A et l'état final sera toujours QA

exemple:

name Mt_remplace_a_par_b
alpha a,b  

a:
a,b,>,a,
 , ,S,QA,
 
QA:
/, , , ,

end
