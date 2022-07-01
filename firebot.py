import sys
from simulation import Simulation

#
# TODO
#

############invalid#################
def invalid():
	print("Invalid command")
	
def invalid2():
	print("Usage: python firebot.py <seed> <width> <height>")
############invalid#################

try:
	if len(sys.argv)>4:
		invalid2()
		exit()
	seed=int(sys.argv[1])
	width=int(sys.argv[2])
	height=int(sys.argv[3])
	if width<=0 or height<=0:
		invalid2()
		exit()
	area=Simulation(seed,width,height)
except IndexError:
	invalid2()
	exit()
except ValueError:
	invalid2()
	exit()
	
#############cover##################
i=2
cover=["+"]
while i<2*int(width)+1:
	cover=cover+["-"]
	i+=1
cover=cover+["+"]
cover="".join(cover)
#############cover##################

#########initial_data###############
trees=area.generate_trees(area.seed)
Day=1
pollution=0
damage=0
wind="none"
tree_num=0
tree_burnt=0
for y in range(0,height):
	for x in range(0,width):
		if trees[y][x].height>0:
			tree_num=tree_num+1
#dir=["north","south","east","west","all","none"]#may use this for a shorter check?
#########initial_data###############

#############fire###################
def fire(x,y,counter):#burn!burn!burn!(set a tree on fire!)
	judge=fire2(x,y)
	if judge==True:
		trees[y][x].intensity=1
		counter +=1
	return counter

def fire2(x,y):#judgement
	current=trees[y][x]
	if current.height !=0 and current.intensity !=0 and current.Burnt_down==False:#a tree on fire and not burnt down
		return "fire"
	if current.height !=0 and current.intensity ==0 and current.Burnt_down==False:#a tree not on fire or not burnt down
		return True
	return False#not a tree
#############fire2##################

############region##################
def region(word):
	if word[1]=="all":
		x1=0
		y1=0
		x2=width
		y2=height
	else:
		x1=int(word[1])
		y1=int(word[2])
		if x1<0 or y1<0:
			invalid()
			return False
		else:
			if len(word)>3:
				if int(word[3])<=0 or int(word[4])<=0:
					invalid()
					return False
				else:
					x2=x1+int(word[3])
					y2=y1+int(word[4])
			else:
				x2=x1+1
				y2=y1+1
			if x2>width or y2>height:
				invalid()
				return False
	return (x1,y1,x2,y2)
############region##################

#############wind##################
def windy(x,y,direction):
	if direction=="north":
		xw=x
		yw=y-1
	elif direction=="east":
		xw=x+1
		yw=y
	elif direction=="west":
		xw=x-1
		yw=y
	elif direction=="south":
		xw=x
		yw=y+1
	elif direction=="none":
		return
	elif direction=="all":
		windy(x,y,"north")
		windy(x,y,"south")
		windy(x,y,"west")
		windy(x,y,"east")
		return
	else:
		return False
	if xw<0 or yw<0 or xw>width-1 or yw>height-1:
		return
	judge=fire2(xw,yw)
	if judge==True:
		fire(xw,yw,0)
		trees[yw][xw].spread=False
#############wind##################

###########extinguish###############
def extinguish(x,y,counter):
	current=trees[y][x]
	current_intensity=int(current.intensity)
	current_height=int(current.height)
	judge=fire2(x,y)
	if judge=="fire":
		trees[y][x].intensity=0
		counter +=1
	return counter
###########extinguish###############

print("Day: {}".format(Day))
print("Wind: {}".format(wind))
print()

