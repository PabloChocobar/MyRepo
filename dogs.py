
import os
import json
from PIL import Image
from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage

app = ClarifaiApp(api_key='f7f15032b1a04f1fafc2092c63e50e9f')
model = app.models.get('general-v1.3')

# detect image contents for all subimages
pixels = []
for i in range(0,87*87):
    image = ClImage(file_obj=open("hotdogs/out"+str(i).zfill(4)+".jpg", 'rb'))
    response = model.predict([image])

    hot = False
    concepts = response['outputs'][0]['data']['concepts']
    for concept in concepts:
        if 'food' in concept['name']:
            hot = True
    pixels += [1 if hot == True else 0]

# make qr code image
(w,h)=(87,87)

outimg = Image.new( 'RGB', (w,h), "white")
pixels_out = outimg.load()

p = 0
for i in range(0,h):
    for j in range(0,w):
        print(pixels[p])
        if pixels[p] == 1:
            pixels_out[j,i]=(0,0,0)
        else:
            pixels_out[j,i]=(255,255,255)
        p += 1

outimg = outimg.resize((5*w,5*h))
outimg.save("pixels_outimg2.png","png")
