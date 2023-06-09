import smtplib
import os
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

my_email = os.getenv("MY_EMAIL")
password = os.getenv("PASSWORD")
receiver_email = os.getenv("RECEIVER_EMAIL")


class Send_Email:
    def __init__(self) -> None:
        pass

    def send_email(
        self,
        wfh_jobs: List,
        perth_jobs: List,
    ) -> str:
        seen = set()
        unique_wfh_titles = []
        unique_perth_titles = []

        for job in wfh_jobs:
            # Convert the dictionary to a tuple of (key, value) pairs and hash it
            job_tuple = tuple(job.items())
            if job_tuple not in seen:
                # Add the tuple to the set of seen items
                seen.add(job_tuple)
                # Append the unique job to the new list
                unique_wfh_titles.append(job)

        for job in perth_jobs:
            # Convert the dictionary to a tuple of (key, value) pairs and hash it
            job_tuple = tuple(job.items())
            if job_tuple not in seen:
                # Add the tuple to the set of seen items
                seen.add(job_tuple)
                # Append the unique job to the new list
                unique_perth_titles.append(job)

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)

            wfh_job_details = [
                f"{job_title}! Click the link to see the job now: {link}\n"
                for job in unique_wfh_titles
                for job_title, link in job.items()
            ]

            perth_job_details = [
                f"{job_title}! Click the link to see the job now: {link}\n"
                for job in unique_perth_titles
                for job_title, link in job.items()
            ]

            message = MIMEMultipart()
            message["Subject"] = "Job Alert"
            html_content = f"""
            <html>
            <body>
            <h1>Working From Home</h1>
            <ul>
            {''.join(f"<li>{job}</li>" for job in wfh_job_details)}
            </ul>
            <h1>Perth Based Jobs</h1>
            <ul>
            {''.join(f"<li>{job}</li>" for job in perth_job_details)}
            </ul>
            </body>
            </html>
            """
            message.attach(MIMEText(html_content, "html"))

            # message = f"Subject: Job Alert\n\n<h2>Working From Home Jobs</h2>\n\n{wfh_job_details}\n\n<h2>Perth Based Jobs</h2>\n\n{perth_job_details}"

            connection.sendmail(
                from_addr=my_email, to_addrs=receiver_email, msg=message.as_string()
            )
        return f"Email successfully sent to {receiver_email}."
