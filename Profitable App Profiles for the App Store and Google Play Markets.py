import csv
# The Apple Store dataset
with open("AppleStore.csv", "r", encoding="utf-8") as csv_file:
    data = csv.reader(csv_file)
    apple_apps_data = list(data)
    ios = apple_apps_data[1:]
    ios_header = apple_apps_data[0]
    
# The Google Play Store dataset
with open("googleplaystore.csv", "r", encoding="utf-8") as csv_file:
    data = csv.reader(csv_file)
    google_apps_data = list(data)
    android = google_apps_data[1:]
    android_header = google_apps_data[0]

# Function's used to print rows of dataset in a readable way
def explore_data(dataset, header=False):
    for row in dataset[:3]:
        print(row)
        
    if header:
        print("\nNumber of row: " + str(len(dataset)))
        print("Number of column: " + str(len(dataset[0]))) 
        
print(ios_header)
explore_data(ios, True)

print(android_header)
explore_data(android, True)
print("\n-----------\n")

# DATA CLEANING
# 1. Deleting incorrect data
print(android_header)
print(str(android[10472])) #The error row 10472 in Google Play Store
print(str(android[0]))

print(len(android))
del android[10472]  # don't run this more than once
print(len(android))
print("\n-----------\n")

# 2. Removing duplicate entries
    # Cause the main difference happens on the fourth position (the number of reviews) of each duplicate entries of an app, the different numbers show the data was collected at different times. Rather than removing duplicates randomly, we'll only keep the row with the highest number of reviews and remove the other entries for any given app.
duplicate_apps = []
unique_apps = []
for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
print(duplicate_apps[:5])
print(len(duplicate_apps))

# We expect that android_clean only has unique rows/apps which is expected to be 9,659 rows.
print('Expected length: ', len(android) - len(duplicate_apps)) # 9,659
unique_apps = []
android_clean = []
for app in android:
    name = app[0]
    if name not in unique_apps:
        unique_apps.append(name)
        android_clean.append(app)
    else:
        if app[3] > android_clean[unique_apps.index(name)][3]:
            android_clean[unique_apps.index(name)] = app
print(len(android_clean)) # 9,659

explore_data(android_clean, True)

reviews_max = {}
for row in android:
    name = row[0]
    n_reviews = float(row[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
android_clean = []
already_added = []
for row in android:
    name = row[0]
    n_reviews = float(row[3])
    if n_reviews == reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)
print(len(android_clean))
print("\n-----------\n")

# Removing Non-English Apps¶
print(ios[813])
print(ios[6731][1])
print('\n')
print(android_clean[4412][0])
print(android_clean[7940][0])

print(ord('a'), ", ", ord('A'), ", ", ord('爱'), ", ", ord('5'), ", ", ord('+'))

def English_app(dataset, index_name):
    Eng_apps = []
    for i in range(len(dataset)):
        count = 0
        name = dataset[i][index_name]
        for j in range(len(name)):
            character = ord(name[j])
            if character > 127:
                count += 1
        if count <= 3:
            Eng_apps.append(dataset[i])
    return Eng_apps

English_android = English_app(android_clean, 0)
English_ios = English_app(ios, 1)

explore_data(English_android, True)
print("\n")
explore_data(English_ios, True)
print("\n-----------\n")

# Isolated the free apps
def free_apps(dataset, price_index):
    free_apps = []
    for app in dataset:
        price = app[price_index]
            
        if price == "0.0" or price == "0":
            free_apps.append(app)
    return free_apps

free_android = free_apps(English_android, 7)
free_ios = free_apps(English_ios, 4)

print(len(free_android))
print(len(free_ios))