from flask import Flask,render_template,redirect,url_for,request,jsonify,flash
from datetime import date
from requests import Session
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

from flask_login import UserMixin,login_user,LoginManager,login_required,current_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash



app= Flask(__name__,template_folder="template")
app.app_context().push()
Bootstrap(app)
# Sample data for rover, camera, and Earth date


# NASA API URL
NASA_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?earth_date={}&api_key=DEMO_KEY"



@app.route('/mars')
def mars():
    return render_template("index.html")






# NASA API URL template (you can replace this with the actual NASA API URL)
NASA_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?earth_date={}&api_key=KUpVblrfxDR4h5wOwEE9GUOQ32NkaaTKN5JFrJxn"

# Define a dictionary to store user state information
user_state = {}

# Define lists of valid options for rover, camera, and earth date
rovers = ["curiosity", "spirit", "opportunity"]
cameras = ["fhaz", "rhaz", "mast"]
earth_dates = ["2017-06-13", "2018-05-20"]  # Replace with valid dates

# NASA API URL template (you can replace this with the actual NASA API URL)
NASA_API_URL = "https://api.nasa.gov/mars-photos/api/v1/rovers/{}/photos?earth_date={}&api_key=KUpVblrfxDR4h5wOwEE9GUOQ32NkaaTKN5JFrJxn"

@app.route('/chatbot')
def mars2():
    return render_template("index2.html")

@app.route('/user_reply', methods=['POST'])
def handle_user_reply():
    data = request.form
    user_id = "unique_user_id"  # You can use a session or other user identification method here
    user_message = data["msg"].lower()

    if user_message == "hi":
        response_text = "Hey, welcome to Mars Rover Photos! Do you need a specific image or do you have another query?"
        user_state[user_id] = {"step": "initial"}
    elif user_id in user_state:
        current_step = user_state[user_id]["step"]

        if current_step == "initial":
            if "specific" in user_message:
                user_state[user_id]["step"] = "choose_rover"
                response_text = "Great! Let's start by choosing a Mars rover. Please choose a Mars rover (Curiosity, Spirit, Opportunity)."
            else:
                response_text = "I'm here to help you explore Mars Rover Photos. You can ask for specific images or have other queries."
        elif current_step == "choose_rover":
            if user_message in rovers:
                user_state[user_id]["selected_rover"] = user_message
                user_state[user_id]["step"] = "choose_camera"
                response_text = "You've chosen {}. Now, please choose a camera (e.g., FHAZ, RHAZ, MAST, etc.).".format(
                    user_state[user_id]["selected_rover"])
            else:
                response_text = "Please choose a valid Mars rover (Curiosity, Spirit, Opportunity)."
        elif current_step == "choose_camera":
            if user_message in cameras:
                user_state[user_id]["selected_camera"] = user_message
                user_state[user_id]["step"] = "choose_earth_date"
                response_text = "You've chosen {}. Now, please provide an Earth date (e.g., 2017-06-13).".format(
                    user_state[user_id]["selected_camera"])
            else:
                response_text = "Please choose a valid camera (e.g., FHAZ, RHAZ, MAST, etc.)."
        elif current_step == "choose_earth_date":
            selected_rover = user_state[user_id]["selected_rover"].lower()
            selected_camera=user_state[user_id]["selected_camera"].lower()
            
            # Define launch dates for each rover
            rover_launch_dates = {
                "curiosity": "2015-06-03",
                "spirit": "2004-01-04",
                "opportunity": "2004-01-25"
                # Add launch dates for other rovers as needed
            }

            if selected_rover in rover_launch_dates:
                launch_date = rover_launch_dates[selected_rover]

                if user_message >= launch_date:
                    earth_date = user_message
                    api_url = NASA_API_URL.format(selected_rover, earth_date)
                    # Here, you can make an API request to NASA and fetch images using the api_url
                    # For this example, we'll just provide the API URL in the response
                    text = "You've chosen Earth date {}. You can fetch images from this API URL: {}".format(
                        earth_date, api_url)
                    del user_state[user_id]  # Conversation ends
                    response_text={"redirect": "/display_image",  # Replace '/another_page' with the actual URL you want to redirect to
                                        "api_url": api_url,  # Include the API URL
                                        "selected_rover": selected_rover,  # Include the selected rover
                                        "selected_camera": selected_camera,  # Include the selected camera
                                        "earth_date": earth_date  # Include the Earth date
                                                                                             } 
                    print(response_text)         
                    return jsonify(response_text)
                    
                else:
                    response_text = "Please provide a valid Earth date on or after the launch date of {} ({}).".format(
                        selected_rover.capitalize(), launch_date)
            else:
                response_text = "Invalid rover selection."
    else:
        response_text = "I'm here to help you explore Mars Rover Photos. You can ask for specific images or have other queries."

    return jsonify({"message": response_text})

