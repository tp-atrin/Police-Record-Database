def db_reading(f):
    data_list = []

    with open(f, "r") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if line:
            if f == "incidents.txt":
                fields = line.split(", ")
                incident_data = {
                    "date-time": fields[0],
                    "location": fields[1],
                    "felony": fields[2],
                    "officer-id": int(fields[3]),
                    "incident-id": int(fields[4])
                }
                data_list.append(incident_data)
            elif f == "suspects.txt":
                fields = line.split(", ")
                suspect_data = {
                    "first-name": fields[0],
                    "last-name": fields[1],
                    "date-of-birth": fields[2],
                    "address": fields[3],
                    "phone-number": fields[4],
                    "incident-id": int(fields[5])
                }
                data_list.append(suspect_data)
            elif f == "officers.txt":
                fields = line.split(", ")
                officer_data = {
                    "officer-name": fields[0],
                    "badge-number": fields[1],
                    "officer-id": int(fields[2])
                }
                data_list.append(officer_data)

    return data_list


def search_data(suspects_list, incidents_list, officers_list, search_query):
    search_results = []
    
    # Search in suspects list
    for suspect in suspects_list:
        if search_query.isdigit():
            if int(search_query) == suspect['incident-id']:
                search_results.append(suspect)
        else:
            if search_query.lower() == suspect['first-name'].lower() or search_query.lower() == suspect['last-name'].lower():
                search_results.append(suspect)
                corresponding_incident_id = suspect['incident-id']
                corresponding_officer_id = next((incident['officer-id'] for incident in incidents_list if incident['incident-id'] == corresponding_incident_id), None)
                if corresponding_officer_id is not None:
                    corresponding_officer = next((officer for officer in officers_list if officer['officer-id'] == corresponding_officer_id), None)
                    if corresponding_officer is not None:
                        search_results.append(corresponding_officer)
    
    # Search in incidents list
    for incident in incidents_list:
        if search_query.isdigit():
            if int(search_query) == incident['incident-id']:
                search_results.append(incident)
        else:
            if search_query.lower() in incident['location'].lower() or search_query.lower() in incident['felony'].lower():
                search_results.append(incident)
                corresponding_officer_id = incident['officer-id']
                corresponding_officer = next((officer for officer in officers_list if officer['officer-id'] == corresponding_officer_id), None)
                if corresponding_officer is not None:
                    search_results.append(corresponding_officer)
                corresponding_suspects = [suspect for suspect in suspects_list if suspect['incident-id'] == incident['incident-id']]
                search_results.extend(corresponding_suspects)
    
    # Search in officers list
    for officer in officers_list:
        if search_query.isdigit():
            if int(search_query) == officer['officer-id']:
                search_results.append(officer)
    
    return search_results





def add_data(data_list, new_data, file_name):
    data_list.append(new_data)
    with open(file_name, "a") as file:
        if file_name == "incidents.txt":
            file.write(f"{new_data['date-time']}, {new_data['location']}, {new_data['felony']}, {new_data['officer-id']}, {new_data['incident-id']}\n")
        elif file_name == "suspects.txt":
            file.write(f"{new_data['first-name']}, {new_data['last-name']}, {new_data['date-of-birth']}, {new_data['address']}, {new_data['phone-number']}, {new_data['incident-id']}\n")

def add_new_incident():
    new_date_time = input("Enter date and time (e.g., 07.08.2023-12:40): ")
    new_location = input("Enter location: ")
    new_felony = input("Enter felony: ")
    new_officer_id = int(input("Enter officer ID: "))
    new_incident_id = int(input("Enter incident ID: "))

    new_incident_data = {
        "date-time": new_date_time,
        "location": new_location,
        "felony": new_felony,
        "officer-id": new_officer_id,
        "incident-id": new_incident_id
    }

    add_data(incidents_list, new_incident_data, "incidents.txt")
    print("New incident added successfully!")

def add_new_suspect():
    new_first_name = input("Enter first name: ")
    new_last_name = input("Enter last name: ")
    new_date_of_birth = input("Enter date of birth: ")
    new_address = input("Enter address: ")
    new_phone_number = input("Enter phone number: ")
    new_incident_id = int(input("Enter incident ID: "))

    new_suspect_data = {
        "first-name": new_first_name,
        "last-name": new_last_name,
        "date-of-birth": new_date_of_birth,
        "address": new_address,
        "phone-number": new_phone_number,
        "incident-id": new_incident_id
    }

    add_data(suspects_list, new_suspect_data, "suspects.txt")
    print("New suspect added successfully!")




def print_list_heading(heading):
    print("\n" + "=" * 40)
    print(heading)
    print("=" * 40)

def print_person_data(person):
    if "first-name" in person:  # Suspect record
        print(f"Name: {person['first-name']} {person['last-name']}")
        print(f"Date of Birth: {person['date-of-birth']}")
        print(f"Address: {person['address']}")
        print(f"Phone Number: {person['phone-number']}")
        print(f"Incident ID: {person['incident-id']}")
    elif "officer-name" in person:  # Officer record
        print(f"Officer Name: {person['officer-name']}")
        print(f"Badge Number: {person['badge-number']}")
        print(f"Officer ID: {person['officer-id']}")


def print_incident_data(incident):
    print(f"Incident Date-Time: {incident['date-time']}")
    print(f"Location: {incident['location']}")
    print(f"Felony: {incident['felony']}")
    print(f"Officer ID: {incident['officer-id']}")
    print(f"Incident ID: {incident['incident-id']}")




# Read data from the files and create the lists
incidents_list = db_reading("incidents.txt")
suspects_list = db_reading("suspects.txt")
officers_list = db_reading("officers.txt")


while True:
    print("""
        The police record database
        loading...
        plese choose one of the options:

        1. Search by name or incident-id
        2. add a new suspect
        3. add a new incident
        4. print out the lists
        5. Quit

        """)
    ask = str(input("\n"))
    if ask == "1":
        #search by name or incident-id
        search_query = str(input("Please enter the suspect's name or incident-id: "))
        searched_data = search_data(suspects_list, incidents_list, officers_list, search_query)

        print("\nSearch Results:")
        if not searched_data:
            print("No matching records found.")
        else:
            for record in searched_data:
                if "first-name" in record:  # Suspect record
                    print(f"Suspect: {record['first-name']} {record['last-name']}")
                    print(f"Date of Birth: {record['date-of-birth']}")
                    print(f"Address: {record['address']}")
                    print(f"Phone Number: {record['phone-number']}")
                    print(f"Incident ID: {record['incident-id']}")
                elif "date-time" in record:  # Incident record
                    print(f"Incident Date-Time: {record['date-time']}")
                    print(f"Location: {record['location']}")
                    print(f"Felony: {record['felony']}")
                    print(f"Officer ID: {record['officer-id']}")
                    print(f"Incident ID: {record['incident-id']}")
                elif "officer-name" in record:  # Officer record
                    print(f"Officer Name: {record['officer-name']}")
                    print(f"Badge Number: {record['badge-number']}")
                    print(f"Officer ID: {record['officer-id']}")
                print()


    if ask == "2":
        #add a new suspect
        add_new_suspect()

    if ask == "3":

        add_new_incident()

    if ask == "4":
        print_list_heading("Incidents List:")
        for incident in incidents_list:
            print_incident_data(incident)

        print_list_heading("Suspects List:")
        for suspect in suspects_list:
            print_person_data(suspect)

        print_list_heading("Officers List:")
        for officer in officers_list:
            print_person_data(officer)

    if ask == "5":
        print("Thank you for using this database")
        exit(0)