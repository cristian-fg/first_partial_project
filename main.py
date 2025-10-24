import pandas as pd
import json

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

    # Iterate over all questions
    for variable_name, question in questions.items():
        while True:
            answer = input(f"\nQuestion: {question}\nYour answer: ")

            # Handle recycling question separately since it's yes/no
            if variable_name == 'R':
                if answer.lower() in ['yes', 'no']:
                    # Store as numeric value (1 for yes, 2 for no)
                    answers[variable_name] = 1 if answer.lower() == 'yes' else 2
                    break
                print("Please answer 'yes' or 'no'")

            # For numeric questions, ensure valid numeric input
            else:
                try:
                    answers[variable_name] = float(answer)
                    break
                except ValueError:
                    print("Please enter a numeric value")

    # =======================
    # CARBON FOOTPRINT MODEL
    # =======================
    # Weighted sum of multiple lifestyle factors:
    # - Driving hours
    # - Electricity use
    # - Clothing consumption
    # - Flight frequency
    # The recycling variable (R) acts as a multiplier.
    contamination = answers['R'] * (
        0.271 * answers['H'] * 4 +  # Car mileage contribution (assuming 4 weeks/month)
        0.475 * answers['E'] +      # Electricity usage contribution
        25 * answers['C'] * 12 +    # Clothing purchases (yearly impact)
        250 * answers['F']          # Flights contribution
    )

    answers['total_contamination'] = contamination
    print(f"\nTotal Contamination: {contamination:.2f} kg CO₂")

    # Store answers in a DataFrame for easier JSON writing
    df = pd.DataFrame([answers])

    # Append to existing JSON if available, otherwise create a new one
    try:
        existing_df = pd.read_json("answers.json")
        combined_df = pd.concat([existing_df, df], ignore_index=True)
        combined_df.to_json("answers.json", orient="records", indent=4)
    except (FileNotFoundError, ValueError):
        # Create file if it doesn’t exist or is empty
        df.to_json("answers.json", orient="records", indent=4)

def print_json_results():
    """
    Loads previous results from 'answers.json', displays all records,
    and calculates improvement or deterioration in total contamination over time.
    """
    try:
        with open("answers.json", "r") as file:
            data = json.load(file)

            print("\n=== Survey Results ===")
            # Display every entry with its values
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

            total_entries = len(data)
            print(f"\nTotal number of entries: {total_entries}")

            # If there are at least two entries, compute progress
            if total_entries >= 2:
                first = data[0]['total_contamination']
                last = data[-1]['total_contamination']
                prev = data[-2]['total_contamination']

                # Compare last entry to the first (overall change)
                diff_first = first - last
                percent_first = (diff_first / first) * 100 if first != 0 else 0

                # Compare last entry to previous one (recent change)
                diff_prev = prev - last
                percent_prev = (diff_prev / prev) * 100 if prev != 0 else 0

                print("\n=== Progress Summary ===")

                # Report overall change
                if diff_first > 0:
                    print(f"Overall improvement since first record: "
                          f"-{diff_first:.2f} kg CO₂ ({percent_first:.2f}% reduction)")
                elif diff_first < 0:
                    print(f"Overall increase since first record: "
                          f"+{-diff_first:.2f} kg CO₂ ({-percent_first:.2f}% increase)")
                else:
                    print("No change since your first record.")

                # Report change since previous record
                if diff_prev > 0:
                    print(f"Improvement since last time: "
                          f"-{diff_prev:.2f} kg CO₂ ({percent_prev:.2f}% reduction)")
                elif diff_prev < 0:
                    print(f"Increase since last time: "
                          f"+{-diff_prev:.2f} kg CO₂ ({-percent_prev:.2f}% increase)")
                else:
                    print("No change since last time.")
            else:
                print("\nNot enough data to calculate improvement (need at least two records).")

            print("")

    # Handle file or data errors gracefully
    except FileNotFoundError:
        print("\nNo results file found (answers.json)")
    except json.JSONDecodeError:
        print("\nError: The JSON file is corrupted or empty")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

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

# start of the program
if __name__ == "__main__":
    main()
