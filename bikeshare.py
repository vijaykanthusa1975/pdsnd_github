import time
import statistics
import pandas as pd
import numpy as np
import os
import sys 

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }

listOfMonths = ['all','january','february','march','april','may','june']
listOfDays = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Enter input for city (chicago, nyc, washington): "))

        if city.lower() not in CITY_DATA.keys():
            restart1 = str(input('\nInvalid Input. Please enter (chicago or nyc or washington). Do you want to try again? Y or N\n'))
            if restart1.lower() == 'y':
                continue
            else:
                print('\nExiting Program\n')
                sys.exit()
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month= str(input("Enter  input for month (all, January, February, March, April, May, June) "))
        
        if month.lower() not in listOfMonths:
            restart2 = str(input('\nInvalid Input. Please enter (all, January, February, March, April, May, June). Do you want to try again? Y or N\n'))
            if restart2.lower() == 'y':
                continue
            else:
                print('\nExiting Program\n')
                sys.exit()
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day= str(input("Enter input for day of week (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday) "))
         
        if day.lower() not in listOfDays:
            restart3 = str(input('\nInvalid Input. Please enter (all, monday, tuesday, wednesday, thursday, friday, saturday, sunday). Do you want to try again? Y or N\n'))
            if restart3.lower() == 'y':
                continue
            else:
                print('\nExiting Program\n')
                sys.exit()
        else:
            break

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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month.lower() != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day.lower() != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 	

    # display the most common month
    print('Most common month: ', df['Start Time'].dt.month.mode()[0])
    	
    # display the most common day of week
    print('Most common day of week: ', df['Start Time'].dt.weekday_name.mode()[0])

    # display the most common start hour
    print('Most common hour: ', df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n ", df['User Type'].value_counts())
    
    if city.lower()!='washington':
        # Display counts of gender
        print("Counts of gender: \n ", df['Gender'].value_counts())
        # Display earliest, most recent, and most common year of birth
        print("Earliest, most recent, and most common year of birth: \n", int(df['Birth Year'].min()), int(df['Birth Year'].max()),int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display Travel time statistics
    print("Trip duration statistics:\n ",df['Trip Duration'].describe())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station: ", df['Start Station'].mode()[0])

    
    # display most commonly used end station
    print("Most commonly used end station: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    print("Most frequent combination of start station and end station trip: \n", df.groupby(['Start Station','End Station']).size().nlargest(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    #Counter for row slicing 
    cnt=0
    print("Length of data frame: ", len(df.index))
    df.to_csv("file_name1", sep='\t')

    while True and df.empty==False:
        usr_input = input('\nWould you like to iteratively see 5 lines of raw data? Enter "Y" to Continue or "N" to view Statistics Computations \n')
        if usr_input.lower() == 'yes' or usr_input.lower() == 'y':
            print("\n Data Frame \n",df[cnt:cnt+5])
            if cnt<=len(df.index):
                cnt+=5
                continue                    
            else:
                break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        print("You've entered " + city, month, day)
        df = load_data(city.lower(), month.lower(), day.lower())

        raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() == 'yes' or restart.lower() == 'y':
            continue
        else:
            print('\nExiting Program\n')
            break

if __name__ == "__main__":
	main()