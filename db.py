from Tkinter import *
from sqlite3 import *
from tkFileDialog import askopenfilename
from tkMessageBox import *
from ScrolledText import *
import time
import thread

global column_name
global column_type
global db


class ui():
    def __init__(self):
##        root.withdraw()
##        root.iconify()
##        root.deiconify()
##        root.overrideredirect(True)
        
        root.title('Database Manager')
##        root.iconbitmap(r'C:\Python27\programs\GUI\Database\icon.ico')
        root.resizable(width=False,height=False)
        menu = Menu(root)
        root.config(menu=menu,bg = 'skyblue')
        databaseMenu = Menu(menu,bg='white')
        menu.add_cascade(label='Database',menu=databaseMenu)
        databaseMenu.add_command(label='Create Database',command=self.f_create_database)
        databaseMenu.add_command(label='Choose Database',command=self.f_sdb)
        tableMenu = Menu(menu,bg='white')
        
        menu.add_cascade(label='Table',menu=tableMenu)
        tableMenu.add_command(label='Create Table',command=self.f_create_table)
        tableMenu.add_command(label='Choose Table',command=self.f_choose_table)
        tableMenu.add_command(label='Insert into Table',command=self.f_insert)
        tableMenu.add_command(label='Update Table',command=self.f_update)
        tableMenu.add_command(label='Delete From Table',command=self.f_dft)
        tableMenu.add_command(label='Show Table',command=self.f_show)
        tableMenu.add_command(label='Select From Table',command=self.f_sft)
        tableMenu.add_command(label='Delete Table',command=self.f_delete_t)
        toolsMenu = Menu(menu,bg='white')
        menu.add_cascade(label='Tools',menu=toolsMenu)
