import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def validate_input(message, valid_inputs, list_input=False):
    """
    Validate user input for both single entry and multiple entries
    Return single entry as a string and mutliple entries as a list
    """
    while True:
        user_input = input(message)
        if list_input:
            user_input = [x.lower().strip() for x in user_input.split(',')]
            if len([x for x in user_input if x not in valid_inputs])==0:
                break
        else:
            if user_input.lower() in valid_inputs:
                break
        
    return user_input
        

def get_filters():
    """
    Use validate_input function to ask user to specify a city, month(s), and day(s) to analyze.

    Returns:
        (str) city - name of the city to analyze
        (list) month - name(s) of the month(s) to filter by, or "all" to apply no month filter
        (list) day - name(s) of the day(s) of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    message = "Please choose one of the cities of Chicago, New York and Washington:\n"
    valid_inputs = ['chicago', 'new york', 'washington']
    city = validate_input(message, valid_inputs)

    # TO DO: get user input for month (all, january, february, ... , june)
    message = "Please enter 'all' or enter month(s) from 'january' to 'june' (Use ',' to seperate months):\n"
    valid_inputs = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    month = validate_input(message, valid_inputs, list_input=True)
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    message = "Please enter 'all' or weekday(s) such as 'monday' and 'tuesday' (Use ',' to seperate days):\n"
    valid_inputs = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = validate_input(message, valid_inputs, list_input=True)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    pd.read_csv(city)

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city.title()])

    # all column names having the first letter of each work capitalized 
    df.rename(str.title, axis=1)
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month(s) if applicable
    if 'all' not in month:
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month_nums=[]
        for m in month:
            month_nums.append(months.index(m)+1) 
    
        # filter by month(s) to create the new dataframe
        df = df[df['month'].isin(month_nums)]

    # filter by day of week if applicable
    if 'all' not in day:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'].str.lower().isin(day)]
    
    return df


def show_data(df):
    """
    After filtering the data, prompt user if to display 5 lines of raw data each time,
    show the data if the answer is 'yes'; continue the prompt until the user says no.

    Args:
        (DataFrame) df - the filtered dataset available for user to view and explore
    Return:
        Null
    """
    # reset df index to start from 0
    df = df.reset_index()

    # use generator to get indices which are multiple of 5 and 
    # stops at the total number of df rows
    index_gen = (x for x in range(0, df.shape[0], 5))

    while True:
        try:
            i = next(index_gen)
            show = input("Enter 'yes' to show 5 (more) lines of data, 'no' to continue to summary statistics:\n")
            if show != 'yes':
                break
            print(df[i:i+5])
        except StopIteration:
            break
        

def check_col(df, col_name):
    if col_name in df.columns:
        return True
    else:
        print("No data on {} for this city. ".format(col_name))
        return False
        

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    if check_col(df, 'Start Time'):
        # TO DO: display the most common month
        print("The most common month is:", df['month'].mode()[0])

        # TO DO: display the most common day of week
        print("The most common day of week is:", df['day_of_week'].mode()[0])

        # TO DO: display the most common start hour
        print("The most common start hour is:", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    if check_col(df, 'Start Station'):
        # TO DO: display most commonly used start station
        print("The most commonly used start station:", df['Start Station'].mode()[0])

    if check_col(df, 'End Station'):
        # TO DO: display most commonly used end station
        print("The most commonly used end station:", df['End Station'].mode()[0])

    # TO DO: display most frequent combination of start station and end station trip
    if check_col(df, 'Start Station') and check_col(df, 'End Station') :
        print("The most frequent combination of start station and end station trip:", 
            (df['Start Station']+' | '+df['End Station']).mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    if check_col(df, 'Trip Duration'):
        # TO DO: display total travel time
        print("Total travel time: ", df['Trip Duration'].sum())

        # TO DO: display mean travel time
        print("The average travel time: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if check_col(df, 'User Type'): 
        print(pd.DataFrame(df['User Type'].value_counts()),'\n')

    # TO DO: Display counts of gender
    if check_col(df, 'Gender'):
        print(pd.DataFrame(df['Gender'].value_counts()), '\n')

    # TO DO: Display earliest, most recent, and most common year of birth
    if check_col(df, 'Birth Year'):
        print("The birth year of the oldest user is: ", df['Birth Year'].min())
        print("The birth year of the youngest user is: ", df['Birth Year'].max())
        print("The most common birth year of users is: ", df['Birth Year'].mode()[0])
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        print(df.info(),'\n')
        show_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
