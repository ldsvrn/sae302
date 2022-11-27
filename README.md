# SAE-3.02
## Contexte

A l’image du protocole SNMP, nous souhaitons réaliser un système client-serveur
permettant d’envoyer des commandes systèmes permettant de superviser et de
diagnostiquer des machines ou serveurs à distance.

## Fonctionnalités

Nous souhaitons une interface graphique permettant de réaliser l’ensemble des
fonctionnalités suivantes. Sur la base d’un système client-serveur, vous devrez
pouvoir interroger des serveurs sur leur état et leur fonctionnement et même
détecter lorsqu’ils sont déconnectés du réseau. 

Nous souhaitons avoir une liste d’IP ou de noms de machines, sous la forme de
fichier, interroger ces mêmes machines sur leur état. L’interface graphique
permettra d’effectuer les commandes suivantes :

-  Lire un fichier de machines (csv par exemple, avec un port par défaut par exemple)
-  Pouvoir ajouter des machines et enregistrer ces nouvelles machines dans le fichier

- Envoyer des commandes simples à une ou plusieurs machines :
 
    - OS : demande l'OS et le type d'OS par exemple MacOS Darwin ou Linux Ubuntu 21.4
    - RAM : mémoire totale, mémoire utilisée et mémoire libre restante
    - CPU : utilisation de la CPU
    - IP : adresse IP
    - Name : nom de la machine
    - Envoyer des commandes aux serveurs de machines :
        - Disconnect : déconnexion de l’interface permettant de libérer la machine
        monitorée pour permettre de libérer le serveur pour d’autres requêtes
        - Connexion information : IP, nom de la machine
        - Kill : tue le serveur
        - Reset : reset du serveur
  
- De plus, l’interface permettra d’envoyer des commandes données par
  l’utilisateur, par exemple :
 
    - DOS:dir
    - DOS:mkdir toto
    - Linux:ls -la
    - Powershell:get-process
    - python --version
    - ping 192.157.65.78

Pour chacune des commandes lorsque le type de système est spécifié par exemple «
DOS: », « Linux: », « Powershell: », l’OS sera vérifié pour compatibilité et la
commande exécutée et renvoyer au système de monitoring. Lorsque d’aucun système
n’est spécifié (commandes 5 et 6), la commande est lancée quel que soit le
système.

Quelle que soit la commande utilisée, l’interface devra afficher le résultat de
la commande et garder en historique les commandes exécutées sur l’ensemble des
machines. Les machines où sont lancées les commandes pourront être choisies par
une simple sélection entre 1 et l’ensemble des machines. Il serait également
intéressant de savoir si une machine est connectée (et ne pas lancer de
commandes si la machine n’est pas en ligne) et en fonction l’OS de la machine.

Nous n’avons pas spécifiquement de prérequis sur l’interface mais elle se doit
d’être ergonomique et facile d’utilisation tant pour un administrateur système
que pour un débutant averti sur l’administration système.

## Points d’attention

Vous devrez bien sûr gérer l’ensemble des erreurs possibles et éviter tous les
crashs de votre application.

Deux documentations de qualité en anglais (markdown ou en pdf) devront être
rédigés pour l’utilisateur de l’interface et sur un document du développement
effectué afin de pouvoir ajouter de nouvelles fonctionnalités (ou commandes) si
nécessaire.
## Options supplémentaires (à réfléchir en fonction du temps)

- Un graphique sur l’utilisation de la CPU ou la mémoire.

- Nous nous posons également la question sur une connexion sécurisée et chiffrée
entre le client et le serveur, il serait intéressant de voir si sur le réseau
les commandes peuvent apparaître à l’aide d’un outil tel que Wireshark. Si les
commandes ne sont pas sécurisées, il serait donc intéressant de les sécuriser.

- Il serait possible d’ajouter plusieurs clients.
