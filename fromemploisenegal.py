import requests
from bs4 import BeautifulSoup
import psycopg2

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

def insert_jobs_into_db(jobs):
    try:
        # Connexion à la base de données PostgreSQL
        conn = psycopg2.connect(
            dbname="Scrapping",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        # Insertion des données dans la table
        for job in jobs:
            cur.execute("""
                INSERT INTO offre_emploi (title, company, description, date_posted, source)
                VALUES (%s, %s, %s, %s, %s)
            """, (job['title'], job['company'], job['description'], job['date_posted'], job['source']))

        # Validation des transactions
        conn.commit()

        print("Les données ont été insérées avec succès dans la table offre_emploi.")

    except Exception as e:
        print(f"Erreur lors de l'insertion des données dans la base de données: {e}")

    finally:
        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

url = 'https://www.emploisenegal.com/recherche-jobs-senegal?f%5B0%5D=im_field_offre_metiers%3A31'
jobs = scrape_emploisenegal_jobs(url)
insert_jobs_into_db(jobs)
