import requests
from datetime import datetime, timedelta
from random import sample

# Define the daterange function
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def with_dates_astronomy(start_date, end_date, api_key):
    base_url = 'https://api.nasa.gov/planetary/apod'
    apod_data_list = []

    # Convert start_date and end_date to datetime.date objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Calculate the total number of days between start_date and end_date
    total_days = (end_date - start_date).days

    # If there are more than 5 days in the date range, fetch 5 random APOD items
    if total_days > 5:
        random_dates = [start_date + timedelta(days=i) for i in sample(range(total_days), 5)]
    else:
        # If there are 5 or fewer days, fetch data for each day within the range
        random_dates = [start_date + timedelta(days=i) for i in range(total_days + 1)]

    for date in random_dates:
        start_date_str = date.strftime('%Y-%m-%d')
        params = {'api_key': api_key, 'date': start_date_str}
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                data = response.json()
                title = data['title']
                explanation = data['explanation']
                image_url = data.get('hdurl', data.get('url'))
                apod_data_list.append({
                    'Title': title,
                    'Explanation': explanation,
                    'Image_URL': image_url,
                })
            else:
                print(f'Error: Unable to fetch data. Status code: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')

    # Fetch data for all available dates
    if total_days <= 5:
        for date in daterange(start_date, end_date):
            start_date_str = date.strftime('%Y-%m-%d')
            params = {'api_key': api_key, 'date': start_date_str}
            try:
                response = requests.get(base_url, params=params)
                if response.status_code == 200:
                    data = response.json()
                    title = data['title']
                    explanation = data['explanation']
                    image_url = data.get('hdurl', data.get('url'))
                    apod_data_list.append({
                        'Title': title,
                        'Explanation': explanation,
                        'Image_URL': image_url,
                    })
                else:
                    print(f'Error: Unable to fetch data. Status code: {response.status_code}')
            except requests.exceptions.RequestException as e:
                print(f'Error: {e}')

    print("APOD")
    print(apod_data_list)

    return apod_data_list

# Example usage
api_key = 'your_api_key_here'
start_date = '2023-10-10'
end_date = '2023-10-15'
with_dates_data = with_dates_astronomy(start_date, end_date, api_key)
