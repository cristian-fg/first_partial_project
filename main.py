import pandas as pd
import json

questions = {
    'C1': "1. How much has your car mileage increased by this week?",
    'C2': "2. How much electricity do you use per month?",
    'C3': "3. How often do you buy new clothes?",
    'C4': "4. How many flights do you take each year?",
    'C5': "5. Do you recycle and reduce waste? (yes/no)?"
}

answers = {}

for variable_name, question in questions.items():
    while True:
        answer = input(f"\nQuestion: {question}\nYour answer: ")
        if variable_name == 'C5':
            if answer.lower() in ['yes', 'no']:
                # Convert yes/no to 1/2 for calculation
                answers[variable_name] = 1 if answer.lower() == 'yes' else 2
                break
            print("Please answer 'yes' or 'no'")
        else:
            try:
                answers[variable_name] = float(answer)
                break
            except ValueError:
                print("Please enter a numeric value")

# Calculate Total Contamination
# Formula: C5 × (0.271C1 × 4 + 0.475C2 + 25C3 × 12 + 250C4)
contamination = answers['C5'] * (
    0.271 * answers['C1'] * 4 +  # Car mileage contribution
    0.475 * answers['C2'] +      # Electricity usage contribution
    25 * answers['C3'] * 12 +    # Clothes buying contribution
    250 * answers['C4']          # Flights contribution
)

answers['total_contamination'] = contamination
print(f"\nTotal Contamination: {contamination:.2f} kg CO₂")

df = pd.DataFrame([answers])

try:
    existing_df = pd.read_json("answers.json")
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    combined_df.to_json("answers.json", orient="records", indent=4)
except (FileNotFoundError, ValueError):
    df.to_json("answers.json", orient="records", indent=4)

    