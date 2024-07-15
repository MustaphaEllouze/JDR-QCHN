from dataclasses import dataclass
import random

@dataclass
class Son:
    first : str
    second : str
    third : str

    def __str__(self) : return f'{self.first} | {self.second} | {self.third} | '

C = 'boum'
L = 'baa'

tous_sons = [
    Son(C, C, C),
    Son(C, C, L),
    Son(C, L, C),
    Son(C, L, L),
    Son(L, C, C),
    Son(L, C, L),
    Son(L, L, C),
]

# random.shuffle(tous_sons)

step = 0
success = 0
required_success = 7
nb_sounds = len(tous_sons)

while success < required_success :
    mod_step = step%nb_sounds
    if mod_step + success > nb_sounds:
        first_propal = tous_sons[mod_step:]+tous_sons[:(mod_step+success+1)%nb_sounds]
    else:
        first_propal = tous_sons[mod_step:mod_step+success+1]
    if mod_step+1-success < 0:
        second_propal = tous_sons[0:mod_step+2][::-1] + tous_sons[-(mod_step+1-success):][::-1]
    else:
        second_propal = tous_sons[(mod_step+1-success):mod_step+2][::-1]
    
    liste_shuffle = [(1, first_propal), (2, second_propal)]
    random.shuffle(liste_shuffle)
    (answer1, shuff1), (answer2, shuff2) = liste_shuffle

    print('First proposition')
    print("".join([str(e) for e in shuff1]))
    print('')
    
    print('Second proposition')
    print("".join([str(e) for e in shuff2]))

    reponse = int(input('1 or 2 ?'))

    if reponse == 1 and answer1 == 1:
        print('SUCCESS !')
        success += 1
    elif reponse == 2 and answer2 == 1:
        print('SUCCESS !')
        success += 1
    else:
        print('FAILURE !')
        success = 0

    step += 1

print('THE END ! CONGRATS')