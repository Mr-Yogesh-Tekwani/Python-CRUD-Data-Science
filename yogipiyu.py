from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext
import cx_Oracle
import time
import os
import bs4
import requests
import socket
from PIL import ImageTk,Image

win=Tk()
win.geometry("1200x550+50+50")
win.title("Splash")
canvas=Canvas(win,width=1200,height=550)
canvas.pack()

try:
	socket.create_connection(("www.google.com",80))
	res=requests.get("http://ipinfo.io/")
	
	data=res.json()
	city=data['city']
	api_address="http://api.openweathermap.org/data/2.5/weather?units=metric"+"&q="+city+"&appid=cfb3925b639b3f91651bf0a43298d18f"
	lable1=Label(win,text=city,bg="Black",fg='White',font=("Times",15,"bold"))
	lable1.place(x=6,y=515)
	res=requests.get(api_address)
	wdata=requests.get(api_address).json()
	temp=wdata['main']['temp']
	lable2=Label(win,text="Temp= "+str(temp),bg="Black",fg='White',font=("Times",15,"bold"))
	lable2.place(x=1090,y=515)
	res=requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup=bs4.BeautifulSoup(res.text,'lxml')

	quote=soup.find('img',{"class":"p-qotd"})


	image_url="https://www.brainyquote.com"+ quote['data-img-url']
	r=requests.get(image_url)
	from datetime import datetime
	dt=datetime.now().time()
	t=str(dt.hour)+","+str(dt.minute)+","+str(dt.second)+".jpg"
	image_name=t
	#print(image_name)
	
	with open(image_name,'wb') as f:
		f.write(r.content)
except OSError:
	print("check network")
img=ImageTk.PhotoImage(Image.open(image_name))
canvas.create_image(1,1,anchor=NW,image=img)
win.after(3000,win.destroy)
win.mainloop()

root=Tk()
root.title("Student Management System")
root.geometry("1200x1200+50+50")

vist=Toplevel(root)
vist.title("View Student")
vist.geometry("1200x1200+50+50")
vist.withdraw()
stViewData=scrolledtext.ScrolledText(vist,width=60,height=40,font="Arial 9 italic bold")

upst=Toplevel(root)
upst.title("Update Student")
upst.geometry("1200x1200+50+50")
upst.withdraw()

dest=Toplevel(root)
dest.title("Delete Student")
dest.geometry("1200x1200+50+50")
dest.withdraw()




def f4():
	root.deiconify()
	vist.withdraw()
	stViewData.configure(state=NORMAL)
	stViewData.delete('1.0',END)
	
btnViewBack=Button(vist,text="Back",command=f4,font="Arial 20 bold",fg="Black",bg="White")
stViewData.pack()
btnViewBack.pack()

adst=Toplevel(root)
adst.title("Add Student")
adst.geometry("1200x1200+50+50")
adst.withdraw()


lblRno=Label(adst,text="Enter rno",font="Arial 20 bold",fg="Blue",bg="White")
entRno=Entry(adst,bd=7,font="Arial 20 bold",fg="White",bg="Blue")
lblName=Label(adst,text="Enter name",font="Arial 20 bold",fg="Blue",bg="White")
entName=Entry(adst,bd=7,font="Arial 20 bold",fg="White",bg="Blue")
genders=IntVar()
genders.set(1)
rbMale=Radiobutton(adst,text="Male",variable=genders,value=1,font=('Times',25,'bold'),fg="Black")
rbFemale=Radiobutton(adst,text="Female",variable=genders,value=2,font=('Times',25,'bold'),fg="Black")
'''subject=Label(adst,text="Courses:",font=('ariel',25,'bold'),fg="Blue",bg="White")

cMysql=IntVar()
cbMysql=Checkbutton(adst,text="MySQL",variable=cMysql,font=('Times',15,'bold'),fg="White",bg="Blue")
cbMysql.place(x=700,y=375)

cJava=IntVar()
cbJava=Checkbutton(adst,text="Java",variable=cJava,font=('Times',15,'bold'),fg="White",bg="Blue")
cbJava.place(x=420,y=310)

cPython=IntVar()
cbPython=Checkbutton(adst,text="Python",variable=cPython,font=('Times',15,'bold'),fg="White",bg="Blue")
cbPython.place(x=420,y=375)

cAndroid=IntVar()
cbAndroid=Checkbutton(adst,text="Android",variable=cAndroid,font=('Times',15,'bold'),fg="White",bg="Blue")
cbAndroid.place(x=700,y=310)'''	
def f5():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		print('connected')
		#if cJava.get()==1:
			#course=course+"Java,"
		#if cPython.get()==1:
			#course=course+"Python,"
		#if cAndroid.get()==1:
			#course=course+"Android,"
		#if cMysql.get()==1:
			#course=course+"MySQL,"  '''
		#messagebox.showerror("Isuue",course) '''
		
		g=genders.get()
		if g==1:
			gender='Male'
		else:
			gender='Female'
			
					
	

		rno=entRno.get()
		name=entName.get()
			

		if rno=='':
			messagebox.showerror("Isuue","Enter the Rollno please")
		elif rno.isalpha():
			messagebox.showerror("Isuue","Enter valid Rollno please")
		elif name=='':
			messagebox.showerror("Isuue","Enter some alphabets please")
		elif name.isdigit():
			messagebox.showerror("Isuue","Enter valid name please")								
		else:
			rno=int(rno)
			cursor=con.cursor()
			sql="insert into students values('%d','%s','%s')"
			args=(rno,name,gender)
			cursor.execute(sql % args)
			con.commit()
			#print(cursor.rowcount,"record inserted ")
			messagebox.showinfo("Sucess",str(cursor.rowcount)+"records inserted")
			
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		print("issue ",e)
		messagebox.showinfo("Failure","issue"+str(e))
			
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

