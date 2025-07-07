# Tests de `channel-service`

## Créer un canal

Scénario 1 : 
- appel de la route `POST /channel` avec le canal `testPost`
```json
{
    "name": "testCreation",
    "private": false
}
```
- appel de la route `GET /channel`
Résultat attendu : le canal est visible dans la liste des canaux

Scénario 2 : 
- appel de la route avec le canal invisible `testCreation2`
```json
{
    "name": "testPost2",
    "private": true
}
```
- appel de la route `GET /channel`
Résultat attendu : le canal n'est pas visible dans la liste des canaux

Scénario 3 : 
- appel de la route avec un nom de canal vide
```json
{
    "name": "",
    "private": false
}
```
Résultat attendu : erreur dans la réponse JSON


## Changer le sujet d'un canal

Scénario 1 :
- création d'un canal `testTopic` avec `POST /channel`
```json
{
    "name": "testTopic",
    "private": false
}
```
- ajout d'un sujet avec `POST /channel/testTopic/topic`
```json
{
    "topic": "projet"
}
```
- récupérer la configuration avec `GET /channel/testTopic/config` (sauf si le sujet est visible dans `GET /channel`)
Résultat attendu : le sujet du canal est `projet`


## Changer le mode d'un canal

Scénario 1 :
- création d'un canal `testMode` avec `POST /channel`
```json
{
    "name": "testMode",
    "private": false
}
```
- vérification que le canal est visible dans `GET /channel`
- appel de la route pour mettre le canal en privé
- appel de `GET /channel`
Résultat attendu : le canal `testMode` n'est plus visible dans la liste des canaux publics

Scénario 2 :
- création d'un canal `testMode2` avec `POST /channel`
```json
{
    "name": "testMode2",
    "private": false
}
```
- appel de la route pour mettre le canal en privé
- appel de la route pour le mettre à nouveau en privé
Résultat attendu : message ou erreur JSON

Scénario 3 : appel de la route avec un canal qui n'existe pas
```json
{
    "name": "unknownChannel",
    "private": false
}
```
Résultat attendu : erreur dans la réponse JSON

Scénario 4 :
- création d'un canal `testMode3`
```json
{
    "name": "testMode3",
    "private": false
}
```
- appel de la route avec un mode qui n'existe pas
Résultat attendu : erreur dans la réponse JSON

