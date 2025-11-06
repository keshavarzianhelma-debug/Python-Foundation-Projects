import re
import json 
 
class AppointmentSystem:
    def __init__(self):
        self.file_name = "member.txt"
        self.patients = {}
        self.doctors = {}
        self.load_data() 
 
    def validate_password(self, password):
        # Password must be at least 8 characters, contain letters and numbers
        if len(password) < 8:
            return False
        if not re.search(r"[A-Za-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        return True
 
    def load_data(self):
        
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
                self.patients = data.get('patients', {})
                self.doctors = data.get('doctors', {})
        except FileNotFoundError:
           
            pass
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {self.file_name}. Starting with empty data.")
            # Handle potential issues with file content
            self.patients = {}
            self.doctors = {}
 
 
    def save_data(self):
        """Saves patient and doctor data to the text file."""
        data = {
            'patients': self.patients,
            'doctors': self.doctors
        }
        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=4) # Use indent for readability
 
 
    def add_user(self, user_type, user_id, first_name, last_name, dob, address, phone_num, password):
        # Validate password
        if not self.validate_password(password):
            print("Password does not meet the criteria (at least 8 characters, containing letters and numbers).")
            return
 
        user = {
            "First Name": first_name,
            "Last Name": last_name,
            "Date of Birth": dob,
            "Address": address,
            "Phone No": phone_num,
            "Password": password
        }
 
        if user_type.lower() == "patient":
            if user_id in self.patients:
                print(f"Patient ID '{user_id}' already exists.")
                return
            self.patients[user_id] = user
            self.save_data() # Save data after adding
            print(f"Patient '{user_id}' added successfully.")
        elif user_type.lower() == "doctor":
            if user_id in self.doctors:
                print(f"Doctor ID '{user_id}' already exists.")
                return
            self.doctors[user_id] = user
            self.save_data() # Save data after adding
            print(f"Doctor '{user_id}' added successfully.")
        else:
            print("Invalid user type. Must be 'patient' or 'doctor'.")
 
    def amend_user(self, user_type, user_id, key, new_value):
        user_dict = self.patients if user_type.lower() == "patient" else self.doctors if user_type.lower() == "doctor" else None
        if user_dict is None:
            print("Invalid user type.")
            return
 
        if user_id not in user_dict:
            print(f"{user_type.capitalize()} ID '{user_id}' not found.")
            return
 
        if key not in user_dict[user_id]:
            print(f"Invalid key. Available keys: {list(user_dict[user_id].keys())}")
            return
 
        # Special handling for password validation if the key is "Password"
        if key == "Password":
            if not self.validate_password(new_value):
                print("New password does not meet the criteria.")
                return
 
        user_dict[user_id][key] = new_value
        self.save_data() # Save data after amending
        print(f"{key} updated successfully for {user_type} '{user_id}'.")
 
    def delete_user(self, user_type, user_id):
        if user_type.lower() == "patient":
            if user_id in self.patients:
                del self.patients[user_id]
                self.save_data() # Save data after deleting
                print(f"Patient '{user_id}' deleted.")
            else:
                print(f"Patient ID '{user_id}' does not exist.")
        elif user_type.lower() == "doctor":
            if user_id in self.doctors:
                del self.doctors[user_id]
                self.save_data() # Save data after deleting
                print(f"Doctor '{user_id}' deleted.")
            else:
                print(f"Doctor ID '{user_id}' does not exist.")
        else:
            print("Invalid user type.")
 
    def find_patient(self, patient_id):
        self.load_data() # Load data before searching (in case another instance modified the file)
        if patient_id in self.patients:
            print("Patient Found:")
            for key, value in self.patients[patient_id].items():
                print(f"{key}: {value}")
            return self.patients[patient_id]
        else:
            print("Patient does not exist.")
            return None

if __name__ == "__main__":
    app = AppointmentSystem()
 
    while True:
        print("\n--- Appointment System Menu ---")
        print("1: Add User (Patient/Doctor)")
        print("2: Amend User (Patient/Doctor)")
        print("3: Delete User (Patient/Doctor)")
        print("4: Find Patient")
        print("5: Exit")
 
        question = input("what do you want to do? (please write correct number)")
 
        if question == "1":
            user_type = input("Enter user type (patient/doctor): ").lower()
            user_id = input("Create a user ID: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            dob = input("Enter date of birth: ")
            address = input("Enter address: ")
            phone_num = input("Enter phone number: ")
            password = input("Create a password (at least 8 characters, letters and numbers): ")
            app.add_user(user_type, user_id, first_name, last_name, dob, address, phone_num, password)
 
        elif question == "2":
            user_type = input("Enter user type to amend (patient/doctor): ").lower()
            user_id = input(f"Enter the {user_type} ID to amend: ")
            key = input("Enter the field to change (e.g., 'Phone No', 'Address', 'Password'): ")
            new_value = input(f"Enter the new value for '{key}': ")
            app.amend_user(user_type, user_id, key, new_value)
 
        elif question == "3":
            user_type = input("Enter user type to delete (patient/doctor): ").lower()
            user_id = input(f"Enter the {user_type} ID to delete: ")
            app.delete_user(user_type, user_id)
 
        elif question == "4":
            patient_id = input("Enter the patient ID you are looking for: ")
            app.find_patient(patient_id)

        elif question == "5":

           print ("goodbye")
    
    question2=input("do you want to countinue? yes or no ")
    if question2== "yes" :
        question=input("what do you wan to do? (please write correct number) 1: add_user, 2: amend, 3: delete user, 4: find patient ... ")
    else :
        question=="end"
        print(question)


