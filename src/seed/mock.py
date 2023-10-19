from src.schemas.users import CreateUser, Roles
from src.schemas.requests import CreateRequest, TypeRequest, StateRequest
from src.schemas.tickets import CreateTicket, UrgencyTicketEnum

# requests
auth_request = CreateRequest(
    type= TypeRequest.authorization,
    title="Authorization for something",
    description="I need authorization for something"
)
 
account_creation_request_dev = CreateRequest(
    type= TypeRequest.account_creation,
    email="dev@mail.com",
    state=StateRequest.approved,
    title="Account creation for Dev",
    description="I need to register..."
) 

account_creation_request_admin = CreateRequest(
    type= TypeRequest.account_creation,
    email="admin@mail.com",
    state=StateRequest.approved,
    title="Account creation for Admin",
    description="I need to register..."
) 

account_creation_request_employee = CreateRequest(
    type= TypeRequest.account_creation,
    email="employee@mail.com",
    state=StateRequest.approved,
    title="Account creation for Employee",
    description="I need to register..."
) 

account_creation_request_new_user = CreateRequest(
    type= TypeRequest.account_creation,
    email="new@mail.com",
    title="Account creation for new user",
    description="I need to register..."
)     

other_request = CreateRequest(
    type= TypeRequest.other,
    title="Other request",
    description="I need to..."
)

requests_for_creation = [auth_request, account_creation_request_dev,
                         account_creation_request_admin,account_creation_request_employee,
                         account_creation_request_new_user, other_request]


# users
user_admin = CreateUser(
    first_name="Admin",
    last_name="User",
    email="admin@mail.com",
    role=Roles.admin,
    identification="1234568",
    password="admin"
)
 
user_dev = CreateUser(
    first_name="Dev",
    last_name="User",
    email="dev@mail.com",
    role=Roles.developer,
    identification="1234568",
    password="dev"
)

user_employee = CreateUser(
    first_name="Employee",
    last_name="User",
    email="employee@mail.com",
    role=Roles.employee,
    identification="1234568",
    password="employee"
)

users_for_creation = [user_admin, user_dev, user_employee] 

# tickets
ticket_high_urgency = CreateTicket(
    title="Urgent ticket",
    description="We need this now",
    urgency=UrgencyTicketEnum.high,
    category= "food"
)

ticket_medium_urgency = CreateTicket(
    title="Medium ticket",
    description="We need as soon as possible",
    urgency=UrgencyTicketEnum.medium,
    category= "food"
)

ticket_low_urgency = CreateTicket(
    title="Low ticket",
    description="We need this later",
    urgency=UrgencyTicketEnum.low,
    category= "food"
)

tickets_for_creation = [ticket_high_urgency, ticket_medium_urgency, ticket_low_urgency]