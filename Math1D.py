from PIL import Image, ImageDraw, ImageColor
from math import sqrt

def draw_box(x1, y1, x2, y2, file):
	draw = ImageDraw.Draw(file)
	draw.rectangle((x1, y1, x2, y2), fill=None, outline=0, width=5)
	file.save("test.png")

def draw_point(x, y, file): 
	draw = ImageDraw.Draw(file)
	draw.point((x, y))

def generate_rainfall_list():
	global rainlist
	for i in range(5):
		rainlist[i].append(rain.getpixel((2620,1900+82*i)))
		rainlist[i+5].append(rain.getpixel((3220,1900+82*i)))
		
def generate_temp_list():
	for i in range(3):
		templist[i].append(temp.getpixel((2665,2020+i*90)))
		templist[i+3].append(temp.getpixel((3150,2020+i*90)))

def draw_cross(x,y,file):
	draw = ImageDraw.Draw(file)
	draw.line((x+5,y+5,x-5,y-5), fill=(0,255,0), width=2)
	draw.line((x+5,y-5,x-5,y+5), fill=(0,255,0), width=2)
	file.save("test.png")

def generate_contour_list():
	global elevlist
	elevlist = [[1 for j in range(115)] for i in range(1840)]
	for i in range(855,2695):
		for j in range(1900,2015):
			elevlist[i-855][j-1900] = elev.getpixel((i,j))

def get_contour(x,y):
	if elev.getpixel((x,y))[0] < 255 - white_thres and elev.getpixel((x,y))[1] < 255- white_thres and elev.getpixel((x,y))[2] < 255- white_thres:
		for i in range(855,2695):
			for j in range(1900,2015):
				if elevlist[i-855][j-1900][0]-offset < elev.getpixel((x,y))[0] and elev.getpixel((x,y))[0] < elevlist[i-855][j-1900][0]+offset and elevlist[i-855][j-1900][1]-offset < elev.getpixel((x,y))[1] and elev.getpixel((x,y))[1] < elevlist[i-855][j-1900][1]+offset and elevlist[i-855][j-1900][2]-offset < elev.getpixel((x,y))[2] and elev.getpixel((x,y))[2] < elevlist[i-855][j-1900][2]+offset:
					h = ((1231 - (((i-860)/1840) * 1024) ) * 0.2 ) / 1000
					return h

def get_rainfall(x,y):
	for i in range(10):
		if rainlist[i][1] == rain.getpixel((x,y)):
			#draw_cross(x,y,rain)
			return(rainlist[i][0])

def get_temp(x,y):
	for i in range(6):
		if templist[i][1] == temp.getpixel((x,y)):
			#draw_cross(x,y,temp)
			return(templist[i][0])

def get_distance(x1,y1,x2,y2,z):
	d = sqrt(pow((x1-x2) * 0.2 ,2)+pow((y1-y2) * 0.2 ,2) +pow(z,2)) 
	return d

def get_radius(x1,y1,x2,y2):
	r = sqrt(pow((x1-x2),2)+pow((y1-y2),2))  * 0.2
	return r

def put_pixel(x,y,i):
	i = int(i*1.3) 
	r = 0
	g = i
	b = 255
	if i>255:
		g = 255
		b = 511 - i
	print(i,r,g,b)

	for i in range(10):
		for j in range(10):
			new_map.putpixel((x+i-4,y+j-4), (r,g,b))

with Image.open("Images/Elevation.png") as elev, Image.open("Images/Rainfall.png") as rain, Image.open("Images/Temperature.png") as temp:
	
	new_map = Image.new('RGB',(temp.size[0],temp.size[1]),color=(255,255,255))
	rainlist = [[16],[20.3],[24],[27.1],[29.8],[32.4],[35.5],[39.2],[43.5],[48.5]]
	templist = [[73.6],[75.4],[76.7],[77.5],[78.5],[81.7]]
	elevlist = list(list())
	indexlist = list()

	offset = 10
	white_thres = 5
	height = 0
	rainfall = 0

	generate_rainfall_list()
	generate_temp_list()
	generate_contour_list()

	#East Factory
	# 3200
	# 820
	# x (2650,3350)
	# y (300,1400)

	# West Factory
	# 2140
	# 1430
	# x 1600,2690
	# y 900,1980

	# Whole Map
	# x 270,3330
	# y 250,1725

	dest_x = 2140
	dest_y = 1430

	for x in range(1600,2690,10):
		for y in range(900,1980,10):
			r = get_radius(x,y,dest_x,dest_y)
			if r < 100:
				#print(x,y)
				rainfall = get_rainfall(x,y)
				temperature = get_temp(x,y)
				height = get_contour(x,y)
	
				if rainfall == None or temperature == None or height == None or height == None:
					pass
				else:
					distance = get_distance(x,y,dest_x,dest_y,height)
					print("rainfall:", rainfall)
					print("temperature:", temperature)
					print("height:", height)
					print("distance:", distance)
					index = (rainfall*(2*height - height**2)*(100*distance-distance**2))/(temperature)
					print("index:",index)
					indexlist.append(index)
					put_pixel(x,y,index)
					print("x",x,"y",y,"RGB:", 50, (int(index)-5)*32, 255 - (int(index)-5)*32 )
			else:
				pass
		#print(x)
	print("Max:", max(indexlist))
	print("Min:", min(indexlist))
	new_map.save('new_map.png')