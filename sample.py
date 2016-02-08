import thomaslib
from thomaslib import Unit
import sys
import glob
import subprocess
import os
import codecs
import re
import argparse

#allows to open file to match title against setting  in compile.txt. more elegant solution definitely appreciated.
def openfile(name):
	f = codecs.open("%s"%(name),'r',encoding='utf-8')
	line = f.readline()
	titleRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)
	match = titleRegex.match(line)
	title = match.group(1).strip().encode('utf-8')
	f.close()
	return title

# adds option -c to sample.py, which will only compile files set in compile.txt. default compiles all
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', default='all')
args = parser.parse_args()

#list of units -> Unit(name in recipe file,
	#how many times fits the preceding unit in to this one,
	#after how many portions should it be converted to the next higher unit,
	#name to display (optional)
	#fraciton)
units = [
	Unit('Portion', 0, 1.1,'Portion',True),
	Unit('Portionen', 1, 0,'Portionen',True),

	Unit('Glas', 0, 1.1,'Glas',True),
	Unit('Gläser', 1, 0,'Gläser',True),

	Unit('Dose', 0, 1.1,'Dose',True),
	Unit('Dosen', 1, 0,'Dosen',True),

	Unit('Zweig', 0, 1.1,'Zweig',True),
	Unit('Zweige', 1, 0,'Zweige',True),

	Unit('cm', 0, 1000),
	Unit('m', 1000, 0),

	Unit('Beutel', 0, 0),

	Unit('Päckchen', 0, 0,'Päckchen'),
	
	Unit('n', 0, 0,' ',True),

	Unit('Bund', 0, 0,'Bund',True),

	Unit('Prise', 0, 1.1,'Prise',True),
	Unit('Prisen', 1, 3,'Prisen',True),
	Unit('TL', 8, 3,'TL',True),
	Unit('EL', 3, 3,'EL',True),
	Unit('g', 0.1, 999),
	Unit('kg', 1000, 999),
	Unit('t', 1000, 0),

	Unit('Tropfen', 0, 3,'Tropfen',True),
	Unit('TLL', 10, 3, 'TL',True),
	Unit('ELL', 3, 3, 'EL',True),
	Unit('ml', 0.1, 99),
	Unit('dl', 100, 10),
	Unit('l', 10, 0)
]
#read all filenames in Rezepte
files = glob.glob("Rezepte/*txt")   
files.sort()
f = codecs.open('Rezepte.tex','w',encoding='utf8')
h = codecs.open('Rezepte.toc','w',encoding='utf8')
form = thomaslib.Form(f)
compileRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)

#open every file, compile, write to tex & toc, only for some files, if -c some is selected
form.tocheader(h)
var = 2
form.header(f)
if  args.c=='all':
	for name in files:
		recipe = thomaslib.Recipe(units)
		recipe.load(name)
		recipe.setPersons2()
		recipe.saveLatex(f)
		recipe.savetoc(h, var)
		var = var + 1
else:
	for name in files:
		g = codecs.open('compile.txt', 'r', encoding='utf-8')
		while True:
			line = g.readline()
			line = line.split("#")[0] #discad comments
			match = compileRegex.match(line)
			if line == '':
				break
			if  match != None:
				if match.group(1).strip().encode('utf-8') == openfile(name):
					print(match.group(1).strip().encode('utf-8'))
					recipe = thomaslib.Recipe(units)
					recipe.load(name)
					recipe.setPersons2()
					recipe.saveLatex(f)
					recipe.savetoc(h, var)
					var = var + 1
					break
				continue
			else:
				continue
form.end(f)
f.close()
h.close()
# run latex; maybe implement here for other OS than linux 
if sys.platform == 'linux' :
	subprocess.call(["pdflatex", "Rezepte.tex"])
	subprocess.call(["xdg-open", "Rezepte.pdf"])
elif sys.platform == 'win32':
	subprocess.call(["pdflatex", "Rezepte.tex"])
#       	subprocess.call(["start Rezepte.pdf"])
else :
	print('not implemented for your OS yet')
# clean up
os.remove("Rezepte.aux")
os.remove("Rezepte.log")
os.remove("Rezepte.tex")
os.remove("Rezepte.toc")