# Define a dictionary to store user state information
user_state = {}

@app.route('/chatbot2')
def asteroid():
    return render_template("index3.html")

@app.route('/user_reply2', methods=['POST'])
def handle_user_reply2():
    data = request.form
    user_id = "unique_user_id"  # You can use a session or other user identification method here
    user_message = data["msg"].lower()

    response_text = ""
    asteroid_ids = fetch_asteroid_ids()

    if user_message == "hi":
        response_text = "Hey, welcome to the Asteroid Information Chatbot! You can ask for asteroid details by their IDs. " \
                        "To get started, please enter an asteroid ID or 'list' to see available IDs."
        user_state[user_id] = {"step": "initial"}
    elif user_id in user_state:
        current_step = user_state[user_id]["step"]

        if current_step == "initial":
            if user_message == "list":
                # Fetch asteroid IDs from NASA NEO API
                response_text = "Here are some available asteroid IDs: " + ", ".join(asteroid_ids) + ". " \
                                "You can ask for more details by entering an asteroid ID."
            elif user_message in asteroid_ids:
                user_state[user_id]["selected_asteroid_id"] = user_message
                user_state[user_id]["step"] = "get_asteroid_info"
                response_text = "You've chosen asteroid ID {}. Fetching asteroid details...".format(
                    user_state[user_id]["selected_asteroid_id"])
            else:
                response_text = "I'm here to provide information about asteroids. " \
                                "You can enter an asteroid ID or 'list' to see available IDs."
        elif current_step == "get_asteroid_info":
            selected_asteroid_id = user_state[user_id]["selected_asteroid_id"]
            base_url = "http://api.nasa.gov/neo/rest/v1/neo/{}?api_key=DEMO_KEY".format(selected_asteroid_id)

            response = requests.get(base_url)
            asteroid_data = response.json()

            if asteroid_data:
                asteroid_id = asteroid_data["id"]
                asteroid_name = asteroid_data["name"]
                neo_reference_id = asteroid_data["neo_reference_id"]

                most_recent_earth_approach_data = None
                most_recent_jupiter_approach_data = None

                for approach_entry in asteroid_data["close_approach_data"]:
                    approach_date = approach_entry["close_approach_date_full"]
                    epoch_date = approach_entry["epoch_date_close_approach"]
                    orbiting_body = approach_entry["orbiting_body"]

                    if not most_recent_earth_approach_data or (orbiting_body == "Earth" and epoch_date > most_recent_earth_approach_data["epoch_date_close_approach"]):
                        most_recent_earth_approach_data = approach_entry

                    if not most_recent_jupiter_approach_data or (orbiting_body == "Juptr" and epoch_date > most_recent_jupiter_approach_data["epoch_date_close_approach"]):
                        most_recent_jupiter_approach_data = approach_entry

                most_recent_earth_approach_date = most_recent_earth_approach_data["close_approach_date_full"]
                earth_miss_distance_kilometers = most_recent_earth_approach_data["miss_distance"]["kilometers"]
                earth_relative_velocity_kms = most_recent_earth_approach_data["relative_velocity"]["kilometers_per_second"]

                most_recent_jupiter_approach_date = most_recent_jupiter_approach_data["close_approach_date_full"]
                jupiter_miss_distance_kilometers = most_recent_jupiter_approach_data["miss_distance"]["kilometers"]
                jupiter_relative_velocity_kms = most_recent_jupiter_approach_data["relative_velocity"]["kilometers_per_second"]

                response_text = "Asteroid ID: {}\nName: {}\nNEO Reference ID: {} \nMost Recent Closest Approach Date to Earth:{} \nMiss Distance to Earth (Kilometers):{} Relative Velocity to Earth (km/s):{} Most Recent Closest Approach Date to Jupiter:{} Miss Distance to Jupiter (Kilometers):{} Relative Velocity to Jupiter (km/s):{} ".format(
                    asteroid_id, asteroid_name, neo_reference_id, most_recent_earth_approach_date,earth_miss_distance_kilometers,earth_relative_velocity_kms,most_recent_jupiter_approach_date, jupiter_miss_distance_kilometers,jupiter_relative_velocity_kms)

                # Ask if the user has further questions
                user_state[user_id]["step"] = "further_questions"
                response_text += "\nDo you have further questions? If so, please ask, or you can type 'end' to finish."

            else:
                response_text = "Failed to fetch asteroid data. Please try again."

        elif current_step == "further_questions":
            # Handle user's further questions
            # You can add more conditionals based on what the user asks

            if user_message == "end":
                response_text = "Thank you for using the Asteroid Information Chatbot. If you have any more questions in the future, feel free to ask!"
                del user_state[user_id]  # End the conversation

            # Respond to additional questions
            elif "what is asteroid id" in user_message:
                response_text = "Asteroid ID is a unique identifier for a specific asteroid. It helps distinguish one asteroid from another."
            elif "what is recent closest approach date to earth" in user_message:
                response_text = "The Recent Closest Approach Date to Earth is the date when the asteroid came closest to Earth during its orbit. It indicates the most recent encounter with Earth."

            # You can add more conditionals to handle other questions

    else:
        response_text = "I'm here to provide information about asteroids. " \
                        "You can enter an asteroid ID or 'list' to see available IDs."

    return jsonify({"message": response_text})


