import re
import codecs
import math

class Recipe:
	def __init__(self, units, title = '', time = '', device = '', persons = 0, persunit = ''):
		self.units = units
		self.title = title
		self.time = time
		self.device = device
		self.persons = persons
		self.persunit = persunit
		self.instructions = []

	#set number of persons and scale ingredients
	def setPersons(self, persons):
		factor = float(persons) / self.persons
		self.persons = float(persons)

		for instruction in self.instructions:
			for ingredient in instruction.ingredients:
				ingredient.scale(factor)

	#set number of persons and scale ingredients according to persons.tex, call after recipe.load!!
	def setPersons2(self):
		f = codecs.open('persons.txt', 'r', encoding='utf-8')
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
					elif match.group(1) == self.title:
						persons = match.group(2).strip()
					else :
						continue
				continue

			else:
				continue

		self.setPersons(persons)

	#loads recipe from file
	def load(self, filename):
		f = codecs.open(filename, 'r', encoding='utf-8')
		while True:
			line = f.readline()
			line = line.split("#")[0] #discad comments

			if line == '':
				break

			if  titleRegex.match(line) != None:
				self.parseHeader(getTextBlock(f, [line]))
				continue

			if  ingredientRegex.match(line) != None or timeRegex.match(line) != None or emptyRegex.match(line) == None:
				instruction = Instruction(self)
				instruction.load(getTextBlock(f, [line]))
				self.instructions.append(instruction)
				continue

	#parses header
	def parseHeader(self, lines):
		for line in lines:
			match = titleRegex.match(line)
			if  match != None:
				self.title = match.group(1).strip()

			match = headerRegex.match(line)
			if  match != None:
				if match.group(1) == 'time':
					self.time = match.group(2).strip()
				elif match.group(1) == 'device':
					self.device = match.group(2).strip()
				elif match.group(1) == 'persons':
					match = personRegex.match(line)
					self.persons = float(match.group(2))
					if match.group(3) != '':
						self.persunit = match.group(3)
					else:
						self.persunit = 'Personen'

	#prints valid text representation
	def save(self, stream):
	 	stream.write('[%s]\n' % self.title)
	 	stream.write('time: %s\n' % self.time)
	 	stream.write('device: %s\n' % self.device)
	 	stream.write('persons: %s\n\n' % self.persons)

	 	for instruction in self.instructions:
	 		instruction.save(stream)

	#creates valid Latex to use with latex, ig hie schaffe
	def saveLatex(self, stream):
		if self.time :
			stream.write('\\thispagestyle{empty}\n\\section*{\\hyperlink{MyToc}{%s}}\n\\addtocontents{toc}{\\protect\\thispagestyle{empty}}\\addcontentsline{toc}{section}{%s \\textit{%s}}\n\\subsection*{Zeit: %s}\n\\subsection*{%s}\n\\subsection*{%s %s}\n' % (self.title,self.title, self.time, self.time, self.device, fraction(self.persons,True), self.persunit))
		else :
			stream.write('\\thispagestyle{empty}\n\\section*{\\hyperlink{MyToc}{%s}}\n\\addtocontents{toc}{\\protect\\thispagestyle{empty}}\\addcontentsline{toc}{section}{%s \\textit{%s}}\n\\subsection*{%s}\n\\subsection*{%s}\n\\subsection*{%s %s}\n' % (self.title,self.title, self.time,self.time, self.device, fraction(self.persons,True), self.persunit))
		stream.write('\\begin{tabular}{R{3cm}L{4.5cm}D{9cm}}\n\\hline\\\\\\\\\n')
		for instruction in self.instructions:
			instruction.saveLatex(stream)
		stream.write('\\end{tabular}\n\\clearpage\n')

	#creates toc entry
	def savetoc(self, stream, var):
		stream.write('\\contentsline {section}{\\numberline {}%s}{%s}{section.%s}\n'%(self.title,self.time,var))
			
		

class Instruction:
	def __init__(self, recipe, text = ''):
		self.recipe = recipe
		self.text = text
		self.time = ''
		self.ingredients = []

	#loads instructions for instruction lineblock
	def load(self, lines):
		for line in lines:
			match = ingredientRegex.match(line)
			if  match != None:
				nameMultiple =  match.group(3).strip();
				if match.group(4) != '':
					nameMultiple = match.group(4).strip()

				quantities = [str2float(x) for x in match.group(1).split('-')]
				ingredient = Ingredient(self.recipe, quantities, match.group(2), match.group(3).strip(), nameMultiple)
				self.ingredients.append(ingredient)
				continue

			match = timeRegex.match(line)
			if match != None:
				self.time = match.group(1).strip()
			else:
				self.text += line.strip() + ' '

	#prints valid text representation
	def save(self, stream):
	 	if self.time != '':
	 		stream.write("(%s\n" % self.time)
	 	for ingredient in self.ingredients:
	 		ingredient.save(stream)
	 	stream.write("%s\n\n" % self.text)
	
	#prints text for Latex
	def saveLatex(self, stream):
		if self.time != '':
			stream.write("&%s" % self.time)
		for ingredient in self.ingredients:
			ingredient.saveLatex(stream)
			if ingredient != self.ingredients[-1]:
				stream.write("&\\\\")
		stream.write("&%s\\\\\\\\" % self.text)

