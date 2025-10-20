import pandas as pd
import json

questions = {
    'H': "1. How many hours do you drive each week?",
    'E': "2. How much electricity do you use per month? (In kWh which can be seen in your bill)",
    'C': "3. How many pieces of clothing you buy each month? ",
    'F': "4. How many flights do you take each year?",
    'R': "5. Do you recycle and reduce waste? (yes/no)?"
}

def do_questionaire():
    answers = {}

    for variable_name, question in questions.items():
        while True:
            answer = input(f"\nQuestion: {question}\nYour answer: ")
            if variable_name == 'R':
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
    # Formula: CF=(Hx7×2.3)+(E×0.5)+(C×10)+(F×250)−(R×100)
    contamination = answers['R'] * (
        0.271 * answers['H'] * 4 +  # Car mileage contribution
        0.475 * answers['E'] +      # Electricity usage contribution
        25 * answers['C'] * 12 +    # Clothes buying contribution
        250 * answers['F']          # Flights contribution
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

def print_json_results():
    try:
        # Read and display all entries from the JSON file
        with open("answers.json", "r") as file:
            data = json.load(file)
            print("\n=== Survey Results ===")
            for idx, entry in enumerate(data, 1):
                print(f"\nEntry #{idx}:")
                print("-" * 40)
                print(f"Car mileage (weekly): {entry['H']:.2f}")
                print(f"Electricity usage (monthly): {entry['E']:.2f}")
                print(f"Clothes bought (monthly): {entry['C']:.2f}")
                print(f"Flights (yearly): {entry['F']:.2f}")
                print(f"Recycles: {'Yes' if entry['R'] == 1 else 'No'}")
                print(f"Total Contamination: {entry['total_contamination']:.2f} kg CO₂")
                print("-" * 40)
            
            print(f"\nTotal number of entries: {len(data)}")
            
    except FileNotFoundError:
        print("\nNo results file found (answers.json)")
    except json.JSONDecodeError:
        print("\nError: The JSON file is corrupted or empty")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

def main():
    running = True
    print("Welcome to this stupid ass useless program")
    while running:
        command = int(input("Select a command (number):\n1. do questionaire\n2. see previous shit\n3. exit\n> "))
        if command == 1:
            do_questionaire()
        elif command == 2:
            print_json_results()
        elif command == 3:
            running = False
        else:
            print("That's not a valid command. Please try the number according to the commands.")
    print("Thank you for trusting us with this dumb thing idk")

main()
