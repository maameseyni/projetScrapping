import requests
from bs4 import BeautifulSoup

def scrape_emploisenegal_jobs(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Erreur lors de la requête : {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    for job_card in soup.find_all('div', class_='card card-job'):
        title_tag = job_card.find('h3')
        company_tag = job_card.find('a', class_='card-job-company company-name')
        description_tag = job_card.find('div', class_='card-job-description').find('p')
        date_tag = job_card.find('time')

        title = title_tag.text.strip() if title_tag else 'No title provided'
        company = company_tag.text.strip() if company_tag else 'No company provided'
        description = description_tag.text.strip() if description_tag else 'No description provided'
        date_posted = date_tag.text.strip() if date_tag else 'No date provided'

        jobs.append({
            'title': title,
            'company': company,
            'description': description,
            'date_posted': date_posted,
            'source': 'emploisenegal'
        })

    return jobs

url = 'https://www.emploisenegal.com/recherche-jobs-senegal?f%5B0%5D=im_field_offre_metiers%3A31'
jobs = scrape_emploisenegal_jobs(url)

# Enregistrer les données dans un fichier texte
with open('emploisenegal_jobs.txt', 'w', encoding='utf-8') as file:
    for job in jobs:
        file.write(f"Title: {job['title']}\n")
        file.write(f"Company: {job['company']}\n")
        file.write(f"Description: {job['description']}\n")
        file.write(f"Date Posted: {job['date_posted']}\n")
        file.write(f"Source: {job['source']}\n")
        file.write("\n" + "-"*40 + "\n\n")

print("Les données des offres d'emploi ont été enregistrées dans emploisenegal_jobs.txt")
