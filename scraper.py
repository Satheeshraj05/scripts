import requests
from bs4 import BeautifulSoup
import json
import os

# Load the list of top hospitals from the JSON file
with open('../data/top_50_hospitals.json') as f:
    hospitals = json.load(f)

# Function to scrape doctor profiles, treatments, departments, social media links, and vision statement
def scrape_hospital_data(url):
    try:
        # Send a GET request to the hospital's website
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        print(f"Successfully retrieved data from {url} with status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

        # Print the structure of the website to debug
        print(soup.prettify())  # To inspect the actual HTML structure

        # Example: Scraping doctor profiles (update based on actual website structure)
        doctors = []
        for doctor_section in soup.find_all('div', class_='doctor-profile'):  # Modify this based on actual HTML structure
            doctor_name = doctor_section.find('h2').text.strip() if doctor_section.find('h2') else "Unknown"
            doctor_specialty = doctor_section.find('p', class_='specialty').text.strip() if doctor_section.find('p', class_='specialty') else "Unknown"
            doctors.append({
                'name': doctor_name,
                'specialty': doctor_specialty
            })
        print("Doctors: ", doctors)

        # Example: Scraping treatments (update based on actual website structure)
        treatments = []
        for treatment_section in soup.find_all('div', class_='treatment'):  # Modify this based on actual HTML structure
            treatment_name = treatment_section.find('h3').text.strip() if treatment_section.find('h3') else "Unknown"
            treatment_desc = treatment_section.find('p').text.strip() if treatment_section.find('p') else "Unknown"
            treatments.append({
                'name': treatment_name,
                'description': treatment_desc
            })
        print("Treatments: ", treatments)

        # Example: Scraping departments (update based on actual website structure)
        departments = []
        for department_section in soup.find_all('div', class_='department'):  # Modify this based on actual HTML structure
            department_name = department_section.find('h3').text.strip() if department_section.find('h3') else "Unknown"
            department_info = department_section.find('p').text.strip() if department_section.find('p') else "Unknown"
            departments.append({
                'name': department_name,
                'info': department_info
            })
        print("Departments: ", departments)

        # Scraping social media links
        social_media_links = {}
        social_media_section = soup.find('ul', class_='list-inline')  # Modify if needed based on actual structure
        if social_media_section:
            social_media_links['twitter'] = social_media_section.find('a', title="UHN Twitter")['href'] if social_media_section.find('a', title="UHN Twitter") else None
            social_media_links['facebook'] = social_media_section.find('a', title="UHN Facebook")['href'] if social_media_section.find('a', title="UHN Facebook") else None
            social_media_links['youtube'] = social_media_section.find('a', title="UHN Youtube")['href'] if social_media_section.find('a', title="UHN Youtube") else None
            social_media_links['linkedin'] = social_media_section.find('a', title="UHN LinkedIn")['href'] if social_media_section.find('a', title="UHN LinkedIn") else None
            social_media_links['instagram'] = social_media_section.find('a', title="UHN Instagram")['href'] if social_media_section.find('a', title="UHN Instagram") else None
        print("Social Media Links: ", social_media_links)

        # Scraping the vision statement
        vision_section = soup.find('span', class_='fc-blue fw-bolder h5')
        vision_statement = vision_section.text.strip() if vision_section else "Vision not provided"
        print("Vision Statement: ", vision_statement)

        return {
            'doctors': doctors,
            'treatments': treatments,
            'departments': departments,
            'social_media_links': social_media_links,
            'vision_statement': vision_statement
        }
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return None

# Directory to save the scraped data
output_dir = '../data/scraped_hospital_data'
os.makedirs(output_dir, exist_ok=True)

# Scraping data for each hospital
hospital_data = []
for hospital in hospitals:
    name = hospital['name']
    website = hospital['website']
    print(f"Scraping data for {name} ({website})...")
    
    data = scrape_hospital_data(website)
    if data:
        hospital_data.append({
            'name': name,
            'location': 'Not Provided',  # Modify if you have location data
            'data': data
        })

# Save the scraped data to a JSON file
output_file = os.path.join(output_dir, 'scraped_hospital_data.json')
with open(output_file, 'w') as f:
    json.dump(hospital_data, f, indent=4)

print(f"Data scraped successfully and saved to {output_file}")
