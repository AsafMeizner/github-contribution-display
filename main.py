import os
import subprocess
import datetime

# Replace these with your desired message and year
message = "HELLO"
year = 2000
repo_dir = "/"

alphabet_grid = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10011", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00001", "00001", "00001", "00001", "10001", "10001", "01110"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"]
}

first_day_of_year = datetime.date(year, 1, 1)
first_sunday = first_day_of_year + datetime.timedelta(days=(6 - first_day_of_year.weekday()))

weeks_in_year = 52
days_in_week = 7
grid_height = len(alphabet_grid['A'])
max_characters = (weeks_in_year - 1) // (len(alphabet_grid['A'][0]) + 1)
message = message[:max_characters]

grid_width = len(message) * (len(alphabet_grid['A'][0]) + 1)

contribution_grid = [["0"] * weeks_in_year for _ in range(grid_height)]

for i, char in enumerate(message):
    if char in alphabet_grid:
        char_grid = alphabet_grid[char]
        for row in range(grid_height):
            for col in range(len(char_grid[row])):
                contribution_grid[row][i * (len(char_grid[row]) + 1) + col] = char_grid[row][col]

os.makedirs(repo_dir, exist_ok=True)
os.chdir(repo_dir)
subprocess.run(["git", "init"])

with open("text.txt", "w") as f:
    pass

start_date = first_sunday
commits = 0
used_dates = set()
for week in range(weeks_in_year):
    for day in range(days_in_week):
        for row in range(grid_height):
            if week < len(contribution_grid[row]) and contribution_grid[row][week] == "1":
                commit_date = start_date + datetime.timedelta(weeks=week, days=row + 1)  # Add one day to shift everything
                if commit_date not in used_dates:
                    commit_message = f"Commit for {commit_date.isoformat()}"
                    with open("text.txt", "a") as f:
                        f.write(f"{commit_message}\n")
                    subprocess.run(["git", "add", "text.txt"])
                    subprocess.run(["git", "commit", "-m", commit_message, "--date", commit_date.isoformat()])
                    commits += 1
                    used_dates.add(commit_date)

subprocess.run(["git", "remote", "add", "origin", "https://github.com/AsafMeizner/github-contribution-display"])
subprocess.run(["git", "branch", "-M", "master"])
subprocess.run(["git", "push", "-u", "origin", "master", "--force"])

print(f"Created {commits} commits to form the message '{message}' on the GitHub contribution grid for {year}.")
