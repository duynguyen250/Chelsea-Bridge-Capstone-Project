import tkinter as tk
from typing_extensions import IntVar
import pandas as pd
import numpy as np
from joblib import load
from sklearn.linear_model import LinearRegression 

lr_model = load(r"C:\Users\Duy Nguyen\Desktop\Chelsea Bridge\Chelsea-Bridge-Capstone-Project\lr_model.joblib")


root = tk.Tk()

frame_date = tk.LabelFrame(root,text='Date',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_date.grid(row=0,column=0)

frame_weather = tk.LabelFrame(root,text='Weather',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_weather.grid(row=1,column=0)

frame_vessel = tk.LabelFrame(root,text='Vessels and Time',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_vessel.grid(row=2,column=0)

def button_click():
    '''Void function for predicting datetime using linear regression model'''
    date = entry_date.get()
    temp = entry_temp.get()
    tide = entry_tide.get()
    tug = entry_tug.get()
    barge = entry_barge.get()
    tanker = entry_tanker.get()
    
    #eta_bridge = date_convert(entry_eta_bridge.get(),'hour')
    day = date_convert(date,'day')
    month = date_convert(date,'month')
    year = date_convert(date,'year')
    
    row = [day, month, year, temp, tide, tug, barge, tanker, 1, 1, sunrise.get(), sunset.get(), clear.get(), cloudy.get(), overcast.get(), snow.get()]
    minute,hour = predict_date(row)
    tk.Label(root,text=f'The predicted time is {hour}:{minute:.0f}').grid(row=21,column=0)

def predict_date(row):
    """Return the predict value"""
    df = pd.DataFrame(row).T
    df.columns = ['Day', 'Month', 'Year', 'temp', 'Predicted (ft)', 'Tug', 'Barge',
       'Tanker', 'Previous Lift', 'instances_1hr', 'sunrise_flag',
       'sunset_flag', 'clear', 'cloudy', 'overcast', 'snow']
    pred = lr_model.predict(df)
    minute = (pred[0] % 1) *60
    hour = int(pred[0])
    return (minute,hour)

def date_convert(date,how):
    """Convert pandas datetime object into float or int based "how"

    Args:
        date: str 
            User inputed date should be in either (yyyy/mm/dd) or (hh:mm) or both
        how : str 
            How the datetime object would be converted 
            "day","month","year","hour"

    Returns:
        Int 
            if how = "day","month" or "year"
        Float
            if how = "hour"
    """
    datetime = pd.to_datetime(date)
    if how == 'day':
        datetime = datetime.day
    elif how == 'month':
        datetime = datetime.month
    elif how == 'year':
        datetime = datetime.year
    elif how == 'hour':
        datetime = datetime.hour + datetime.minute/60
    return datetime


    
entry_date = tk.Entry(frame_date,width=10)
entry_date.insert(tk.END,'2022/10/02')
entry_date.grid(row=0,column=1)

entry_temp = tk.Entry(frame_weather,width=10)
entry_temp.insert(tk.END,'1')
entry_temp.grid(row=1,column=1)

entry_tide = tk.Entry(frame_weather,width=10)
entry_tide.insert(tk.END,'1')
entry_tide.grid(row=2,column=1)

entry_tug = tk.Entry(frame_vessel,width=10)
entry_tug.insert(tk.END,'1')
entry_tug.grid(row=3,column=1)

entry_barge = tk.Entry(frame_vessel,width=10)
entry_barge.insert(tk.END,'1')
entry_barge.grid(row=4,column=1)

entry_tanker = tk.Entry(frame_vessel,width=10)
entry_tanker.insert(tk.END,'1')
entry_tanker.grid(row=5,column=1)

#entry_eta_bridge = tk.Entry(frame_vessel,width=10)
#entry_eta_bridge.insert(tk.END,'12:00')
#entry_eta_bridge.grid(row=6,column=1)


sunrise = tk.IntVar()
check_sunrise = tk.Checkbutton(frame_weather,text='Sunrise',variable=sunrise)
check_sunrise.grid(row=7,column=0)

sunset = tk.IntVar()
check_sunset = tk.Checkbutton(frame_weather,text='Sunset',variable=sunset)
check_sunset.grid(row=8,column=0)

clear = tk.IntVar()
check_clear = tk.Checkbutton(frame_weather,text='Clear',variable=clear)
check_clear.grid(row=9,column=0)

cloudy = tk.IntVar()
check_cloudy = tk.Checkbutton(frame_weather,text='Cloudy',variable=cloudy)
check_cloudy.grid(row=10,column=0)

overcast = tk.IntVar()
check_overcast = tk.Checkbutton(frame_weather,text='Overcast',variable=overcast)
check_overcast.grid(row=11,column=0)

snow = tk.IntVar()
check_snow = tk.Checkbutton(frame_weather,text='Snow',variable=snow)
check_snow.grid(row=12,column=0)


tk.Button(root, text='Predict',command=button_click,padx=30,font=('Helvatica',10,'bold'),relief=tk.RAISED).grid(row=20,column=0)
tk.Label(frame_date, text="Today's date:").grid(row=0,column=0)
tk.Label(frame_weather, text="Temperature:").grid(row=1,column=0)
tk.Label(frame_weather, text="Tide:").grid(row=2,column=0)
tk.Label(frame_vessel, text="Tug:").grid(row=3,column=0)
tk.Label(frame_vessel, text="Barge:").grid(row=4,column=0)
tk.Label(frame_vessel, text="Tanker:").grid(row=5,column=0)
#tk.Label(frame_vessel, text="ETA Bridge:").grid(row=6,column=0)

entry_date.focus()
root.title('Linear Regression Model')
root.mainloop()