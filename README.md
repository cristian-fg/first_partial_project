# Household Carbon Footprint Tracker

A simple command-line questionnaire that estimates a household's average carbon footprint (kg CO₂) based on driving, electricity usage, clothing purchases, flights, and recycling habits. Results are saved to `answers.json` so you can track progress over time.

## Features
- Interactive questionnaire covering weekly, monthly, and yearly habits.
- Calculates a weighted total contamination score.
- Saves each session to `answers.json`.
- Displays all past entries and summarizes progress (overall and since last record).

## Requirements
- Python 3.7+
- pandas

Install dependencies:
```sh
pip install pandas
```

## Usage
Run the program:
python [main.py](http://_vscodecontentref_/0)

Menu options:
1. Do the questionnaire — prompts for answers and appends results to `answers.json`.
2. See previous results — prints all saved entries and a progress summary.
3. About this application — brief info.
4. Exit.

## Data
- Output file: `answers.json` (array of records)
- Each record contains:
  - H: hours driving per week (number)
  - E: electricity use per month in kWh (number)
  - C: clothing items purchased per month (number)
  - F: round-trip flights per year (number)
  - R: recycling flag (1 = yes, 2 = no)
  - total_contamination: computed total (kg CO₂)

## How the score is computed
The program computes a weighted sum of factors (driving, electricity, clothing, flights) and multiplies by the recycling factor. See the calculation in the source.

## Files
- `main.py` — program entry and logic (questionnaire, calculation, results display).
- `answers.json` — generated runtime data file with saved sessions.

## Notes
- Provide numeric answers for the first four questions and "yes"/"no" for recycling.
- If `answers.json` is missing or corrupted, the program will create or report it.

## Contributing
Small fixes or clarifications in questions and weights are welcome.

## License
No license specified.
```

Referenced symbols and files: `do_questionaire`, `print_json_results`, `main`, main.py, README.md
