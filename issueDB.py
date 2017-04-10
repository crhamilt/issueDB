#!python

# test of using PyCap to talk to redcap and upload records to ISSUES project

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from tkinter import *
from tkinter import messagebox   # some wierdness in tkinter requires this

from collections import OrderedDict

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#     I need to upload the index for user/project to RedCap, not the name.
#        Need to ensure that they are in the same order here as in Redcap!

# user dictionary
USERS = OrderedDict()
USERS['Constance'] = 1
USERS['Bob'] = 2
USERS['Craig'] = 3

# projects dictionary
PROJECTS = OrderedDict()
PROJECTS['Pepper Pilot'] = 1
PROJECTS['Skeletal Muscle'] = 2
PROJECTS['Other'] = 3


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def send_to_redcap(user, my_project, my_id, issue):
    import redcap
    import time

    print('connecting to redcap....')

    # connect to project with APIkey
    redcap_url = 'http://redcapint.tsi.wfubmc.edu/redcap_int/api/'
    #  myToken = 'D742E6ADAA2F023A73B0F9F11C2AF8C9'    #   for Pepper Pilot
    my_token = '2B72CCD23A4D1E841548570DF7D44CF5'
    project = redcap.Project(redcap_url, my_token)
    #  fieldnames are:  projectname, date, issue

    myid = time.strftime('%d/%m/%y-%H:%M:%S')

    # print('field_names: ', project.field_names)
    # print('record_id: ', myid)
    # print('user: ', user)
    # print('project:', myproj)
    # print('issue: ', issue)

    # note that RedCap wants the index for the projects and users, not the names, so use a dictionary to get index
    to_import = [{'record_id': myid, 'user': USERS[user], 'projectname': PROJECTS[my_project],
                  'subjectid': my_id, 'issue': issue}]

    response = project.import_records(to_import)

    # print('Response = ', response)

    if response['count'] == 1:
        print('Upload successful')
        messagebox.showinfo("Redcap Upload", "Upload successful!")
    else:
        print('Upload failed - now you need to whine to tech support...')
        messagebox.showerror("Redcap Upload", "Upload failed - notify tech support.")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def cb_send_to_redcap():
    print('uploading to Redcap')
    send_to_redcap(userChosen.get(), projChosen.get(), idTextbox.get('1.0', 'end - 1c'),
                   issueTextbox.get('1.0', 'end - 1c'))


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def cb_open_redcap():
    import webbrowser

    print('opening Redcap')
    webbrowser.open("https://redcap.tsi.wfubmc.edu/projects.cfm")


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def cb_exit():
    print('Have a swell day!')
    root.quit()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

root = Tk()
# root.geometry('100x110+350+70')

#   TOP FRAME  ..........................

# get the names from the dictionary
USERNAMES = list(USERS)

print('USERNAMES = ', USERNAMES)

frametop = Frame(root)
frametop.pack(side=TOP)

textLabel1 = Label(frametop, text="Issue reporting for projects        V1.0", pady=10)
textLabel1.pack(side=TOP)

userChosen = StringVar()  # this variable will be updated by the OptionMenu
userChosen.set(USERNAMES[0])
userMenu = OptionMenu(root, userChosen, tuple(USERNAMES))
userMenu.pack(side=LEFT)

# get the names from the dictionary
PROJECTNAMES = list(PROJECTS)

projChosen = StringVar()
projChosen.set(PROJECTNAMES[0])
projMenu = OptionMenu(root, projChosen, tuple(PROJECTNAMES))
projMenu.pack(side=RIGHT)

framemid2 = Frame(root)
framemid2.pack()

# label for the text entry
textLabel2 = Label(framemid2, text="Subject ID:", pady=10)
textLabel2.pack(side=LEFT)
# text widget
idTextbox = Text(framemid2, width=10, height=1)
idTextbox.pack(side=RIGHT)

#    MID FRAME  ........................

framemid = Frame(root)
framemid.pack(fill=BOTH, expand=1)
# label for the text entry
textLabel3 = Label(framemid, text="Type your whining here:")
textLabel3.pack(side=TOP)
# text widget
issueTextbox = Text(framemid, width=40, height=10)
issueTextbox.pack(fill=BOTH, expand=1)

#    BOTTOM FRAME  ........................

framebot = Frame(root)
framebot.pack()
# upload button
button_send = Button(framebot, text='Upload', command=cb_send_to_redcap)
button_send.pack(pady=20, padx=20, side=LEFT)

# open redcap url button
button_send = Button(framebot, text='Open RedCap website', command=cb_open_redcap)
button_send.pack(pady=20, padx=20, side=LEFT)

# exit button
button_exit = Button(framebot, text='Exit', command=cb_exit)
button_exit.pack(pady=20, padx=20, side=RIGHT)

root.mainloop()
