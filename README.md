# UE-AD-A1-REST

## Ce qui a été fait :

TP vert :
- Ajout d'un point d'entrée au service Movie (get_movie_by_director) et mise à jour de la doc OpenAPI
- Ecriture du service Times à partir de la doc OpenAPI
- Ecriture du service Booking à partir de la doc OpenAPI
- Ecriture des specs OpenAPI pour le service User et développement du service 
- Appel des services Booking et Movie dans l'endpoint get_user_movie_by_id

TP rouge : 
- Supression de la base de donnée intiale du service Movie
- Connexion à l'API TMDB pour récupération des données de films


## Utilisation

### Prérequis

Une installation docker fonctionnelle (docker et docker-compose)

### Comment lancer

Télécharger l'archive du projet et lancer la commande suivante dans le terminal : 
```bash
$ docker-compose up --build
```