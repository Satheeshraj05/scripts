import json
from transformers import GPT2Tokenizer, GPT2LMHeadModel, Trainer, TrainingArguments

INPUT_PATH = '../data/cleaned_hospital_data.json'
OUTPUT_MODEL_PATH = '../models/hospital_gpt_model/'

def load_data(input_path):
    with open(input_path, 'r') as f:
        data = json.load(f)
    return data

def preprocess_data(data):
    texts = []
    for hospital in data:
        hospital_name = hospital['name']
        doctors = ', '.join([doc['name'] for doc in hospital['data']['doctors'] if doc.get('name')])
        treatments = ', '.join([treat['name'] for treat in hospital['data']['treatments'] if treat.get('name')])
        departments = ', '.join([dept['name'] for dept in hospital['data']['departments'] if dept.get('name')])

        text = f"Hospital: {hospital_name}\nDoctors: {doctors}\nTreatments: {treatments}\nDepartments: {departments}\n"
        texts.append(text)

    return texts

def train_gpt_model(texts):
    # Load pre-trained GPT-2 model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")

    # Tokenize the input texts
    inputs = tokenizer(texts, return_tensors="pt", max_length=512, truncation=True, padding="max_length")

    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_MODEL_PATH,
        num_train_epochs=3,
        per_device_train_batch_size=2,
        logging_dir="./logs",
    )

    # Train the model
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=inputs['input_ids'],
        eval_dataset=inputs['input_ids']
    )
    
    trainer.train()

if __name__ == "__main__":
    data = load_data(INPUT_PATH)
    texts = preprocess_data(data)
    train_gpt_model(texts)
