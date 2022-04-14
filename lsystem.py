import sys, os
import turtle as tt

tt.hideturtle()
tt.speed(0)

class Lsystem:
	def __init__(self):
		self.name = ''
		self.variables = []
		self.constants = []
		self.axiom = ''
		self.rules = []
		self.angle = 90
		self.step = 10
		self.generation = []
		self.iterations = 1
	
	def __repr__(self):
		return ("<Lsystem>\n\t"\
			+ "name: {}\n\t"\
			+ "variables: {}\n\t"\
			+ "constants: {}\n\t"\
			+ "axiom: {}\n\t"\
			+ "rules: {}\n\t"\
			+ "angle: {}\n"\
			+ "</Lsystem>\n"\
		).format(
			str(self.name),
			str(self.variables),
			str(self.constants),
			str(self.axiom),
			str(self.rules),
			str(self.angle)
		)

	def parse_file(self,filename):
		print("Parsing file \"{}\" ...".format(filename))
		with open(filename,'r') as infile:
			
			lines = infile.readlines()
			self.name = os.path.basename(filename).split('.')[0]
			
			for line in lines:

				if not line.strip() or line.strip()[0].startswith('#'):
					continue

				split_line = line.split()
				print(len(split_line[0]))
				if (split_line[0] == 'terminal'):
					self.constants.append(split_line[1])
				elif (split_line[0] == 'axiom'):
					self.axiom = split_line[1]
				elif (split_line[0] == 'rule'):
					non_terminal, expansion = split_line[1].split('->')
					if not non_terminal in self.variables:
						self.variables.append(non_terminal)
					self.rules.append((non_terminal.strip(), expansion.strip()))
				elif (split_line[0] == 'angle'):
					self.angle = float(split_line[1])
				elif (split_line[0] == 'step'):
					self.step = int(split_line[1])
				elif (split_line[0] == 'iterations'):
					self.iterations = int(split_line[1])
				else:
					raise Exception('\n[ERROR] Cannot parse line: {}\n'.format(line))

			if (
				self.name == '' or self.variables == [] or \
				self.axiom == '' or self.rules == [] or \
				self.angle == None
			):
				print("[ERROR] Parsing failed. Missing some field")
				print(self)
				exit(1)

		print("Finished parsing")

	def compile(self, filename):
		try:
			self.parse_file(filename)
		except IOError:
			print("[ERROR] File {} not found".format(filename))
			print("\nTry any of the following from examples directory")
			print(os.listdir('examples'))
			print("\nExample:")
			print("python lsystem.py examples/pythagoriantree.txt 4")
			exit(1)

		print("Compiling ..."),
		self.generation.append(self.axiom)
		for i in range(self.iterations):
			self.generation.append(self.expand(self.generation[i]))
		print("Done")

	def expand(self,string):
		expanded_string = ''
		for character in string:
			if character in self.constants:
				expanded_string += character
			elif character in self.variables:
				for rule in self.rules:
					if rule[0] == character:
						expanded_string += rule[1]
						break
			else:
				raise Exception(
					'[ERROR] Unknown character {} in string {}\n'.format(character, string)
				)

		return expanded_string	

	def draw(self):
		screen = tt.Screen()
		screen.tracer(0)

		stack = []
		tt.penup()
		tt.setpos(0, -200)
		tt.seth(90)
		tt.pendown()

		print("Drawing the lsystem ...")
		for i, codebit in enumerate(self.generation[-1]):

			if codebit in ['F', 'A', 'B']:
				tt.forward(self.step)
			elif codebit == '+':
				tt.right(self.angle)
			elif codebit == '-':
				tt.left(self.angle)
			elif codebit == '[':
				stack.append((tt.pos(), tt.heading()))
			elif codebit == ']':
				position, heading = stack.pop()
				tt.penup()
				tt.goto(position)
				tt.seth(heading)
				tt.pendown()

		print("Done drawing")
		print("Saving file as {}.jpg".format(self.name)),
		self.save()
		print("Done")

		screen.update()
		screen.mainloop()

	def save(self):
		from PIL import Image
		from PIL import EpsImagePlugin
		import io

		EpsImagePlugin.gs_windows_binary =  r'C:\Program Files\gs\gs9.56.1\bin\gswin64c' # change to location of GhostScript

		screen = tt.getscreen()
		canvas = screen.getcanvas()
		postscript = canvas.postscript().encode('utf-8')
		img = Image.open(io.BytesIO(postscript))
		img.save('pics/{}.jpg'.format(self.name))

if __name__ == '__main__':

	lsystem = Lsystem()

	try:
		lsystem.compile(sys.argv[1])

		print(lsystem) 
		lsystem.draw()
	except IndexError:
		print("[ERROR] Wrong usage. Use the following syntax")
		print("$ python lsystem.py filename\n")
		print("Example: ")
		print("$ python lsystem.py lsys/plant.lsys")
		exit(1)