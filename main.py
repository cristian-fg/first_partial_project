import pandas as pd
import json
from datetime import datetime

# Dictionary holding all the questionnaire questions.
# Each key represents a variable name (H, E, C, F, R),
# and each value is a string with the actual question text.
questions = {
    'H': "1. How many hours do you drive each week on average?",
    'E': "2. How much electricity does your household use each month? (You can find this in kWh on your electricity bill — e.g., 250 kWh)",
    'C': "3. On average, how many new clothing items do you buy each month (shirts, pants, shoes, etc.)?",
    'F': "4. How many round-trip flights do you take per year?",
    'R': "5. Do you regularly recycle materials like paper, plastic, and glass? (yes/no)"
}

def do_questionaire():
    """
    Runs the interactive questionnaire, collects user responses,
    calculates total carbon contamination, and saves results to a JSON file.
    """
    answers = {}

    for variable_name, question in questions.items():
        while True:
            answer = input(f"\nQuestion: {question}\nYour answer: ")

            # Handle recycling question separately (yes/no)
            if variable_name == 'R':
                if answer.lower() in ['yes', 'no']:
                    answers[variable_name] = 1 if answer.lower() == 'yes' else 2
                    answers["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    break
                else:
                    print("Please answer 'yes' or 'no'.")
            else:
                try:
                    value = float(answer)
                    if value < 0:
                        print("Please enter a non-negative value.")
                    else:
                        answers[variable_name] = value
                        answers["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        break
                except ValueError:
                    print("Please enter a numeric value.")

    # =======================
    # CARBON FOOTPRINT MODEL
    # =======================
    contamination = answers['R'] * (
        0.271 * answers['H'] * 4 +  # Hours driven weekly
        0.475 * answers['E'] +      # Electricity usage
        25 * answers['C'] * 12 +    # Clothing purchases
        250 * answers['F']          # Flights
    )

    answers['total_contamination'] = contamination
    print(f"\nTotal Contamination: {contamination:.2f} kg CO₂")

    df = pd.DataFrame([answers])

    # Append to existing JSON or create new
    try:
        existing_df = pd.read_json("answers.json")
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_json("answers.json", orient="records", indent=4)
    except (FileNotFoundError, ValueError):
        df.to_json("answers.json", orient="records", indent=4)

def print_json_results():
    """
    Loads previous results from 'answers.json', displays all records with timestamps,
    shows per-category improvement, and draws an ASCII graph of total contamination trend.
    """
    try:
        with open("answers.json", "r") as file:
            data = json.load(file)

        print("\n=== Survey Results ===")

        # Display each record neatly
        for idx, entry in enumerate(data, 1):
            timestamp = entry.get("timestamp", "No timestamp recorded")
            print(f"\nEntry #{idx}:")
            print("-" * 40)
            print(f"Timestamp: {timestamp}")
            print(f"Hours driven in car (weekly): {float(entry.get('H', 0)):.2f}")
            print(f"Electricity usage (monthly): {float(entry.get('E', 0)):.2f}")
            print(f"Clothes bought (monthly): {float(entry.get('C', 0)):.2f}")
            print(f"Flights (yearly): {float(entry.get('F', 0)):.2f}")
            print(f"Recycles: {'Yes' if entry.get('R') == 1 else 'No'}")
            print(f"Total Contamination: {float(entry.get('total_contamination', 0)):.2f} kg CO₂")
            print("-" * 40)

        total_entries = len(data)
        print(f"\nTotal number of entries: {total_entries}")

        if total_entries >= 2:
            first = float(data[0].get('total_contamination', 0))
            last = float(data[-1].get('total_contamination', 0))
            prev = float(data[-2].get('total_contamination', 0))

            diff_first = first - last
            percent_first = (diff_first / first) * 100 if first != 0 else 0

            diff_prev = prev - last
            percent_prev = (diff_prev / prev) * 100 if prev != 0 else 0

            print("\n=== Progress Summary ===")
            if diff_first > 0:
                print(f"Overall improvement since first record: "
                      f"-{diff_first:.2f} kg CO₂ ({percent_first:.2f}% reduction)")
            elif diff_first < 0:
                print(f"Overall increase since first record: "
                      f"+{-diff_first:.2f} kg CO₂ ({-percent_first:.2f}% increase)")
            else:
                print("No change since your first record.")

            if diff_prev > 0:
                print(f"Improvement since last time: "
                      f"-{diff_prev:.2f} kg CO₂ ({percent_prev:.2f}% reduction)")
            elif diff_prev < 0:
                print(f"Increase since last time: "
                      f"+{-diff_prev:.2f} kg CO₂ ({-percent_prev:.2f}% increase)")
            else:
                print("No change since last time.")

            # === Per-category improvement ===
            categories = ['H', 'E', 'C', 'F']
            names = {
                'H': 'Car Hours',
                'E': 'Electricity',
                'C': 'Clothes',
                'F': 'Flights'
            }
            print("\n=== Category Improvements (since last entry) ===")
            for cat in categories:
                old = float(data[-2].get(cat, 0))
                new = float(data[-1].get(cat, 0))
                diff = old - new
                percent = (diff / old) * 100 if old != 0 else 0
                trend = "↓" if diff > 0 else ("↑" if diff < 0 else "→")
                print(f"{names[cat]:<15}: {trend} {abs(percent):6.2f}% change")

            # === ASCII Graph ===
            print("\n=== Total Contamination Trend ===")
            values = [float(entry.get('total_contamination', 0)) for entry in data]
            max_val = max(values)
            min_val = min(values)
            scale = 50 / (max_val - min_val) if max_val != min_val else 1

            for i, v in enumerate(values):
                bar_len = int((v - min_val) * scale)
                print(f"#{i+1:<2} | " + "█" * bar_len + f" {v:.2f} kg CO₂")

        else:
            print("\nNot enough data to calculate improvement (need at least two records).")

        print("")

    except FileNotFoundError:
        print("\nNo results file found (answers.json).")
    except json.JSONDecodeError:
        print("\nError: The JSON file is corrupted or empty.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

def main():
    """
    Main program loop — provides a text-based interface
    for taking the questionnaire, viewing results, and exiting.
    """
    running = True
    print("Welcome to the carbon footprint quiz")
    while running:
        try:
            # User selects a command
            command = int(input(
                "Select a command (number):\n"
                "1. Do the questionnaire\n"
                "2. See previous results\n"
                "3. About this application\n"
                "4. Exit\n> "
            ))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

        # Menu options
        if command == 1:
            do_questionaire()
        elif command == 2:
            print_json_results()
        elif command == 3:
            print("")
            print("This application helps you estimate your carbon footprint.")
            print("You can take the questionnaire multiple times and see how much you've improved over time.")
            print("")
        elif command == 4:
            running = False
        else:
            print("That's not a valid command. Please try again.")

    print("Thank you for using this program.\nClosing program...")

if __name__ == "__main__":
    main()
