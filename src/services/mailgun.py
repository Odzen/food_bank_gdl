from src.config.mailgun import mailgun_settings
import httpx
import requests



class MailgunService():

    def __init__(self):
        self.data = {"from": f"{mailgun_settings.mailgun_from}@{mailgun_settings.mailgun_domain}"}
        
        
    async def send_template_email(self, to: str, subject: str, template: str, variables: dict):
        data = self.data
        
        data["to"] = to
        data["subject"] = subject
        data["template"] = template
        data["h:X-Mailgun-Variables"] = variables.__str__()
        
        try:
            response = requests.post(
                    f"https://{mailgun_settings.mailgun_api_url}/{mailgun_settings.mailgun_domain}/messages",
                    auth=("api", mailgun_settings.mailgun_api_key),
                    data=data)
            return response.json()
        except Exception as e:
            raise e
    