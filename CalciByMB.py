from tkinter import *
import tkinter.messagebox as tmsg
from functools import partial
from string import ascii_letters
from tkHyperlinkManager import HyperlinkManager
import webbrowser as web

def mainWindow():
    """ Function which drives the Main Window """

    splashScreen.destroy()

    def display(event, element):
        """This method displays the corresponding button's text"""

        if textArea.get() == "Error":
            values.set("")
            textArea.update()

        elif textArea.select_present():
            textArea.delete("sel.first", "sel.last")

        elif textArea.get() in ['+', '/', '*']:
            textArea.delete(0, END)

        textArea.insert(string=element, index=INSERT)

    def deleter(event):
        """This method deletes the elements from the text entry and works exactly like the backspace key"""

        if textArea.select_present():
            textArea.delete("sel.first", "sel.last")
        else:
            textArea.delete(textArea.index(INSERT) - 1, textArea.index(INSERT))

    def evaluate(event):
        """This method performs the evaluations of the entered text in the entry area"""

        operation = textArea.get()

        try:
            answer = eval(values.get())
        except Exception as exceptionName:
            answer = "Error"
            print(exceptionName)

        values.set(answer)
        textArea.update()
        textArea.select_range(0, END)

        # global historyList
        historyList[operation] = answer

    def clearHistory(historyBox):
        # global historyList
        historyBox.delete(0, END)
        historyList.clear()

    def showHistory():
        """This method is used to show the history window of the applied calculations"""

        widthSize, heightSize = 500, 450
        count = 1

        historyWindow = Toplevel(root)
        historyWindow.title("History - Calci By MB")
        historyWindow.geometry(f"{widthSize}x{heightSize}")
        historyWindow.minsize(widthSize, heightSize)
        historyWindow.maxsize(widthSize + 500, heightSize)
        historyWindow.configure(bg=themeDict["defaultAppBg"])

        try:
            historyWindow.wm_iconbitmap("Assets/Icons/historyWindow.ico")
        except Exception as exceptionName:
            print(exceptionName)

        if historyList == {}:
            tmsg.showinfo("History", "There is no history yet!\nPlease sweat the app out!")
            historyWindow.destroy()

        else:

            scrollBarHistory = Scrollbar(historyWindow)
            scrollBarHistory.pack(side=RIGHT, fill=Y)

            historyListBox = Listbox(historyWindow, yscrollcommand=scrollBarHistory.set, height=50,
                                     font=(themeDict["defFont"], 15), bg=themeDict["defaultAppBg"],
                                     fg=themeDict["defaultFontColor"],
                                     selectbackground=themeDict["defSelectBgForListBox"],
                                     selectforeground=themeDict["defSelectFgForListBox"])

            historyExitButton = Button(historyWindow, text="Exit", command=historyWindow.destroy, width=5,
                                       font=(themeDict["defFont"], 15), bg=themeDict["defaultButtonBg"],
                                       fg=themeDict["defaultButtonFg"],
                                       activebackground=themeDict["defaultButtonActiveBg"],
                                       activeforeground=themeDict["defaultButtonActiveFg"])
            historyExitButton.pack(anchor=N, side=RIGHT)

            historyClearButton = Button(historyWindow, text="Clear", command=partial(clearHistory, historyListBox),
                                        width=5, font=(themeDict["defFont"], 15), bg=themeDict["defaultButtonBg"],
                                        fg=themeDict["defaultButtonFg"],
                                        activebackground=themeDict["defaultButtonActiveBg"],
                                        activeforeground=themeDict["defaultButtonActiveFg"])

            historyClearButton.pack(anchor=N, side=LEFT)

            for key, value in historyList.items():
                historyListBox.insert(END, f"{count}) -> {key} = {value}\n")
                count += 1

            historyListBox.pack(fill=BOTH)
            scrollBarHistory.config(command=historyListBox.yview)

        historyWindow.mainloop()

    def setTheme(themesDict):
        """This function is used to set the theme of the applications' various windows"""

        if themeVar.get() == "Light Mode":
            root.configure(bg="light cyan")
            for count in range(16):
                buttonVarList[count].config(bg="sky blue", fg="midnight blue", activebackground="cadet blue",
                                            activeforeground="turquoise")
            buttonForBackSpace.config(bg="sky blue", fg="midnight blue", activebackground="cadet blue",
                                      activeforeground="turquoise", image=backspaceIconLight)
            buttonForClearAll.config(bg="sky blue", fg="midnight blue", activebackground="cadet blue",
                                     activeforeground="turquoise")
            for count in range(4):
                buttonFramesList[count].config(bg="light cyan")
            frameMisc.config(bg="light cyan")
            textFrame.config(bg="light cyan")
            textArea.config(fg="slateblue4", bg="pale turquoise")

            themesDict["defSelectFgForListBox"] = "black"
            themesDict["defSelectBgForListBox"] = "light blue"
            themesDict["defaultAppBg"] = "light cyan"
            themesDict["defaultFontColor"] = "midnight blue"
            themesDict["defaultButtonBg"] = "sky blue"
            themesDict["defaultButtonFg"] = "midnight blue"
            themesDict["defaultButtonActiveFg"] = "turquoise"
            themesDict["defaultButtonActiveBg"] = "cadet blue"
            themesDict["defBgHelpWindow"] = "white"
            themesDict["defFgHelpWindow"] = "black"

        else:
            root.configure(bg="black")
            for count in range(16):
                buttonVarList[count].config(bg="grey25", fg="lavender", activebackground="grey10",
                                            activeforeground="snow")
            buttonForBackSpace.config(bg="grey25", fg="lavender", activebackground="grey10",
                                      activeforeground="snow", image=backspaceIconDark)
            buttonForClearAll.config(bg="grey25", fg="lavender", activebackground="grey10",
                                     activeforeground="snow")
            for count in range(4):
                buttonFramesList[count].config(bg="grey5")
            frameMisc.config(bg="grey5")
            textFrame.config(bg="grey36")
            textArea.config(fg="thistle2", bg="grey")

            themesDict["defSelectFgForListBox"] = "white"
            themesDict["defSelectBgForListBox"] = "grey10"
            themesDict["defaultAppBg"] = "grey36"
            themesDict["defaultFontColor"] = "lavender"
            themesDict["defaultButtonBg"] = "grey25"
            themesDict["defaultButtonFg"] = "lavender"
            themesDict["defaultButtonActiveBg"] = "grey10"
            themesDict["defaultButtonActiveFg"] = "snow"
            themesDict["defBgHelpWindow"] = "black"
            themesDict["defFgHelpWindow"] = "white"

    def showHelp():
        """This function displays the help window of the calculator application"""

        helpWindow = Toplevel(root)
        helpWidth = 720
        helpHeight = 480
        helpWindow.geometry(f"{helpWidth}x{helpHeight}")
        helpWindow.minsize(helpWidth, helpHeight)
        helpWindow.title("Help - Calci By MB")

        try:
            helpWindow.wm_iconbitmap("Assets/Icons/helpIcon.ico")
        except Exception as exceptionName:
            print(exceptionName)

        scrollBarY = Scrollbar(helpWindow)
        scrollBarY.pack(side=RIGHT, fill=Y)

        helpContentArea = Text(helpWindow, yscrollcommand=scrollBarY.set, height=450, font=(themeDict["defFont"], 15),
                               bg=themeDict["defBgHelpWindow"], fg=themeDict["defFgHelpWindow"])
        helpContentArea.pack(fill=BOTH)

        scrollBarY.config(command=helpContentArea.yview)
        imageVarList = ["image-1", "image-2", "image-3"]
        contentAndImages = {"exponentFeature.png": "---Welcome to the help window of Calci Application---\n\nThis "
                                                   "application is designed to keep in mind the changing trends of "
                                                   "the tech industry and works accordingly, smooth like a breeze.\n"
                                                   "It has got some cool features:-\n\n1.The \"single line"
                                                   "exponent\" feature:\nYou can calculate the exponent of a number "
                                                   "by a number in the following way:\n\n",
                            "doubleDivideFeature.png": "2.The \"Double Divide Feature\"\nYou can get only the floor "
                                                       "value during a divide operation by adding 2 divide symbols"
                                                       " between operands and if you specify only a single divide "
                                                       "symbol, it will perform a full divide operation:\n\n",
                            "multipleMinusSign.png": "3. The\"Algebraic Feature\"\nIf you specify 2 or more minus"
                                                     " symbols between operands then it will act according to algebraic"
                                                     " evaluation i.e. specifying 2 minus symbols"
                                                     " will perform addition operation and so on\n\n,"
                            }

        count = 0
        for key, value in contentAndImages.items():
            helpContentArea.insert(END, value)
            imageVarList[count] = PhotoImage(file=f"Assets/Images/{key}")
            helpContentArea.image_create(END, image=imageVarList[count])
            helpContentArea.insert(END, "\n\n")
            count += 1

        helpContentArea.insert(END, "More features soon in the next updates\nStay Tuned!")

        helpContentArea.config(state=DISABLED)
        helpWindow.mainloop()

    def setFont():
        """This function changes the font of the applications' various windows"""

        try:
            for fontType in fontList:
                if fontVar.get() == fontType:
                    # global defFont
                    themeDict["defFont"] = fontType
                    textArea.config(font=(fontType, 25))
                    for buttonCount in range(16):
                        buttonVarList[buttonCount].config(font=(fontType, 20))
                    buttonForClearAll.config(font=(fontType, 19))

                    if fontType == fontList[0]:
                        root.geometry(f"{widthRoot}x{heightRoot}")
                        root.minsize(370, 685)
                        buttonForBackSpace.config(width=170)
                    elif fontType == fontList[1]:
                        root.geometry("378x660")
                        root.minsize(widthRoot + 8, heightRoot - 20)
                        buttonForBackSpace.config(width=160)
                    elif fontType == fontList[2]:
                        root.geometry("375x725")
                        root.minsize(375, 725)
                        buttonForBackSpace.config(width=170)
                    elif fontType == fontList[3]:
                        root.geometry(f"{widthRoot - 10}x{heightRoot - 100}")
                        root.minsize(widthRoot - 10, heightRoot - 100)
                        buttonForBackSpace.config(width=160)
                    elif fontType == fontList[4]:
                        root.geometry("410x705")
                        root.minsize(410, 700)
                        buttonForBackSpace.config(width=190)
                    elif fontType == fontList[5]:
                        root.geometry("436x698")
                        root.minsize(436, 698)
                        buttonForBackSpace.config(width=200)
                    elif fontType == fontList[6]:
                        root.geometry("438x700")
                        root.minsize(438, 780)
                        buttonForBackSpace.config(width=180)

        except Exception as exceptionName:
            print(exceptionName)

    def onAppClose():
        """This function shows a warning type dialog box to leave the app or not"""

        if tmsg.askokcancel("So Soon :(", "Are you sure you wanna quit??\nAlthough I can do this all day"):
            root.destroy()

    def showAbout():
        """This function displays the about window of thr application"""

        aboutWindow = Toplevel(root)
        aboutWindowWidth = 360
        aboutWindowHeight = 200
        aboutWindow.geometry(f"{aboutWindowWidth}x{aboutWindowHeight}")
        aboutWindow.title("About - Calci By MB")
        aboutWindow.resizable(False, False)

        try:
            aboutWindow.wm_iconbitmap("Assets/Icons/aboutIcon.ico")
        except Exception as exceptionName:
            print(exceptionName)

        textAreaAbout = Text(aboutWindow, width=aboutWindowWidth, height=aboutWindowHeight, font=(themeDict["defFont"],
                                                                                                  10),
                             fg=themeDict["defFgHelpWindow"], bg=themeDict["defBgHelpWindow"])
        textAreaAbout.pack()
        link = HyperlinkManager(textAreaAbout)
        textAreaAbout.insert(END, "\n")
        textAreaAbout.insert(END, "This calculator is developed and designed by ")
        textAreaAbout.insert(END, "Mohammed Bhanpurawala", link.add(partial(web.open,
                                                                            "https://www.instagram.com"
                                                                            "/hell_raiser1101/?hl=en")))
        textAreaAbout.insert(END, "\nCalculator version 10.2103.8.0\n© 2021 MB Inc. All rights reserved.\n\n", )
        textAreaAbout.insert(END, "Connect With Me:  ")
        textAreaAbout.insert(END, "Instagram", link.add(partial(web.open,
                                                                "https://www.instagram.com/hell_raiser1101/?hl=en")))
        textAreaAbout.insert(END, " ")
        textAreaAbout.insert(END, "Facebook", link.add(partial(web.open,
                                                               "https://www.facebook.com/mohammed.bhanpurawala.315/")))

        textAreaAbout.config(state=DISABLED)
        aboutWindow.mainloop()

    # Theme Colors
    themeDict = {"defaultAppBg": "light cyan", "defaultFrameBg": "light cyan", "defaultTextFrameBg": "white",
                 "defaultFontColor": "slateblue4", "defFont": "Cascadia Code", "defaultButtonBg": "sky blue",
                 "defaultButtonFg": "midnight blue", "defaultButtonActiveBg": "cadet blue",
                 "defaultButtonActiveFg": "turquoise", "defaultTextAreaBg": "pale turquoise",
                 "defSelectBgForListBox": "light blue", "defSelectFgForListBox": "black",
                 "defBgHelpWindow": "white", "defFgHelpWindow": "black"}

    # Structure of the application
    root = Tk()
    widthRoot = 370
    heightRoot = 685
    middleXRoot = root.winfo_screenwidth() // 2
    middleYRoot = root.winfo_screenheight() // 2

    # This will start the application in the centre of the screen
    root.geometry(f"{widthRoot}x{heightRoot}+{middleXRoot - (widthRoot // 2)}+{middleYRoot - (heightRoot // 2)}")
    root.resizable(False, False)
    root.title("Calci - By Mohammed Bhanpurawala")
    root.protocol("WM_DELETE_WINDOW", onAppClose)

    try:
        root.wm_iconbitmap("Assets/Icons/mainIcon.ico")
    except Exception as e:
        print(e)

    root.configure(bg=themeDict["defaultAppBg"])

    # Variables
    values = StringVar()
    historyList = {}

    # Entry widget and frame declaration
    textFrame = Frame(root, relief=SUNKEN, bg=themeDict["defaultTextFrameBg"])
    textArea = Entry(textFrame, textvar=values, font=(themeDict["defFont"], 25), fg=themeDict["defaultFontColor"],
                     width=30, bg=themeDict["defaultTextAreaBg"])
    textArea.pack(padx=5, pady=2)
    textFrame.pack(pady=3)

    # Disabling the alphabet keys and equal key
    for i in ascii_letters:
        textArea.bind(f"<{i}>", lambda event: "break")
    textArea.bind("<equal>", lambda event: "break")

    # Button List to set buttons in app
    buttonList = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", ".", "0", "=", "+"]

    # Declaring a list for Button Frames and appending names in it
    buttonFramesList = []
    buttonVarList = []
    for i in range(16):
        buttonVarList.append(f"button-{i + 1}")
        if i < 4:
            buttonFramesList.append(f"frame{i + 1}")

    # Setting the buttons and frames of the app
    num = 0
    for i in range(4):
        buttonFramesList[num] = Frame(root, bg=themeDict["defaultFrameBg"])
        fromIndex = i * 4
        toIndex = i * 4 + 4
        for j in range(fromIndex, toIndex):
            buttonVarList[j] = Button(buttonFramesList[num], text=buttonList[j], bg=themeDict["defaultButtonBg"],
                                      fg=themeDict["defaultButtonFg"],
                                      activebackground=themeDict["defaultButtonActiveBg"],
                                      font=(themeDict["defFont"], 20), width=5,
                                      height=3, activeforeground=themeDict["defaultButtonActiveFg"])
            buttonVarList[j].pack(side=LEFT, padx=1, pady=1)
            if buttonList[j] != "=":
                buttonVarList[j].bind('<Button-1>', partial(display, element=buttonList[j]))
                if buttonList[j].isdigit():
                    buttonVarList[j].bind(f'<Key-{buttonList[j]}>', partial(display, element=buttonList[j]))
            else:
                buttonVarList[j].bind('<Button-1>', evaluate)

        buttonFramesList[num].pack(side=TOP)
        num += 1

    # Frame for Backspace and Clear all button
    frameMisc = Frame(root, bg=themeDict["defaultFrameBg"])

    # Setting up Backspace button
    backspaceIconLight = PhotoImage(file="Assets/Images/backspaceLight.png")
    backspaceIconDark = PhotoImage(file="Assets/Images/backspaceDark.png")
    buttonForBackSpace = Button(frameMisc, image=backspaceIconLight, bg=themeDict["defaultButtonBg"],
                                fg=themeDict["defaultButtonFg"],
                                activebackground=themeDict["defaultButtonActiveBg"], font=(themeDict["defFont"], 19),
                                width=170, height=98,
                                activeforeground=themeDict["defaultButtonActiveFg"])
    buttonForBackSpace.bind("<Button-1>", deleter)
    buttonForBackSpace.pack(side=LEFT, padx=1)

    # Setting up Clear All button
    buttonForClearAll = Button(frameMisc, text="C", bg=themeDict["defaultButtonBg"], fg=themeDict["defaultButtonFg"],
                               activebackground=themeDict["defaultButtonActiveBg"], font=(themeDict["defFont"], 19),
                               width=11, height=2, activeforeground=themeDict["defaultButtonActiveFg"])
    buttonForClearAll.bind("<Button-1>", lambda event: textArea.delete(0, END))
    buttonForClearAll.pack(side=LEFT, padx=1)

    # Packing the frame containing above buttons
    frameMisc.pack(padx=1, pady=1)

    # Binding the return key to perform the evaluate operation
    root.bind("<Return>", evaluate)

    mainMenu = Menu(root)

    themeVar = StringVar(value="Light Mode")
    fontList = ["Cascadia Code", "Bradley Hand ITC", "Comic Sans MS", "Forte", "Kristen ITC", "Lucida Calligraphy",
                "Segoe Script"]
    fontVar = StringVar(value=themeDict["defFont"])

    historyMenu = Menu(mainMenu, tearoff=0)
    themesMenu = Menu(mainMenu, tearoff=0)
    helpMenu = Menu(mainMenu, tearoff=0)
    aboutMenu = Menu(mainMenu, tearoff=0)
    fontMenu = Menu(mainMenu, tearoff=0)

    historyMenu.add_command(label="Show History", command=showHistory)
    mainMenu.add_cascade(label="History", menu=historyMenu)

    themesMenu.add_radiobutton(label="Light Mode", command=partial(setTheme, themeDict), variable=themeVar)
    themesMenu.add_radiobutton(label="Dark Mode", command=partial(setTheme, themeDict), variable=themeVar)
    mainMenu.add_cascade(label="Themes", menu=themesMenu)

    for fontName in fontList:
        fontMenu.add_radiobutton(label=f"{fontName}", variable=fontVar, command=setFont)
    mainMenu.add_cascade(label="Fonts", menu=fontMenu)

    helpMenu.add_command(label="Show Help", command=showHelp)
    mainMenu.add_cascade(label="Help", menu=helpMenu)

    aboutMenu.add_command(label="About", command=showAbout)

    mainMenu.add_cascade(label="About", menu=aboutMenu)

    root.config(menu=mainMenu)

    root.mainloop()


splashScreen = Tk()
width, height = 370, 685
middleXSplash = splashScreen.winfo_screenwidth() // 2
middleYSplash = splashScreen.winfo_screenheight() // 2
splashScreen.geometry(f"{width}x{height}+{middleXSplash - width // 2}+{middleYSplash - height // 2}")
splashScreen.overrideredirect(True)

splashImage = PhotoImage(file="Assets/Images/splashScreenImage.png")

Label(splashScreen, image=splashImage).pack()
splashScreen.after(2000, mainWindow)

mainloop()
