import json
import time
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.reed.co.uk'
path = '/jobs/developer-jobs-in-london'
pages = 10


def get_html(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def get_details(url):
    soup = get_html(url)
    description = soup.find(class_='description').text
    skills = []
    if (soup.find(class_='skills-list')):
        skills = soup.find(
            class_='skills-list').text.strip().replace('/ /g', '').split('\n')

    return [description, skills]


def get_jobs(url):
    print('start: ' + url)
    data = []
    soup = get_html(url)
    jobs = soup.find_all(class_='job-result-card')
    for job in jobs:
        title = job.find(class_='job-result-heading__title').text.strip()
        salary = job.find(class_='job-metadata__item--salary').text.strip()
        location = job.find(class_='job-metadata__item--location').text.strip()
        remote = ''
        if (job.find(class_='job-metadata__item--remote')):
            remote = job.find(class_='job-metadata__item--remote').text.strip()
        job_type = job.find(class_='job-metadata__item--type').text.strip()

        time.sleep(1)

        details_link = job.find(
            'a', class_='job-result-card__block-link')['href']
        details = get_details(base_url + details_link)

        data.append({
            'title': title,
            'salary': salary,
            'location': location,
            'remote': remote,
            'job_type': job_type,
            'description': details[0],
            'skills': details[1]
        })
        print(jobs.index(job) + 1, 'of', len(jobs), 'done')
    return data


data = []
for i in range(1, pages + 1):
    url = base_url + path + '?pageno=' + str(i)
    data += get_jobs(url)
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
