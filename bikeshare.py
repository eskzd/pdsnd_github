import pandas as pd
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

# dictionary with available months
MONTH_DATA = {'0': 'all',
              '1': 'january',
              '2': 'february',
              '3': 'march',
              '4': 'april',
              '5': 'may',
              '6': 'june'}

# dictionary with available days
DAYS_DATA = {'0': 'all',
             '1': 'monday',
             '2': 'tuesday',
             '3': 'wednesday',
             '4': 'thursday',
             '5': 'friday',
             '6': 'saturday',
             '7': 'sunday'}

welcome_message = '''
                                           $"   *.
               d$$$$$$$P"                  $    J
                   ^$.                     4r  "
                   d"b                    .db
                  P   $                  e" $
         ..ec.. ."     *.              zP   $.zec..
     .^        3*b.     *.           .P" .@"4F      "4
   ."         d"  ^b.    *c        .$"  d"   $         %
  /          P      $.    "c      d"   @     3r         3
 4        .eE........$r===e$$$$eeP    J       *..        b
 $       $$$$$       $   4$$$$$$$     F       d$$$.      4
 $       $$$$$       $   4$$$$$$$     L       *$$$"      4
 4         "      ""3P ===$$$$$$"     3                  P
  *                 $       """        b                J
   ".             .P                    %.             @
     %.         z*"                      ^%.        .r"
        "*==*""                             ^"*==*""   Gilo94'

'''
# This ASCII pic can be found at
# https://asciiart.website/index.php?art=transportation/bicycles

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print(welcome_message)
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n').lower()
        try:
            CITY_DATA[city]
            break
        except KeyError:
            print('Invalid input. Please enter the city name again (e.g., Chicago, New York City, Washington)')

    # get user input for month (all, january, february, ... , june)
    print('DATA FILTER SETTINGS')
    while True:
        print('Type number to select filter by month:')
        month = input('0 - no filter\n1 - January\n2 - February\n3 - March\n4 - April\n5 - May\n6 - June\n').lower()
        try:
            month = MONTH_DATA[month]
            break
        except KeyError:
            print('Invalid input. Input should be one digit only, from 0 to 6.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        print('Type number to select filter by day:')
        day = input('0 - no filter\n1 - Monday\n2 - Tuesday\n3 - Wednesday\n4 - Thuesday\n5 - Friday\n6 - Saturday\n7 - Sunday\n').lower()
        try:
            day = DAYS_DATA[day]
            break
        except KeyError:
            print('Invalid input. Input should be one digit only, from 0 to 7.')

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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day of Week'] = df['Start Time'].dt.day_name()
    # Practice Solution #3: Loading and Filtering Data has an error on line 27 AttributeError:
    #                               'DatetimeProperties' object has no attribute 'weekday_name'
    # "dt.weekday_name" changed to "day_name()" because of new syntax in pandas version > 0.22
    # https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.day_name.html
    # https://stackoverflow.com/questions/60339049/weekday-name-from-a-pandas-dataframe-date-object

    # extract hour from Start Time to create new column
    df['Hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: {} (count:{})'.
          format(df['Month'].mode()[0], len(df[df['Month'] == df['Month'].mode()[0]])))

    # display the most common day of week
    print('The most common day of week is: {} (count:{})'.
          format(df['Day of Week'].mode()[0], len(df[df['Day of Week'] == df['Day of Week'].mode()[0]])))

    # display the most common start hour
    print('The most common start hour is: {} (count:{})'.
          format(df['Hour'].mode()[0], len(df[df['Hour'] == df['Hour'].mode()[0]])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station is: {} (count:{})'.
          format(df['Start Station'].mode()[0], len(df[df['Start Station'] == df['Start Station'].mode()[0]])))

    # display most commonly used end station
    print('The most commonly used end station is: {} (count:{})'.
          format(df['End Station'].mode()[0], len(df[df['End Station'] == df['End Station'].mode()[0]])))

    # display most frequent combination of start station and end station trip
    print('The most frequent combination of start station and end station trip is:')
    print(' '*4, (df['Start Station'] + ' -> ' + df['End Station']).mode()[0], '(count: {})'.
          format(len(df[df['Start Station'] == df['Start Station'].mode()[0]])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is: {} years ({} minutes)'.
          format(round(df['Trip Duration'].sum() / 525600, 1), df['Trip Duration'].sum()))

    # display mean travel time
    print('Mean travel time is: {} hours ({} minutes)'.
          format(round(df['Trip Duration'].mean() / 60, 1), round(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Counts of user types:\n{}'.format(df['User Type'].value_counts().to_string(header=False)))

    # Display counts of gender
    print('\nCounts of gender:\n{}'.format(df['Gender'].value_counts().to_string(header=False)))

    # Display earliest, most recent, and most common year of birth
    print('\nYear of birth:')
    print('-earliest: {}'.format(int(df['Birth Year'].min())))
    print('-most recent: {}'.format(int(df['Birth Year'].max())))
    print('-most common: {}'.format(int(df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def cycling_benefits(df):
    """This function calculates how much money users have potentially saved on gas,
    based on Trip Duration and statistics found on the internet.

    Let's assume that average fuel consumption per vehicle is 25.7 miles per gallon
        (https://www.energy.gov/eere/vehicles/articles/fotw-1177-march-15-2021-preliminary-data-show-average-fuel-economy-new-light)
    "On average, Americans drive 29.2 miles per day"
        (https://newsroom.aaa.com/2015/04/new-study-reveals-much-motorists-drive)
    So this gives us average fuel consumption 29.2 / 25.7 = 1.13 gallons per day (1440 minutes)
    Average fuel price as of 02-07-2023 is 3.53$
        (https://gasprices.aaa.com/state-gas-price-averages/)
    Now we can calculate potentially saved money per one minute
    3.53 * 1.13 / 1440 = 0.0027$
    """

    print('\nCalculating Cycling Benefits...\n')
    start_time = time.time()

    avg_consumption = 25.7
    avg_drive = 29.2
    avg_consumption_per_day = avg_drive / avg_consumption
    fuel_price = 3.53
    money_per_minute = fuel_price * avg_consumption_per_day / 1440

    # same data as in trip_duration_stats function plus fuel consumption calculations:
    # total
    print('Potentially gas money saved by users:')
    print('-total: {}$ ({}$ x {} minutes)'.
          format(round(money_per_minute * df['Trip Duration'].sum(), 2), money_per_minute, df['Trip Duration'].sum()))

    # mean
    print('-mean: {}$ ({}$ x {} minutes)'.
          format(round(money_per_minute * df['Trip Duration'].mean(), 2), money_per_minute, round(df['Trip Duration'].mean())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city != 'washington':  # washington.csv has no "Gender" and "Birth Year" columns
            user_stats(df)
        cycling_benefits(df)

        print('PRINTING RAW DATA')
        i = 1
        while True:
            print(df.iloc[i:i + 5])
            i += 5
            more_data = input('\nWould you like to see 5 more rows? Enter yes or no.\n')
            if more_data.lower() != 'yes':
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
