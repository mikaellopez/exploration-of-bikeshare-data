import time
import pandas as pd

def set_filters():
    error_message = "❌ You either misspelled your choice or didn't enter"
    while True:
        city = input("Do you want to see bikeshare data for "
                     "Chicago, New York, or Washington? ").title()
        if city in CITY_DATA:
            break
        else:
            print(f"{error_message} one of the three cities available to choose from. ❌")
    filter_data = input("Do you want to filter the data? (y/n) ").lower()
    month = "all"
    day = "all"
    if filter_data != "n":
        filter_type = input("Do you want to filter the data by "
                            "m\u0332onth, d\u0332ay, or b\u0332oth? (m/d/b) ").lower()
        if filter_type == "m" or filter_type == "b":
            print("(You can only filter by the first six months of the year, i.e., "
                  f"{', '.join(months)})")
            while True:
                filter_month = input("Which month do you want to filter by? ").capitalize()
                if filter_month in months:
                    month = months.index(filter_month) + 1
                    break
                else:
                    print(f"{error_message} one of the six months available to choose from. ❌")
        if filter_type == "d" or filter_type == "b":
            while True:
                day = input("Which day of the week do you want to filter by? ").capitalize()
                if day in days:
                    break
                else:
                    print(f"{error_message} a day of the week. ❌")
    m, d = "", ""
    if month != "all":
        m = f", in {months[month - 1]}"
    if day != "all":
        d = f", on {day}s"
    print(f"\nYou've selected bikeshare data for {city}{m}{d}.")
    cont_restart = input("Do you want to c\u0332ontinue or do you want to r\u0332estart? (c/r) ")
    if cont_restart != "c":
        print("⟲")
        set_filters()
    else:
        print("\n" + "-" * 58 + "\n")
    return city, month, day

def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name() #.dt.weekday_name for older versions of Pandas
    df["hour"] = df["Start Time"].dt.hour
    if month != "all":
        df = df[df["month"] == month]
    if day != "all":
        df = df[df["day_of_week"] == day]
    return df

def time_stats(df):
    """Displays what month, day, and hour people bikeshare most frequently."""
    print("⏳ Calculating when people bikeshare most frequently...\n")
    start_time = time.time()
    month, day = "", ""
    if len(df["month"].unique()) != 1:
        month = f"in {months[df['month'].mode()[0] - 1]}, "
    if len(df["day_of_week"].unique()) != 1:
        day = f"on {df['day_of_week'].mode()[0]}s, "
    hour = df["hour"].mode()[0]
    if hour < 12:
        hour = f"at {df['hour'].mode()[0]} am"
    else:
        hour = f"at {df['hour'].mode()[0] - 12} pm"
    print(f"People bikeshare most frequently {month}{day}{hour}.\n")
    print(f"⌛ The calculation took {time.time() - start_time} seconds.\n")
    input("Press Enter to see more statistics.")
    print("\n" + "-" * 68 + "\n")

def station_stats(df):
    print("⏳ Calculating which stations and which trip are most popular...\n")
    start_time = time.time()
    popular_start = df["Start Station"].mode()[0]
    popular_end = df["End Station"].mode()[0]
    print(f"The most popular station to start from is {popular_start}.")
    print(f"The most popular station to end a trip at is {popular_end}.")
    df["Trip"] = df["Start Station"] + " to " + df["End Station"]
    popular_trip = df["Trip"].mode()[0]
    print(f"The most popular trip is from {popular_trip}.\n")
    print(f"⌛ The calculations took {time.time() - start_time} seconds.\n")
    input("Press Enter to see the more statistics.")
    print("\n" + "-" * 53 + "\n")

