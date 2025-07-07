# GROUPE 3 : channel-service - Gestion des canaux IRC
## Objectif du service
Le but de notre (micro)-service est la gestion des canaux IRC, c'est à dire des différents salons de communication. Les channels auront une configuration donnant acces au parametres suivants :
- Sujet
- Invitation
- Rôles (owners, moderators, invited, banned)
- Private : true, false

Les objectifs à faire sont : 
|Tâche|Description|Fini ?|Test|
|-|-|-|-|
|GET /channel | Liste des serveurs public|Non|Non|
|POST /channel | Créer un nouveau canal|Non|Non|
|GET /channel/<nom>/users| Affiche les utilisateurs du canal |Non|Non|
|PATCH /channel/<nom>| Modification du sujet / mode du canal|Non|Non|
|POST /channel/<nom>/topic|Modifier uniquement le sujet|Non|Non|
|POST /channel/<nom>/mode|Modifier uniquement le mode (privé, public, lecture seul)|Non|Non|
|GET /channel/<nom>/config|Recupere toute la config du canal|Non|Non|
|POST /channel/<nom>/invite|Inviter une personne|Non|Non|
|POST /channel/<nom>/ban|Bannir une personne|Non|Non|
|DELETE /channel/<nom>|Supprimer un canal|Non|Non|

## Instruction de lancement

1- Telecharger le depôt git.
2- Ouvrir la cmd
3- Ouvrir le fichier telécharger depuis la cmd (via des commandes comme ls ou cd)
4- Tappé la commande '''docker-compose up -d'''
## Exemples d'appel

Un utilisateur arrive et veut parler de son sujet prefere : Du magres de canard.
Il cherche un channel et va donc chercher "IP/channel" pour chercher un channel et decide d'utiliser la commande pour rejoindre le channel "CanardEnjoyer". Parlant de son sujet prefere, l'un des modérateur utilisa la commande "IP/channel/<nom>/ban" pour banir notre utilisateur fan de canard.