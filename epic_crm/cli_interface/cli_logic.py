import requests
import sys

API_BASE_URL = "http://localhost:8000/"
TOKEN = None

def get_token():
    return TOKEN

def set_token(new_token):
    global TOKEN
    TOKEN = new_token

def login(username, password):
    response = requests.post(f"{API_BASE_URL}/api-token-auth/", data={'username': username, 'password': password})
    if response.status_code == 200:
        set_token(response.json()['token'])
        print("Login successful.")
        return True
    else:
        print("Login failed.")
        return False

def logout():
    global TOKEN
    if TOKEN:
        headers = {'Authorization': f'Token {TOKEN}'}
        response = requests.post(f"{API_BASE_URL}api/users/logout/", headers=headers)
        if response.status_code == 200:
            print("Déconnexion réussie du côté serveur.")
        else:
            print("Échec de la déconnexion du côté serveur.")
    set_token(None)
    print("You have been logged out.")

# Fonction pour lister les clients
def list_clients():
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    filter_param = input("Entrez un paramètre de filtrage (par exemple, field1=value) ou laissez vide pour voir tous les clients : ")

    if filter_param.strip():
        response = requests.get(f"{API_BASE_URL}api/clients/clients/?{filter_param}", headers=headers)
    else:
        response = requests.get(f"{API_BASE_URL}api/clients/clients/", headers=headers)
    if response.status_code == 200:
        clients = response.json()
        for client in clients:
            print(f"{client['id']} - {client['full_name']} - {client['email']}")
    else:
        print("Failed to retrieve clients. Status code: {response.status_code} - {response.text}")

# Fonction pour ajouter un client
def add_client(full_name, email, phone, company_name):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    client_data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'company_name': company_name
    }
    response = requests.post(f"{API_BASE_URL}api/clients/clients/", headers=headers, data=client_data)
    if response.status_code == 201:
        print("Client added successfully.")
    else:
        print(f"Failed to add client. Status code: {response.status_code}, Response: {response.text}")

# Fonction pour mettre à jour un client
def update_client(client_id, full_name, email, phone, company_name):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    client_data = {
        'full_name': full_name,
        'email': email,
        'phone': phone,
        'company_name': company_name
    }
    if full_name:
        client_data['full_name'] = full_name
    if email:
        client_data['email'] = email
    if phone:
        client_data['phone'] = phone
    if company_name:
        client_data['company_name'] = company_name

    response = requests.patch(f"{API_BASE_URL}api/clients/clients/{client_id}/", headers=headers, data=client_data)
    if response.status_code == 200:
        print("Client updated successfully.")
    else:
        print(f"Failed to update client. Status code: {response.status_code}, Response: {response.text}")

# Fonction pour supprimer un client
def delete_client(client_id):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{API_BASE_URL}api/clients/clients/{client_id}/", headers=headers)
    if response.status_code == 204:
        print("Client deleted successfully.")
    else:
        print(f"Failed to delete client. Status code: {response.status_code} - {response.text}")

# Fonction pour lister les contrats
def list_contracts():
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    filter_param = input("Entrez un paramètre de filtrage (par exemple, field1=value) ou laissez vide pour voir tous les contrats : ")

    if filter_param.strip():
        response = requests.get(f"{API_BASE_URL}api/contracts/contracts/?{filter_param}", headers=headers)
    else:
        response = requests.get(f"{API_BASE_URL}api/contracts/contracts/", headers=headers)
    if response.status_code == 200:
        contracts = response.json()
        for contract in contracts:
            print(f"Contract ID: {contract['id']} - Client: {contract['client']}")
    else:
        print("Failed to retrieve contracts. Status code: {response.status_code} - {response.text}")

# Fonction pour ajouter un contrat
def add_contract(client_id, total_amount, amount_due, status, sales_contact):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    contract_data = {
        'client': client_id,
        'total_amount': total_amount,
        'amount_due': amount_due,
        'status': status,
        'sales_contact': sales_contact
    }
    response = requests.post(f"{API_BASE_URL}api/contracts/contracts/", headers=headers, data=contract_data)
    if response.status_code == 201:
        print("Contract added successfully.")
    else:
        print(f"Failed to add contract. Status code: {response.status_code} - {response.text}")

# Fonction pour mettre à jour un contrat
def update_contract(contract_id, client_id, total_amount,amount_due, status, sales_contact):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    contract_data = {}
    if client_id:
        contract_data['client_id'] = client_id
    if total_amount:
        contract_data['total_amount'] = total_amount
    if amount_due:
        contract_data['amount_due'] = amount_due
    if status:
        contract_data['status'] = status
    if sales_contact:
        contract_data['sales_contact'] = sales_contact

    response = requests.patch(f"{API_BASE_URL}api/contracts/contracts/{contract_id}/", headers=headers, data=contract_data)
    if response.status_code == 200:
        print("Contract updated successfully.")
    else:
        print(f"Failed to update contract. Status code: {response.status_code} - {response.text}")

