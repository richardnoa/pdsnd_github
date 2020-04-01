import time
import pandas as pd
import numpy as np
from collections import defaultdict

### Static Data for the project ###

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
CITY_NAMES = ["Chicago", "New York City", "Washington"]
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

### functions for the project ###
def display_time(seconds, granularity=5):
    """
    Converts Seconds to granular time.
    Args:
        (int) seconds

    Returns:
        (str) with time 'weeks, days, hours, minutes, seconds'
    """
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Which city do you want to explore: Chicago = 1, New York City = 2, Washington = 3 ?')
    while True:
        try:
            city_input = int(input())
            if 0 < city_input < 4:
                break
            else:
                print('Sorry pleas select one of the three city with number: 1-3!')
        except ValueError:
            print('Sorry pleas select one of the three city with number: 1-3!')
    print('You selected {}'.format(CITY_NAMES[city_input -1]))
    # TO DO: get user input for month (all, january, february, ... , june)
    print('Which month do you want to explore: all, January = 1, February = 2, March = 3, April = 4, May = 5, ... ?')
    while True:
        month_input = input()
        if month_input == "all":
            break
        try:
            month_input = int(month_input)
            if 0 < month_input < 13:
                break
            else:
                print('Sorry pleas select all or one month with number: 1-12!')
        except ValueError:
            print('Sorry pleas select all or one month with number: 1-12!')
    if month_input == "all":
        print('You selected {} months'.format(month_input))
        month_input=13
    else:
        print('You selected {}'.format(MONTHS[month_input -1]))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print('Which day do you want to explore: all, Monday = 1,Tuesday = 2,Wednesday = 3, ... ?')
    while True:
        day_input = input()
        if day_input == "all":
            break
        try:
            day_input = int(day_input)
            if 0 < day_input < 8:
                break
            else:
                print('Sorry pleas select all or one day with number: 1-7!')
        except ValueError:
            print('Sorry pleas select all or one day with number: 1-7!')
    if day_input == "all":
        print('You selected {} days'.format(day_input))
        day_input=8
    else:
        print('You selected {}'.format(DAYS[day_input -1]))

    print('-'*40)
    city, month, day = city_input, month_input, day_input
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    filename = CITY_DATA[CITY_NAMES[city-1].lower()]
    df = pd.read_csv(filename)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    if month < 13:
        df = df.loc[df['Start Time'].dt.month == month]
    if day < 8:
        df = df.loc[df['Start Time'].dt.day == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['Start Time'].dt.month.value_counts().idxmax()
    print("Most common month is {}".format(MONTHS[common_month]))
    # TO DO: display the most common day of week
    common_day = df['Start Time'].dt.weekday.value_counts().idxmax()
    print("Most common day is {}".format(DAYS[common_day-1]))

    # TO DO: display the most common start hour
    common_start_hour = df['Start Time'].dt.hour.value_counts().idxmax()
    print("Most common start hour is {} o'clock".format(common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_max_value_from_df(df,colum):
    stations = df[colum].tolist()
    common_station = {}
    for station in stations:
        if station in common_station.keys():
            common_station[station] += 1
        else:
            common_station[station]=1
    most_common = max(common_station, key=common_station.get)
    return most_common

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # TO DO: display most commonly used start station
    print("The most commonly used start station is: {}".format(show_max_value_from_df(df,'Start Station')))
    # TO DO: display most commonly used end station
    print("The most commonly used end station is: {}".format(show_max_value_from_df(df,'End Station')))
    # TO DO: display most frequent combination of start station and end station trip
    common_combination_stations = {}
    start_stations = df['Start Station'].tolist()
    end_stations = df['End Station'].tolist()
    for i in range(len(start_stations)):
        combination = start_stations[i] + ' to ' + end_stations[i]
        if combination in common_combination_stations:
            common_combination_stations[combination] += 1
        else:
            common_combination_stations[combination] = 1

    most_common_combination = max(common_combination_stations, key=common_combination_stations.get)
    print("The most frequent combination of stations is: {}".format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time is: {}'.format(display_time(total_travel_time)))
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Mean travel time is: {}'.format(display_time(mean_travel_time)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    count_user_typs = pd.DataFrame(df.groupby(['User Type']).agg(['count']))
    print(count_user_typs['Unnamed: 0'])

    # TO DO: Display counts of gender
    count_gender_data = pd.DataFrame(df.groupby(['Gender']).agg(['count']))
    print(count_gender_data['Unnamed: 0'])

    # TO DO: Display earliest, most recent, and most common year of birth
    birth_min = int(df['Birth Year'].max())
    print('Birth of the youngest passenger is: {}'.format(birth_min))
    birth_max = int(df['Birth Year'].min())
    print('Birth of the oldest passenger is: {}'.format(birth_max))
    birth_mean = int(df['Birth Year'].mean())
    print('Most common age of passengers is: {}'.format(birth_mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

### main blog of the project ###

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
