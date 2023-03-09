from tkinter import *
from tkinter.messagebox import *
from PIL import ImageTk, Image

import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
db=mydb.cursor()


# db.execute("CREATE TABLE users (name VARCHAR(255), income int,oid INT AUTO_INCREMENT PRIMARY KEY)")




root=Tk()
root.title('Bank')
h=Label(root, text="Apna Desi Bank",font=("Times", "24", "bold italic"),bg='#FFEF78')
root.geometry("410x412")
root['background']='#A8E7E9'
im = Image.open("Bank.jpg")
im= im.resize((300, 300))
my_im = ImageTk.PhotoImage(im)
bank_im= Label(image=my_im)
bank_im.grid(row=1,column=1,columnspan=3,rowspan=10)

h.grid(row=0,column=1,columnspan=3,pady=20)

def show():
    sroot = Toplevel(root)
    sroot.title("Users")
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
    sroot['background'] = '#FFDAB9'
    db = dbase.cursor()
    db.execute("SELECT *, oid FROM users ")
    records=db.fetchall()
    i=1
    Label(sroot, text='name', width=20).grid(row=0, column=0,pady=15)
    Label(sroot, text='amount', width=20).grid(row=0, column=1,pady=15)
    Label(sroot,text='id',width=20).grid(row=0,column=2,pady=30)
    for record in records:
        Label(sroot,text=record[0],width=20).grid(row=i,column=0,pady=10)
        Label(sroot, text=record[1], width=20).grid(row=i, column=1,pady=10)
        Label(sroot, text=record[2], width=20).grid(row=i, column=2,pady=10)
        i+=1
    exit = Button(sroot, text='Exit', command=sroot.destroy,width=100).grid(row=i, columnspan=3)
    


def add(name,income):
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")

    db = dbase.cursor()

    # Insert
    db.execute("INSERT INTO users (name, income) VALUES (%s, %s)",(name.get(),income.get()))
    

    dbase.commit()


    dbase.close()

    # Clear The Text Boxes
    name.delete(0, END)
    income.delete(0,END)




def create():
    
    aroot = Toplevel(root)

    name = Entry(aroot, width=30)
    name.grid(row=0, column=1, padx=20, pady=(10, 0))
    income = Entry(aroot, width=30)
    income.grid(row=1, column=1, padx=20, pady=(10, 0))

    
    name_label = Label(aroot, text='Enter name', width=10)
    name_label.grid(row=0, column=0, padx=10, pady=(10, 0))
    income_label = Label(aroot, text='Deposits', width=30)
    income_label.grid(row=1, column=0, padx=10, pady=(10, 0))
    Submit_button=Button(aroot, text='Submit',command =lambda :add(name,income),width=100).grid(row =2,columnspan=2,pady=10)
    exit = Button(aroot, text='Exit', command=aroot.destroy,width=100).grid(row =3,columnspan=2)

    return
def remove(idx):
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
  

    print(idx)
    db = dbase.cursor()

    db.execute("DELETE from users WHERE oid = " + idx)

    dbase.commit()
    dbase.close()

    return
def verify(name,idx):
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
    db=dbase.cursor()
    db.execute("SELECT  *,oid FROM users ")
    records=db.fetchall()
    for record in records:
        if(record[0]==name and str(record[2])==idx):
            return True

    dbase.commit()
    dbase.close()
    return False
def submit_delete(name,idx):
    name_1=name.get()
    idx_1=idx.get()
    if verify(name_1,idx_1):
        remove(idx_1)
        print(showinfo('successful','successfully deleted'))
        name.delete(0, END)
        idx.delete(0, END)
    else:
        print(showerror('error', 'invalid'))


def delete():

    droot = Toplevel(root)
    droot['background'] = '#A8E7E9'
    droot.title('Delete User')
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")

    db = dbase.cursor()
    db.execute("SELECT *, oid FROM users ")

    name = Entry(droot, width=30)
    name.grid(row=0, column=1, padx=20, pady=(10, 0))

    idx = Entry(droot, width=30)
    idx.grid(row=1, column=1, padx=20, pady=(10, 0))


    name_label = Label(droot, text='Enter name', width=10,bg='#A8E7E9')
    name_label.grid(row=0, column=0, padx=10, pady=(10, 0))


    idx_label = Label(droot, text='ID', width=10,bg='#A8E7E9')
    idx_label.grid(row=1, column=0, padx=10, pady=(10, 0))

    btn1=Button(droot, text="submit", command=lambda :submit_delete(name,idx),width=70).grid(row=2,columnspan=2,pady=10)
    exit = Button(droot, text='Exit', command=droot.destroy,width=70).grid(row=3, columnspan=2)


