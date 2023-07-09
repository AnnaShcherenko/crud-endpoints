# crud-endpoints
Simple API to manage customers.

## Remarks
This project was made with the simpliest frontend part (HTML+CSS) to make it easier to check if the code works correct.
Since HTML does not support DELETE and PUT requests, they were done using POST request. However, Django view was made with support of DELETE and PUT requests as well.

## Installation

1. Clone the repository:

    https://github.com/AnnaShcherenko/crud-endpoints.git

2. Go inside project directory:

    cd app

3. If it is necessary install poetry 

4. Install project dependencies using Poetry:

    poetry install

5. Activate the virtual environment:

    poetry shell

6. Navigate to the Django project derictory:

    cd crudendpoints

7. Apply database migrations:

    python manage.py migrate

8. Start the development server:

    python manage.py runserver

9. Open the web browser and access the application at http://localhost:8000/.

### Usage

CRUD endpoints in project:
- Create a customer: 
    In all pages of project you can find link CREATE.
    Fill in the required fields in the create customer form and click "Save" to create a new customer.
View customer details: Click on a customer's name in the customer list to view their details.
Delete a customer: Click the "Delete" button next to a customer to delete them from the database.
Update customer details: Click the "Edit" link next to a customer to update their information.


