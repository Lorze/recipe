import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
from   pyforms.Controls import ControlList
import subprocess
import codecs
import glob
import re
import sys

#i think, i have a problem with the encoding on this one, will first have to figure that out before finishing
class Rezepte(BaseWidget):

	def __init__(self):
		super(Rezepte,self).__init__('Rezepte')

#Define the organization of the forms
		self._formset = ['',('_button','_allbutton',' '),('_newfile','_newbutton', ' '),('_persons',' '),('_openbutton',' ','_set',' '),('_filelist')]

#Definition of the forms fields

		files = glob.glob("Rezepte/*txt")   
		files.sort()
		self.files = files
		self._newfile = ControlText('','Name')
		self._persons = ControlText('Personen','%s'%personnr('persons'))
		self._button = ControlButton('Kompilieren')
		self._set = ControlButton('Speichern')
		self._allbutton = ControlButton('alle Kompilieren')
		self._newbutton = ControlButton('Rezept erstellen')
		self._openbutton = ControlButton('open')
		self._filelist = ControlList()
		self._filelist.horizontalHeaders = ['Titel', 'Personen', 'Kompilieren',' ']
		for name in files:
			title =openfile(name)
			persons = personnr(title)
			comp = compil(title)
			self._filelist += [title, persons, comp,' ']
			
#Define the button action
		self._button.value = self.__buttonAction
		self._allbutton.value = self.__allbuttonAction
		self._openbutton.value = self.__openbuttonAction
		self._newbutton.value = self.__newbuttonAction

#compiles only some chosen recipes		 
	def __buttonAction(self):
		"""Button action event"""
		save(self)
		subprocess.call(["python3", "sample.py", "-c some"])

#compiles all recipes
	def __allbuttonAction(self):
		"""Button action event"""
		subprocess.call(["python3", "sample.py"])

#opens selected files
	def __openbuttonAction(self):
		"""Button action event"""
		for number in self._filelist.mouseSelectedRowsIndexes :
			subprocess.call(["xdg-open", "%s"%(self.files[number])])

#creates new file with given name
	def __newbuttonAction(self):
		"""Button action event"""
		self._newfileValue = self._newfile.value
		f = codecs.open("Rezepte/%s.txt"%(self._newfileValue.lower()),'w',encoding='utf-8')
		f.write('[%s]\ntime: \ndevice: \npersons:1 \n\n>1ELL Beispielflussigkeit \nkochen ' %self._newfileValue)
		f.close()
		subprocess.call(["xdg-open", "Rezepte/%s.txt"%(self._newfileValue.lower())])

	
def openfile(name):
	f = codecs.open("%s"%(name),'r',encoding='utf-8')
	line = f.readline()
	titleRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)
	match = titleRegex.match(line)
	title = match.group(1).strip().encode('utf-8')
	f.close()
	return title

#should safe all things set im the GUI, not yet complete
def save(self):
	persons = self._persons.value.encode('utf-8')
	specpers = self._filelist.value
	with open('persons.txt', 'r') as file:
		data = file.readlines()
	data[0] = '[persons]%s\n'%persons
	with open('persons.txt', 'w') as file:
		file.writelines(data)

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
				if match.group(1).strip().encode('utf-8') == title:
					persons = match.group(2).strip().encode('utf-8')
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
	compileRegex = re.compile('\[([\w\s\',-]+)\]([0-1])', re.UNICODE)
	while True:
		line = f.readline()
		line = line.split("#")[0] #discad comments
		match = compileRegex.match(line)
		comp = 0
		if line == '':
			break
		if  match != None:
			if match.group(1).strip().encode('utf-8') == '%s'%name:				
				comp = match.group(2).strip().encode('utf-8')
				break
			continue
		else:
			continue
	return comp

#Execute the application
if __name__ == "__main__":   pyforms.startApp( Rezepte )

