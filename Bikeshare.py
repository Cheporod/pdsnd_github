############################
# BikeShare Python Project #
############################

import tkinter as tk
from tkinter import ttk 
import time
import pandas as pd
import numpy as np
import os


# I used the absolute path for the csv files provided.
CITY_DATA = { 'chicago': '/Users/josen/Documents/VS Code/CDAO_Bootcamp/Python lessons/Final Project/bikeshare_final/chicago.csv',
              'new york city': '/Users/josen/Documents/VS Code/CDAO_Bootcamp/Python lessons/Final Project/bikeshare_final/new_york_city.csv',
              'washington': '/Users/josen/Documents/VS Code/CDAO_Bootcamp/Python lessons/Final Project/bikeshare_final/washington.csv' }

def on_button_click():
    var.set(1)
    tasks()

def destroy_window(): #Close window
    global running
    window.destroy()
    running = False  
    
######## User Input Interface Window ###########################
def create_gui():
    global window
    global city_entry
    global month_entry
    global day_entry
    global var
    
    window = tk.Tk() 

    frame = tk.Frame(window)
    frame.pack()
    
    window.configure(bg='Gray')
    window.title("Bike Share Data Query Tool")

    def city():
        cities = "Chicago, New York City, Washington, chicago, new york city, washington"
        input = city_entry.get()
        
        if len(input) == 0:
            status1.configure(text = "Still Waiting")
        
        elif input in cities:
            status1.configure(text = "Input Correct!")
        
        else:
            status1.configure(text = "Input Incorrect")

    def month():
        months = "All, all, January, February, March, April, May, June, january, february, march, april, may, june"
        input = month_entry.get()
    
        if len(input) == 0:
            status2.configure(text = "Still Waiting")
        
        elif input in months:
            status2.configure(text = "Input Correct!")
        
        else:
            status2.configure(text = "Input Incorrect")

    def day():
        days = "All, all, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, monday, tuesday, wednesday, thursday, friday, saturday, sunday"
        input = day_entry.get()
        
        if len(input) == 0:
            status3.configure(text = "Still Waiting")
        
        elif input in days:
            status3.configure(text = "Input Correct!")
        
        else:
            status3.configure(text = "Input Incorrect")
    
      
    ############ Title Grid ##############
    title_frame = tk.LabelFrame(frame)
    title_frame.grid(row=0, column=0, padx=10, pady=10)

    title_label = tk.Label(title_frame,text="Welcome!\n To Bike Share Data Exploration v1.0",
        font=('Time New Roman', 24),
        fg='#9c390e',
        bg='black',
        bd=10,
        padx=10,
        pady=10)
    title_label.pack()

    ####### User input grid ###############
    user_info_frame =tk.LabelFrame(frame, text="Entry Form",font=('Time New Roman', 16))
    user_info_frame.grid(row=1, column=0, pady=5)

    city_label = tk.Label(user_info_frame, text="Step 1: Please choose from the following cities\n1. Chicago 2. New York City 3. Washington",
        font=('Time New Roman', 14),
        fg='#9c390e',
        bd=10,
        padx=10,
        pady=10)
    city_label.grid(row=0, column=0)

    city_entry = tk.Entry(user_info_frame, font=('Time New Roman', 14))
    city_entry.grid(row=1, column=0)

    vali_1 = tk.Button(user_info_frame, text = "Validate", command=city)
    vali_1.grid(row=2, column=0)

    status1 = tk.Label(user_info_frame,text="...Waiting for input")
    status1.grid(row=3, column=0)

    month_label = tk.Label(user_info_frame, text="Step 2: Please Select a Month\nBetween January to June; or All",
        font=('Time New Roman', 14),
        fg='#9c390e',
        bd=10,
        padx=10,
        pady=10)
    month_label.grid(row=0, column=1)

    month_entry = tk.Entry(user_info_frame, font=('Time New Roman', 14))
    month_entry.grid(row=1, column=1)

    vali_2 = tk.Button(user_info_frame, text = "Validate", command=month)
    vali_2.grid(row=2, column=1)

    status2 = tk.Label(user_info_frame,text="...Waiting for input")
    status2.grid(row=3, column=1)

    day_label = tk.Label(user_info_frame, text="Step 3: Please Select a day of the week; or All",
        font=('Time New Roman', 14),
        fg='#9c390e',
        bd=10,
        padx=10,
        pady=10)
    day_label.grid(row=0, column=2)

    day_entry = tk.Entry(user_info_frame, font=('Time New Roman', 14))
    day_entry.grid(row=1, column=2)

    vali_3 = tk.Button(user_info_frame, text = "Validate", command=day)
    vali_3.grid(row=2, column=2)

    status3 = tk.Label(user_info_frame,text="...Waiting for input")
    status3.grid(row=3, column=2)

    for widget in user_info_frame.winfo_children():
        widget.grid_configure(padx=10, pady=5)

    ############ Run Program Grid ##############
    progr_frame = tk.LabelFrame(frame)
    progr_frame.grid(row=3, column=0, padx=5, pady=5)

    var = tk.IntVar() 
     
    button = tk.Button(progr_frame, text="Run Program",
                font=('Time New roman', 18), 
                fg="#090952",
                command=tasks)
    button.pack()

    ############ Banner Grid ##############
    banner_frame = tk.LabelFrame(frame)
    banner_frame.grid(row=4, column=0, padx=10, pady=10)

    banner_label = tk.Label(banner_frame, text="See results and answer other questions in the windows terminal", font=('Time New roman', 14), 
                    fg="#090952")
    banner_label.pack()

    return window

