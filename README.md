# Q.U.A.C.K.-Library-Management-System
![image](https://github.com/user-attachments/assets/64c047a8-d581-4bae-8ed6-2d2cd818d194)
The purpose of this document is to provide all the necessary information about
the Q.U.A.C.K. Library Management System. It will cover a general overview of the
project and its intentions, a summary of how our project came to and the process by
which we got here, technical details on what exactly is happening behind the scenes,
and finally, how the project fits with some basic Agile principles.
In one sentence, the best way to explain the Q.U.A.C.K. Library Management
System is its a locally-hosted web app with a clean and intuitive UI to interact with a
library’s NoSQL cloud Database. 

It fits in with the challenge statement/problem that was
given at the start of the development in that it features password encryption, an
inventory of books and movies that is accessible from any machine with resources that
are easily updatable, user data is stored and features hierarchy that allows for different
classes of user, and finally, an event system that has an interactive calendar for
scheduling events and RSVP functionality for library members. 

![image](https://github.com/user-attachments/assets/ba8047b6-6eb2-405e-bfd3-c012fc4eed62)

The software
architecture pattern is client-server because we felt the project would be based around
the shared library inventory data. That also ties into our decision to use a shared
database architecture. Since the database does not have many components, a shared
database would work just fine and keep project complexity down. 

MongoDB was used as the database for this project. It was
chosen because it is NoSQL which provides freedom to layout our database as we saw
fit. 

The other main tool was Flask which was used to route pages and load HTML files. It
was chosen because it interacts well with MongoDB in a development stack. The user
interface part of the system context model refers to the HTML pages displayed by Flask
and is what allows the user to navigate through the services of our system.

![image](https://github.com/user-attachments/assets/63afd777-7d24-4d5f-9e21-a69aa82b1efa)


requirements.txt describes all packages/libraries needed for compilation.
It is recommended packages/libraries are installed in a virtual environment for the purpose of consistency across all development platforms.
To check what is already installed (most desirably inside of virtual environment), enter "pip freeze"
To put these into the requirements.txt file, enter "pip freeze > requirements.txt"

To make things simple, if a package/library is manually installed, edit this README with the command you used, seeing as many are dependencies for a single package installed...

pip install flask  
pip install pymongo  
pip install cryptography  

The following are example pages of the web app.

Admin Home Page:
![Admin Home Page](https://github.com/user-attachments/assets/6207b85c-20bc-4495-9f30-c791e6c291bb)

Catalog Page (Admin POV):
![image](https://github.com/user-attachments/assets/df43c987-3871-46e2-b322-cf8fe694041d)

Events Page:
![image](https://github.com/user-attachments/assets/5e8ab8a3-fb9f-4496-988e-11c649b30ef6)

Manage Users Page (Admin POV):
![image](https://github.com/user-attachments/assets/956b9288-c659-4e9a-a4fd-42d355aa5ada)

Create Event Page (Admin POV):
![image](https://github.com/user-attachments/assets/fa41cac5-bd72-4e26-94c5-5ac1c8cbd88b)

Create New Item Page (Admin POV):
![image](https://github.com/user-attachments/assets/84888c39-5134-490e-ba37-27a58933e154)

Home Page (Member POV):
![image](https://github.com/user-attachments/assets/a03bff54-f597-4e9d-962d-be1e858b3917)

Catalog Page (Member POV):
![image](https://github.com/user-attachments/assets/7dfe4e22-6b53-4a00-b922-d4a3665c50f9)


