#import ambrosia
from Tkinter import *
import csv

root = Tk()

root.title("Recepies Network")

ingredients=[]
ingredients_to_search=[]

with open("header.csv") as resultFile:
   rr = csv.reader(resultFile)
   for row in rr:
       ingredients=row[2:]

def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, root.END)
        print(self.entry.get())


var_1 = StringVar(root)

label_1 = Label(root, text="Search Recipes:")
entry_1 = Entry(root)  # this should search through the strings listed under listbox_2 configs
ingredients_to_search=entry_1.get()


def searchButton():
    print (entry_1.get())
    ingredients_to_search=entry_1.get().split(',')
    print(ingredients_to_search)
    entry_1.delete(0,END)

button_1 = Button(root, text="Search", command=searchButton)



def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print 'You selected item %d: "%s"' % (index, value)
    if(entry_1.get()==""):
        entry_1.insert(0,  value)
    else:
        entry_1.insert(0,entry_1.get()+", "+value)



label_2 = Label(root, text="List of Ingredients")
scrollbar_1 = Scrollbar(root)
listbox_2 = Listbox(root, yscrollcommand=scrollbar_1.set)
listbox_2.bind('<<ListboxSelect>>', onselect)


scrollbar_1.config(command=listbox_2.yview)

string_list=[]
for i in ingredients:
    string_list.append(StringVar(root, name=i))

count=1
for i in string_list:
    listbox_2.insert(count,i)
    count+=1



# grid additions
root.geometry("700x600")
label_1.grid(columnspan=2, row=0, column=15)
entry_1.grid(columnspan=2, row=1, column=16)
button_1.grid(columnspan=2, row=2, column=15)

label_2.grid(row=0, column=0)
listbox_2.grid(rowspan=6, columnspan=6, row=1, column=0)
scrollbar_1.grid(rowspan=6, row=2, column=4, sticky=N + S)

root.mainloop()