btnAddSave=Button(adst,text="Save",command=f5,font="Arial 20 bold",fg="White",bg="Blue")

def f2():
	root.deiconify()
	adst.withdraw()
btnAddBack=Button(adst,text="Back",command=f2,font="Arial 20 bold",fg="White",bg="Blue")

lblRno.pack(pady=10)
entRno.pack(pady=10)
lblName.pack(pady=10)
entName.pack(pady=10)
rbMale.place(x=400,y=250)
rbFemale.place(x=700,y=250)
#subject.place(x=200,y=300)

btnAddSave.place(x=600,y=450)
btnAddBack.place(x=600,y=550)  





def f1():
	adst.deiconify()
	root.withdraw()
welcome=Label(root,text="YOGESH.T  D7A  68",font=('Quantify',50,'bold'),fg="Black",bg="White")
welcome.pack(pady=25)
btnAdd=Button(root,text="Add a Student",command=f1,font="Arial 20 bold",fg="White",bg="Blue")
#------------------------view starts-----------------------------------------------------------
def f3():
	vist.deiconify()
	root.withdraw()
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		print('connected')
		sql="select * from students order by rno"
		cursor=con.cursor()
		cursor.execute(sql)
		rows=cursor.fetchall()
		info=""
		for r in rows:
			print("rno ",r[0],"name ",r[1],"gender ",r[2])
			info=info+" rno "+str(r[0])+" name "+r[1]+" gender "+r[2]+"\n"
		stViewData.insert(INSERT,info)
		stViewData.configure(state=DISABLED)
			
	except cx_Oracle.DatabaseError as e:
		print("issue ",e)
			
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnView=Button(root,text="View the Students",command=f3,font="Arial 20 bold",fg="White",bg="Blue")
btnAdd.pack(pady=25)
btnView.pack(pady=25)
#-----------------update starts---------------------------------------------------
lblUpRno=Label(upst,text="Enter rno",font="Arial 20 bold",fg="Blue",bg="White")
entUpRno=Entry(upst,bd=7,font="Arial 20 bold",fg="White",bg="Blue")
lblUpName=Label(upst,text="Enter name",font="Arial 20 bold",fg="Blue",bg="White")
entUpName=Entry(upst,bd=7,font="Arial 20 bold",fg="White",bg="Blue")
def f8():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		s1=entUpRno.get()
		n1=entUpName.get()
		if s1=='':
			messagebox.showerror("Isuue","Enter the Rollno please")
		elif s1.isalpha():
			messagebox.showerror("Isuue","Enter valid Rollno to update")
		elif n1=='':
			messagebox.showerror("Isuue","Enter some name")
		elif n1.isdigit():
			messagebox.showerror("Isuue","Enter valid new name")								
		else:
			s1=int(s1)			
			cursor=con.cursor()
			sql="update students set name='%s' where rno='%d'"
			args=(n1,s1)
			cursor.execute(sql % args)
			con.commit()
			#print(cursor.rowcount,"rows updated")
			messagebox.showinfo("Sucess",str(cursor.rowcount)+" record updated")	
		
			
	except cx_Oracle.DatabaseError as e:
		print("issue ",e)
		messagebox.showinfo("Failure","issue"+str(e))
			
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	
btnUpSave=Button(upst,text="Save",command=f8,font="Arial 20 bold",fg="White",bg="Blue")

def f7():
	root.deiconify()
	upst.withdraw()
btnUpBack=Button(upst,text="Back",command=f7,font="Arial 20 bold",fg="White",bg="Blue")

lblUpRno.pack(pady=10)
entUpRno.pack(pady=10)
lblUpName.pack(pady=10)
entUpName.pack(pady=10)
btnUpSave.pack(pady=10)
btnUpBack.pack(pady=10)



def f6():
	upst.deiconify()
	root.withdraw()
btnUpdate=Button(root,text="Update a Student",command=f6,font="Arial 20 bold",fg="White",bg="Blue")
btnUpdate.pack(pady=25)
#-------------------------------------------------------------

lblDeRno=Label(dest,text="Enter rno",font="Arial 20 bold",fg="Blue",bg="White")
entDeRno=Entry(dest,bd=7,font="Arial 20 bold",fg="White",bg="Blue")
def f10():
	con=None
	cursor=None
	try:
		con=cx_Oracle.connect("system/abc123")
		s2=entDeRno.get()
		if s2=='':
			messagebox.showerror("Isuue","Enter the Rollno to be deleted")
		elif s2.isalpha():
			messagebox.showerror("Isuue","Enter valid Rollno to remove")			
		else:
			s2=int(s2)
			cursor=con.cursor()
			sql="delete from students where rno='%d'"
			args=(s2)
			cursor.execute(sql % args)
			con.commit()
			#print(cursor.rowcount,"rows deleted")
			messagebox.showinfo("Sucess",str(cursor.rowcount)+" record deleted")	
			
		
			
	except cx_Oracle.DatabaseError as e:
		print("issue ",e)
		messagebox.showinfo("Failure","issue"+str(e))	
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
btnDeSave=Button(dest,text="Save",command=f10,font="Arial 20 bold",fg="White",bg="Blue")

def f9():
	root.deiconify()
	dest.withdraw()
btnDeBack=Button(dest,text="Back",command=f9,font="Arial 20 bold",fg="White",bg="Blue")

lblDeRno.pack(pady=10)
entDeRno.pack(pady=10)
btnDeSave.pack(pady=10)
btnDeBack.pack(pady=10)

def f8():
	dest.deiconify()
	root.withdraw()
btnDelete=Button(root,text="Delete a Student",command=f8,font="Arial 20 bold",fg="White",bg="Blue")
btnDelete.pack(pady=25)
root.mainloop()
