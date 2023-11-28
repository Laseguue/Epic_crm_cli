import cli_logic
import getpass
import signal
import sys

def signal_handler(sig, frame):
    graceful_exit()

def graceful_exit():
    print('Fermeture du programme.')
    if cli_logic.get_token():
        cli_logic.logout()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def prompt_fields(fields):
    return {field.replace(" ", "_").lower(): input(f"{field} : ") for field in fields}

def add_client_prompt():
    fields = ["Nom complet", "Email", "Téléphone", "Nom de l'entreprise"]
    cli_logic.add_client(**prompt_fields(fields))

def update_client_prompt():
    fields = ["ID du client à mettre à jour", "Nouveau nom complet", "Nouvel email", "Nouveau téléphone", "Nouveau nom de l'entreprise"]
    cli_logic.update_client(**prompt_fields(fields))

def delete_client_prompt():
    client_id = input("ID du client à supprimer : ")
    cli_logic.delete_client(client_id)

def add_contract_prompt():
    user_role = cli_logic.get_user_role()
    fields = ["ID du client pour le contrat", "Montant total du contrat", "Montant dû", "Statut du contrat"]
    contract_info = prompt_fields(fields)

    if 'Management' in user_role:
        contract_info["sales_contact"] = input("ID de l'utilisateur Sales Contact : ")

    cli_logic.add_contract(**contract_info)

def update_contract_prompt():
    user_role = cli_logic.get_user_role()
    fields = ["ID du contrat à mettre à jour", "ID du client pour le contrat", "Montant total du contrat", "Montant dû", "Statut du contrat"]
    contract_info = prompt_fields(fields)

    if 'Management' in user_role:
        contract_info["sales_contact"] = input("ID de l'utilisateur Sales Contact : ")

    cli_logic.update_contract(**contract_info)

def delete_contract_prompt():
    contract_id = input("ID du contrat à supprimer : ")
    cli_logic.delete_contract(contract_id)

def add_event_prompt():
    fields = ["ID du contrat pour l'événement", "Date de début de l'événement", "Date de fin de l'événement", "Lieu de l'événement", "Nombre de participants", "Notes sur l'événement"]
    event_info = prompt_fields(fields)
    cli_logic.add_event(**event_info)

def update_event_prompt():
    user_role = cli_logic.get_user_role()
    fields = ["ID de l'événement à mettre à jour", "Nouvelle date de début de l'événement", "Nouvelle date de fin de l'événement", "Nouveau lieu de l'événement", "Nouveau nombre de participants", "Nouvelles notes sur l'événement"]
    event_info = prompt_fields(fields)

    if 'Management' in user_role:
        event_info["support_contact"] = input("ID de l'utilisateur support à assigner à l'événement : ")

    cli_logic.update_event(**event_info)

def delete_event_prompt():
    event_id = input("ID de l'événement à supprimer : ")
    cli_logic.delete_event(event_id)

def add_user_prompt():
    fields = ["Nom d'utilisateur", "Mot de passe", "Email", "Prénom", "Nom de famille", "Groupe"]
    user_info = prompt_fields(fields)
    user_info['mot_de_passe'] = getpass.getpass("Mot de passe : ")
    cli_logic.add_user(**user_info)

def update_user_prompt():
    fields = ["ID de l'utilisateur à mettre à jour", "Nom d'utilisateur", "Email", "Prénom", "Nom de famille", "Groupe"]
    user_info = prompt_fields(fields)
    cli_logic.update_user(**user_info)

def delete_user_prompt():
    user_id = input("ID de l'utilisateur à supprimer : ")
    cli_logic.delete_user(user_id)

def login():
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")
    if cli_logic.login(username, password):
        return cli_logic.get_user_role()

def logout():
    cli_logic.logout()
    return []

def main_menu():
    user_role = []

    menu_options = {
        "1": (login, []),
        "2": (manage_clients_menu, ['Sales']),
        "3": (manage_contracts_menu, ['Management', 'Sales']),
        "4": (manage_events_menu, ['Management', 'Support', 'Sales']),
        "5": (manage_users_menu, ['Management']),
        "6": (logout, [])
    }

    while True:
        print_menu_options(user_role)
        choice = input("Entrez le numéro de votre choix : ")

        if choice in menu_options and (not menu_options[choice][1] or any(role in user_role for role in menu_options[choice][1])):
            user_role = menu_options[choice][0]()
        elif choice == "0":
            graceful_exit()
        else:
            print("Choix invalide, veuillez réessayer.")