def fetch_asteroid_ids():
    url = "http://api.nasa.gov/neo/rest/v1/neo/browse?page=0&size=20&api_key=DEMO_KEY"
    response = requests.get(url)
    asteroid_ids = []

    if response.status_code == 200:
        json_data = response.json()
        for neo in json_data["near_earth_objects"]:
            asteroid_ids.append(neo["id"])
    return asteroid_ids


@app.route('/images')
def images():
    return render_template("new_image2.html")


import requests


def filter_photos_by_camera(json_data, camera_name):
    if json_data is not None and 'photos' in json_data:
        filtered_photos = [photo['img_src'] for photo in json_data['photos'] if photo['camera']['name'] == camera_name]
        return filtered_photos
    return None

import random
@app.route('/display_image', methods=['GET'])
def display_image():
    api_url = request.args.get('api_url')
    selected_rover = request.args.get('rover')
    selected_camera = request.args.get('camera')
    earth_date = request.args.get('date')
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # JSON data fetched successfully
            json_data = response.json()
            # print( json_data)
            if json_data is not None and 'photos' in json_data:
                filtered_photos = [photo['img_src'] for photo in json_data['photos'] if photo['camera']['name'] ==selected_camera.upper() ]
                print( filtered_photos)
                print(len(filtered_photos))
                if(len(filtered_photos)==0):
                    return jsonify({"error":" No data found on this specific  date."})
                if(len(filtered_photos)>6):
                    filtered_photos = random.sample(filtered_photos, 6)

        
    except requests.exceptions.RequestException as e:
        # Handle exceptions or return None
        print(f"Error: {e}")

    # Here, you can use the api_url and other parameters to display the image or perform other actions
    # For example, you can render a template to display the image
    
    
    return render_template('new_image2.html', api_url=api_url, rover=selected_rover, camera=selected_camera, date=earth_date,photos=filtered_photos)
@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/neo')
def neo():
    return render_template('NEO.html')


@app.route('/astronomy2')

def astronomy2():
    explanation= request.args.get("explanation")
    title= request.args.get("title")
    image=request.args.get("image")
    date=request.args.get("date")
    print("your title is")
    print(title)
    print(date)
    
    return render_template('astronomy2.html',explanation=explanation,title=title,image=image,date=date)