def update(t_id,id,amt,income,f_name,t_name):
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
    db = dbase.cursor()

    db.execute("SELECT  income FROM users where oid = " + t_id)
    t_income=(db.fetchall())[0][0]
    newm1 = amt+t_income
    val=(newm1,t_id)
    db.execute("UPDATE users SET income = %s where oid = %s",val)
               
    newm1=income-amt

    db.execute("UPDATE users SET income =%s where oid = %s ",(newm1,id))
    
    dbase.commit()
    dbase.close()

def submit(t_name,t_id,id,name,amt,income):
    if verify(t_name,t_id):
        if int(amt)<income:
            update(t_id,id,int(amt),income,name,t_name)
            print(showinfo('successful',"transaction complete"))
            money_root.destroy()
            troot.destroy()
        else:
            print(showerror('error','you dont have sufficient balance'))
    else:
        print(showerror('error',"invalid name or id"))


def money(idx,name):

    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")
    # Create cursor
    db = dbase.cursor()
    global money_root
    money_root = Tk()
    money_root.title("Transfer Money")

    db.execute("SELECT *, oid FROM users where oid = " +idx)
    record=(db.fetchall())[0]
    Label(money_root,text="name: "+record[0]).grid(row=0,column= 0,padx=20)
    Label(money_root,text="money: "+str(record[1])).grid(row=0,column= 1,padx=20)
    Label(money_root,text="transfer to: ").grid(row=1,column= 0,padx=10,pady=10)
    Label(money_root,text="amount: ").grid(row=3,column= 0)

    t_name=Entry(money_root,width=30)
    t_name.grid(row=1,column=1)
    t_name.insert(0,"Enter name")

    t_id = Entry(money_root, width=30)
    t_id.grid(row=2, column=1)
    t_id.insert(0, "Enter id")

    amt = Entry(money_root, width=30)
    amt.grid(row=3, column=1)

    Button(money_root,text="Transfer",command=lambda:submit(t_name.get(),t_id.get(),idx,name,amt.get(),record[1])).grid(row=4,column=1)
    dbase.commit()
    dbase.close()
    return

def submit_transfer(name,idx):
    if verify(name,idx):
        money(idx,name)
    else:
        print(showerror("invalid user"))
def transfer():

    global troot
    troot = Toplevel(root)

    troot.title("step1")
    dbase =  mysql.connector.connect(host="localhost",user="root",passwd="Harshit@123",database="user_book3")

    db = dbase.cursor()
    db.execute("SELECT *, oid FROM users ")
    records = db.fetchall()

    name = Entry(troot, width=30,font=30)
    name.grid(row=0, column=1, padx=20, pady=(10, 0))
    idx= Entry(troot, width=30,font=30)
    idx.grid(row=1, column=1, padx=20, pady=(10, 0))
    Button(troot,text='Submit',command=lambda:submit_transfer(name.get(),idx.get()),width=70,bg='#FA8072',font=30).grid(row=2,columnspan=2,pady=10)

    name_label = Label(troot, text='Enter name', width=10,font=30)
    name_label.grid(row=0, column=0, padx=10, pady=(10, 0))

    idx_label = Label(troot, text='id', width=30,font=30)
    idx_label.grid(row=1, column=0, padx=10, pady=(10, 0))
    dbase.commit()
    dbase.close()


db.execute("SELECT *, oid FROM users ")
rec=db.fetchall()
print(rec)
cbutton=Button(root, text='CREATE USERS', command=create,width=14).grid(row=1,column=0,pady=5,padx=3)
dbutton=Button(root, text='DELETE USERS', command=delete,width=14).grid(row=2,column=0,pady=5,padx=3)



tbutton=Button(root, text="TRANSFER MONEY", command=transfer,width=14).grid(row=3,column=0,pady=5,padx=3)
sbutton=Button(root, text="SHOW USERS", command=show,width=14).grid(row=4,column=0,pady=5,padx=3)
Button(root, text="EXIT", command=root.destroy,width=14).grid(row=5,column=0,pady=5)


root.mainloop()