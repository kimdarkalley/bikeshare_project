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
    print("Let's look at some bikeshare data for areas within the US.")
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to explore data about Chicago, New York City, or Washington?\n').lower().strip()
    while city not in ['chicago','new york city','washington']:
        city=input('Sorry, I did not catch that. Try again:\n').lower().strip()

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month_filter = input('Would you like to filter the data by month? Enter yes or no.\n').lower()
        if month_filter == 'yes':
            month = input('Which month? January, February, March, April, May, June?\n').lower()
            break
        elif month_filter == 'no':
            month = 'all'
            break
        else:
            continue

     # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day_filter = input('Would you like to filter by the day of the week? Enter yes or no.\n').lower()
        if day_filter == 'yes':
            day = input('Which day? Please type the full name of the day.\n').lower()
            break
        elif day_filter == 'no':
            day = 'all'
            break
        else:
            continue

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
    df = pd.read_csv (CITY_DATA[city])
    df ['Start Time'] = pd.to_datetime (df['Start Time'])
    df ['month'] = df ['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df= df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df ['month'].value_counts().idxmax()
    print('The most popular month is: ', popular_month)

    # TO DO: display the most common day of week
    popular_day = df ['day_of_week'].value_counts().idxmax()
    print('The most popular day is: ', popular_day)
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df ['hour'].value_counts().idxmax()
    print('The most popular hour is: ', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start = df ['Start Station'].value_counts().idxmax()
    print('The most popular start station is: ', popular_start)
    # TO DO: display most commonly used end station
    popular_end = df ['End Station'].value_counts().idxmax()
    print('The most popular end station is: ', popular_end)
    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df.groupby (['Start Station', 'End Station']).size().nlargest(1)
    print('The most popular route is: ', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel = int(df['Trip Duration'].sum() /60)
    print('The total travel time in minutes is: ', total_travel)
    # TO DO: display mean travel time
    avg_travel = int(df['Trip Duration'].mean() /60)
    print('The total average travel time in minutes is: ',avg_travel)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].value_counts()
    print('The number of each user type is: ', user_type)

    # TO DO: Display counts of gender
    if 'Gender' not in df.columns:
        print('Gender data is not available for this city')
    else:
        gender = df['Gender'].value_counts()
        print('The counts of each gender are: ', gender)

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' not in df.columns:
        print('Birth year data is not available for this city')
    else:
        df.dropna(subset=['Birth Year'])
        early_birthyear = int(df['Birth Year'].min())
        print('The earliest birth year is: ', early_birthyear)
        recent_birthyear = int(df['Birth Year'].max())
        print('The most recent birth year is: ', recent_birthyear)
        common_birthyear = int(df['Birth Year'].mode()[0])
        print('The most common year of birth is: ', common_birthyear)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    # Displays raw data with option for more lines
    view_data = input('Would you like to view 5 rows of raw individual trip data? Please enter yes or no.\n').lower().strip()
    st = 0
    while view_data =='yes':
        print(df.iloc[st:st+5])
        st +=5
        view_data = input('Would you like to view 5 more rows? Please type yes or no.\n').lower().strip()
    else:
        print('-'*40)

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
