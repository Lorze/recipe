#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt4 import QtGui # Import the PyQt4 module we'll need
from PyQt4 import QtCore
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys # We need sys so that we can pass argv to QApplication
import new
import dialog
import design # This file holds our MainWindow and all design related things
				# it also keeps events etc that we defined in Qt Designer
import subprocess
import codecs
import glob
import re
import sys
import os
import time

class NewApp(QtGui.QWidget, new.Ui_Dialog): #OK
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in design.py file automatically
		self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
		self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.new_file)

	def new_file(self):
		self.name = str(self.newName.text())
		self.time = str(self.newTime.text())
		self.device = str(self.newDevice.text())
		self.persons = str(self.newPersons.text())

		f = codecs.open("Rezepte/%s.txt"%(self.name.lower()),'w',encoding='utf-8')
		f.write('[%s]\ntime:%s \ndevice:%s \npersons:%s \n\n>1ELL Beispielflussigkeit \nkochen ' %(self.name,self.time,self.device,self.persons))
		f.close()
		self.dialog = EditorApp("Rezepte/%s.txt"%(self.name.lower()))
		f =  codecs.open("Rezepte/%s.txt"%(self.name.lower()),'r','utf-8')
		with f:
			text = f.read()
			self.dialog.textEdit.setText(text)
		self.dialog.show() 
		self.dialog.get_old()
		self.close()

class EditorApp(QtGui.QWidget, dialog.Ui_Dialog):
	def __init__(self, name):
		super(self.__class__, self).__init__()
		self.name = name
		self.setupUi(self)  # This is defined in design.py file automatically
		self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.close)
		self.buttonBox.button(QtGui.QDialogButtonBox.Save).clicked.connect(self.save_data)
		self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.buttonBox.button(QtGui.QDialogButtonBox.Reset).clicked.connect(self.reset)
		
	def save_data (self):
		data = self.textEdit.toPlainText()
		f = codecs.open("%s"%(self.name),'w',encoding='utf-8')
		f.write(data)
		f.close()

	def ok (self):
		data = self.textEdit.toPlainText()
		f = codecs.open("%s"%(self.name),'w',encoding='utf-8')
		f.write(data)
		f.close()
		self.close()

	def reset(self):
		self.textEdit.setText(self.old)

	def get_old (self):
		self.old = self.textEdit.toPlainText()



