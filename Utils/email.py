import os, resend

resend.api_key = os.environ.get("resend_api_key")

def send_email(**message):
  try:
    params = {
      "from": "TNH <info@terranaturalherbs.co.tz>",
      "to": message["receiver"],
      "subject": message["subject"],
      "html": message["message"],
    }
    email = resend.Emails.send(params)
    print(email)
  except Exception as e:
    print(repr(e))
