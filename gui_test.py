import tkinter as tk
from typing_extensions import IntVar
import pandas as pd
import numpy as np
from joblib import load
from sklearn.linear_model import LinearRegression 
from tkinter import StringVar, messagebox
from tkinter import filedialog

root = tk.Tk()

frame_title = tk.Frame(root)
frame_title.grid(row=0,column=0)

frame_date = tk.LabelFrame(root,text='Date',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_date.grid(row=1,column=0)

frame_weather = tk.LabelFrame(root,text='Weather',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_weather.grid(row=2,column=0)

frame_vessel = tk.LabelFrame(root,text='Vessels and Time',font=('Helvatica',10,'bold'),relief=tk.SUNKEN)
frame_vessel.grid(row=3,column=0)

def browse_model():
    """Ask user for joblib model directory and set path to global variable
    """
    global model_path
    model_path = tk.filedialog.askopenfilename()
   

def button_click():
    
    """Void function for generating linear regression result based on the inputted values
    """
    date = entry_date.get()
    temp = entry_temp.get()
    tide = entry_tide.get()
    tug = entry_tug.get()
    barge = entry_barge.get()
    tanker = entry_tanker.get()
    try:
        date = pd.to_datetime(date)
    except:
        messagebox.showerror(title='Python Error',message='Please ensure the Today\'s date is in yyyy/mm/dd format')
    for var in [tug,barge,tanker]:
        try:     
            var = int(var)
        except:
            messagebox.showerror(title='Python Error',message='Please ensure the value for Tug, Barge and Tanker are integers')
    for var in [temp,tide]:
        try:     
            var = float(var)
        except:
            messagebox.showerror(title='Python Error',message='Please ensure the value for Temperature and Predicted Tide are decimal numbers')
    
    #eta_bridge = date_convert(entry_eta_bridge.get(),'hour')
    day = date_convert(date,'day')
    month = date_convert(date,'month')
    year = date_convert(date,'year')
    
    row = [day, month, year, temp, tide, tug, barge, tanker, 1, 1, sunrise.get(), sunset.get(), clear.get(), cloudy.get(), overcast.get(), snow.get()]
    minute,hour = predict_date(row)
    #tk.Label(root,text=f'The lift predicted time is {hour}:{minute:.0f}',font=('Helvatica',10,'bold'),state='readonly').grid(row=21,column=0)
    predict_text = StringVar()
    predict_text.set(f'{hour}:{minute:.0f}')
    tk.Entry(root,font=('Helvatica',10,'bold'),state='readonly',textvariable=predict_text,width=5,foreground='red').grid(row=22,column=0)
    tk.Label(root, text='The Predicted Time of the Bridge Lift is:',font=('Helvatica',10)).grid(row=21,column=0)
    

def predict_date(row):
    """Takes in list of features and convert it into a pandas DataFrame

    Args:
        row: list 
            List contains all the features for prediction.


    Returns: 
        Pandas DataFrame
            List of all features with specific column names
    """
    
    try:
        lr_model = load(model_path)
    except:
        messagebox.showerror(title='Python Error',message='Please select the correct model file')
        
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
check_sunrise.grid(row=7,column=0,sticky=tk.W)

sunset = tk.IntVar()
check_sunset = tk.Checkbutton(frame_weather,text='Sunset',variable=sunset)
check_sunset.grid(row=8,column=0,sticky=tk.W)

clear = tk.IntVar()
check_clear = tk.Checkbutton(frame_weather,text='Clear',variable=clear)
check_clear.grid(row=9,column=0,sticky=tk.W)

cloudy = tk.IntVar()
check_cloudy = tk.Checkbutton(frame_weather,text='Cloudy',variable=cloudy)
check_cloudy.grid(row=10,column=0,sticky=tk.W)

overcast = tk.IntVar()
check_overcast = tk.Checkbutton(frame_weather,text='Overcast',variable=overcast)
check_overcast.grid(row=11,column=0,sticky=tk.W)

snow = tk.IntVar()
check_snow = tk.Checkbutton(frame_weather,text='Snow',variable=snow)
check_snow.grid(row=12,column=0,sticky=tk.W)


tk.Button(root, text='Predict',command=button_click,padx=30,font=('Helvatica',10,'bold'),relief=tk.RAISED).grid(row=20,column=0)
tk.Button(frame_title, text='Select Model File',command=browse_model,padx=30,font=('Helvatica',10,'bold'),relief=tk.RAISED).grid(row=20,column=0)
tk.Label(frame_date, text="Today's date:").grid(row=0,column=0)
tk.Label(frame_weather, text="Temperature:").grid(row=1,column=0,sticky=tk.W)
tk.Label(frame_weather, text="Predicted Tide:").grid(row=2,column=0)
tk.Label(frame_vessel, text="Tug:").grid(row=3,column=0)
tk.Label(frame_vessel, text="Barge:").grid(row=4,column=0)
tk.Label(frame_vessel, text="Tanker:").grid(row=5,column=0)
tk.Label(frame_title, text='Chelsea Bridge Lift \n Bridge Time Predictor',font=('Helvatica',13,'bold')).grid(row=0,column=0)
#tk.Label(frame_vessel, text="ETA Bridge:").grid(row=6,column=0)


entry_date.focus()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.mainloop()