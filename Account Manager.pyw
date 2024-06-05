import PySimpleGUI as sg
import pyautogui as pg
import pygetwindow
import csv
import os
import time
import pyperclip
import tkinter
#Handle reading file and populating

os.chdir(os.path.dirname(os.path.abspath(__file__)))

account_data = []
masked_data = []
def read_csv(path):
    try:
        with open(path, mode="r",newline="") as file:
            csv_r = csv.reader(file)
            data = list(csv_r)
        file.close()
    except FileNotFoundError as fnf:
        with open(path, mode="a") as file:
            createfile = csv.writer(file)
        file.close()
        with open(path, mode="r",newline="") as file:
            csv_r = csv.reader(file)
            data = list(csv_r)
        file.close()

    return data

def write_csv(path, fields):
    with open(path,mode="a",newline='') as file:
        writer=csv.writer(file)
        writer.writerow(fields)
    file.close()
    
    update_table()

def delete_from_csv(path, rowd):
    with open(path, mode='r', newline='') as file:
        csv_r =csv.reader(file)
        rows = list(csv_r)

        if 0 <= rowd < len(rows):
            rows.pop(rowd)
        with open(path, mode='w',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

    file.close()
    update_table()

def update_table():
    global account_data
    global masked_data
    account_data=read_csv("accounts.csv")
    masked_data = [[row[0], '*' * len(row[1]), row[2]] for row in account_data]
    
    window["tbl"].update(values=masked_data)

def validateText(key, phtext):
     if(values[key].strip()!="") & (values[key].strip()!=phtext):
         return True
     else:
         return False

def toggleDisables(key, bool):
    window[key].update(disabled=bool)

#Strings for placeholders
accname_text="Login name"
password_text="Password"
riotid_text="Name#EUW"

#Layouts for entry
accname_c = [
    [sg.Text("Account Name")],
    [sg.Input(
        s=15,
        default_text=accname_text,
        key="IN1"
        )]

]
password_c = [
    [sg.Text("Password")],
    [sg.Input(
        s=15,
        default_text=password_text,
        key="IN2"
        )]
]
riotid_c = [
    [sg.Text("Riot ID")],
    [sg.Input(
        s=15, 
        default_text=riotid_text,
        key="IN3"
        )]
]

buttons_c = [
    [
        sg.Button(button_text="Delete",size=12, disabled=True,key="deleteBtn")
    ],
    
    [
        sg.Button(button_text="Login",size=12,disabled=True,key="loginBtn")
    ]
    ,
    [
        sg.Button(button_text="Logout",size=12,key="logoutBtn")
    ]
    
]

#Building layout
account_data = read_csv("accounts.csv")
masked_data = [[row[0], '*' * len(row[1]), row[2]] for row in account_data]


layout = [

     [
        sg.Column(accname_c),
        sg.Column(password_c),
        sg.Column(riotid_c),    
    
    
        sg.Push(),
        sg.Column([[sg.Button(button_text="Enter",size=12,key="enterBtn")]]),
        
    ],
    [
        sg.HSeparator()        
    ],
    [   sg.Table(
                values=masked_data, 
                headings=["Account Name", "Password", "Riot name"],justification="center",auto_size_columns=False, size=(720,480),key="tbl",enable_events=True,
                select_mode=sg.TABLE_SELECT_MODE_BROWSE,enable_click_events=True,background_color="gray",max_col_width=15,cols_justification="lll",col_widths=[15,15,15]
                ),
        sg.vtop(sg.Column(buttons_c))
    ]



    ]

window = sg.Window("Account Manager", layout, use_default_focus=False, finalize=True, size=(575,480))

window['IN1'].bind('<FocusIn>', ' IFOCUS')
window['IN2'].bind('<FocusIn>', ' IFOCUS')
window['IN3'].bind('<FocusIn>', ' IFOCUS')

window['IN1'].bind('<FocusOut>', ' FOCUSLOST')
window['IN2'].bind('<FocusOut>', ' FOCUSLOST')
window['IN3'].bind('<FocusOut>', ' FOCUSLOST')

window['tbl'].bind('<FocusIn>', ' FOCUS')
window['tbl'].bind('<FocusOut>', ' FOCUSLOST')
window['tbl'].bind('<Button-1>', ' CLICK')
#Event handling in window
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:              #closing
        break

    #print(f'Event: {event}, Values: {values}')

    #autofill handling
    if event == "IN1 IFOCUS":
        window["tbl"].update(select_rows=[])
        if(values["IN1"].strip()==accname_text):
            window["IN1"].update("")
    elif event == "IN2 IFOCUS":           
        window["tbl"].update(select_rows=[])
        if(values["IN2"].strip()==password_text): 
            window["IN2"].update("")            
    elif event == "IN3 IFOCUS":        
        window["tbl"].update(select_rows=[])
        if(values["IN3"].strip()==riotid_text):
            window["IN3"].update("")


    if event == "IN1 FOCUSLOST":
        if(values["IN1"].strip()==""):
            window["IN1"].update(accname_text)
    elif event == "IN2 FOCUSLOST":
        if(values["IN2"].strip()==""):
            window["IN2"].update(password_text)
    elif event == "IN3 FOCUSLOST":
        if(values["IN3"].strip()==""):
            window["IN3"].update(riotid_text)                
  
    if event == "enterBtn":
        fields = []
        if(validateText("IN1",accname_text)&validateText("IN2",password_text))&validateText("IN3",riotid_text):
            fields = [values["IN1"],values["IN2"],values["IN3"]]
        else:
            sg.popup_ok("Invalid input")    
        if(fields):
            write_csv("accounts.csv", fields)
    
    #print(event)
    if event == "deleteBtn":     
     
        selected_row = values["tbl"]
        update_table()
        selected_index =  selected_row[0]                   
        selected_name = account_data[selected_index][2]
        ch = sg.popup_ok_cancel(f"Are you sure you wish to delete {selected_name}?", "",  title="Confirm delete",no_titlebar=True,background_color="gray",line_width=100)
        if ch == "OK":
                 delete_from_csv("accounts.csv",selected_index)


    if event == "tbl FOCUS":
        toggleDisables("loginBtn",False)
        toggleDisables("deleteBtn",False)
    if event == "tbl FOCUSLOST":    
        toggleDisables("loginBtn",True)
        toggleDisables("deleteBtn",True)
    if event == "tbl CLICK":            
        try: 
            if values["tbl"] == []:
                values["tbl"] = 0            
                window["tbl"].update(select_rows=[0])
        except tkinter.TclError as e:
            read_csv("accounts.csv")



    if event == "logoutBtn":        
    #get open clients, if any
        
        try:            
            leagueClient = pygetwindow.getWindowsWithTitle("League of Legends")[0]    
            clientSize = leagueClient.size
            if (leagueClient):
                clientSizeVariables = [[[25,17],[752,501]], #1600 0
                                       [[25,17],[617,398]], #1280 1
                                       [[17,12],[487,326]]] #1024 2
                x = 0
                y = 0
                leagueClient.activate()
                leagueClient.restore()
                start = leagueClient.topright
                if clientSize[0] == 1600:
                    x = (start[0] - clientSizeVariables[0][0][0])
                    y = (start[1] + clientSizeVariables[0][0][1])
                    pg.moveTo(x,y)
                    pg.click()
                    time.sleep(0.25)
                    x = (start[0] - clientSizeVariables[0][1][0])
                    y = (start[1] + clientSizeVariables[0][1][1])
                    pg.moveTo(x,y)
                    pg.click()        
                    time.sleep(0.25)            
                elif clientSize[0]== 1280:
                    x = (start[0] - clientSizeVariables[1][0][0])
                    y = (start[1] + clientSizeVariables[1][0][1])
                    pg.moveTo(x,y)
                    time.sleep(0.25)
                    pg.click()
                    x = (start[0] - clientSizeVariables[1][1][0])
                    y = (start[1] + clientSizeVariables[1][1][1])
                    pg.moveTo(x,y)
                    time.sleep(0.25)
                    pg.click()
                elif clientSize[0]==1024:
                    x = (start[0] - clientSizeVariables[2][0][0])
                    y = (start[1] + clientSizeVariables[2][0][1])
                    pg.moveTo(x,y)
                    time.sleep(0.25)
                    pg.click()
                    x = (start[0] - clientSizeVariables[2][1][0])
                    y = (start[1] + clientSizeVariables[2][1][1])
                    pg.moveTo(x,y)
                    time.sleep(0.25)
                    pg.click()
                    
        except IndexError as i:
            sg.popup("No client logged in")
        
    if event == "loginBtn": 
        try:            
            leagueClient = pygetwindow.getWindowsWithTitle("League of Legends")[0]              
            sg.Popup("You are already logged in")
        except IndexError as i: 
            try:
                riotClient = pygetwindow.getWindowsWithTitle("Riot Client")[0]
                start = riotClient.topright
                
                riotClient.activate()
                riotClient.restore()
                x = (start[0] - 1367)
                y = (start[1] + 82)
                
                time.sleep(0.1)
                color = pg.pixel(x, y)
                if color == (235, 0, 41):
                    origX, origY = pg.position()
                    pg.moveTo(start[0]-1362,start[1]+264)
                    pg.click()

                    pg.moveTo(origX,origY)
                    
                    #enter accountname
                    
                    selected_row = values["tbl"]
                    selected_index = selected_row[0]                   
                    selected_name = account_data[selected_index][0]
                    selected_password = account_data[selected_index][1]
                    pg.keyDown('ctrl')
                    pg.press('a')
                    pg.keyUp('ctrl')
                    time.sleep(0.05)
                    pg.press('delete')

                    
                    pyperclip.copy(selected_name)                    
                    pg.keyDown('ctrl')
                    pg.press('v')
                    pg.keyUp('ctrl')
                    
                    #enter password
                    time.sleep(0.05)
                    pg.press('tab')
                    #press enter
                    #pg.write(selected_password)
                    pyperclip.copy(selected_password)
                    pg.keyDown('ctrl')
                    pg.press('v')
                    pg.keyUp('ctrl')
                    pyperclip.copy("")
                    pg.press('enter')
                else:
                    sg.Popup("Navigate to sign in screen")
            except IndexError as e:
                #add open riot app
                sg.Popup("No riot client open")

       
window.close()
