import cli_logic, cli_prompt
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

def main_menu():
    user_role = []

    while True:
        print("\nMenu Principal de l'API Epic Events CRM")
        if not cli_logic.get_token():
            print("1 - Se connecter")
            print("0 - Quitter")
            choice = input("Entrez le numéro de votre choix : ")

            if choice == "1":
                username = input("Nom d'utilisateur : ")
                password = getpass.getpass("Mot de passe : ")
                if cli_logic.login(username, password):
                    user_role = cli_logic.get_user_role()
            elif choice == "0":
                print("Au revoir !")
                break
        else:
            print("2 - Gérer les clients")
            print("3 - Gérer les contrats")
            print("4 - Gérer les événements")

            if 'Management' in user_role:
                print("5 - Gérer les utilisateurs")

            print("6 - Se déconnecter")
            print("0 - Quitter")

            choice = input("Entrez le numéro de votre choix : ")
            valid_choices = ["2", "3", "4", "6", "0"]
            if 'Management' in user_role:
                valid_choices.append("5")

            if choice not in valid_choices:
                print("Choix invalide, veuillez réessayer.")
                continue

            if choice == "2":
                manage_clients_menu(user_role)
            elif choice == "3":
                manage_contracts_menu(user_role)
            elif choice == "4":
                manage_events_menu(user_role)
            elif choice == "5" and 'Management' in user_role:
                manage_users_menu(user_role)
            elif choice == "6":
                cli_logic.logout()
                user_role = None
            elif choice == "0":
                if cli_logic.get_token():
                    cli_logic.logout()
                print("Au revoir !")
                break

        input("Appuyez sur Entrée pour continuer...")

def manage_clients_menu(user_role):
    while True:
        print("\nGestion des Clients")
        print("1 - Lister les clients")
        if 'Sales' in user_role:
            print("2 - Ajouter un client")
            print("3 - Mettre à jour un client")
            print("4 - Supprimer un client")
        print("0 - Retour")

        choice = input("Entrez le numéro de votre choix : ")
        valid_choices = ["1", "0"]
        if 'Sales' in user_role:
            valid_choices.extend(["2", "3", "4"])

        if choice not in valid_choices:
            print("Choix invalide, veuillez réessayer.")
            continue

        if choice == "1":
            cli_logic.list_clients()
        elif choice == "2" and 'Sales' in user_role:
            cli_prompt.add_client_prompt()
        elif choice == "3" and 'Sales' in user_role:
            cli_prompt.update_client_prompt()
        elif choice == "4" and 'Sales' in user_role:
            cli_prompt.delete_client_prompt()
        elif choice == "0":
            break

def manage_contracts_menu(user_role):
    while True:
        print("\nGestion des Contrats")
        print("1 - Lister les contrats")
        valid_choices = ["1", "0"]
        
        if 'Management' in user_role:
            print("2 - Ajouter un contrat")
            valid_choices.append("2")
        if 'Management' in user_role or 'Sales' in user_role:
            print("3 - Mettre à jour un contrat")
            valid_choices.append("3")
        if 'Management' in user_role:
            print("4 - Supprimer un contrat")
            valid_choices.append("4")

        print("0 - Retour")
        choice = input("Entrez le numéro de votre choix : ")

        if choice not in valid_choices:
            print("Choix invalide, veuillez réessayer.")
            continue

        if choice == "1":
            cli_logic.list_contracts()
        elif choice == "2" and 'Management' in user_role:
            cli_prompt.add_contract_prompt()
        elif choice == "3" and ('Sales' in user_role or 'Management' in user_role):
            cli_prompt.update_contract_prompt()
        elif choice == "4" and 'Management' in user_role:
            cli_prompt.delete_contract_prompt()
        elif choice == "0":
            break

def manage_events_menu(user_role):
    while True:
        print("\nGestion des Événements")
        print("1 - Lister les événements")
        valid_choices = ["1", "0"]

        if 'Sales' in user_role:
            print("2 - Ajouter un événement")
            valid_choices.append("2")
        if 'Management' in user_role or 'Support' in user_role:
            print("3 - Mettre à jour un événement")
            valid_choices.append("3")
        if 'Management' in user_role:
            print("4 - Supprimer un événement")
            valid_choices.append("4")

        print("0 - Retour")
        choice = input("Entrez le numéro de votre choix : ")

        if choice not in valid_choices:
            print("Choix invalide, veuillez réessayer.")
            continue

        if choice == "1":
            cli_logic.list_events()
        elif choice == "2" and 'Sales' in user_role:
            cli_prompt.add_event_prompt()
        elif choice == "3" and ('Management' in user_role or 'Support' in user_role):
            cli_prompt.update_event_prompt()
        elif choice == "4" and 'Management' in user_role:
            cli_prompt.delete_event_prompt()
        elif choice == "0":
            break
    
def manage_users_menu(user_role):
    while True:
        print("\nGestion des Utilisateurs")
        valid_choices = ["0"]

        if 'Management' in user_role:
            print("1 - Ajouter un utilisateur")
            print("2 - Modifier un utilisateur")
            print("3 - Supprimer un utilisateur")
            print("4 - Lister les utilisateurs")
            valid_choices.extend(["1", "2", "3", "4"])

        print("0 - Retour")
        choice = input("Entrez le numéro de votre choix : ")

        if choice not in valid_choices:
            print("Choix invalide, veuillez réessayer.")
            continue

        if choice == "1" and 'Management' in user_role:
            cli_prompt.add_user_prompt()
        elif choice == "2" and 'Management' in user_role:
            cli_prompt.update_user_prompt()
        elif choice == "3" and 'Management' in user_role:
            cli_prompt.delete_user_prompt()
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