def trip_duration_stats(df):
    print("⏳ Calculating trip duration statistics...\n")
    start_time = time.time()
    travel_time_total = df["Trip Duration"].sum()
    hours = f"{int(travel_time_total // 3600)} hours"
    minutes = f"{int((travel_time_total % 3600) // 60)} minutes"
    seconds = f"{int(travel_time_total % 60)} seconds"
    print(f"The total travel time is {hours}, {minutes}, {seconds}.")
    travel_time_mean = df["Trip Duration"].mean()
    minutes = f"{int(travel_time_mean // 60)} minutes"
    seconds = f", {int(travel_time_mean % 60)} seconds"
    print(f"The average travel time is {minutes}{seconds}.\n")
    print(f"⌛ The calculations took {time.time() - start_time} seconds.\n")
    input("Press Enter to see more statistics.")
    print("\n" + "-" * 53 + "\n")

def user_stats(df):
    print("⏳ Calculating user statistics...\n")
    start_time = time.time()
    print(f"{'User Type':<14}{'Amount'}\n")
    user_types = df["User Type"].value_counts()
    for index, value in user_types.items():
        print(f"{index:<14}{value}")
    print(f"\n⌛ The calculation took {time.time() - start_time} seconds.\n")
    if "Gender" in df.columns:
        input("Press Enter to see more statistics.")
        print()
        start_time = time.time()
        print(f"{'Gender':<14}{'Amount'}\n")
        genders = df["Gender"].value_counts()
        for index, value in genders.items():
            print(f"{index:<14}{value}")
        print(f"\n⌛ The calculation took {time.time() - start_time} seconds.\n")
    if "Birth Year" in df.columns:
        input("Press Enter to see more statistics.")
        print()
        start_time = time.time()
        birth_year_earliest = int(min(df["Birth Year"]))
        birth_year_latest = int(max(df["Birth Year"]))
        birth_year_mode = int(df["Birth Year"].mode()[0])
        print(f"The oldest user was born in {birth_year_earliest}.")
        print(f"The youngest user was born in {birth_year_latest}.")
        print(f"The most common year of birth among users is {birth_year_mode}.")
        print(f"\n⌛ The calculation took {time.time() - start_time} seconds.\n")
    input("Press Enter to continue.")
    print("\n" + "-" * 53 + "\n")

def display_data(df):
    view_data = input("Would you like to view five rows of individual trip data? (y/n) ").lower()
    if view_data == "y":
        start_loc = 0
        while start_loc < len(df):
            for i in range (start_loc, start_loc + 5):
                print()
                print(f"{'#':<18}{df['Unnamed: 0'][i]}")
                print(f"{'User Type':<18}{df['User Type'][i]}")
                if "Gender" in df.columns:
                    print(f"{'Gender':<18}{df['Gender'][i]}")
                if "Birth Year" in df.columns:
                    if df['Birth Year'][i] > 0:
                        print(f"{'Birth Year':<18}{int(df['Birth Year'][i])}")
                    else:
                        print(f"{'Birth Year':<18}{df['Birth Year'][i]}")
                print(f"{'Start Station':<18}{df['Start Station'][i]}")
                print(f"{'Start Time':<18}{df['Start Time'][i]}")
                print(f"{'End Station':<18}{df['End Station'][i]}")
                print(f"{'End Time':<18}{df['End Time'][i]}")
                print(f"{'Trip Duration':<18}{df['Trip Duration'][i]} seconds")
            start_loc += 5
            cont = input("\nDo you want to see five more rows of data? (y/n) ").lower()
            if cont == "n":
                print()
                break

def main():
    print("🚲 🚲 🚲 BIKESHARE STATISTICS FOR THREE US CITIES 🚲 🚲 🚲\n")
    while True:
        print("Let's explore some bikeshare data!\n")
        city, month, day = set_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input("Would you like to restart and explore more bikeshare data? (y/n) ").lower()
        if restart == "n":
            break
        print("⟲")

CITY_DATA = {"Chicago": "chicago.csv",
             "New York": "new_york_city.csv",
             "Washington": "washington.csv"}
months = ["January", "February", "March", "April", "May", "June"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
if __name__ == "__main__":
    main()
