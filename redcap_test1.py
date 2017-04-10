# test of using PyCap to talk to redcap

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from Tkinter import *

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     I need to upload the index for user/project to RedCap, not the name.
#        Need to ensure that they are in the same order here as in Redcap!

# user dictionary
USERS = { "Constance":1, "Bob":2,"Craig":3}
# projects dictionary
PROJECTS = { "Pepper Pilot":1, "Skeletal Muscle":2,"Other":3}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def sendToRedcap(user, myproj, issue):

    import redcap
    import time

    print('connecting to redcap....')

    # connect to project with APIkey
    redCapURL = 'http://redcapint.tsi.wfubmc.edu/redcap_int/api/'
    #  myToken = 'D742E6ADAA2F023A73B0F9F11C2AF8C9'    #   for Pepper Pilot
    myToken = '2B72CCD23A4D1E841548570DF7D44CF5'
    project = redcap.Project(redCapURL, myToken)
    #  fieldnames are:  projectname, date, issue

    myid = time.strftime('%d/%m/%y-%H:%M:%S')

    print('field_names: ', project.field_names)
    print('record_id: ', myid)
    print('user: ', user)
    print('project:', myproj)
    print('issue: ', issue)

    # note that RedCap wants the index for the projects and users, not the names, so use a dictionary
    to_import = [{'record_id': myid, 'user': USERS[user], 'projectname': PROJECTS[myproj], 'issue': issue}]

    response = project.import_records(to_import)

    print('Response = ', response)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def CB_sendToRedcap():
    print 'uploading to Redcap'
    sendToRedcap(userChosen.get(), projChosen.get(), issueTextbox.get('1.0', 'end - 1c'))
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def CB_exit():
    print 'Have a swell day!'
    root.quit()

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk()
# root.geometry('100x110+350+70')

# get the names from the dictionary
USERNAMES = USERS.keys()

userChosen = StringVar(root)
userChosen.set(USERNAMES[0])
userMenu = apply(OptionMenu, (root, userChosen) + tuple(USERNAMES))
userMenu.pack()

# get the names from the dictionary
PROJECTNAMES = PROJECTS.keys()

projChosen = StringVar(root)
projChosen.set(PROJECTNAMES[0])
projMenu = apply(OptionMenu, (root, projChosen) + tuple(PROJECTNAMES))
projMenu.pack()

# upload button
button_send = Button(root, text='Upload', command=CB_sendToRedcap)
button_send.pack(pady=20, padx=20)

# exit button
button_exit = Button(root, text='Exit', command=CB_exit)
button_exit.pack(pady=20, padx=20)

# text widget
issueTextbox = Text(root, width=40, height=10)
issueTextbox.pack()

root.mainloop()