class Ingredient:
	def __init__(self, recipe, quantities, unit, name, nameMultiple):
		self.quantities = quantities
		self.name = name
		self.nameMultiple = nameMultiple
		self.recipe = recipe
		self.unit = self.getUnit(unit)

	#scale ingredient, converts unit automatically
	def scale(self, factor):
		self.quantities = [x * factor for x in self.quantities]
		units = self.recipe.units;
		index = -1

		for i in range(0, len(units)):
			if units[i].name == self.unit.name:
				index = i
				break
	
		if index != -1:
			while units[index].convertAfter != 0 and self.quantities[0] >= units[index].convertAfter:
				index += 1
				self.quantities = [x / units[index].ratio for x in self.quantities]

			while units[index].ratio != 0 and self.quantities[0] < units[index - 1].convertAfter / units[index].ratio:
				self.quantities = [x * units[index].ratio for x in self.quantities]
				index -= 1

			self.unit = units[index]

	def getUnit(self, name):
		for unit in self.recipe.units:
			if unit.name == name:
				return unit
		return Unit(name, 0, 0, '', True) 

	#prints valid text representation in latex format
	def save(self, stream):
	 	name = self.name
	 	if self.nameMultiple != name:
	 		name += '/' + self.nameMultiple

	 	quantities = '-'.join([float2str(x) for x in self.quantities])
	 	output = '%s %s %s' % (quantities, self.unit.name, name)
	 	stream.write('>' + output.strip() + '\n')

	#prints text for Latex, in latex format
	def saveLatex(self, stream):
		name = self.name
		if self.quantities[-1] >= 1:
			name = self.nameMultiple

		quantities = '\\textendash'.join([fraction(x, self.unit.frac) for x in self.quantities])
		output = '%s %s& %s' % (quantities, self.unit.getName(), name)
		stream.write(output.strip())


class Unit:
	def __init__(self, name, ratio, convertAfter, displayName = '', frac=False):
		self.name = name
		self.ratio = ratio
		self.convertAfter = convertAfter
		self.displayName = displayName
		self.frac = frac

	#get display name
	def getName(self):
		if self.displayName == '':
			return self.name
		return self.displayName

# OK, do everything without a csv
class Form:
	def __init__(self,stream):
		self.stream = stream

	def header(self, stream):
		stream.write('\\documentclass[12pt,a4paper]{scrartcl}\n'
			+'\\setkomafont{sectioning}{\\normalfont\\bfseries}\n'
			+'\\usepackage[ngerman]{babel}\n'
			+'\\usepackage[utf8x]{inputenc}\n'
			+'\\usepackage{tocloft}\n'
			+'\\usepackage{array}\n'
			+'\\newcolumntype{L}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}b{#1}}\n'
			+'\\newcolumntype{D}[1]{>{\\raggedright\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}p{#1}}\n'
			+'\\newcolumntype{R}[1]{>{\\raggedleft\\let\\newline\\\\\\arraybackslash\\hspace{0pt}}b{#1}}\n'
			+'\\cftpagenumbersoff{section}'
			+'\\usepackage[paper=a4paper,left=16mm,right=16mm,top=20mm,bottom=20mm]{geometry}\n'
			+'\\usepackage[colorlinks, pdfpagelabels, pdfstartview = FitH,bookmarksopen = true, bookmarksnumbered = true, linkcolor = black, plainpages = false, citecolor = black]{hyperref}\n'
			+'\\begin{document}\n'
			+'\\tableofcontents\n'
			+'\\clearpage\n')
	
	def end(self, stream):
		stream.write('\\end{document}\n')

	def tocheader(self, stream):
		stream.write('\\select@language {ngerman}\n')

#regex expression for parsing
titleRegex = re.compile('\[([\w\s\',-]+)\]', re.UNICODE)
headerRegex = re.compile('([A-Za-z0-9]+):(.+)', re.UNICODE )
personRegex = re.compile('([A-Za-z0-9]+):\s*([0-9]+)\s*([A-Za-zäöüÖÄÜ]*)', re.UNICODE )
setPersonRegex = re.compile('\[([\w\s\',-]+)\]([0-9]+)', re.UNICODE)
ingredientRegex = re.compile('>\s*([0-9\.-]*)\s*([\w]*)\s+([\w][\w\-:\s,]+)/?([\w\-:\s,]*)$', re.UNICODE)
timeRegex = re.compile('\(s*([\w\s-]+)', re.UNICODE)
emptyRegex = re.compile('^\s*$', re.UNICODE)

#gets all successive lines without empty lines in between
def getTextBlock(f, lines = []):
	while True:
		line = f.readline()
		line = line.split("#")[0] #discard comments

		if emptyRegex.match(line) != None:
			return lines
		lines.append(line)

#converts all strings including '' to float
def str2float(string):
	if not string:
		return 0
	return float(string)

#coverts all floats to string, 0 = ''
def float2str(number):
	if number == 0:
		return '';
	return str(number)

#writes line to stream
def writeline(stream, line):
	stream.write(line + '\n')

# converts number to latex fraction
def fraction(a,frac):
	fract = [[9,1,1,1,1,2,3,5,9],[9,6,4,3,2,3,4,6,9]]
	border = [0.083,0.208,0.292,0.417,0.583,0.708,0.792,0.917,2]
	b = a-int(a)
	i = 0
	while b > border[i]:
		i = i+1
	c = int(a+0.083)
	if fract[0][i] != 9 and frac:
		output = '%s$\\frac{%s}{%s}$' % (float2str(c), float2str(fract[0][i]),float2str(fract[1][i]))
	else:
		if frac:
			output = float2str(c)

		else:
			exp = int(math.log10(a))-1
			a = round(a*2,-exp)/2
			if a == int(a):
				output = float2str(int(a))
			else :
				output = float2str(a)
	return output
