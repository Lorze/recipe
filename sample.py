import thomaslib
from thomaslib import Unit
import sys
import glob
import subprocess
import os
import codecs

#list of units -> Unit(name in recipe file,
	#how many times fits the preceding unit in to this one,
	#after how many portions should it be converted to the next higher unit,
	#name to display (optional)
	#fraciton)
units = [
	Unit('Portion', 0, 1,'Portion',True),
	Unit('Portionen', 1, 0,'Portionen',True),

	Unit('Glas', 0, 1,'Glas',True),
	Unit('Gläser', 1, 0,'Gläser',True),

	Unit('Dose', 0, 1,'Dose',True),
	Unit('Dosen', 1, 0,'Dosen',True),

	Unit('Zweig', 0, 1,'Zweig',True),
	Unit('Zweige', 1, 0,'Zweige',True),

	Unit('cm', 0, 1000),
	Unit('m', 1000, 0),

	Unit('Beutel', 0, 0),

	Unit('Päckchen', 0, 0,'Päckchen'),

	Unit('Bund', 0, 0),

	Unit('Prise', 0, 1,'Prise',True),
	Unit('Prisen', 1, 3,'Prisen',True),
	Unit('TL', 8, 3,'TL',True),
	Unit('EL', 3, 3,'EL',True),
	Unit('g', 0.1, 1000),
	Unit('kg', 1000, 1000),
	Unit('t', 1000, 0),

	Unit('Tropfen', 0, 3,'Tropfen',True),
	Unit('TLL', 10, 3, 'TL',True),
	Unit('ELL', 3, 3, 'EL',True),
	Unit('ml', 0.1, 10),
	Unit('cl', 10, 10),
	Unit('dl', 10, 10),
	Unit('l', 10, 0)
]

#read all filenames in Rezepte
files = glob.glob("Rezepte/*txt")   
files.sort()
h = codecs.open('Rezepte.toc','w',encoding='utf8')
f = codecs.open('Rezepte.tex','w',encoding='utf8')
form = thomaslib.Form(f)

#open every file, compile, write to tex & toc
form.tocheader(h)
var = 2
form.header(f)
for name in files:
	recipe = thomaslib.Recipe(units)
	recipe.load(name)
	recipe.setPersons(8)
	recipe.saveLatex(f)
	recipe.savetoc(h, var)
	var = var + 1
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