# Fonction pour supprimer un contrat
def delete_contract(contract_id):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{API_BASE_URL}api/contracts/contracts/{contract_id}/", headers=headers)
    if response.status_code == 204:
        print("Contract deleted successfully.")
    else:
        print(f"Failed to delete contract. Status code: {response.status_code} - {response.text}")

# Fonction pour lister les événements
def list_events():
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    filter_param = input("Entrez un paramètre de filtrage (par exemple, field1=value) ou laissez vide pour voir tous les événements : ")

    if filter_param.strip():
        response = requests.get(f"{API_BASE_URL}api/events/events/?{filter_param}", headers=headers)
    else:
        response = requests.get(f"{API_BASE_URL}api/events/events/", headers=headers)
    if response.status_code == 200:
        events = response.json()
        for event in events:
            print(f"Event ID: {event['id']} - contract: {event['contract']} - support_contact: {event['support_contact']} - location: {event['location']}")
    else:
        print("Failed to retrieve events. Status code: {response.status_code} - {response.text}")

# Fonction pour ajouter un événement
def add_event(contract_id, event_start_date, event_end_date, location, attendees, notes):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    event_data = {
        'contract': contract_id,
        'event_start_date': event_start_date,
        'event_end_date': event_end_date,
        'location': location,
        'attendees': attendees,
        'notes': notes
    }
    response = requests.post(f"{API_BASE_URL}api/events/events/", headers=headers, data=event_data)
    if response.status_code == 201:
        print("Event added successfully.")
    else:
        print(f"Failed to add event. Status code: {response.status_code} - {response.text}")

# Fonction pour mettre à jour un événement
def update_event(event_id, event_start_date, event_end_date, location, attendees, notes, support_contact=None):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    event_data = {}
    if event_start_date:
        event_data['event_start_date'] = event_start_date
    if event_end_date:
        event_data['event_end_date'] = event_end_date
    if location:
        event_data['location'] = location
    if attendees:
        event_data['attendees'] = attendees
    if notes:
        event_data['notes'] = notes
    if support_contact:
        event_data['support_contact'] = support_contact

    response = requests.patch(f"{API_BASE_URL}api/events/events/{event_id}/", headers=headers, data=event_data)
    if response.status_code == 200:
        print("Event updated successfully.")
    else:
        print(f"Failed to update event. Status code: {response.status_code} - {response.text}")

# Fonction pour supprimer un événement
def delete_event(event_id):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{API_BASE_URL}api/events/events/{event_id}/", headers=headers)
    if response.status_code == 204:
        print("Event deleted successfully.")
    else:
        print(f"Failed to delete event. Status code: {response.status_code} - {response.text}")

def list_users():
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    filter_param = input("Entrez un paramètre de filtrage (par exemple, field1=value) ou laissez vide pour voir tous les utilisateurs : ")

    if filter_param.strip():
        response = requests.get(f"{API_BASE_URL}api/users/users/?{filter_param}", headers=headers)
    else:
        response = requests.get(f"{API_BASE_URL}api/users/users/", headers=headers)
    if response.status_code == 200:
        users = response.json()
        for user in users:
            print(f"User ID: {user['id']} - Username : {user['username']} - First name :{user['first_name']} - Last name :{user['last_name']}  - Groupe :{user['groups']}")
    else:
        print("Failed to retrieve Users.Status code: {response.status_code} - {response.text}")

# Fonction pour ajouter un utilisateur
def add_user(username, password, email, first_name, last_name, group):
    token = get_token()
    if token:
        headers = {'Authorization': f'Token {token}'}
        user_data = {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'groups': [group]
        }
        response = requests.post(f"{API_BASE_URL}api/users/users/", headers=headers, data=user_data)
        if response.status_code == 201:
            print("User added successfully.")
        else:
            print(f"Failed to add user. Status code: {response.status_code} - {response.text}")
    else:
        print("You must be logged in as an admin to perform this action.")

def update_user(user_id, username, email, first_name, last_name, group):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    user_data = {}
    if username:
        user_data['username'] = username
    if email:
        user_data['email'] = email
    if first_name:
        user_data['first_name'] = first_name
    if last_name:
        user_data['last_name'] = last_name
    if group:
        user_data['groups'] = [group]

    response = requests.patch(f"{API_BASE_URL}api/users/users/{user_id}/", headers=headers, data=user_data)
    if response.status_code == 200:
        print("User updated successfully.")
    else:
        print(f"Failed to update user. Status code: {response.status_code} - {response.text}")

def delete_user(user_id):
    token = get_token()
    headers = {'Authorization': f'Token {token}'}
    response = requests.delete(f"{API_BASE_URL}api/users/users/{user_id}/", headers=headers)
    if response.status_code == 204:
        print("User deleted successfully.")
    else:
        print(f"Failed to delete user. Status code: {response.status_code} - {response.text}")

def get_user_role():
    token = get_token()
    if token:
        headers = {'Authorization': f'Token {token}'}
        response = requests.get(f"{API_BASE_URL}api/users/me/", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            if 'groups' in user_data:
                return user_data['groups']
            else:
                return []
        else:
            print("Erreur lors de la récupération du rôle de l'utilisateur.")
            return []
    else:
        print("Non connecté.")
        return []