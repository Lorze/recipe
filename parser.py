import re
import codecs
import glob

titleRegex = re.compile('\\n\\s*(?:\\\\[a-z]+\\{([0-9\\./]+)\\}(?:\\{([0-9./]*)\\})?(?:\\{([A-Za-z]*)\\})?)?([A-Za-z\\\\\\{\\}]*\\s*)&(.+?)(?=\\\\\\\\|&)&?([^&]*)\\\\(?:\\\\|end)', re.UNICODE)
blu =  re.compile('\\\\oder\\{([\\w\\s]+)\\}\\{([\\w\\s]+)\\}', re.UNICODE)
bla = re.compile('\\s+',  re.UNICODE)
time = re.compile('sekunde|minute|stunde|tag|woche|monat',  re.UNICODE | re.IGNORECASE)
titime = re.compile('\\\\addcontents[^\\\\\\n]*\\{([\\w\\s]+)(?:.*\\{([\\w\\s.]+)\\})?\\}', re.UNICODE)
device = re.compile('\\\\subsubsection.*\\{([^:\\n]*?)\\}', re.UNICODE)
persons = re.compile('\\\\pers\\{([0-9]+)\\}', re.UNICODE)

#read all filenames in Rezepte
files = glob.glob("RezepteLatex/*tex")   

def parseFloat(string):
	parts = string.split('/')

	if len(parts) == 1:
		return float(parts[0])
	else:
		return float(parts[0])/float(parts[1])

def stripString(adw):
	if not adw:
		return '';
	return bla.sub(adw.replace('\\\\', '').replace('\n', '').replace('\\', '\\\\'), ' ').strip()

def parseName(string, both):
	match = blu.match(string)

	if match:
		if both:
			return stripString(match.group(1)) + '/' + stripString(match.group(2))
		return stripString(match.group(1))
	return stripString(string)


#open every file, compile, write to tex
for name in files:
	f = codecs.open(name, 'r', encoding='utf-8')
	o = codecs.open(name.replace('RezepteLatex', 'Rezepte').replace('.tex', '.txt'), 'w', encoding='utf-8')
	content = f.read();

	print(name)
	match = titime.search(content)
	o.write('[%s]\n' % stripString(match.group(1)))
	o.write('time: %s\n' % stripString(match.group(2)))
	o.write('device: %s\n' % stripString(device.search(content).group(1)))
	o.write('persons: %s\n\n' % int(persons.search(content).group(1)))

	for match in titleRegex.finditer(content):
		line = '>'
		if match.group(1):
			line += str(parseFloat(match.group(1)))
		if match.group(2):
			line += '-' + str(parseFloat(match.group(2)))
		line += ' ';

		if match.group(3):
			line += match.group(3).strip() + ' '
		if match.group(4):
			line += parseName(match.group(4).strip(), False) + ' '
		if match.group(5):
			if time.search(match.group(5)):
				line = '(' + stripString(match.group(5));
			else:
				line += parseName(match.group(5).strip(), True) + ' '

		line = line.strip();
		if match.group(6).strip():
			if len(line) > 1:
				line += '\n'
			else:
				line = ''
			line += stripString(match.group(6)) + '\n'

		o.write(line + '\n');