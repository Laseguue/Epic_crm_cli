import cli_logic
import getpass

def add_client_prompt():
    full_name = input("Nom complet : ")
    email = input("Email : ")
    phone = input("Téléphone : ")
    company_name = input("Nom de l'entreprise : ")
    cli_logic.add_client(full_name, email, phone, company_name)

def update_client_prompt():
    client_id = input("ID du client à mettre à jour : ")
    full_name = input("Nouveau nom complet : ")
    email = input("Nouvel email : ")
    phone = input("Nouveau téléphone : ")
    company_name = input("Nouveau nom de l'entreprise : ")
    cli_logic.update_client(client_id, full_name, email, phone, company_name)

def delete_client_prompt():
    client_id = input("ID du client à supprimer : ")
    cli_logic.delete_client(client_id)

def add_contract_prompt():
    user_role = cli_logic.get_user_role()
    client_id = input("ID du client pour le contrat : ")
    total_amount = input("Montant total du contrat : ")
    amount_due = input("Montant dû : ")
    status = input("Statut du contrat (True pour signé, False sinon) : ")
    sales_contact = None
    if 'Management' in user_role:
        sales_contact = input("ID de l'utilisateur Sales Contact : ")
    cli_logic.add_contract(client_id, total_amount,amount_due, status, sales_contact)

def update_contract_prompt():
    user_role = cli_logic.get_user_role()
    contract_id = input("ID du contrat à mettre à jour : ")
    client_id = input("ID du client pour le contrat : ")
    total_amount = input("Montant total du contrat : ")
    amount_due = input("Montant dû : ")
    status = input("Statut du contrat (True pour signé, False sinon) : ")
    sales_contact = None
    if 'Management' in user_role:
        sales_contact = input("ID de l'utilisateur Sales Contact : ")
    cli_logic.update_contract(contract_id, client_id, total_amount,amount_due, status, sales_contact)

def delete_contract_prompt():
    contract_id = input("ID du contrat à supprimer : ")
    cli_logic.delete_contract(contract_id)

def add_event_prompt():
    contract_id = input("ID du contrat pour l'événement : ")
    event_start_date = input("Date de début de l'événement (YYYY-MM-DD HH:MM:SS) : ")
    event_end_date = input("Date de fin de l'événement (YYYY-MM-DD HH:MM:SS) : ")
    location = input("Lieu de l'événement : ")
    attendees = input("Nombre de participants : ")
    notes = input("Notes sur l'événement : ")
    cli_logic.add_event(contract_id, event_start_date, event_end_date, location, attendees, notes)

def update_event_prompt():
    user_role = cli_logic.get_user_role()
    event_id = input("ID de l'événement à mettre à jour : ")
    event_start_date = input("Nouvelle date de début de l'événement (YYYY-MM-DD HH:MM:SS) : ")
    event_end_date = input("Nouvelle date de fin de l'événement (YYYY-MM-DD HH:MM:SS) : ")
    location = input("Nouveau lieu de l'événement : ")
    attendees = input("Nouveau nombre de participants : ")
    notes = input("Nouvelles notes sur l'événement : ")
    if "Management" in user_role:
        support_contact = input("ID de l'utilisateur support à assigner à l'événement : ")
        cli_logic.update_event(event_id, event_start_date, event_end_date, location, attendees, notes, support_contact)
    else:
        cli_logic.update_event(event_id, event_start_date, event_end_date, location, attendees, notes)

def delete_event_prompt():
    event_id = input("ID de l'événement à supprimer : ")
    cli_logic.delete_event(event_id)

def add_user_prompt():
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")
    email = input("Email : ")
    first_name = input("Prénom : ")
    last_name = input("Nom de famille : ")
    group = input("Groupe (Management, Sales, Support) : ")
    cli_logic.add_user(username, password, email, first_name, last_name, group)

def update_user_prompt():
    user_id = input("ID de l'utilisateur à mettre à jour : ")
    username = input("Nom d'utilisateur : ")
    email = input("Email : ")
    first_name = input("Prénom : ")
    last_name = input("Nom de famille : ")
    group = input("Groupe (Management, Sales, Support) : ")
    cli_logic.update_user(user_id, username, email, first_name, last_name, group)

def delete_user_prompt():
    user_id = input("ID de l'utilisateur à supprimer : ")
    cli_logic.delete_user(user_id)