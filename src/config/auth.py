from fastapi.security import OAuth2PasswordBearer

# Defining token retreival path
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login", auto_error = False)