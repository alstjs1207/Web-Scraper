import requests
from bs4 import BeautifulSoup
LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"

def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})
    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find("div", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_achor = company.find("a")
    if company_achor is not None:
        company = str(company_achor.string)
    else:
        company = str(company.string)
    #location = html.find("span",{"class":"location accessible-contrast-color-location"})
    #location = str(location.string)
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company.strip(),
        "location": location,
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed page {page}/{last_page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        for re in results:
            job = extract_job(re)
            jobs.append(job)
    return jobs


def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs