# GROUPE 3 : channel-service - Gestion des canaux IRC
## Objectif du service
Le but de notre (micro)-service est la gestion des canaux IRC, c'est-à-dire des différents salons de communication. Les channels auront une configuration donnant accès aux paramètres suivants :
- Sujet
- Invitation
- Rôles (owners, moderators, invited, banned)
- Private : true, false

Les objectifs à faire sont : 
|Tâche|Description|Fini ?|Tester|
|-|-|-|-|
|GET /channel | Liste des serveurs publics|Oui|Non|
|POST /channel | Créer un nouveau canal|Non|Non|
|GET /channel/<nom>/users| Affiche les utilisateurs du canal |Oui|Non|
|PATCH /channel/<nom>| Modification du sujet / mode du canal|Non|Non|
|POST /channel/<nom>/topic|Modifier uniquement le sujet|Non|Non|
|POST /channel/<nom>/mode|Modifier uniquement le mode (privé, public, lecture seule)|Non|Non|
|GET /channel/<nom>/config|Récupère toute la config du canal|Oui|Non|
|POST /channel/<nom>/invite|Inviter une personne|Non|Non|
|POST /channel/<nom>/ban|Bannir une personne|Non|Non|
|DELETE /channel/<nom>|Supprimer un canal|Non|Non|

## Instruction de lancement

1. Télécharger le dépôt git.
2. Ouvrir la cmd
3. Ouvrir le fichier téléchargé depuis la cmd (via des commandes comme ls ou cd)
4. Tapez la commande '''sudo docker-compose up --build -d'''

Voici les étapes qui se produisent lorsque l'on exécute le docker-compose :
```bash
    Step 1/5 : FROM python:3.11-slim
    ---> 0b14a859cdba
    Step 2/5 : WORKDIR /app
    ---> Using cache
    ---> 050cbcb65de7
    Step 3/5 : COPY . .
    ---> 5885d63fcf68
    Step 4/5 : RUN pip install --no-cache-dir -r requirements.txt
    ---> Running in 2abca38467bd
    Step 5/5 : CMD ["python", "app.py"]
    ---> Running in 327bc359291e
    ---> Removed intermediate container 327bc359291e
    ---> 99814d77ff2a
    Successfully built 99814d77ff2a
    Successfully tagged canaduck-groupe3_channel-service:latest
    Creating canaduck-groupe3_mysql_1 ... done
    Creating canaduck-groupe3_channel-service_1 ... done 
```

## Exemples d'appel

Un utilisateur arrive et veut parler de son sujet préféré : du magret de canard.
Il cherche un channel et va donc chercher "IP/channel" pour chercher un channel et décide d'utiliser la commande pour rejoindre le channel "CanardEnjoyer".
Parlant de son sujet préféré, l'un des modérateurs utilise la commande "IP/channel/nom/ban" pour bannir notre utilisateur fan de magrets de canard.
Ce dernier crée un channel via un curl "/channel" avec des données, pour créer son channel.
 Il décide d'inviter des personnes en curl via le "/channel/nom/invite"
