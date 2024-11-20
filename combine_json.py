import json

# List of JSON files to combine
json_files = ['1.json', 'games_data.json']

# Dictionary to hold unique game data (using game name as the unique key)
games_dict = {}

# Combine the data from all JSON files
for file in json_files:
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            for game in data:
                # Use the game name as a unique identifier, replace duplicates with the latest entry
                games_dict[game['name']] = game
    except FileNotFoundError:
        print(f"File {file} not found. Skipping.")
    except json.JSONDecodeError:
        print(f"Error reading {file}. Skipping.")

# Convert the dictionary back to a list of games
combined_games = list(games_dict.values())

# Sort by "final_score" in descending order
combined_games.sort(key=lambda x: x['final_score'], reverse=True)

# Write the combined, unique, sorted data to a new JSON file
with open('SeriesXS_games_data.json', 'w') as f:
    json.dump(combined_games, f, indent=4)

print("Combined and sorted JSON file created")
