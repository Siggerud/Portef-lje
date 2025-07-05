# this app is for rebalancing portfolios

import tkinter as tk
from tkinter import ttk
from csvtool import Csvtool

root = tk.Tk()
root.geometry("900x500")
root.title("Portefølje")

# Create instance of Tool
Tool = Csvtool()


# import Data about portfolio
def getPortfolio():
    deposit = entryDeposit.get()
    importList = Tool.createPortfolio(deposit)

    if len(importList) == 6:
        Button2.config(
            state="active"
        )  # make button active if import of list is successful

        # make numbers green or red dependent on wether the funds are under or above
        # the ideal value
        for i in range(len(importList)):
            for j in range(len(importList[i])):
                entryList[i][j].set(importList[i][j])
                if i == 5:
                    if importList[i][j][0] != "-":
                        entryConfigList[2][j].config(foreground="red")
                        entryConfigList[5][j].config(foreground="red")
                    else:
                        entryConfigList[2][j].config(foreground="green")
                        entryConfigList[5][j].config(foreground="green")


# get tips about what funds to invest in
def getTips():
    sortedList = Tool.sortLists()

    entryConfigs = buildTipEntries(sortedList)

    for i in range(len(sortedList[1])):
        if sortedList[1][i][0] != "-":
            entryConfigs[1][i].config(foreground="red")
            entryConfigs[2][i].config(foreground="red")
        else:
            entryConfigs[1][i].config(foreground="green")
            entryConfigs[2][i].config(foreground="green")


# build list for tipsed funds and return list with entries
def buildTipEntries(sortedList):
    entryTipConfig = []
    for i in range(len(sortedList)):
        temp = []
        for j in range(len(sortedList[i])):
            entryTip = tk.Entry(root)
            entryTip.grid(row=j + 11, column=i)
            entryTip.insert(0, sortedList[i][j])
            temp.append(entryTip)
        entryTipConfig.append(temp)

    return entryTipConfig


# Create button
Button1 = tk.Button(root, text="Import", command=getPortfolio, bg="green")
Button1.grid(row=1, column=2)

Button2 = tk.Button(root, text="Get tips", state="disabled", command=getTips)
Button2.grid(row=10, column=0)

# deposit entry and label
labelDeposit = tk.Label(root, text="Deposit")
labelDeposit.grid(row=1, column=0)

valueDeposit = tk.StringVar()
entryDeposit = tk.Entry(root, textvariable=valueDeposit)
entryDeposit.grid(row=1, column=1)

# defining titles
labelSector = tk.Label(root, text="Sectors")
labelSector.grid(row=2, column=0)

labelIdealWeights = tk.Label(root, text="Ideal weights")
labelIdealWeights.grid(row=2, column=1)

labelCurrentWeights = tk.Label(root, text="Current weights")
labelCurrentWeights.grid(row=2, column=2)

labelDiffPercent = tk.Label(root, text="Diff. in %")
labelDiffPercent.grid(row=2, column=3)

labelIdealValues = tk.Label(root, text="Ideal values")
labelIdealValues.grid(row=2, column=4)

labelCurrentValues = tk.Label(root, text="Current values")
labelCurrentValues.grid(row=2, column=5)

labelDiffValue = tk.Label(root, text="Diff. in value")
labelDiffValue.grid(row=2, column=6)


# defining sectors
sectors = Tool.sectors

text1 = tk.StringVar(root, value=sectors[0])
text2 = tk.StringVar(root, value=sectors[1])
text3 = tk.StringVar(root, value=sectors[2])
text4 = tk.StringVar(root, value=sectors[3])
text5 = tk.StringVar(root, value=sectors[4])
text6 = tk.StringVar(root, value=sectors[5])
text7 = tk.StringVar(root, value=sectors[6])

# defining entries for sectors
entry1 = ttk.Entry(root, textvariable=text1)
entry2 = ttk.Entry(root, textvariable=text2)
entry3 = ttk.Entry(root, textvariable=text3)
entry4 = ttk.Entry(root, textvariable=text4)
entry5 = ttk.Entry(root, textvariable=text5)
entry6 = ttk.Entry(root, textvariable=text6)
entry7 = ttk.Entry(root, textvariable=text7)

# defining location of entries
entry1.grid(row=3, column=0)
entry2.grid(row=4, column=0)
entry3.grid(row=5, column=0)
entry4.grid(row=6, column=0)
entry5.grid(row=7, column=0)
entry6.grid(row=8, column=0)
entry7.grid(row=9, column=0)

# making empty entries
entryList = []
entryConfigList = []
for i in range(6):
    temp = []
    tempEntry = []
    for j in range(7):
        value = tk.StringVar()
        entry = ttk.Entry(root, textvariable=value)
        entry.grid(row=j + 3, column=i + 1)
        temp.append(value)
        tempEntry.append(entry)

    entryConfigList.append(tempEntry)
    entryList.append(temp)

root.mainloop()