class ExampleApp(QtGui.QMainWindow, design.Ui_MainWindow):
	def __init__(self):
		super(self.__class__, self).__init__()
		QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf8"))
		self.setupUi(self)  # This is defined in design.py file automatically
		self.compileAll.clicked.connect(self.compile_all) 
		self.compileSelected.clicked.connect(self.compile_some) 
		self.actionOpen.triggered.connect(self.file_open)
		self.actionSave.triggered.connect(self.personChangeAll)
		self.actionNew.triggered.connect(self.file_new)
		self.selectedFiles.setColumnCount(2)
		self.selectedFiles.resizeColumnsToContents()
		self.selectedFiles.setColumnWidth(0, 300)
		self.allFiles.setColumnCount(2)
		self.allFiles.resizeColumnsToContents()
		self.allFiles.setColumnWidth(0, 300)
		self.allLoad()
		self.selectedLoad()
		self.allFiles.doubleClicked.connect(self.doCompile)
		self.selectedFiles.doubleClicked.connect(self.dontCompile)
		self.allPersons.setValue(int(personnr("persons")))
		self.allPersons.valueChanged.connect(self.personChange)
				
	def contextMenuEvent(self, event):
		self.personChangeAll()
		menu = QMenu(self)
		openAction = menu.addAction("Open")
		newAction = menu.addAction("New")
		quitAction = menu.addAction("Quit")
		action = menu.exec_(self.mapToGlobal(event.pos()))
		if action == quitAction:
			qApp.quit()
		if action == openAction:
			name = self.files[self.allFiles.currentRow()]
			self.name = name
			self.dialog = EditorApp(self.name)
			f =  codecs.open(name,'r','utf-8')
			with f:
				text = f.read()
				self.dialog.textEdit.setText(text)
			self.dialog.show() 
			self.dialog.get_old()
		if action == newAction:
			self.new = NewApp()
			self.new.show()

	def doCompile(self):
		self.personChangeAll()
		data = self.allFiles.item(self.allFiles.currentRow(),0).text()
		self.somefiles.append('[%s]\n'%(data))
		f = codecs.open('compile.txt', 'w',encoding='utf-8')
		for line in self.somefiles:
			f.write(line)
		f.close()
		self.reload()

	def dontCompile(self):
		self.personChangeAll()
		data = self.selectedFiles.item(self.selectedFiles.currentRow(),0).text()
		temp = []
		for line in self.somefiles:
			if line == '[%s]\n'%(data):
				pass
			else:
				temp.append(line)
		self.somefiles = temp
		f = codecs.open('compile.txt', 'w',encoding='utf-8')
		for line in self.somefiles:
			f.write(line)
		f.close()
		self.reload()
		
	def personChange(self):
		self.personChangeAll()
		f = codecs.open('persons.txt', 'r', encoding='utf-8')
		setPersonRegex = re.compile('\[([\w\s\',-]+)\]([0-9]+)', re.UNICODE)
		temp = []
		while True:
			line = f.readline()
			line = line.split("#")[0] #discad comments
			if line == '':
				break
			if setPersonRegex.match(line) != None:
				match = setPersonRegex.match(line)
				if match != None:
					if match.group(1).strip() == "persons":
						temp.append("[persons]%s\n"%self.allPersons.value())
					else :
						temp.append(line)
				continue
			else:
				continue
		f = codecs.open('persons.txt', 'w',encoding='utf-8')
		for line in temp:
			f.write(line)
		f.close()

	def personChangeAll(self):
		temp = []
		temp.append("[persons]%s\n"%self.allPersons.value())
		for i in range(0,len(self.files)):
			if self.allFiles.item(i,1).text()!= '':
				temp.append("[%s]%s\n"%(self.allFiles.item(i,0).text(),self.allFiles.item(i,1).text()))
		f = codecs.open('persons.txt', 'w',encoding='utf-8')
		for line in temp:
			f.write(line)
		f.close()


	def selectedLoad(self):
		files = glob.glob("Rezepte/*txt")   
		files.sort()
		self.files = files
		self.somefiles = []
		i=0
		for name in files:
			self.selectedFiles.setRowCount(i+1)
			title =openfile(name)
			persons = personnr(title)
			comp = compil(title)
			if comp:
				self.selectedFiles.setItem(i,0,  QTableWidgetItem(title))
				self.selectedFiles.setItem(i,1,  QTableWidgetItem(persons))
				self.somefiles.append('[%s]\n'%(title))
				i=i+1
		
	def allLoad(self):
		files = glob.glob("Rezepte/*txt")   
		files.sort()
		self.files = files
		i=0
		for name in files:
			self.allFiles.setRowCount(i+1)
			title =openfile(name)
			persons = personnr(title)
			self.allFiles.setItem(i,0,  QTableWidgetItem(title))
			self.allFiles.setItem(i,1,  QTableWidgetItem(persons))
			i=i+1			

	def compile_all(self):              
		self.personChangeAll()
		subprocess.call(["python3", "sample.py"])

	def compile_some(self):
		self.personChangeAll()
		subprocess.call(["python3", "sample.py", "-c some"])

	def file_open(self): 
		self.personChangeAll()
		self.dialog = EditorApp(self.name)
		name = self.files[self.allFiles.currentRow()]
		f =  codecs.open(name,'r','utf-8')
		with f:
			text = f.read()
			self.dialog.textEdit.setText(text)
		self.dialog.show() 
		self.dialog.get_old()

	def file_new(self):
		self.personChangeAll()
		self.new = NewApp()
		self.new.show()
		

	def reload(self):
		self.personChangeAll()
		self.selectedLoad()
		self.allLoad()



def openfile(name):
	f = codecs.open("%s"%(name),'r',encoding='utf-8')
	line = f.readline()
	titleRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)
	match = titleRegex.match(line)
	title = match.group(1).strip()
	f.close()
	return title

#reads persons.txt, where person settings are saved
def personnr(title):
	f = codecs.open('persons.txt', 'r', encoding='utf-8')
	setPersonRegex = re.compile('\[([\w\s\',-]+)\]([0-9]+)', re.UNICODE)
	while True:
		line = f.readline()
		line = line.split("#")[0] #discad comments
		if line == '':
			break
		if  setPersonRegex.match(line) != None:
			match = setPersonRegex.match(line)
			if  match != None:

				if match.group(1).strip() == title:
					persons = match.group(2).strip()
				elif match.group(1) == 'persons':
					persons = ''
				else :
					continue
			continue
		else:
			continue
	return persons


#reads compile.txt, in which the compilation settings will be saved
def compil(name):
	f = codecs.open('compile.txt', 'r', encoding='utf-8')
	compileRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)
	while True:
		line = f.readline()
		line = line.split("#")[0] #discad comments
		match = compileRegex.match(line)
		comp = ''
		if line == '':
			break
		if  match != None:
			if match.group(1).strip() == '%s'%name:				
				comp = 1
				break
			continue
		else:
			continue
	return comp


def main():
	app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
	form = ExampleApp()                 # We set the form to be our ExampleApp (design)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app

if __name__ == '__main__':              # if we're running file directly and not importing it
	main()                              # run the main function