def print_menu_options(user_role):
    print("\nMenu Principal de l'API Epic Events CRM")
    if not cli_logic.get_token():
        print("1 - Se connecter\n0 - Quitter")
    else:
        print("2 - Gérer les clients\n3 - Gérer les contrats\n4 - Gérer les événements")
        if 'Management' in user_role:
            print("5 - Gérer les utilisateurs")
        print("6 - Se déconnecter\n0 - Quitter")

def manage_clients_menu():
    user_role = cli_logic.get_user_role()
    while True:
        print("\nGestion des Clients")
        print("1 - Lister les clients")
        if 'Sales' in user_role:
            print("2 - Ajouter un client")
            print("3 - Mettre à jour un client")
            print("4 - Supprimer un client")
        print("0 - Retour")

        choice = input("Entrez le numéro de votre choix : ")
        if choice == "1":
            cli_logic.list_clients()
        elif choice == "2" and 'Sales' in user_role:
            add_client_prompt()
        elif choice == "3" and 'Sales' in user_role:
            update_client_prompt()
        elif choice == "4" and 'Sales' in user_role:
            delete_client_prompt()
        elif choice == "0":
            break

def manage_contracts_menu():
    user_role = cli_logic.get_user_role()
    while True:
        print("\nGestion des Contrats")
        print("1 - Lister les contrats")
        if 'Management' in user_role:
            print("2 - Ajouter un contrat")
            print("4 - Supprimer un contrat")
        if 'Management' in user_role or 'Sales' in user_role:
            print("3 - Mettre à jour un contrat")
        print("0 - Retour")

        choice = input("Entrez le numéro de votre choix : ")
        if choice == "1":
            cli_logic.list_contracts()
        elif choice == "2" and 'Management' in user_role:
            add_contract_prompt()
        elif choice == "3" and ('Management' in user_role or 'Sales' in user_role):
            update_contract_prompt()
        elif choice == "4" and 'Management' in user_role:
            delete_contract_prompt()
        elif choice == "0":
            break

def manage_events_menu():
    user_role = cli_logic.get_user_role()
    while True:
        print("\nGestion des Événements")
        print("1 - Lister les événements")
        if 'Sales' in user_role or 'Management' in user_role:
            print("2 - Ajouter un événement")
        if 'Management' in user_role or 'Support' in user_role:
            print("3 - Mettre à jour un événement")
        if 'Management' in user_role:
            print("4 - Supprimer un événement")
        print("0 - Retour")

        choice = input("Entrez le numéro de votre choix : ")
        if choice == "1":
            cli_logic.list_events()
        elif choice == "2" and ('Sales' in user_role or 'Management' in user_role):
            add_event_prompt()
        elif choice == "3" and ('Management' in user_role or 'Support' in user_role):
            update_event_prompt()
        elif choice == "4" and 'Management' in user_role:
            delete_event_prompt()
        elif choice == "0":
            break

def manage_users_menu():
    user_role = cli_logic.get_user_role()
    while True:
        print("\nGestion des Utilisateurs")
        if 'Management' in user_role:
            print("1 - Ajouter un utilisateur")
            print("2 - Modifier un utilisateur")
            print("3 - Supprimer un utilisateur")
            print("4 - Lister les utilisateurs")
        print("0 - Retour")

        choice = input("Entrez le numéro de votre choix : ")
        if choice == "1" and 'Management' in user_role:
            add_user_prompt()
        elif choice == "2" and 'Management' in user_role:
            update_user_prompt()
        elif choice == "3" and 'Management' in user_role:
            delete_user_prompt()
        elif choice == "4" and 'Management' in user_role:
            cli_logic.list_users()
        elif choice == "0":
            break

if __name__ == "__main__":
    try:
        main_menu()
    except Exception as e:
        print(f"Une erreur inattendue est survenue: {e}")
        graceful_exit()
