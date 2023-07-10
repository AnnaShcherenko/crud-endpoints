# crud-endpoints
Simple API to manage customers.

## Remarks
- The project was made using Python + Django REST framework.

- Black was used for formatting.

- This project was made with the simpliest frontend part (HTML+CSS) to make it easier to check if the code works correct.

- SQLite was used as a database. 

- Since HTML does not support DELETE and PUT requests, they were done using POST request.

- Unit tests were added to the project. To run the tests: python manage.py test


## Installation

**1. Clone the repository:**

    https://github.com/AnnaShcherenko/crud-endpoints.git

**2. Go inside project directory:**

    cd app

**3. Make sure you have poetry installed, if not:**

    brew install poetry 

**4. Install project dependencies using Poetry:**

    poetry install

**5. Activate the virtual environment:**

    poetry shell

**6. Navigate to the Django project derictory:**

    cd crudendpoints

**7. Apply database migrations if db is empty:**

    python manage.py migrate

**8. Start the development server:**

    python manage.py runserver

**9. Open the web browser and access the application at:**

    http://localhost:8000/




## Usage: CRUD endpoints

**Create a customer:**

    http://127.0.0.1:8000/create_customer/

    In all pages of the project you can find link "Create Customer".
    Fill in the required fields in the create customer form and click "Save" to create a new customer.

**View all customers from database:**

    http://127.0.0.1:8000/customers_list/

    In all pages of the project you can find link "List Customers".
    Click on the link "List Customers" to view all created customers.

**View customer details:**

    http://127.0.0.1:8000/customer/<customer id>/

    There is a link "Details" under every customer from the page with customers list.
    Click on the link "Details" to view the details of the customer you are interested in.

**Delete a customer:**

    http://127.0.0.1:8000/customer/delete/<customer id>/

    You can delete customer from the page with customers list and from the page with customer details.
    Click the "Delete" button next to a customer. Then confirm that you are confident in your actions. Finally the customer will be deleted from the database.

**Update customer details:**

    http://127.0.0.1:8000/customer/<customer id>/update

    You can update customer details from the page with customers list and from the page with customer details.   
    Click the "Edit" link next to a customer to update their information.