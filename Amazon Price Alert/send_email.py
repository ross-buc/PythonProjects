import smtplib
import os

my_email = os.environ.get("ENV_EMAIL")
password = os.environ.get("ENV_PASS")
receiver_email = os.environ.get("ENV_EMAIL")


def send_email(product, price, link):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=receiver_email,
            msg=f"Subject:Price Alert\n\n{product} is now ${price}! Click the link to purchase now. {link}"
        )
    return print(f"Email successfully sent to {my_email}.")
