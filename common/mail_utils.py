from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
import threading
from common.encoder import encode
import json

URL_RESET_PSWD = "http://app.edjobster.com/auth/reset-password/"
URL_EMAIL_VERIFY = "http://app.edjobster.com/auth/activate?token="
URL_EMAIL_ACTIVATE = "http://app.edjobster.com/auth/verify/"


class ResetPasswordMailer(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        print("===========send mail=========")
        token = self.token
        name = token.user.first_name + " " + token.user.last_name
        link = URL_RESET_PSWD + encode(token.id)
        data = {"name": name, "link": link}

        msg_html = render_to_string("password-reset-mail.html", {"data": data})

        send_mail(
            "Edjobster| Password Reset",
            "Rest your password",
            "faimsoft@gmail.com",
            [self.token.user.email],
            html_message=msg_html,
            fail_silently=False,
        )


class EmailVerificationMailer(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        print("===========send mail=========")
        token = self.token
        name = token.user.first_name + " " + token.user.last_name
        link = URL_EMAIL_VERIFY + encode(token.id)
        data = {"name": name, "link": link}

        msg_html = render_to_string("email-verification.html", {"data": data})

        send_mail(
            "Edjobster| Verify Account",
            "Verify Account",
            "info@edjobster.com",
            [self.token.user.email],
            html_message=msg_html,
            fail_silently=False,
        )


class EmailActivationMailer(threading.Thread):
    def __init__(self, token):
        threading.Thread.__init__(self)
        self.token = token

    def run(self):
        print("===========send mail=========")
        token = self.token
        name = token.user.first_name + " " + token.user.last_name
        link = URL_EMAIL_ACTIVATE + encode(token.id)
        data = {"name": name, "link": link}

        msg_html = render_to_string("account-activate.html", {"data": data})

        send_mail(
            "Edjobster| Activate Account",
            "Activate Account",
            "faimsoft@gmail.com",
            [self.token.user.email],
            html_message=msg_html,
            fail_silently=False,
        )

class CandidateMailer(threading.Thread):
    def __init__(self, body, emails):
        threading.Thread.__init__(self)
        self.body = body
        self.emails = emails

    def run(self):
        print("===========send mail=========")
        body = self.body
        data = json.dumps(body)

        emails = self.emails
        print(emails, 'email email')
        
        msg_html = render_to_string("candidate-mail.html", {"data": data})

        send_mail(
            "Edjobster| Candidate Mail",
            "Candidate Mail",
            "info@edjobster.com",
            emails,
            html_message=msg_html,
            fail_silently=False,
        )
