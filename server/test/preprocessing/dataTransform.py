from PIL import Image, ImageFont, ImageDraw
import hashlib
#from osgeo import gdal

#gets Summer Stats using the GDAL lib
def summary_stats(image_file):
    sumstats=[[0,0,0,0],0,0,"VolcanoID"]
     #sumstats[0]= coordinates [N,E,S,W]
     #sumstats[1]= satellite info (int?)
     #sumstats[2]= volcano id int
     #sumstats[3]= volcano name string
    return (sumstats)

#adds Text to an image file
def add_text(image_file, text, position=(0, 0)):
    img = Image.open(image_file)
    draw = ImageDraw.Draw(img)
    draw.text(position, text, (0,0,0)) #(0,0,0) is color Black
    draw = ImageDraw.Draw(img)
    return img

#compresses and saves images
def compress_image(image_file, compression_amount=85):
    img = Image.open(image_file)
    width, height= img.size
    img = img.resize((width,height),Image.LANCZOS)
    return img

#Saves the 4 images with the hash as their name
def save_images(image_file):
    ogImg = Image.open(image_file)
    sumStats=summary_stats(image_file)
    ImgName=str(sumStats[1])+" "+str(sumStats[2]) #Satellite Info and Volcano ID
    saveName=hashlib.sha256(ImgName.encode()).hexdigest()
    ogImg.save(saveName+".tif",optimize=True,quality=95)
    ogImg.save(saveName+".png",optimize=True,quality=95)
    compImg=compress_image(image_file)
    compImg.save(saveName+".comp.png",optimize=True,quality=95)
    modImg=add_text(image_file,sumStats[3], position=(0,0)) #Writes Volcano Name to image
    modImg.save(saveName+".mod.png",optimize=True,quality=95)
    return modImg
