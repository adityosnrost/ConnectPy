import sys
from PIL import Image, ImageWin

file_name = sys.argv[1]
file_name_out = sys.argv[2]
img = Image.open (file_name)
result_width = 1080
result_height = 1080
	
# 1920x1080 to 1080x1080
# border_height = (img.height-result_height)/2
# border_width = (img.width-result_width)/2
# print border_height
# print border_width
# img = img.crop((border_width, border_height, img.width-border_width, img.height-border_height))


# border_height = (img.height-result_height)/2
border_width = (img.width-result_width)/2
img = img.crop((border_width, 340, img.width-border_width, 1350))
	
img.save(file_name_out)