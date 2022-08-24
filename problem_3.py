
import sqlite3
#class Menu takes input form user
class Menu:
    #main menu
    def main(self):
        print("Contact book - main menu")
        print("INSERT CONTACT press 1")
        print("FIND CONTACT press 2")
        print("UPDATE CONTACT press 3")
        print("DELETE CONTACT press 4")
        print("for SHOW ALL CONTACT press 5")
        print("for QUIT press Q")
        
        self._choice_num = input()
        if self._choice_num == "1":
            try:
                print("write first name")
                self._first_name = input()
                print("write last name")
                self._last_name = input()
                print("write addres")
                self._addres = input()
                print("write email")
                self._email = input()
                print("write phone number")
                self._phone = int(input())
                print("your new contact\n")
                print("first name:{0}\nlast name:{1}\naddres:{2}\nemail:{3}\nphone number:{4}"
                .format(self._first_name, self._last_name, self._addres, self._email, self._phone))    
                sql.insert(self._first_name, self._last_name, self._addres, self._email, self._phone) 
            except:
                print("New data are incorectly,please try again.")
            menu.main()
        
        elif self._choice_num == "2":
                try:
                    print("For find contact write first name:")
                    self._first_name = input()
                    print("last name:")
                    self._last_name = input()
                    sql.find(self._first_name, self._last_name)
                except:
                    print("Data are incorectly, please try again.")
                menu.main()
        
        elif self._choice_num == "3":
            try:
                print("write first name")
                self._first_name = input()
                print("write last name")
                self._last_name = input()
                self._id = sql.id(self._first_name, self._last_name)
                if self._id:
                    print("Write new data for update contact.")
                    print("New addres")
                    self._new_addres = input()
                    print("New email")
                    self._new_email = input()
                    print("New phone number")
                    self._new_phone = int(input())
                    sql.update(self._id, self._new_addres, self._new_email, self._new_phone) 
            except:
                print("New data are incorectly,please try again.")
            menu.main()

        elif self._choice_num == "4":
                try:
                    print("For delete contact write first name:")
                    self._first_name = input()
                    print("last name:")
                    self._last_name = input()
                    self._id = sql.id(self._first_name, self._last_name)
                    if self._id:
                        sql.delete(self._id)
                except:
                    print("Data are incorectly, please try again.") 
                menu.main()
            
        elif self._choice_num == "5":
            print("LIST ALL CONTACT")
            sql.list()
            print("Back to main menu press Enter")
            input()
            menu.main()
        elif self._choice_num == "Q":
            sql.close_conn()
        else:
            print("Incoreect choice. Please try again.")
            menu.main()

#class SQLite serves database
class SQLite:
    # SQLite conection
    def create_conn(self):
        try:
            # Making a connection between sqlite3 database and Python Program
            self._sqliteConnection = sqlite3.connect('SQLite_contact_book.db')
            self._cursor = self._sqliteConnection.cursor()
            print("Connected to SQLite")
            
        except sqlite3.Error as error:
            print("Failed to connect with sqlite3 database", error)
            self._sqliteConnection = False
        return self._sqliteConnection, self._cursor
    
    #for create SQL table
    def create_table(self, sqliteConnection,  cursor):
        self._sqliteConnection = sqliteConnection
        self._cursor = cursor
        
        table = """ CREATE TABLE IF NOT EXISTS CONTACT_BOOK (
            
            First_Name CHAR(25) NOT NULL,
            Last_Name CHAR(25),
            Addres CHAR(255),
            Email CHAR(25),
            Phone INTEGER(15),
            ID integer PRIMARY KEY 
        ); """
        self._cursor.execute(table)
        print("Table CONTACT_BOOK is Ready")
    
    # delete SQL table
    def drop_table(self, cursor, table_name):
        self._table_name = table_name
        self._cursor = cursor
        self._cursor.execute("DROP TABLE IF EXISTS {0}".format(self._table_name))
        print("Table {0} deleted".format(self._table_name))
    
    #insert data in SQL
    def insert(self, first_name, last_name, addres, email, phone):
        self._first_name = first_name
        self._last_name = last_name
        self._addres = addres
        self._email = email
        self._phone = phone
               
        try:
            self._cursor.execute("INSERT INTO CONTACT_BOOK (First_Name,  Last_Name, Addres,  Email, Phone) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(self._first_name, self._last_name, self._addres, self._email, self._phone))
            self._sqliteConnection.commit()
            print ("Contact saved\n")   
        except:
            print ("Error input data. Contact not saved.")
    
    #Find data from database. Key colummb is First_Name OR Last_Name.
    def find(self, first_name, last_name):
            self._first_name = first_name
            self._last_name = last_name
            self._cursor.execute("SELECT First_Name, Last_Name, Addres, Email, Phone from CONTACT_BOOK WHERE First_Name='{0}' OR Last_Name='{1}'".format(self._first_name, self._last_name))
            row_true = True
            for row in self._cursor:
                row_true = False
                print("Contact find:","first name:", row[0], ", last name:",row[1], ", addres:",row[2],
                     ", email:",row[3], ", phone number:",row[4])
            if row_true:    
                print("Contact dont exist.")
    
    #find id from database. Key colummb is First_Name AND Last_Name.
    def id(self, first_name, last_name):
            self._first_name = first_name
            self._last_name = last_name        
            self._cursor.execute("SELECT First_Name, Last_Name, Addres, Email, Phone, ID from CONTACT_BOOK WHERE First_Name='{0}' AND Last_Name='{1}'".format(self._first_name, self._last_name))
            row_true = True
            for row in self._cursor:
                row_true = False
                print("Contact find:","first name:", row[0], ", last name:",row[1], ", addres:",row[2],
                     ", email:",row[3], ", phone number:",row[4])
                self._id_contact = row[5]
            if row_true:    
                print("Contact dont find.")
                return False
            else:
                return self._id_contact

    #Delete row form database. Key colummb is ID.
    def delete(self, id_contact):
            self._id_contact = id_contact
            self._cursor.execute("DELETE from CONTACT_BOOK WHERE ID ='{0}'".format(self._id_contact))
            self._sqliteConnection.commit()
            print("Contact deleted.")
    
    #Update addres, email and phone.
    def update(self, id, new_addres, new_email, new_phone):
            self._id = id
            self._new_addres = new_addres
            self._new_email = new_email
            self._new_phone = str(new_phone)

            self._cursor.execute("UPDATE CONTACT_BOOK SET Addres='{0}',  Email='{1}', Phone='{2}' WHERE ID ='{3}'".format(self._new_addres, self._new_email, self._new_phone, self._id))
            self._sqliteConnection.commit()
            print("Contact updated.")

    #Return whole llist of database.
    def list(self):
            self._cursor.execute("SELECT First_Name, Last_Name, Addres,  Email, Phone from CONTACT_BOOK ORDER BY First_Name")
            for row in self._cursor:
                print("first name:", row[0], "last name:",row[1], "addres:",row[2], "email:",row[3], "phone number:",row[4])
    
    # Close SQL conection.
    def close_conn(self):
        if self._sqliteConnection:
            self._sqliteConnection.close()
            print("the sqlite connection is closed")
            

sql = SQLite()
sqliteConnection, cursor = sql.create_conn()
menu = Menu()
menu.main()

#Create table.
#sql.create_table(sqliteConnection, cursor)

#Delete table.
#sql.drop_table(cursor, "CONTACT_BOOK")
