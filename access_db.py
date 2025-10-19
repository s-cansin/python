from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import QSqlTableModel, QSqlDatabase, QSqlQuery



#### LOCATE ACCESS FILE INTO C:\Users\Administrator\Desktop\ DIRECTORY
#### OR CHANGE DEFAULT DIRECTORY INTO THE TEXTBOX!!!!!

app = QApplication([])
 
window = QWidget()
window.setGeometry(50,50,1200,600)

window.setWindowTitle('Database Manager')
etiket = QLabel('Database Dir')
openbutton = QPushButton('Browse File')

directory = QLineEdit("")
directory.setText(r"C:\\Users\\Administrator\\Desktop\\db.accdb")

tablo = QTableView()
closebutton = QPushButton('Close')


def FuncExitForm():
	sys.exit()


def FuncGetData():
	filename = os.path.join(directory.text())
	db = QSqlDatabase.addDatabase("QODBC")
	db.setDatabaseName("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DSN='';DBQ=" + directory.text())
	db.open()
	model = QSqlTableModel(window,db)
	model.setTable("calls")
	sorgu = QSqlQuery("select TOP 10 name,surname,phone,home from address")
	model.setQuery(sorgu)
	model.submit()
	tablo.setModel(model)
	tablo.show()



window.connect(closebutton, SIGNAL('pressed()'), FuncExitForm)
window.connect(openbutton, SIGNAL('pressed()'), FuncGetData)

design = QHBoxLayout()
design.addWidget(etiket)
design.addWidget(directory)
design.addWidget(openbutton)

design.addWidget(tablo)
design.addWidget(closebutton)
 
window.setLayout(design)
window.show()
app.exec_()