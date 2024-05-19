import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Define valid inputs!

    cities = ['chicago', 'new york city', 'washington']
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    # get user input for city (chicago, new york city, washington).  

    while True:
        city = input("Which city would you like to analyze? (Chicago, New York City, Washington): ").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid input. Please enter a valid city name from the list provided.")


    # get user input for month (all, january, february, ... , june)

    while True:
        month = input("Which month? January, February, March, April, May, June, or type 'all' to not apply a month filter: ").lower()
        if month in months:
            break 
        else:
            print("Invalid input. Please enter a valid month name from the provided list or 'all'.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
            
    while True:
        day = input("Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or type 'all' to not apply a day filter:").lower()
        if day in days:
            break
        else:
            print("Invalid input. Please enter a valid day name from the provided list or 'all'.")


    print('-'*40)
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
    # Load data file into dataframe

    df = pd.read_csv(CITY_DATA[city])

    # Convert the start time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable

    if month != 'all':
        month = df['Start Time'].dt.month_name().str.lower() == month
        df = df[month] 

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].mode()[0]
    print("Most Common Month:", common_month)


    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print("Most Common Day Of The Week:", common_day)


    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print("Most Common Start Hour:", common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Commonly Used Start Station: {common_start_station}")


    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Commonly Used End Station: {common_end_station}")


    # display most frequent combination of start station and end station trip
    df['Start-End Station Combination'] = df['Start Station'] + " to " + df['End Station']
    common_station_combination = df['Start-End Station Combination'].mode()[0]
    print(f"Most Frequent Combination of Start and End Station Trip: {common_station_combination}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()

    # Convert from seconds to hours to make more readable

    total_travel_time_hours = total_travel_time / 3600
    print(f"Total Travel Time: {total_travel_time} seconds, which is approximately {total_travel_time_hours: .2f} hours.")


    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()

    # Convert from seconds to minutes to make more readable

    mean_travel_time_minutes = mean_travel_time / 60
    print(f"Mean Travel Time: {mean_travel_time} seconds, which is approximately {mean_travel_time_minutes: .2f} minutes.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types_counts = df['User Type'].value_counts()
    print("Counts of User Types:\n", user_types_counts)


    # Display counts of gender

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print("\nCounts of Gender:\n", gender_counts)
    else:
        print("\nGender information is not available for this city.")


    # Display earliest, most recent, and most common year of birth
    
    if 'Birth Year' in df.columns:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print("\nEarliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", most_recent_year)
        print("Most Common Year of Birth:", most_common_year)
    else:
        print("\nBirth Year information is not available for this city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """Displays 5 lines of raw data upon request by the user."""
    i = 0
    while True:
        raw_data = input("\nWould you like to see 5 lines of raw data? Enter yes or no. \n")
        if raw_data.lower() == 'yes':
            print(df.iloc[i:i+5])
            i += 5
        elif raw_data.lower() == 'no':
            break
        else:
            print("Sorry, I didn't understand that. Please type 'yes' or 'no'.")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Display raw data if the user opts to
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()