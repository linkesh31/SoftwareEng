Call a Doctor Application

1.Overview
The "Call a Doctor" application facilitates seamless medical consultations between patients and doctors. It leverages Python for backend logic and GUI development using Tkinter, integrates with MySQL for data storage, and was developed using Visual Studio Code for coding and debugging.

2.Features
- User Authentication: Secure registration and login functionality for patients, doctors, clinic admins, and system admins.
- Doctor Search: Find doctors by specialty and location.
- Appointment Booking: Schedule appointments with preferred doctors.

3.Technologies Used
-Python: Backend logic and Tkinter for GUI development.
-MySQL: Relational database management system for storing user, doctor, and appointment data.
-Visual Studio Code: Integrated Development Environment (IDE) for coding, debugging, and version control.
-Figma: Collaborative interface design tool for prototyping and iterating on UI/UX designs.

4.Getting Started
*To run this project locally, follow these steps:
*Prerequisites
-Python 3.x installed on your local machine
-MySQL installed and running locally or accessible remotely
-Visual Studio Code installed for development
-Figma account for viewing and editing UI designs

Installation
Clone the repository:

bash
Copy code
git clone https://github.com/linkesh31/SoftwareEng.git
cd SoftwareEng
Install dependencies:

bash
Copy code
pip install pillow mysql-connector-python tkcalendar
If you need to install custom versions of Tkinter or other system libraries, ensure they are installed according to your operating system's requirements:

bash
Copy code
pip install custom-tkinter
Set up MySQL database:

Create a MySQL database and configure connection settings in your project.
Import the provided SQL script or manually create the following tables based on the schema provided.
Run the application:

bash
Copy code
# Example: python main.py
Access the application:
Open your Tkinter GUI application locally.

Database Schema
Here are the details of the database tables used in the "Call a Doctor" application:

Users Table
Stores general information about all users (patients, doctors, admins).

Column Name	Datatype	Attributes
user_id	INT	PRIMARY KEY, AUTO_INCREMENT
username	VARCHAR(50)	NOT NULL, UNIQUE
password	VARCHAR(255)	NOT NULL
email	VARCHAR(100)	NOT NULL, UNIQUE
phone_number	VARCHAR(20)	
date_of_birth	DATE	
address	VARCHAR(255)	
role	ENUM('admin', 'clinic_admin', 'doctor', 'patient')	NOT NULL
fullname	VARCHAR(45)	
Prescriptions Table
Stores information about prescriptions given to patients.

Column Name	Datatype	Attributes
prescription_id	INT	PRIMARY KEY, AUTO_INCREMENT
appointment_id	INT	NOT NULL
doctor_id	INT	NOT NULL
patient_id	INT	NOT NULL
medical_report	TEXT	
Patients Table
Stores detailed information about patients.

Column Name	Datatype	Attributes
patient_id	INT	PRIMARY KEY, AUTO_INCREMENT
user_id	INT	NOT NULL
fullname	VARCHAR(100)	NOT NULL
identification_number	VARCHAR(12)	
gender	ENUM('male', 'female')	
Doctors Table
Stores detailed information about doctors.

Column Name	Datatype	Attributes
doctor_id	INT	PRIMARY KEY, AUTO_INCREMENT
user_id	INT	NOT NULL
fullname	VARCHAR(100)	NOT NULL
clinic_id	INT	
is_available	TINYINT(1)	DEFAULT '1'
gender	ENUM('male', 'female')	
identification_number	VARCHAR(12)	
Clinics Table
Stores information about clinics.

Column Name	Datatype	Attributes
clinic_id	INT	PRIMARY KEY, AUTO_INCREMENT
clinic_name	VARCHAR(100)	NOT NULL
address	TEXT	
is_approved	TINYINT(1)	DEFAULT '0'
clinic_license	BLOB	
Appointments Table
Stores information about appointments between doctors and patients.

Column Name	Datatype	Attributes
appointment_id	INT	PRIMARY KEY, AUTO_INCREMENT
patient_id	INT	NOT NULL
clinic_id	INT	
doctor_id	INT	NOT NULL
appointment_date	DATE	
appointment_request_status	ENUM('pending', 'accepted', 'declined')	DEFAULT 'pending'
appointment_time	TIME	
treatment_status	ENUM('pending', 'done', 'canceled')	DEFAULT 'pending'
reason	VARCHAR(45)	
Admin_Clinics Table
Stores relationships between admins and clinics they manage.

Column Name	Datatype	Attributes
admin_clinic_id	INT	PRIMARY KEY, AUTO_INCREMENT
admin_id	INT	NOT NULL
clinic_id	INT	NOT NULL
user_id	INT	NOT NULL

Usage
~User Manual
*For Patients
1.Patient Registration
-Description: New patients need to sign up to access the services.
-Steps:
      a)Navigate to the registration page.
      b)Fill in the required information (name, email, password).
      c)Verify your email address.

2.Find and Call a Doctor
-Description: Patients can find doctors based on specialty and location.
-Steps:
      a)Use the search functionality to enter the desired specialty or location.
      b)Browse through the list of doctors matching the criteria.
      c)Click on a doctor's profile to view details.

3.Schedule Appointments
-Description: Patients can schedule appointments with their preferred doctors.
-Steps:
      a)Select a doctor from the search results.
      b)Choose an available time slot from the doctor's schedule.
      c)Confirm the appointment details.

4.Conduct Consultations
-Description: Patients can join video consultations at the scheduled time.
-Steps:
      a)Discuss medical concerns with the doctor.

*For Doctors
1.View Appointments
-Description: Doctors can view their past and upcoming appointments.
-Steps:
       a)Log in with doctor credentials.
       b)Navigate to the doctor dashboard.
       c)View the list of past and upcoming appointments.

2.Generate Prescriptions
-Description: Doctors can generate prescriptions for patients.
-Steps:
      a)Select an appointment from the list.
      b)Generate and save the prescription for the patient.

3.View Medical History
-Description: Doctors can view the medical history of patients they are treating.
-Steps:
      a)Select a patient from the list of appointments.
      b)View the patient's medical history and previous prescriptions.

4.View and Edit Profile
-Description: Doctors can view and update their profile information.
-Steps:
      a)Navigate to the profile section.
      b)Edit profile details as needed and save changes.

*For Clinic Admins
1.Clinic Admin Setup
-Description: Clinic administrators manage doctors and appointments within their clinic.
-Steps:
      a)Log in with admin credentials provided by system administrators.
      b)Navigate to the admin dashboard.
      c)Add or remove doctors, manage schedules, and view clinic performance metrics.

2.Manage Doctors
-Description: Add or remove doctors from the clinic.
-Steps:
      a)Navigate to the "Manage Doctors" section.
      b)Add new doctors by entering their details.
      c)Remove doctors who are no longer part of the clinic.

3.Manage Appointments
-Description: Admins handle scheduling and coordination of appointments.
-Steps:
      a)View all scheduled appointments.
      b)Manage appointment requests from patients and confirm or decline them as needed.

*For System Admins
1.System Admin Configuration
-Description: System administrators oversee the entire application and its functionality.
-Steps:
      a)Log in with system admin credentials.
      b)Access the system admin dashboard.
      c)Manage user roles, system settings, and overall application performance.
      d)View registered clinics.
      e)Accept or reject clinic registration requests.


Contributing
We welcome contributions to enhance the "Call a Doctor" application. To contribute:

Fork the repository.
Create your feature branch (git checkout -b feature/YourFeature).
Commit your changes (git commit -am 'Add some feature').
Push to the branch (git push origin feature/YourFeature).
Create a new Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
