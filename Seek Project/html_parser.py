import requests
import time
from bs4 import BeautifulSoup


class Soup:
    """
    A class for scraping and processing job data using BeautifulSoup.
    """

    def create_soup(self, url):
        """
        Create a BeautifulSoup object by scraping the provided URL.

        Args:
            url (str): The URL to scrape.

        Returns:
            BeautifulSoup: The BeautifulSoup object containing the scraped data.
        """
        soup = BeautifulSoup("", "html.parser")
        for num in range(5):
            page_url = url if num == 0 else f"{url}?page={num}"
            response = requests.get(page_url)
            seek_data = response.text
            soup.append(BeautifulSoup(seek_data, "html.parser"))
            time.sleep(4)
        return soup

    def build_list(self, soup):
        """
        Build a list of junior job titles and their corresponding links.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the job data.

        Returns:
            list: A list of dictionaries, each representing a junior job title and link.
        """
        junior_titles = []
        job_title_tags = soup.find_all("a", {"data-automation": "jobTitle"})
        for tag in job_title_tags:
            job = tag.text
            if "junior" in job.lower():
                href = f'https://www.seek.com.au{tag.get("href")}'
                job_complete = {job: href}
                junior_titles.append(job_complete)
        return junior_titles
