from json import load, dump
from json.decoder import JSONDecodeError
from bokeh.plotting import figure, show, output_file
from datetime import datetime, timedelta
from math import pi
import numpy as np

from utils import getAveragePB

# pb means Personal Best.

#       Below is how i would store the pb's , where the each day have specific times where the user wrote the attempt
# pb = {
#     "May 20, 2024": {
#         "05:07:52": 45,
#         "18:30:02": 50,
#         "23:12:00": 73
#     },
#     "May 21, 2024": {
#         "13:00:04": 41
#     }
# }
#       also when plotting it, take the average attempt of each day and set it the pb of the day


    


def main() :
   
    date : datetime = datetime.now().strftime("%B %d, %Y")

    greeting : str = f"\n\t\t\tWelcome to your PB Tracker.\n\t\t\t\t{date}\n\nType 'exit' or 'q' to exit the program. and Type 'show' to show plot to represent your progress in a graphical way."
    print(greeting)

    Running  : bool = True
    while Running :     # the main loop

        currentdate : datetime = datetime.now().strftime("%B %d, %Y")   # a nicely formated date ( M D, Y)
        currenttime : datetime = datetime.now().strftime("%H:%M:%S")    # a nicely formated time ( H:M:S )
        
        invalidInput : bool = True
        while invalidInput:
            try:
                attempt  : str = input("\nEnter your PB time as seconds\n >>> ")
                
                # if user wants to quit
                if attempt.lower() == "exit" or attempt.lower() == "q":
                    exit()
                
                # if user wants to show the date as a plot
                elif attempt.lower() == "show":
                    showplot     : bool = True
                    invalidInput : bool = False

                else:
                    attempt      : int  = int( attempt )
                    showplot     : bool = False
                    invalidInput : bool = False        # means the input is valid
    
            except ValueError:
                print("\nInvalid input!, you should write your Personal Best time as a seconds")

        isJsonEmpty : bool = False      # the stating value
        try:
            with open("PB.json", "r") as file :
                pb = load(file)
        except JSONDecodeError:
            isJsonEmpty : bool = True           # means the file is empty, and that's okay.
        except FileNotFoundError:
            isJsonEmpty : bool = True           # a not existing file is also empty.. or is it?

        if showplot :
            
            if isJsonEmpty :
                print("\nYou have no data to display, how about you start by entering your PB of today?")
            
            else:   # if the json file is not empty

                months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
}


                output_file("PBProgress.html")

                # i should definantly make a function for converting strings formated dates into datetime opject.
                theLastDate : str = ( sorted(pb.keys())[-1] ).strip()   # to get the last date in the pb data stripped, so we can use it to get the next two days after it
                month_day, year = theLastDate.split(",") # to split the year from the date
                year  : int = int( year )
                month : int = months[ month_day[:3] ]   # to get the month as a three letter string representing the month
                day   : int = int( month_day[4:] )     # to get the month as an integer

                lastDate = datetime(year, month, day)

                nextTwoDays = [ (lastDate + timedelta(days=1) ).strftime("%B %d, %Y") , (lastDate + timedelta(days=2) ).strftime("%B %d, %Y") ]
                actualDays  = [ date for date, time_attempt in pb.items() ]

                # this is the days in PB.json that will be at the x axis
                categories = actualDays + nextTwoDays

        
                # these are the data
                x = [ day for day, time_attempt in pb.items() ]
                y = [ getAveragePB(time_attempt) for day, time_attempt in pb.items() ]

                p = figure(x_range=categories, title="Your Rubik's Cube PB Progress.", background_fill_color="#292a2b", x_axis_label="Date", y_axis_label="Personal Best")

                p.xaxis.major_label_text_color = "#1a1a1a"
                p.yaxis.major_label_text_color = "#1a1a1a"

                p.xgrid.grid_line_color = "#1a1a1a"
                p.ygrid.grid_line_color = "#1a1a1a"

                p.xaxis.major_label_orientation = pi/9 # this one to rotate the x axis labels.

                p.line(x=x, y=y, line_color="#d970ff", line_width=3, line_dash=[8, 8], line_alpha=0.2)

                p.circle(x=x, y=y, fill_color="#edd9ff", fill_alpha=1, radius= 0.1)

                show(p)

        else: # when user dont want to show plot

            if isJsonEmpty :    # if its empty then lets add the pb of today as the first pb!

                today         : datetime = datetime.now()
                yesterday     : datetime = ( today - timedelta(days=1) ).strftime("%B %d, %Y")
                twoDaysBefore : datetime = ( today - timedelta(days=2) ).strftime("%B %d, %Y")

                pb : dict[ str, dict[str, int] ] = {
                    str( twoDaysBefore ):{
                        str( currenttime ): None    # two day before the first attempt for better result imo
                    },
                    str( yesterday ):{ 
                        str( currenttime ): None    # one day before the first attempt for better result imo
                    },
                    str( currentdate ):{
                        str( currenttime ): attempt # the first attempt in the file
                    }
                }
            
            else:   # if the file wasnt empty

                if str ( currentdate ) not in pb :
                    time_attempt : dict[ str, int ] = { str( currenttime ): attempt }   # a dictionary of the time and pb of the user

                    pb[currentdate] = time_attempt          # adding time_Attempt to the pb[currentdate]
                else:       # if the user added previous pb's on the same day
                    date : dict[ str, int] = pb[currentdate]
                    date[currenttime] = attempt

            with open("PB.json", "w") as file :
                dump(pb, file)



            

if __name__ == "__main__" :
    main()