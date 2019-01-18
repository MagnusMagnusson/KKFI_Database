from PIL import Image
from PIL import ImageDraw, ImageFont
import io
import zipfile
from django.utils.encoding import *
from django.db import transaction
from catdb.models import *

def get_nomtag(nomination):
	bigFont = ImageFont.truetype("/opt/django-env/kkidb/catdb/static/OpenSans-Bold.ttf", 42)
	smallFont = ImageFont.truetype("/opt/django-env/kkidb/catdb/static/OpenSans-Light.ttf", 18)
	buff = io.BytesIO()
	ZF = zipfile.ZipFile(buff,mode='w')
	w = 595 / 2
	h = 210
	count = len(nomination['Everyone'])
	if(count % 2 == 1):
		count += 1
	if(count > 1):
		col = 2
	row = count / 2

	page = 0
	img = None
	i = -1
	for cat in nomination['Everyone']:
		i += 1
		if(i % 8 == 0):
			if img != None:
				with io.BytesIO() as output:
					img.save(output,format="BMP")
					contents = output.getvalue()
					ZF.writestr("Image"+str(i/8)+".bmp",contents)
			img = Image.new("RGB",(w * col,h*4),"#FFFFFF")
			draw = ImageDraw.Draw(img)
		wOffset = ((i % 8) % 2) * w
		hOffset = ((i % 8) / 2) * h
		text = "UNKNOWN"
		if cat in nomination['Kittens']:
			text = "Kitten"
		elif cat in nomination['Younglings']:
			text = "Junior"
		elif cat in nomination['Males']:
			text = "Male"
		elif cat in nomination['Females']:
			text = "Female"
		elif cat in nomination['nMales']:
			text = "N.Male"
		elif cat in nomination['nFemales']:
			text ="N.Female"

		draw.text((wOffset + 34,hOffset + 34),cat.color.ems.breed +" "+ cat.color.ems.ems,fill="#000000",font = smallFont)
		draw.text((wOffset + w - 80,hOffset + 34),text,fill="#000000",font = smallFont)
		draw.text((wOffset + 35,hOffset + h - 34),cat.judge.name,fill="#000000",font = smallFont)
		draw.text((wOffset + w - 80,hOffset + h - 34),"Cat. "+ str(cat.color.ems.category),fill="#000000",font = smallFont)
		draw.text((wOffset + (w/2),hOffset + (h/2)-21),str(cat.entryId.cat_show_number),fill="#000000",font = bigFont)


	if i % 8 != 0:
		with io.BytesIO() as output:
			img.save(output,format="BMP")
			contents = output.getvalue()
			ZF.writestr("Image"+str(1 + (i/8))+".bmp",contents)
	ZF.close()
	return buff
