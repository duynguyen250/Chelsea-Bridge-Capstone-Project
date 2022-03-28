import tkinter as tk
from typing_extensions import IntVar
import pandas as pd
import numpy as np
from joblib import load
from sklearn.linear_model import LinearRegression 

lr_model = load("lr_model.joblib")


root = tk.Tk()

def button_click():
    date = entry_date.get()
    temp = entry_temp.get()
    tide = entry_tide.get()
    tug = entry_tug.get()
    barge = entry_barge.get()
    tanker = entry_tanker.get()
    
    datetime = pd.to_datetime(date)
    day = datetime.day
    month = datetime.month
    year = datetime.year
    
    row = [day, month, year, temp, tide, tug, barge, tanker, 1, 1, sunrise.get(), sunset.get(), 1, 0, 0, 0]
    df = pd.DataFrame(row).T
    df.columns = ['Day', 'Month', 'Year', 'temp', 'Predicted (ft)', 'Tug', 'Barge',
       'Tanker', 'Previous Lift', 'instances_1hr', 'sunrise_flag',
       'sunset_flag', 'clear', 'cloudy', 'overcast', 'snow']
    pred = lr_model.predict(df)
    minute = (pred[0] % 1) *60
    hour = int(pred[0])
    tk.Label(root,text=f'The predicted time is {hour}:{minute:.0f}').grid(row=11,column=0)
    
entry_date = tk.Entry(width=10)
entry_date.insert(tk.END,'2022/10/02')
entry_date.grid(row=0,column=1)

entry_temp = tk.Entry(width=10)
entry_temp.insert(tk.END,'1')
entry_temp.grid(row=1,column=1)

entry_tide = tk.Entry(width=10)
entry_tide.insert(tk.END,'1')
entry_tide.grid(row=2,column=1)

entry_tug = tk.Entry(width=10)
entry_tug.insert(tk.END,'1')
entry_tug.grid(row=3,column=1)

entry_barge = tk.Entry(width=10)
entry_barge.insert(tk.END,'1')
entry_barge.grid(row=4,column=1)

entry_tanker = tk.Entry(width=10)
entry_tanker.insert(tk.END,'1')
entry_tanker.grid(row=5,column=1)

sunrise = tk.IntVar()
check_sunrise = tk.Checkbutton(text='Sunrise',variable=sunrise)
check_sunrise.grid(row=6,column=0)

sunset = tk.IntVar()
check_sunset = tk.Checkbutton(text='Sunset',variable=sunset)
check_sunset.grid(row=7,column=0)


tk.Button(root, text='Predict',command=button_click).grid(row=10,column=1)
tk.Label(root, text="Today's date:").grid(row=0,column=0)
tk.Label(root, text="Temperature:").grid(row=1,column=0)
tk.Label(root, text="Tide:").grid(row=2,column=0)
tk.Label(root, text="Tug:").grid(row=3,column=0)
tk.Label(root, text="Barge:").grid(row=4,column=0)
tk.Label(root, text="Tanker:").grid(row=5,column=0)

entry_date.focus()
root.title('Linear Regression Model')
root.columnconfigure(0,weight=1)
root.rowconfigure(0,weight=1)
root.mainloop()