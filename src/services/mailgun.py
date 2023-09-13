from src.config.mailgun import mailgun_settings
from src.schemas.mailgun import SendEmailBody, ResponseEmailSent
import json
import requests

class MailgunService():

    def __init__(self):
        self.data = {"from": f"{mailgun_settings.mailgun_from}@{mailgun_settings.mailgun_domain}"}
           
    def send_template_email(self, send_email_body: SendEmailBody) -> ResponseEmailSent:
        data = self.data
        
        to = f"{send_email_body.recipient_name} <{send_email_body.recipient_email}>"
        
        data["to"] = to
        data["subject"] = send_email_body.subject
        data["template"] = send_email_body.template
        data["h:X-Mailgun-Variables"] = json.dumps(send_email_body.variables)
        
        try:
            response = requests.post(
                    f"https://{mailgun_settings.mailgun_api_url}/{mailgun_settings.mailgun_domain}/messages",
                    auth=("api", mailgun_settings.mailgun_api_key),
                    data=data)
            
            return ResponseEmailSent(**response.json())
        
        except Exception as e:
            raise e
    