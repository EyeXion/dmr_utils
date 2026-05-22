# dmr_utils


Comment ça marche pour le tranceiver

Donc il y a deux parties au flowgraph :

- Une partie Rx
- Une partie Tx

## Rx

C'est basé sur un démodulateur NBFM dans gnuradio fait à la main sinon ça marche pô.
Donc ça envoie le flux démodulé dans un socket Unix à 48kHz

dsd-fme prend le relai ensuite pour le symbol sync, calcul de FEC, dissection blabla, et le logging (port 52052)

Donc il faut utiliser la version dsd-fme du repo !!! c'est un fork, j'ai un peu modifié pour avoir la connexion au flowgraph !!

Bien mettre l'option "-Q ../../../tmp/a"  pour que ça marche
"-Z" pour le logging des trames AMBES

Ensuite, dsd-fme log les trames en format "joli" (trames par burst, + CACH), et il faut donc écouter sur le port 52020 `nc -lu 52020`

On peut mettre la sortie dans un fichier pour le réinjecter plus tard, modifier, ...


## Tx

Donc en Tx, là c'est les truc bizarres.
Donc du coup la plupart du temps on envoie rien, on envoie du coup une porteuse quand même, toujours pas réussi à faire en sorte de pouvoir avoir rien puis que ça envoie à cause des délais des filtres qui se vident pas assez vite -> délai dans l'envoie

mais pour l'instant good enough, ça change pas grand d'envoyer la porteuse au final.

Bref, du coup en entrée, on a un block grc custom qui permet 

- de fecth dans un socket (52010 par défault) les trames en bytes à envoyer avec le délai de silence voulu aussi
- de parser ce qu'on reçoit, pour avoir le nombre de symbole de silence et les trames à envoyer
- envoie ça dans le flowgraph, avec un tag de "tx_sob" pour le début du burst et tx_eob pour la fin
- on a toute la chaine de traitement
- puis on a un block custom de gate qui regarde les tags pour voir quand est-ce qu'on envoie la porteuse juste, ou alors quand estce qu'on envoie des symboles

ça marche plutot bien !
Le format c'est la sortie du Rx, donc c'est directement reliable

pour plus de custom, on peut spécifier le silence entre deux bursts en nombre de symboles :

1 03 0F2D124A06E0127C4A80E08044CD5D7F77FD757AC9DC2EB851A886E18CC24FA59F

SILENCE:280

Pour avoir après la trame 280 symboles de silence. ça pourra servir maybe

Aussi, y'a le script dans le repo qui permet d'envoyer depuis un fichier ds trames dans le flowgraph : 
python ./send_socket_args.py -f test3.txt -p 52010 -r 3 -d 1

le -r -> pour le nombre de fois où on envoie tout le fichier
-d -> delais entre chaque repet
