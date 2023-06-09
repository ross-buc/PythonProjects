from send_email import Send_Email
from html_parser import Soup
from typing import List

## Import Classes
soup = Soup()
send_email = Send_Email()

# fmt: off
seek_urls = [
    ## URL for Seek website with the following filters:
    ## Jobs with Junior python in the title name
    ## and Jobs working from home
    "https://www.seek.com.au/junior-python-developer-jobs?where=Work%20from%20home",


    ## URL for Seek website with the following filters:
    ## Jobs with Junior python in the title name
    ## and Jobs working within Western Australia
    "https://www.seek.com.au/junior-python-developer-jobs/in-Western-Australia-WA",


    ## URL for Seek website with the following filters:
    ## Jobs with Junior in the title name
    ## and Jobs working from home
    "https://www.seek.com.au/junior-developer-jobs?where=Work%20from%20home",


    ## URL for Seek website with the following filters:
    ## Jobs with Junior python in the title name
    ## and Jobs working within Western Australia
    "https://www.seek.com.au/junior-developer-jobs/in-Western-Australia-WA"
]
# fmt: on

wfh_list_of_jobs = []
perth_list_of_jobs = []

for url in seek_urls:
    seek_soup = soup.create_soup(url)
    jobs = soup.build_list(seek_soup)

    if "home" in url:
        wfh_list_of_jobs.extend(jobs)
    else:
        perth_list_of_jobs.extend(jobs)

    print(f"{url} complete... loading")

print("Search has completed, emailing now...")
print(send_email.send_email(wfh_jobs=wfh_list_of_jobs, perth_jobs=perth_list_of_jobs))
