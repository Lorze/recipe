import pyforms
from   pyforms          import BaseWidget
from   pyforms.Controls import ControlText
from   pyforms.Controls import ControlButton
from   pyforms.Controls import ControlList
import subprocess
import codecs
import glob
import re

class Rezepte(BaseWidget):

	def __init__(self):
		super(Rezepte,self).__init__('Rezepte')

#Define the organization of the forms
		self._formset = ['',('_openbutton',' ','_button','','_newfile','_newbutton', ' '),'',('_filelist')]
#The ' ' is used to indicate that a empty space should be placed at the bottom of the window
#If you remove the ' ' the forms will occupy the entire window

#Definition of the forms fields

		files = glob.glob("Rezepte/*txt")   
		files.sort()
		self._newfile = ControlText('','Name')
		self._button = ControlButton('Kompilieren')
		self._newbutton = ControlButton('Rezept erstellen')
		self._openbutton = ControlButton('open')
		self._filelist = ControlList()
		self._filelist.horizontalHeaders = ['Title', 'Ammount', 'Compile']
		for name in files:
			title = openfile(name)
			persons = personnr(title,name)
			comp = compil(name)
			self._filelist += [title, persons, comp]

#Define the button action
		self._button.value = self.__buttonAction
		self._newbutton.value = self.__newbuttonAction

	def __buttonAction(self):
		"""Button action event"""
		subprocess.call(["python3", "sample.py"])

	def __openbuttonAction(self):
		"""Button action event"""
		print(1)

	def __newbuttonAction(self):
		"""Button action event"""
		self._newfileValue = self._newfile.value
		f = codecs.open("Rezepte/%s.txt"%(self._newfileValue.lower()),'w',encoding='utf-8')
		f.write('[%s]\ntime: \ndevice: \npersons: \n\n>1ELL Beispielflussigkeit \nkochen ' %self._newfileValue)
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

def personnr(title,name):
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
				if match.group(1) == 'persons':
					persons = match.group(2).strip()
				elif match.group(1).strip().encode('utf-8') == title:
					persons = match.group(2).strip()
				else :
					continue
			continue
		else:
			continue
	return persons

def compil(name):
	f = codecs.open("%s"%(name),'r',encoding='utf-8')
	compileRegex = re.compile('\[([\w\s\',-]+)\]([\w\s\',-]+)', re.UNICODE)
	while True:
		line = f.readline()
		line = line.split("#")[0] #discad comments
		if line == '':
			break
		if  compileRegex.match(line) != None:
			match = compileRegex.match(line)
			comp = match.group(2).strip()
			continue
		else:
			continue
	return comp

#Execute the application
if __name__ == "__main__":   pyforms.startApp( Rezepte )

