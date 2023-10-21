import requests

# Define the URL
url = "http://api.nasa.gov/neo/rest/v1/neo/browse?page=0&size=20&api_key=DEMO_KEY"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Initialize an empty list to store the "id" values
id_list = []

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    json_data = response.json()

    # Extract "id" values from each object in the "near_earth_objects" list and append to the list
    for neo in json_data["near_earth_objects"]:
        id_list.append(neo["id"])

    # Print the list of "id" values
    print(id_list)
    base_url = "http://api.nasa.gov/neo/rest/v1/neo/{}?api_key=DEMO_KEY"

    # Ask the user to input an asteroid ID
    asteroid_id = input("Enter an asteroid ID: ")

    # Construct the full URL with the provided ID
    url = base_url.format(asteroid_id)

    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON data from the response
        asteroid_data = response.json()
        
        # Extract and display relevant information about the asteroid
        print("Asteroid ID:", asteroid_data["id"])
        print("Name:", asteroid_data["name"])
        print("NEO Reference ID:", asteroid_data["neo_reference_id"])
        # Add more fields as needed
        

        # Iterate through the close approach data to find the most recent entry
       # Initialize variables to store the most recent approach data for Earth and Jupiter
        most_recent_earth_approach_data = None
        most_recent_jupiter_approach_data = None

        # Iterate through the close approach data to find the most recent approaches
        for approach_entry in asteroid_data["close_approach_data"]:
            approach_date = approach_entry["close_approach_date_full"]
            epoch_date = approach_entry["epoch_date_close_approach"]
            orbiting_body = approach_entry["orbiting_body"]

            # Check if this entry is more recent than the current most recent one
            if not most_recent_earth_approach_data or (orbiting_body == "Earth" and epoch_date > most_recent_earth_approach_data["epoch_date_close_approach"]):
                most_recent_earth_approach_data = approach_entry

            if not most_recent_jupiter_approach_data or (orbiting_body == "Juptr" and epoch_date > most_recent_jupiter_approach_data["epoch_date_close_approach"]):
                most_recent_jupiter_approach_data = approach_entry

        # Extract the details of the most recent Earth approach
        most_recent_earth_approach_date = most_recent_earth_approach_data["close_approach_date_full"]
        earth_miss_distance_kilometers = most_recent_earth_approach_data["miss_distance"]["kilometers"]
        earth_relative_velocity_kms = most_recent_earth_approach_data["relative_velocity"]["kilometers_per_second"]

        # Extract the details of the most recent Jupiter approach
        most_recent_jupiter_approach_date = most_recent_jupiter_approach_data["close_approach_date_full"]
        jupiter_miss_distance_kilometers = most_recent_jupiter_approach_data["miss_distance"]["kilometers"]
        jupiter_relative_velocity_kms = most_recent_jupiter_approach_data["relative_velocity"]["kilometers_per_second"]

        # Print the most recent approach details for Earth
        print("Most Recent Closest Approach Date to Earth:", most_recent_earth_approach_date)
        print("Miss Distance to Earth (Kilometers):", earth_miss_distance_kilometers)
        print("Relative Velocity to Earth (km/s):", earth_relative_velocity_kms)

        # Print the most recent approach details for Jupiter
        print("Most Recent Closest Approach Date to Jupiter:", most_recent_jupiter_approach_date)
        print("Miss Distance to Jupiter (Kilometers):", jupiter_miss_distance_kilometers)
        print("Relative Velocity to Jupiter (km/s):", jupiter_relative_velocity_kms)
                
    
else:
    print("Failed to fetch data. Status code:", response.status_code)
