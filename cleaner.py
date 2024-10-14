import json

INPUT_PATH = '../data/hospital_data.json'
OUTPUT_PATH = '../data/cleaned_hospital_data.json'

def clean_data(input_path, output_path):
    with open(input_path, 'r') as f:
        hospital_data = json.load(f)

    cleaned_data = []
    
    for hospital in hospital_data:
        cleaned_hospital = {
            'name': hospital['name'],
            'location': hospital.get('location', 'Not Provided'),
            'data': {
                'doctors': [doc for doc in hospital['data']['doctors'] if doc.get('name')],
                'treatments': [treat for treat in hospital['data']['treatments'] if treat.get('name')],
                'departments': [dept for dept in hospital['data']['departments'] if dept.get('name')]
            }
        }
        cleaned_data.append(cleaned_hospital)

    # Save the cleaned data to a JSON file
    with open(output_path, 'w') as f:
        json.dump(cleaned_data, f, indent=4)

if __name__ == "__main__":
    clean_data(INPUT_PATH, OUTPUT_PATH)