############Run main tasks--> Program flow control######################
def tasks():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        
        if restart.lower() == 'yes':
            print("Please return to Entry Form--> Provide input and run program again")
            window.wait_variable(var)
        
        if restart.lower() != 'yes':
            destroy_window()
            break

################User Input###############################
# Asks user to specify a city, month, and day to analyze.
# I implemented a validation button on the App GUI for users to check their entry prior to run program.
def get_filters():
    city = ''
    
    while city not in CITY_DATA.keys():
        print("\nWelcome to this program.")
        city = city_entry.get().lower()

    if city not in CITY_DATA.keys(): 
        print("\nPlease check your input .")
        print("\nRestarting...")

    print(f"\nYou have chosen {city.title()} as your city.")
    
# Get user input for month or all 
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nThank you for shoosing a month between January and June.")
        print("\nYou could also opt to view data for all months.")
        month = month_entry.get().lower()

    if month not in MONTH_DATA.keys(): #(No using the tkinter GUI this will display in the console)
        print("\nInvalid input. Please try again.")
        print("\nRestarting...")

    print(f"\nYou have chosen {month.title()} as your month.")

# get user input for day of week or all 
    DAY_LIST = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = ''
    while day not in DAY_LIST:
        print("\nThank you for shoosing a weekday.")
        day = day_entry.get().lower()

    if day not in DAY_LIST: #(No using the tkinter GUI this will display in the console)
        print("\nInvalid input. Please try again.")
        print("\nRestarting...")

    print(f"\nYou have chosen {day.title()} as your day.")
    print(f"\nYou have chosen to view data for the following --> City: {city.title()}, Month: {month.title()}, Day: {day.title()}")
    print('-'*40)

    return city, month, day

################################################################

def load_data(city, month, day):
#Load data for city
    print("\nLoading data...")
    df = pd.read_csv(CITY_DATA[city])

#Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

#Extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

#Filter by month if applicable
    if month != 'all':
        #Use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        #Filter by month to create the new dataframe
        df = df[df['month'] == month]

#Filter by day of week if applicable
    if day != 'all':
        #Filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

#Returns the selected file with relevant information
    return df

###########################POPULAR TIME OF TRAVEL#######################################
def time_stats(df):
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

 # display the most common month
    popular_month = df['month'].mode()[0]

    print(f"Most Popular Month (1 = Jan,2 = Feb,3 = Mar,4 = Apr,5= May,6 = Jun): {popular_month}")

# display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print(f"\nMost Popular Day: {popular_day}")

# display the most common start hour. first,extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    
    print(f"\nMost Popular Start Hour: {popular_hour}")

#Prints the time taken to perform the calculation    
    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

#################POPULAR STATION AND TRIP###############################################
def station_stats(df):
    
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

# display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]

    print(f"The most commonly used start station: {common_start_station}")

# display most commonly used end station
    common_end_station = df['End Station'].mode()[0]

    print(f"\nThe most commonly used end station: {common_end_station}")

# display most frequent combination of start station and end station trip
    df['Start To End'] = df['Start Station'].str.cat(df['End Station'], sep=' to ')
    combo = df['Start To End'].mode()[0]

    print(f"\nThe most frequent combination of trips are from {combo}.")

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

############ TRIP DURATION ##################################################
def trip_duration_stats(df):
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

# display total travel time
    total_duration = df['Trip Duration'].sum()
    
#Finds out the duration in minutes and seconds format
    minute, second = divmod(total_duration, 60)
    
#find the duration in hours and minutes
    hour, minute = divmod(minute, 60)
    print(f"The total trip duration is {hour} hours, {minute} minutes and {second} seconds.")

# display mean travel time
    average_duration = round(df['Trip Duration'].mean())
#Finds the average duration in minutes and seconds format
    mins, sec = divmod(average_duration, 60)
#This filter prints the time in hours, mins, sec format if the mins exceed 60
    if mins > 60:
        hrs, mins = divmod(mins, 60)
        print(f"\nThe average trip duration is {hrs} hours, {mins} minutes and {sec} seconds.")
    else:
        print(f"\nThe average trip duration is {mins} minutes and {sec} seconds.")

    print("\nThis took %.3f seconds." % (time.time() - start_time))
    print('-'*40)

####################BIKE USER INFORMATION#####################################################
def user_stats(df):
 
    print('\nCalculating User Stats...\n')
    start_time = time.time()

# Display counts of user types
    user_type = df['User Type'].value_counts()

    print(f"The types of users by number are given below:\n{user_type}")
   
# Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(f"\nThe types of users by gender are given below:\n{gender}")
    except:
        print("\nThere is no 'Gender' column in this file.")

# Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common_year = int(df['Birth Year'].mode()[0])
        print(f"\nThe earliest year of birth: {earliest}\n\nThe most recent year of birth: {recent}\n\nThe most common year of birth: {common_year}")
    except:
        print("There are no birth year details in this file.")

        print("\nThis took %.3f seconds." % (time.time() - start_time))
        print('-'*40)

######################Ask user if they want to continue viewing data####################################
    rdata = 'yes'
    counter = 0

    while rdata == 'yes':
        print("Do you wish to view more raw data?")
        counter += 5
        rdata = input().lower()
#If user opts for it, this displays next 5 rows of data
        if rdata == "yes":
             print(df[counter:counter+5])
        elif rdata != "yes":
             break

        print('-'*40)


#################Main program Entry###################
def main():
    window = create_gui()
    window.mainloop() # place window on computer screen
    
    
if __name__ == "__main__":
	main()
        
 




