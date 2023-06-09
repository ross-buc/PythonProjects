import requests
import time
from bs4 import BeautifulSoup


class Soup:
    def create_soup(self, url):
        soup = BeautifulSoup("", "html.parser")
        for num in range(5):
            page_url = url if num == 0 else f"{url}?page={num}"
            response = requests.get(page_url)
            seek_data = response.text
            soup.append(BeautifulSoup(seek_data, "html.parser"))
            time.sleep(4)
        return soup

    def build_list(self, soup):
        junior_titles = []
        job_title_tags = soup.find_all("a", {"data-automation": "jobTitle"})
        for tag in job_title_tags:
            job = tag.text
            if "junior" in job.lower():
                href = f'https://www.seek.com.au{tag.get("href")}'
                job_complete = {job: href}
                junior_titles.append(job_complete)
        return junior_titles


# class Soup:
#     def create_soup(self, url):
#         soup = BeautifulSoup("", "html.parser")

#         for num in range(5):
#             if num == 0:
#                 page_url = url
#             else:
#                 page_url = f"{url}?page={num}"

#             response = requests.get(page_url)
#             seek_data = response.text
#             soup.append(BeautifulSoup(seek_data, "html.parser"))

#             time.sleep(4)

#         return soup

#     def build_list(self, soup):
#         job_titles = [
#             tag.text for tag in soup.find_all("a", {"data-automation": "jobTitle"})
#         ]

#         junior_titles = []

#         for job in job_titles:
#             if "junior" in job or "Junior" in job:
#                 job_title_tag = soup.find("a", string=job)
#                 href = f'https://www.seek.com.au{job_title_tag.get("href")}'
#                 job_complete = {job: href}
#                 junior_titles.append(job_complete)

#         return junior_titles