##        toolsMenu.add_command(label='Import Table from Excel',command=self.void)
        toolsMenu.add_command(label='Export Table in Excel',command=self.f_export)
        toolsMenu.add_command(label='SQL Query Executer',command=self.f_sqle)
        
        self.b_create_database = Button(root,text='Create Database',width=20,height=1,bg='lightgreen',command=self.f_create_database)
        self.b_choose_database = Button(root,text='Choose Database',width=20,height=1,bg='lightgreen',command=self.f_sdb)
        self.b_create_table = Button(root,text='Create Table',width=20,height=1,bg='lightgreen',command=self.f_create_table)
        self.b_choose_table = Button(root,text='Choose Table',width=20,height=1,bg='lightgreen',command=self.f_choose_table)
        self.b_insert = Button(root,text='Insert Into Table',width=20,height=1,bg='lightgreen',command=self.f_insert)
        self.b_update = Button(root,text='Update Table',width=20,height=1,bg='lightgreen',command=self.f_update)
        self.b_delete = Button(root,text='Delete From Table',width=20,height=1,bg='lightgreen',command=self.f_dft)
        self.b_show = Button(root,text='Show Table',width=20,height=1,bg='lightgreen',command=self.f_show)
        self.b_select = Button(root,text='Select From Table',width=20,height=1,bg='lightgreen',command=self.f_sft)
        self.b_drop = Button(root,text='Delete Table',width=20,height=1,bg='lightgreen',command=self.f_delete_t)


        self.l_database = Label(root,text='Database:',bg = 'skyblue')
        self.l_table = Label(root,text='Table:',bg = 'skyblue')

        self.b_create_database.grid(row=3,padx=7,pady=2)
        self.b_choose_database.grid(row=4,padx=7,pady=2)
        self.b_create_table.grid(row=5,padx=7,pady=2)
        self.b_choose_table.grid(row=6,padx=7,pady=2)
        self.b_insert.grid(row=7,padx=7,pady=2)
        self.b_show.grid(row=8,padx=7,pady=2)
        self.b_select.grid(row=9,padx=7,pady=2)
        self.b_update.grid(row=10,padx=7,pady=2)
        self.b_delete.grid(row=11,padx=7,pady=2)
        self.b_drop.grid(row=12,padx=7,pady=2)

        

        self.log = ScrolledText(root,bd=5)
        self.log.tag_configure('warning',foreground='red')
        self.log.tag_configure('success',foreground='green')
        self.log.tag_configure('normal',foreground='blue')

        
        self.l_database.grid(row=0,column=1,sticky='w')
        self.l_table.grid(row=1,column=1,sticky='w')
        self.log.grid(row=3,column=1,rowspan=30,padx=7,pady=7)
        
        self.allset = 0



    def f_create_database(self):
        self.cdb_win = Toplevel(root)
        l_cdb = Label(self.cdb_win,text='Name of Database: ')
        self.e_cdb = Entry(self.cdb_win)
        b_cdb = Button(self.cdb_win,text='Create',command=self.cdb)
        l_cdb.grid(row=0)
        self.e_cdb.grid(row=0,column=1)
        b_cdb.grid(row=0,column=2)
        self.set_toplevel(self.cdb_win)

        

    def cdb(self):
        global db
        db = self.e_cdb.get()
        if db == '':
            self.log.insert(END,'>>> Database Name Can Not be Empty\n','warning')
            self.cdb_win.destroy()
            return
        db = db+'.db'
        print db
        try:
            global connection
            connection = connect(db)
            global c
            c = connection.cursor()
        except Exception as e:
            self.log.insert(END,'>>> '+str(e)+'\n','warning')
        else:
            self.allset = 1
            self.log.insert(END,'>>> Database '+db+' is Created\n','success')
            self.l_database.config(text='Database: '+db)
            self.l_table.config(text='Table: ')
        self.cdb_win.destroy()
        

    def f_sdb(self):
        global db
        db = askopenfilename(filetypes=[('Databse','*.db')])
        print db
        if db == '':
            self.log.insert(END,'>>> No Database Selected\n','normal')
            return
        try:
            global connection
            connection = connect(db)
            global c
            c = connection.cursor()
        except Exception as e:
            self.log.insert(END,'>>> '+str(e)+'\n','warning')
        else:
            self.allset = 1
            self.log.insert(END,'>>> Database '+db+' is Selected\n','success')
            self.l_database.config(text='Database: '+db)
            self.l_table.config(text='Table: ')
        

    
    def f_create_table(self):
        if self.allset == 0:
            self.log.insert(END,'>>> Select/Create a Database to Create Table\n','warning')
            return
        self.ct_win = Toplevel(root)
        l_column_name = Label(self.ct_win,text='Enter Column Name ("," Saperated):',pady=5).grid(row=0,sticky='E')
        l_column_type = Label(self.ct_win,text='Enter Column Type ("," Saperated):',pady=5).grid(row=1,sticky='E')
        l_table_name = Label(self.ct_win,text='Enter Table Name:',pady=5).grid(row=2,sticky='E')
        self.e_column_name = Entry(self.ct_win,width=40)
        self.e_column_type = Entry(self.ct_win,width=40)
        self.e_table_name = Entry(self.ct_win,width=40)
        self.e_column_name.grid(row=0,column=1)
        self.e_column_type.grid(row=1,column=1)
        self.e_table_name.grid(row=2,column=1)
        b_ct = Button(self.ct_win,text='Create Table',command=self.ct).grid(row=3,column=1)
        self.set_toplevel(self.ct_win)

        
    def ct(self):
        qp = ''
        global column_name
        global column_type
        column_name = self.e_column_name.get().split(',')
        column_type = self.e_column_type.get().split(',')
        self.table_name = self.e_table_name.get()
        if len(column_name) != len(column_type):
            self.log.insert(END,'>>> Error: Wrong Inputs\n','warning')
            self.ct_win.destroy()
            return
        for i,v in enumerate(column_name):
            qp = qp + v + ' ' +  column_type[i] + ','
        qp = qp[:-1]
        query = 'create table '+self.table_name+' ('+qp+')'
        try:
            c.execute(query)
        except Exception as e:
            self.log.insert(END,'>>> '+str(e)+'\n''warning')
        else:
            self.allset = 2
            self.log.insert(END,'>>> Table '+self.table_name+' is Created\n','success')
            self.l_table.config(text='Table: '+self.table_name)
            print '>>> Table '+self.table_name+' is Created'
        self.ct_win.destroy()

    def f_choose_table(self):
        if self.allset == 0:
            self.log.insert(END,'>>> Select/Create a Database to Create Table\n','warning')
            return
        self.v = IntVar()
        self.v.set(-1)
        self.st_win = Toplevel(root)
        try:
            c.execute('select name from sqlite_master where type="table"')
            self.l = c.fetchall()
            if len(self.l) == 0:
                self.log.insert(END,'>>> Database '+db+' has no Table\n','normal')
                self.st_win.destroy()
                return
            Label(self.st_win,text='Select a Table: ',width=30).grid(row=0)
            for i,l_tables in enumerate(self.l):
                Radiobutton(self.st_win,text=l_tables[0],variable=self.v,indicatoron=0,command=self.st,value=i,width=20).grid(row=(i+1),column=0,pady=5)
        except Exception as e:
            self.log.insert(END,'>>> '+str(e)+'\n','warning')
        self.set_toplevel(self.st_win)


    def st(self):
        self.table_name = self.l[self.v.get()][0]
        global column_name
        global column_type
        c.execute('select * from '+self.table_name)
        column_name = [i[0] for i in c.description]
        c.execute('select sql from sqlite_master where name = "'+self.table_name+'"')
        sql = c.fetchone()[0]
        sql = sql[sql.index('(')+1:-1]
        p = [i.split(" ")[1] for i in sql.split(',')]
        column_type = p
        self.st_win.destroy()
        self.allset = 2
        self.log.insert(END,'>>> Table '+self.table_name+' is Selected\n','success')
        self.l_table.config(text='Table: '+self.table_name)
        print '>>> Table '+self.table_name+' is Selected'


    def f_insert(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Insert\n','warning')
            return
        global e
        l = []
        e = []
        self.i_win = Toplevel(root)
        for i,cn in enumerate(column_name):
            e.append(Entry(self.i_win))
            l.append(Label(self.i_win,text=cn+" ("+column_type[i]+") : ",pady=3))
            l[i].grid(row=i,column=0,sticky='E')
            e[i].grid(row=i,column=1)
        Button(self.i_win,text='Insert Data',command=self.insert).grid(row=len(e),column=1)
        self.set_toplevel(self.i_win)

    def insert(self):
        qp = ''
        for i,v in enumerate(e):
            if column_type[i] == 'text':
                qp = qp + "'"+v.get()+"'" + ','
            else:
                if v.get()!='':
                    qp = qp +v.get() + ','
                else:
                    qp=qp + "'',"
        qp = qp[:-1]
        query = 'insert into '+self.table_name+' values('+qp+')'
        try:
            print '>>> ' + query
            c.execute(query)
            connection.commit()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
        else:
            self.log.insert(END,'>>> 1 row Affected\n','normal')
        self.i_win.destroy()
        self.f_insert()


    def f_show(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Show Table\n','warning')
            return
        try:
            query = 'select * from '+self.table_name
            print '>>> ' + query
            c.execute(query)
            val = c.fetchall()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
            return

        qp = '|'
        select_win = Toplevel(root)
        select_win.title('Table: '+self.table_name)
        for i,v in enumerate(column_name):
            qp = qp + v + ' (' + column_type[i]+')' + '\t|\t'
            Label(select_win,text=str(v)+' ('+column_type[i]+')',width='20',bg='blue',fg='yellow').grid(row=1,column=i,pady=4,padx=2,ipady=5)
        self.log.insert(END,'>>> RESULT <<<\n','normal')
        self.log.insert(END,qp+'\n','success')
        
        for r,v in enumerate(val):
            qp='|'
            for col,i in enumerate(v):
                Label(select_win,text=str(i),width='20',bg='white').grid(row=r+2,column=col,pady=2,padx=2)
                qp = qp + str(i) + '\t|\t'    
            self.log.insert(END,qp+'\n')
        
        self.set_toplevel(select_win)


    def f_sft(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Select From Table\n','warning')
            return
        self.sft_win = Toplevel(root)
        Label(self.sft_win,text='Select Columns to Show').grid(row=0,columnspan=2)
        self.vars=[]
        for i,v in enumerate(column_name):
            var = IntVar()
            Checkbutton(self.sft_win,text=v,variable=var).grid(row=i+1,padx=10,sticky='w')
            self.vars.append(var)
        self.e_s_c = Entry(self.sft_win)
        Label(self.sft_win,text='where').grid(row=len(column_name)+1,sticky='E')
        self.e_s_c.grid(row=len(column_name)+1,column=1)
        Button(self.sft_win,text='Select',width=20,command=self.sft).grid(row=len(column_name)+2,columnspan=2,padx=10,pady=5)
        self.set_toplevel(self.sft_win)


    def sft(self):
        qp = 'select '

        for i,v in enumerate(column_name):
            if self.vars[i].get() == 1:
                qp = qp + column_name[i] + ','
        qp = qp[:-1] + ' from ' + self.table_name
        if self.e_s_c.get() != '':
            qp = qp + ' where ' +self.e_s_c.get()
        print qp
        try:
            print '>>> ' + qp
            c.execute(qp)
            val = c.fetchall()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
            return

        qp = '|'
        col = 0
        select_win = Toplevel(root)
        for i,v in enumerate(column_name):
            if self.vars[i].get() == 1:
                qp = qp + v + ' (' + column_type[i]+')' + '\t|\t'
                Label(select_win,text=str(v)+' ('+column_type[i]+')',width='20',bg='blue',fg='yellow').grid(row=1,column=col,pady=4,padx=2,ipady=5)
                col+=1
        self.log.insert(END,'>>> RESULT <<<\n','normal')
        self.log.insert(END,qp+'\n','success')
        
        for r,v in enumerate(val):
            qp='|'
            for col,i in enumerate(v):
                Label(select_win,text=str(i),width='20',bg='white').grid(row=r+2,column=col,pady=2,padx=2)
                qp = qp + str(i) + '\t|\t'    
            self.log.insert(END,qp+'\n')
        select_win.title('Table: '+self.table_name)
        self.set_toplevel(select_win)

        
    def set_toplevel(self,top):
        x = root.winfo_x()
        y = root.winfo_y()
        root_y = root.winfo_height()
        root_x = root.winfo_width()
        top.update()
        h = top.winfo_height()
        w = top.winfo_width()
        top.geometry('+%d+%d'%(x-w/2+root_x/2,y-h/2+root_y/2))
        top.iconbitmap(r'C:\Python27\programs\GUI\Database\icon.ico')
        top.resizable(width=False,height=False)




    def f_update(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Update Table\n','warning')
            return
        global u_e
        l = []
        u_e = []
        self.u_win = Toplevel(root)
        for i,cn in enumerate(column_name):
            u_e.append(Entry(self.u_win))
            l.append(Label(self.u_win,text=cn+" ("+column_type[i]+") : ",pady=3))
            l[i].grid(row=i,column=0,sticky='E')
            u_e[i].grid(row=i,column=1)
        l_u_c = Label(self.u_win,text='where').grid(row=len(u_e),column=0)
        self.e_u_c = Entry(self.u_win)
        self.e_u_c.grid(row=len(u_e),column=1)
        Button(self.u_win,text='Update Data',command=self.update).grid(row=len(u_e)+1,column=1)
        self.set_toplevel(self.u_win)

    def update(self):
        qp = ''
        for i,v in enumerate(u_e):
            if v.get() != '':
                if column_type[i] == 'text':
                    qp = qp + column_name[i] + '="' + v.get() + '",'
                else:
                    qp = qp + column_name[i] + '=' + v.get() + ','
        qp = qp[:-1]
        query = 'update '+self.table_name+ ' set '+qp
        if self.e_u_c.get()!='':
            query = query + ' where '+ self.e_u_c.get()
        try:
            print '>>> ' + query
            c.execute(query)
            connection.commit()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
        else:
            self.log.insert(END,'>>> Table '+self.table_name+' Updated\n','success')
        self.u_win.destroy()

        

    def f_dft(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Delete From Table\n','warning')
            return
        self.dft_win = Toplevel(root)
        Label(self.dft_win,text='Condition: ',pady=5).grid(row=0)
        self.e_dft = Entry(self.dft_win)
        Button(self.dft_win,text='Delete',command=self.delete_ft).grid(row=1,columnspan=2)
        Label(self.dft_win,text='--- OR ---',pady=5).grid(row=2,columnspan=2)
        Button(self.dft_win,text='Delete All',command=self.delete_all).grid(row=3,columnspan=2)
        self.e_dft.grid(row=0,column=1)
        self.set_toplevel(self.dft_win)


        

    def delete_ft(self):
        
        qp = 'delete from '+self.table_name + ' where '
        condition = self.e_dft.get()
        if condition=='':
            self.log.insert(END,'>>> Can not Delete Without a Valid Condition\n','warning')
            self.dft_win.destroy()        
            return
        qp = qp + condition
        ans = askokcancel('Attempt To Delete From Table','Are You Sure You Want To Delete From Table') 
        if ans != True:
            self.log.insert(END,'>>> Delete Process On Table '+self.table_name+' Aborted\n')
            self.dft_win.destroy()
            return
        try:
            print '>>> ' + qp
            c.execute(qp)
            connection.commit()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
        else:
            self.log.insert(END,'>>> Data Deleted From '+self.table_name+'\n','success')
        self.dft_win.destroy()

    def delete_all(self):
        ans = askokcancel('Attempt To Delete The Table','Are You Sure You Want To Delete The Table') 
        if ans != True:
            self.log.insert(END,'>>> Delete Process On Table '+self.table_name+' Aborted\n')
            return
        try:
            query = 'delete from '+self.table_name
            print '>>> ' + query
            c.execute(query)
            connection.commit()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
        else:
            self.log.insert(END,'>>> All Data Deleted from '+self.table_name+'\n')
        self.dft_win.destroy()

    

    def f_delete_t(self):
        
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Delete Table\n','warning')
            return
        ans = askokcancel('Attempt To Delete The Table','Are You Sure You Want To Delete The Table')
        print ans
        if ans != True:
            self.log.insert(END,'>>> Delete Process On Table '+self.table_name+' Aborted\n')
            return
        try:
            query = 'drop table '+self.table_name
            c.execute(query)
            print '>>> ' + query
            connection.commit()
        except Exception as ex:
            self.log.insert(END,'>>> '+str(ex)+'\n','warning')
        else:
            self.allset=1
            self.l_table.config(text='Table: '+self.table_name+' Deleted')
            self.log.insert(END,'>>> Table '+self.table_name+' Deleted\n','success')
            
            
            



    def f_sqle(self):
        root.lower()
        print '\n------------------------------------------------------------------\n'
        if self.allset == 0:
            self.log.insert(END,'>>> Select/Create a Databse to Run SQL Query Executer\n','warning')
            print '>>> Select/Create a Databse to Run SQL Query Executer\n'
            time.sleep(1)
            root.lift()
            return
        print '>>> Database: '+db+'\nSQL Query Executer Running...'
        print '>>> Enter "quit" to return back'
        self.log.insert(END,'>>> ----------------------------------------------------\n\n','warning')
        self.log.insert(END,'>>> SQL Query Executer is Running in CMD\n>>> Enter "quit" in CMD to close Query Executer\n','normal')
        while True:
            line = raw_input('Query: ')
            if line == 'quit':
                connection.commit()
                self.log.insert(END,'>>> SQL Query Executer Closed\n','normal')
                self.log.insert(END,'>>> ----------------------------------------------------\n\n','warning')
                print '>>> SQL Query Executer Closed'
                print '\n------------------------------------------------------------------\n'
                time.sleep(1)
                root.lift()
                return
            query = 'c.execute("'+line+'")'
            try:
                exec(query)
                if line[0:6] == 'select':
                    val = c.fetchall()
                    for row in val:
                        for i in row:
                            print i,'\t',
                        print ''
            except Exception as ex:
                print '>>> '+str(ex)+'\n'




##    def f_import(self):
##        if self.allset == 0:
##            self.log.insert(END,'>>> Select/Create a Database to Import Table\n')
##            return
##        self.file_xlsx = askopenfilename(filetypes = [('Excell File','*.xls')])
##        if self.file_xlsx != '':
##            self.import_win = Toplevel(root)
##            Label(self.import_win,text='Enter Details of Table',pady=5).grid(columnspan=2)
##            Label(self.import_win,text='Table Name: ',pady=5).grid(row=2)
##            Label(self.import_win,text='Enter Column Type ("," Saperated):',pady=5).grid(row=1)
##            self.e_ct = Entry(self.import_win,width=40)
##            self.e_tn = Entry(self.import_win,width=40)
##            self.e_ct.grid(row=1,column=1)
##            self.e_tn.grid(row=2,column=1)
##            b_ct = Button(self.import_win,text='Create Table',command=self.import_xlsx).grid(row=3,column=1)
##
##    def import_xlsx(self):
##        qp = ''
##        ct = self.e_ct.get().split(',')
##        tn = self.e_tn.get()
##        try:
##            fo_xlsx = open(self.file_xlsx,'r')
##            cn = fo_xlsx.readline()
##            print cn
##        except Exception as ex:
##            self.log.insert(END,'>>> '+str(ex)+'\n')
##            return
##        print cn,ct,tn
##        if len(column_name) != len(column_type):
##            self.log.insert(END,'>>> Error: Wrong Inputs\n')
##            self.ct_win.destroy()
##            return
##        for i,v in enumerate(cn):
##            qp = qp + v + ' ' +  column_type[i] + ','
##        qp = qp[:-1]
##        query = 'create table '+self.table_name+' ('+qp+')'
##        try:
##            c.execute(query)
##        except Exception as e:
##            self.log.insert(END,'>>> '+str(e)+'\n')
##        else:
##            pass
##        self.ct_win.destroy()




    def f_export(self):
        if self.allset != 2:
            self.log.insert(END,'>>> Select/Create a Table to Export\n','warning')
            return
        f_xls = open(self.table_name+'.xls','w')
        c.execute('select * from '+self.table_name)
        v = c.fetchall()
        l = ''
        for i in column_name:
            l = l + str(i) + '\t'
        l = l + '\n'
        for i in v:
            for val in i:
                l = l + str(val) + '\t'
            l=l+'\n'
        print l
        self.log.insert(END,'>>> Table '+self.table_name+' is saved as '+ self.table_name+'.xls ','success')
        f_xls.write(l)
        f_xls.close()




            
    def void(self):
        pass



        

root = Tk()
obj = ui()
root.mainloop()
