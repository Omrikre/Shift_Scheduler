import gdown
import pandas as pd
import pulp

# Variables
min_workers = 2
max_workers_mid_week = 3
max_workers_weekend = 2

# Shift hours
shifts = {
    'day': {"start": "07:00", "end": "15:00"},
    'evening': {"start": "15:00", "end": "23:00"},
    'night': {"start": "23:00", "end": "07:00"}
}




# Print the results
print("Status:", pulp.LpStatus[model.status])
print("Total cost:", pulp.value(model.objective))
for i in df.index:
    print(df['name'][i], "=", x[i].varValue)

def create_schedule():
    # Read the data
    df = pd.read_csv('data.csv', index_col=0)

    # Create the model
    model = pulp.LpProblem("Minimize cost", pulp.LpMinimize)

    # Create the decision variables
    x = pulp.LpVariable.dicts("x", df.index, lowBound=0, cat='Integer')

    # Add the objective function
    model += pulp.lpSum([df['cost'][i] * x[i] for i in df.index])

    # Add the constraints
    for i in df.index:
        model += pulp.lpSum([df['ingredient'][i][j] * x[i] for i in df.index]) >= df['min'][j]
        model += pulp.lpSum([df['ingredient'][i][j] * x[i] for i in df.index]) <= df['max'][j]

    # Solve the model
    model.solve()

def get_data(url):
    print("Enter the google sheets url: \n")
    url = input()

    #clear the console
    print("\033c", end="")

    # Download the data to csv
    gdown.download(url, 'workers_avl.csv', quiet=False)

    
    # check if the download was successful
    if os.path.exists('workers_avl.csv'):
        print("Download successful")
    else:
        print("Download unsuccessful")
        print("Please check the url and try again")

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def print_schedule():
    print("Schedule: \n")

def main():
    get_data(url)
    create_schedule()
    print_schedule()

if __name__ == '__main__':
    main()