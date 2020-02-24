from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import time
import datetime
from get_city import get_city_name
from get_weather import getweather
from download_image import a_image_download
from PIL import Image
from PIL import ImageTk
from get_weather import *
from matplotlib import pyplot as plt


class Splash(Toplevel):
	def __init__(self, parent):
		Toplevel.__init__(self, parent)
		self.title("Student Management System")
		self.geometry("400x400+200+200")

		a_image_download()

		load = Image.open("quote_of_day "+ str(datetime.datetime.now().date()) +".jpg" )
		load = load.resize((400, 250), Image.ANTIALIAS)
		render = ImageTk.PhotoImage(load)

		img = Label(self, image=render)
		img.grid(row=0,columnspan=2)

		city = get_city_name()
		weather = getweather(city)

		lblCity = Label(self, text="City:"+str(city))
		lblWeather = Label(self, text="Weather:"+str(weather)+"°C")
		lblCity.grid(row=1,padx=50)
		lblWeather.grid(row=1,column=1,padx=50)

		## required to make window show before the program gets to the mainloop
		self.update()

class root(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.withdraw()
        splash = Splash(self)

        ## simulate a delay while loading
        time.sleep(4)

        ## finished loading so destroy splash
        splash.destroy()

        ## show window again
        self.deiconify()

root = root()
root.title("Student Management System")
root.geometry("400x400+200+200")

# root window widgets

def click_on_add():
	add_student.deiconify()
	root.withdraw()

btnAdd = Button(root, text="Add Student", command = click_on_add)
btnAdd.pack(pady=10)


def click_on_view():
	view_student.deiconify()
	root.withdraw()
	stViewData.config(state=NORMAL)
	stViewData.delete("1.0",END)
	rows = view_all()
	if rows is not None:
		info = ""			
		for r in rows:
			info += "Rno:" + str(r[0]) + "\t\tName:" + str(r[1]) + "\t\tMarks:" + str(r[2]) + '\n'
		stViewData.insert(INSERT, info)
	else:
		stViewData.insert(INSERT, "No records avaialble")
	stViewData.config(state = DISABLED)
btnView = Button(root, text="View Student", command = click_on_view)
btnView.pack(pady=10)


def click_on_update():
	update_student.deiconify()
	root.withdraw()
btnUpdate = Button(root, text="Update Student", command = click_on_update)
btnUpdate.pack(pady=10)


def click_on_delete():
	delete_student.deiconify()
	root.withdraw()
btndelete = Button(root, text="Delete Student", command = click_on_delete)
btndelete.pack(pady=10)

def click_on_graph():
	rows = view_all()
	if rows is not None:
		info = {}
		for r in rows:
			info[str(r[1])] = r[2]
		plt.bar(info.keys(), info.values(), width=0.25)
		plt.show()

btnShowGraph = Button(root, text="Show Marks Graph",command=click_on_graph)
btnShowGraph.pack(pady=10)

# root window widgets done

# add_student window widgets

add_student = Toplevel(root)
add_student.title("Add Student")
add_student.geometry("400x400+200+200")
add_student.withdraw()

addLblRno = Label(add_student, text="Enter Roll No:")
addEntRno = Entry(add_student, bd = 5)
addLblName = Label(add_student, text="Enter Name:")
addEntName = Entry(add_student, bd = 5)
addLblMarks = Label(add_student, text="Enter Marks:")
addEntMarks = Entry(add_student, bd = 5)

# functions for click on save of addWindow to insert a record into db
def insert(rno,name,marks):
	try:
		conn = cx_Oracle.connect('system/abc123@localhost')
		print("Connected")
		cursor = conn.cursor()
		sql =  "insert into student values('%d','%s','%d')"
		args = (rno,name,marks)
		cursor.execute(sql % args)
		conn.commit()
		return True
	except cx_Oracle.DatabaseError as e:			
		conn.rollback()
		messagebox.showerror("Failure","Can't Add "+name+"\nIssue is:"+str(e))
		return False
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()
			print("Disconnected")
def add_save_student():
	try:
		rno = int(addEntRno.get().strip())
		if rno <= 0:
			messagebox.showerror("Failure","Roll No's are Positive only!!")
			return
		marks = int(addEntMarks.get().strip())
		if marks <= 0 or marks > 100:
			messagebox.showerror("Failure","Marks are Between 0 and 100 only!!")
			return
		name = addEntName.get().strip()
		if (not name.isalpha()) or len(name)<=0:
			messagebox.showerror("Failure","Names are Alphabets Only")
			return
		if insert(rno, name, marks):
			messagebox.showinfo("Success", "Inserted")
			print("Inserted")
		else:
			messagebox.showerror("error", "Not Inserted")
	except ValueError:
		messagebox.showerror("Failure","Please Enter Integers Only")
	finally:
		addEntRno.delete(0,END)
		addEntName.delete(0,END)
		addEntMarks.delete(0,END)

addBtnSave = Button(add_student, text = "Save", command = add_save_student)

def add_back_student():
	add_student.withdraw()
	root.deiconify()
addBtnBack = Button(add_student, text = "Back", command = add_back_student)

addLblRno.pack(pady=10)
addEntRno.pack(pady=10)
addLblName.pack(pady=10)
addEntName.pack(pady=10)
addLblMarks.pack(pady=10)
addEntMarks.pack(pady=10)
addBtnSave.pack(pady=10)
addBtnBack.pack(pady=10)


# add_student window done

# view_student window widgets

view_student = Toplevel(root)
view_student.title("View Student")
view_student.geometry("400x400+200+200")
view_student.withdraw()
stViewData = scrolledtext.ScrolledText(view_student, width=30, height=10)
stViewData.pack()

def view_all():
	try:
		conn = cx_Oracle.connect('system/abc123@localhost')
		print("Connected")
		cursor = conn.cursor()
		sql =  "select * from student"
		cursor.execute(sql)
		rows = cursor.fetchall()
		return rows
	except cx_Oracle.DatabaseError as e:			
		messagebox.showerror("Failure","Issue is:"+str(e))
		return None
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()
			print("Disconnected")

def view_back_student():
	view_student.withdraw()
	root.deiconify()
	stViewData.delete("1.0", END)
viewBtnBack = Button(view_student, text = "Back", command = view_back_student)
viewBtnBack.pack()
# view_student window done

# update_student widgets window
update_student = Toplevel(root)
update_student.title("Update Student")
update_student.geometry("400x400+200+200")
update_student.withdraw()


updateLblRno = Label(update_student, text="Enter Roll No To Update:")
updateEntRno = Entry(update_student, bd = 5)
updateLblName = Label(update_student, text="Enter updated Name:")
updateEntName = Entry(update_student, bd = 5)

updateLblRno.pack(pady=10)
updateEntRno.pack(pady=10)
updateLblName.pack(pady=10)
updateEntName.pack(pady=10)

def update(rno,name):
	try:
		conn = cx_Oracle.connect('system/abc123@localhost')
		print("Connected")
		cursor = conn.cursor()
		sql =  "update student set name='%s' where rno ='%d'"
		args = (name,rno)
		cursor.execute(sql % args)
		conn.commit()
		return True
	except cx_Oracle.DatabaseError as e:			
		conn.rollback()
		messagebox.showerror("Failure","Can't Update"+str(rno)+"\nIssue is:"+str(e))
		return False
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()
			print("Disconnected")
def update_save_student():
	try:
		rno =  int(updateEntRno.get().strip())
		if rno <= 0:
			messagebox.showerror("Failure","Roll No's are Positive only!!")
			return
		name = updateEntName.get().strip()
		if (not name.isalpha()) or len(name)<=0:
			messagebox.showerror("Failure","Names are Alphabets Only")
			return
		if update(rno,name):
			messagebox.showinfo("Success","Updated")
		else:
			messagebox.showerror("Failure","Can't Update")
	except ValueError:
		messagebox.showerror("Failure","Please Enter Integers Only")
	finally:
		updateEntRno.delete(0,END)
		updateEntName.delete(0,END)
updateBtnSave = Button(update_student, text = "Save", command = update_save_student)
updateBtnSave.pack(pady=10)

def update_back_student():
	update_student.withdraw()
	root.deiconify()
updateBtnBack = Button(update_student, text = "Back", command = update_back_student)
updateBtnBack.pack(pady=10)
# update student window done

#delete student window started

delete_student = Toplevel(root)
delete_student.title("Delete Student")
delete_student.geometry("400x400+200+200")
delete_student.withdraw()

deleteLblRno = Label(delete_student, text="Enter Roll No To Delete:")
deleteEntRno = Entry(delete_student, bd = 5)

deleteLblRno.pack(pady=10)
deleteEntRno.pack(pady=10)

def delete(rno):
	try:
		conn = cx_Oracle.connect('system/abc123@localhost')
		print("Connected")
		cursor = conn.cursor()
		sql =  "delete from student where rno = '%d'"
		args = (rno)
		cursor.execute(sql % args)		
		conn.commit()
		if cursor.rowcount == 0:
			print("Can't Delete")
			messagebox.showwarning("Failure","Roll No doesn't exist!!")
			return False
		return True
	except cx_Oracle.DatabaseError as e:			
		cursor.rollback()
		messagebox.showerror("Failure","Can't Delete"+str(rno)+"\nIssue is"+str(e))
		return False
	finally:
		if cursor is not None:
			cursor.close()
		if conn is not None:
			conn.close()
			print("Disconnected")
def delete_a_student():
	try:
		rno = int(deleteEntRno.get().strip())
		if rno<0:
			messagebox.showerror("Failure","Roll Nos are Positive")
			return
		if delete(rno):
			messagebox.showinfo("Success","Deleted Successfully!!")
		else:
			messagebox.showerror("Failure","Can't Delete")
	except ValueError:
		messagebox.showerror("Failure","Please Enter Integers Only")
	finally:
		deleteEntRno.delete(0,END)
deleteBtnSave = Button(delete_student, text = "Delete", command = delete_a_student)
deleteBtnSave.pack(pady=10)

def delete_back_student():
	delete_student.withdraw()
	root.deiconify()
deleteBtnBack = Button(delete_student, text = "Back", command = delete_back_student)
deleteBtnBack.pack(pady=10)
#delete window completed

root.mainloop()