while True:
	try:
		word=input("> ")
		word=word.lower()
		word=word.split()
		if len(word)==0:
			break
		command=word[0]
		if len(word)>5:
			invalid()

		elif command=="bye":
			if len(word)==1:
				break
			else:
				invalid()

		elif command=="help":
			if len(word)==1:
				print("BYE\nHELP\n\nDATA\nSTATUS\n\nNEXT <days>\nSHOW <attribute>\n\nFIRE <region>\nWIND <direction>\nEXTINGUISH <region>")
			else:
				invalid()

		elif command=="status":
			if len(word)==1:
				print("Day: {}".format(Day))
				print("Wind: {}".format(wind))
			else:
				invalid()

		elif command=="data":
			if len(word)==1:
				print("Damage: {:.2f}%".format(damage*100))
				print("Pollution: {}".format(pollution))
			else:
				invalid()
				
		elif command=="next":
			if len(word)>2:
				invalid()
			else:
				if len(word)==1:
					Day=Day+1
					past=1
				else:
					past=int(word[1])
					Day=Day+past
	
				if past>0:
					print("Day: {}".format(Day))
					print("Wind: {}".format(wind))
					i=0
					while i<past:
						for x in range(0,width):
							for y in range(0,height):
								trees[y][x].spread=True
		#######################fire_update######################################
						for x in range(0,width):
							for y in range(0,height):
								judge=fire2(x,y)
								if judge=="fire" and trees[y][x].spread==True:
									windy(x,y,wind)
									current_intensity=trees[y][x].intensity
									trees[y][x].intensity=current_intensity+1
								if judge=="fire" and trees[y][x].intensity>9:
									current_height=trees[y][x].height
									if trees[y][x].Burnt_down==False:
										trees[y][x].height=current_height-1
										if trees[y][x].height<=0:
											trees[y][x].Burnt_down=True
		#######################fire_update######################################					

		#######################pollution########################################
						for x in range(0,width):
							for y in range(0,height):
								if trees[y][x].Burnt_down==True:
									current_height=0
									current_intensity=0
									tree_burnt=tree_burnt+1 #for damage
								else:
									current_height=int(trees[y][x].height)
									if trees[y][x].intensity==0:
										current_intensity=0
									else:
										current_intensity=int(trees[y][x].show_intensity())
								pollution=pollution-current_height+current_intensity
						if pollution<0:
							pollution=0
		#########################pollution######################################

						damage=tree_burnt/tree_num #damage
						tree_burnt=0
						i+=1
				else:
					invalid()

		elif command=="show":
			if len(word)>2:
				invalid()
			elif word[1]=="fire":
				print(cover)
				for i in trees:
					print("|",end="")
					for num, y in enumerate(i):
						if num==width-1:
							print(y.show_intensity(),end="|\n")
						else:
							print(y.show_intensity(),end=" ")
				print(cover)
			elif word[1]=="height":
				print(cover)
				for i in trees:
					print("|",end="")
					for num, y in enumerate(i):
						if num==width-1:
							print(y.show_height(),end="|\n")
						else:
							print(y.show_height(),end=" ")
				print(cover)
			else:
				invalid()
		elif command=="wind":
			direction=word[1]
			if direction !="north" and direction !="none" and direction !="west" and direction !="south" and direction !="all" and direction !="east":
				invalid()
			elif len(word)>2:
				invalid()
			else:
				wind=direction
				print("Set wind to {}".format(wind))

		elif command=="fire":
			cood=region(word)
			if cood !=False:
				x1=cood[0]
				y1=cood[1]
				x2=cood[2]
				y2=cood[3]
				counter=0
				for x in range(x1,x2):
					for y in range(y1,y2):
						counter=fire(x,y,counter)
				if counter !=0:
					print("Started a fire")
				else:
					print("No fires were started")

		elif command=="extinguish":
			cood=region(word)
			if cood !=False:
				x1=cood[0]
				y1=cood[1]
				x2=cood[2]
				y2=cood[3]
				counter=0
				for x in range(x1,x2):
					for y in range(y1,y2):
						counter=extinguish(x,y,counter)
				if counter !=0:
					print("Extinguished fires")
				else:
					print("No fires to extinguish")
		else:
			invalid()
	except EOFError:
		print()
		break
	except IndexError:
		invalid()
	except ValueError:
		invalid()
	print()
print("bye")
