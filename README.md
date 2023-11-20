# Epic Events CRM CLI

## Description
Cette interface en ligne de commande (CLI) est conçue pour interagir avec l'API Epic Events CRM. Elle permet de gérer des clients, des contrats, des événements, et des utilisateurs.

## Installation
- Assurez-vous d'avoir Python installé sur votre système.
- Clonez le dépôt contenant les scripts CLI.
- Installez les dépendances nécessaires via pip install -r requirements.txt (si applicable).

## Utilisation

#### Lancement
- Pour démarrer l'application, exécutez :
python cli_interface/cli_menu.py

### Fonctionnalités

#### Générales
- Gestion des signaux : L'application gère les signaux SIGINT et SIGTERM pour une sortie gracieuse.

#### Authentification
- Connexion : Les utilisateurs doivent se connecter pour accéder aux fonctionnalités.
- Déconnexion : Les utilisateurs peuvent se déconnecter.

#### Gestion des Clients
- Lister : Affiche tous les clients.
- Ajouter : Crée un nouveau client.
- Mettre à jour : Modifie les informations d'un client existant.
- Supprimer : Supprime un client.

#### Gestion des Contrats
- Lister : Affiche tous les contrats.
- Ajouter : Crée un nouveau contrat.
- Mettre à jour : Modifie un contrat existant.
- Supprimer : Supprime un contrat.

#### Gestion des Événements
- Lister : Affiche tous les événements.
- Ajouter : Crée un nouvel événement.
- Mettre à jour : Modifie un événement existant.
- Supprimer : Supprime un événement.

#### Gestion des Utilisateurs (Réservée aux utilisateurs du groupe 'Management')
- Lister : Affiche tous les utilisateurs.
- Ajouter : Crée un nouvel utilisateur.
- Mettre à jour : Modifie un utilisateur existant.
- Supprimer : Supprime un utilisateur.

### Menus
- Menu Principal : Permet d'accéder aux différentes fonctionnalités en fonction du rôle de l'utilisateur.
- Menus spécifiques : Pour les clients, contrats, événements et utilisateurs.

### Fonctionnalités Avancées

#### Filtrage des Listes
L'application permet un filtrage détaillé des listes de clients, contrats, événements et utilisateurs.

##### Clients
- `full_name` : Filtrer par nom complet.
- `email` : Filtrer par adresse email.
- `phone` : Filtrer par numéro de téléphone.
- `company_name` : Filtrer par nom d'entreprise.
- `sales_contact` : Filtrer par contact commercial.
- `date_created` : Filtrer par date de création.
- `last_update` : Filtrer par date de dernière mise à jour.

##### Contrats
- `client` : Filtrer par client.
- `sales_contact` : Filtrer par contact commercial.
- `total_amount` : Filtrer par montant total du contrat.
- `amount_due` : Filtrer par montant dû.
- `creation_date` : Filtrer par date de création.
- `status` : Filtrer par statut du contrat.
- `sales_contact_is_null` : Filtrer les contrats sans contact commercial.
- `unpaid` : Filtrer les contrats non payés.

##### Événements
- `contract` : Filtrer par contrat associé.
- `support_contact` : Filtrer par contact de support.
- `event_start_date` : Filtrer par date de début de l'événement.
- `event_end_date` : Filtrer par date de fin de l'événement.
- `location` : Filtrer par lieu.
- `attendees` : Filtrer par nombre de participants.
- `notes` : Filtrer par notes.
- `support_contact_is_null` : Filtrer les événements sans contact de support.
- `my_events` : Filtrer les événements attribués à l'utilisateur connecté.

##### Utilisateurs
- `id` : Filtrer par identifiant.
- `username` : Filtrer par nom d'utilisateur.
- `email` : Filtrer par email.
- `first_name` : Filtrer par prénom.
- `last_name` : Filtrer par nom de famille.
- `groups` : Filtrer par groupe d'appartenance.