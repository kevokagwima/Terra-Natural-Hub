import os, resend

resend.api_key = os.environ.get("resend_api_key")

def send_email():
  try:
    params = {
      "from": "TNH <terranaturalherbs.co.tz>",
      "to": "kevokagwima@gmail.com",
      "subject": "Test",
      "html": "It works",
    }
    email = resend.Emails.send(params)
    print(email)
  except Exception as e:
    print(repr(e))
