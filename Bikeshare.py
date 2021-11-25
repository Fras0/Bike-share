import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cities = ["chicago","new york","washington"]
    city = input("Would you like to see data for Chicago, new york, or Washington?\n")
    
    while (city not in cities):
        city = input("Please enter a valid city : ")
        
    

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = input("Which month?Enter (all) if dont want filter by month  : ")
    
    while ((month.lower() not in months) and (month.lower()!="all")):
        month = input("Please enter valid month : ")
    


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['sunday','monday','tuesday','wednesday', 'thursday','friday','saturday']
    day = input("Which day?Enter (all) if dont want filter by day  : ")
    while((day.lower() not in days) and (day.lower() != "all")):
        day = input("Please enter a valid day : ")

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
    
        # dealing with null values 
     
    df["User Type"] = df["User Type"].fillna(value = "Customer")
        
    if (city.lower()!= "washington"):
        df["Gender"] = df["Gender"].fillna(value = "Unknown")
        df["Birth Year"] = df["Birth Year"].fillna(value = int(df["Birth Year"].mean()))
        
        


    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df["month"].mode()[0]
    print("The most common month is : "+ str(popular_month))


    # TO DO: display the most common day of week
    popular_day = df["day_of_week"].mode()[0]
    print("The most common day is : "+ str(popular_day))

    # TO DO: display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    popular_hour = df["hour"].mode()[0]
    print("The most common hour is : "+ str(popular_hour))
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly start station is "+ str(df["Start Station"].mode()[0]) + " with number of trips of "+str(df["Start Station"].value_counts()[0]))


    # TO DO: display most commonly used end station
    print("The most commonly end station is "+str(df["End Station"].mode()[0]) + " with number of trips of "+str(df["End Station"].value_counts()[0]))


    # TO DO: display most frequent combination of start station and end station trip
    df['Trip'] = df[['Start Station', 'End Station']].apply(lambda x: ' , '.join(x), axis=1)
    print("The most commonly trip is "+str(df["Trip"].mode()[0]) + " with number of trips of "+str(df["Trip"].value_counts()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("The total time traveled is : " + str(df["Trip Duration"].sum()))
    

    # TO DO: display mean travel time
    print("The average time traveled is :" + str(df["Trip Duration"].mean()))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("User Types\n"+str(df["User Type"].value_counts()))


    # TO DO: Display counts of gender
    try:
        
        print("Gender\n"+str(df["Gender"].value_counts()))


    # TO DO: Display earliest, most recent, and most common year of birth
        print("The earlies year of birth is : "+ str(df["Birth Year"].min()))
        print("The most recent year of birth is : "+ str(df["Birth Year"].max()))
        print("The most common year of birth is : "+ str(df["Birth Year"].mode()[0]))
    except:
        print("there is no data for gender or birth date for this country")
            
    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_display = input("Would you like to view 5 rows of individual trip data? Enter y or n?")
        start_loc = 0
        while (view_display =="y" ):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_display = input("Do you wish to continue?(y/n): ").lower()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