import random
from datetime import date, timedelta
api_key = 'DEMO_KEY'
def fetch_random_astronomy():
    
    start_date = date(1995, 6, 16)  # NASA APOD API start date
    end_date = date.today()  # Current date
    apod_data_list = []
    def random_date(start_date, end_date):
        delta = end_date - start_date
        random_days = random.randint(0, delta.days)
        return start_date + timedelta(days=random_days)

    for _ in range(5):
        random_date_value = random_date(start_date, end_date)
        random_date_str = random_date_value.strftime('%Y-%m-%d')
        api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={random_date_str}'

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                title = data['title']
                explanation = data['explanation']
                image_url = data.get('hdurl', data.get('url'))
                apod_data_list.append({
                    'Title': title,
                    'Explanation': explanation,
                    'Image_URL': image_url,
                    'Date': random_date_str
                })
            else:
                print(f'Error: Unable to fetch data for date {random_date_str}. Status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
    return apod_data_list


import requests
from random import sample
from datetime import timedelta
from datetime import datetime, timedelta

def with_dates_astronomy(start_date, end_date):
    apod_data_list = []
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()


    # Calculate the total number of days between start_date and end_date
    total_days = (end_date - start_date).days
    print("total_days")
    print(total_days)

    # If there are more than 5 days in the date range, fetch 5 random APOD items
    if total_days > 5:
        apod_data_list = []
        def random_date(start_date, end_date):
            delta = end_date - start_date
            random_days = random.randint(0, delta.days)
            return start_date + timedelta(days=random_days)

        for _ in range(5):
            random_date_value = random_date(start_date, end_date)
            random_date_str = random_date_value.strftime('%Y-%m-%d')
            api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={random_date_str}'

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    title = data['title']
                    explanation = data['explanation']
                    image_url = data.get('hdurl', data.get('url'))
                    apod_data_list.append({
                        'Title': title,
                        'Explanation': explanation,
                        'Image_URL': image_url,
                        'Date': random_date_str
                    })
                else:
                    print(f'Error: Unable to fetch data for date {random_date_str}. Status code: {response.status_code}')
            except requests.exceptions.RequestException as e:
                print(f'Error: {e}')
        


    # If there are fewer than 5 elements, fetch data for all available dates
    if total_days <= 5:
        for date in range(start_date, end_date + timedelta(days=1)):
            start_date_str = date.strftime('%Y-%m-%d')
            api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={start_date_str}'
            
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    data = response.json()
                    title = data['title']
                    explanation = data['explanation']
                    image_url = data.get('hdurl', data.get('url'))
                    apod_data_list.append({
                        'Title': title,
                        'Explanation': explanation,
                        'Image_URL': image_url,
                        'Date': start_date_str
                    })
                else:
                    print(f'Error: Unable to fetch data. Status code: {response.status_code}')
            except requests.exceptions.RequestException as e:
                print(f'Error: {e}')
    print("APOD")
    for apod in apod_data_list:
        print("list includes")
        print(apod['Title'])

    return apod_data_list

import json

@app.route('/astronomy',methods=['GET', 'POST'])
def astronomy():
    
    if request.method=="POST":
        print("why")
        start_date= request.form.get('start_date')
        end_date= request.form.get('end_date')
        print("hello")
        print(start_date)
        with_dates_data=with_dates_astronomy(start_date,end_date)
        print("helloguys")
        # for apod in with_dates_data:
        #     print(apod['Date'])
        with_dates_data_json = json.dumps(with_dates_data)
        return redirect(url_for('pagination',with_dates_data_json=with_dates_data_json))
    else:
        print("hey")
    api_key = 'KUpVblrfxDR4h5wOwEE9GUOQ32NkaaTKN5JFrJxn'

    # NASA APOD API URL
    api_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'

    try:
        # Send a GET request to the API
        response = requests.get(api_url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            print(data)
            # Extract the relevant data
            title = data['title']
            image_url = data.get('hdurl', data.get('url'))
            print("image url")
            print(image_url)
            explanation = data['explanation']
            date = data['date']

            # Print the data
            print(f'Title: {title}')
            print(f'Image_URL: {image_url}')
            
            print(f'Date: {date}')
        else:
            print(f'Error: Unable to fetch data. Status code: {response.status_code}')

    except requests.exceptions.RequestException as e:

        print(f'Error: {e}')


    apod_data_list=fetch_random_astronomy()
    # print(apod_data_list)
    



    return render_template('astronomy.html',title=title,image1_url=image_url,explanation=explanation,date=date,apod_data_list=apod_data_list)

@app.route('/pagination')
def pagination():
    with_dates_data_json = request.args.get('with_dates_data_json')
    with_dates_data = json.loads(with_dates_data_json)
    for apod in with_dates_data:
        print("Titles are")
        print(apod['Title'])
   
    return render_template('pagination.html',with_dates_data=with_dates_data)
if __name__ == '__main__':
    app.run(debug=True)

