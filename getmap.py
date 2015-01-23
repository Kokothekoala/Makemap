from math import tan,asinh,pi
import os
import urllib
import Image
import ImageFont
import ImageDraw
#XXX: different files

class getTile:
  def __init__(self,zoom,lat,lon):
    if int(zoom)>0 and int(zoom)<19:
      self.zoom=int(zoom)
    else:
      raise ValueError("Zoom should be in range [0,19]")
    if lat>-180 and lat<180: 
      self.lat=lat
    else:
      raise ValueError("Lattitude should be in range [-180,180]")
    if lon>-90 and lon<90:
      self.lon=lon
    else:
      raise ValueError("Longitude should be in range [-90,90]")
    self.degreetotile()
    print(str(self.x)+" "+str(self.y))
  
  def d2r(self,degree):
    return degree*pi/180

  def degreetotile(self):
    n=pow(2,self.zoom)
    self.x=int(n*(self.lon+180)/360)
    self.xpx=(n*(self.lon+180)/360-self.x)*256
    self.y=int(n*(1-asinh(tan(self.d2r(self.lat)))/pi)/2)
    self.ypx=(n*(1-asinh(tan(self.d2r(self.lat)))/pi)/2-self.y)*256



class getTiles:

  def __init__(self,zoom,bound1,bound2,server,ext,out):
    self.bound1=bound1
    self.bound2=bound2
    self.urlparts=[]
# XXX: should take regex as server
    self.server=server
    self.ext=ext
    self.out=out
    self.zoom=zoom
    self.testfunc()


  def generatelist(self):
    for i in range(self.bound1.x,self.bound2.x+1):
      for j in range(self.bound1.y,self.bound2.y+1):
        print (str(i))
        self.urlparts.append("/"+str(self.zoom)+"/"+str(i)+"/"+str(j))
    print(str(len(self.urlparts)))
  

  def makedirs(self):
    for i in range(self.bound1.x,self.bound2.x+1):
      if not os.path.exists(self.out+"/"+str(self.zoom)+"/"+str(i)):
        os.makedirs(self.out+"/"+str(self.zoom)+"/"+str(i))

  def downloadtiles(self):
    j=0
    for i in self.urlparts:
      j+=1
      print("Downloading tile "+str(j)+" of "+str(len(self.urlparts)))
      url=self.server+i+"."+self.ext
      print(url)
      filename=self.out+i+"."+self.ext
      print filename
      urllib.urlretrieve(url,filename)

  def testfunc(self):
    self.generatelist()
    self.makedirs()
    self.downloadtiles()

class Overlay:
  
  def __init__(self,zoom,bound1,bound2,layers,label,result):
    self.zoom=zoom
    self.bound1=bound1
    self.bound2=bound2
    self.layers=layers
    self.result=result
    self.label=label

  def makemap(self):
    sizex=256*(abs(self.bound2.x-self.bound1.x)+1)
    sizey=256*(abs(self.bound2.y-self.bound1.y)+1)
    size=(sizex,sizey)
    back=Image.new("RGB",size)
    draw=ImageDraw.Draw(back)
    for x in range(self.bound1.x,self.bound2.x+1):
      for y in range(self.bound1.y,self.bound2.y+1):
        for layer in self.layers:
          f=open(layer+"/"+str(self.zoom)+"/"+str(x)+"/"+str(y)+".png")
          ol=Image.open(f) 
          posx=x/self.bound1.x*sizex
          posy=x/self.bound1.x*sizex
          #ol.convert("RGBA")
          back.paste(ol,((x-self.bound1.x)*256,(y-self.bound1.y)*256),ol)
          f.close()
    #for label in self.labels:
    for x in self.label:
      posx=x[2][0]
      posy=x[2][1]
      bd=getTile(self.zoom,posx,posy)
      posxx=(bd.x-self.bound1.x)*256+int(bd.xpx)
      posyy=(bd.y-self.bound1.y)*256+int(bd.ypx)
      if x[0]=="city":
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 7+pow(self.zoom-7,2)*2)
        coef=self.zoom/2
        draw.polygon(((posxx+coef,posyy+coef),(posxx+coef,posyy-coef),(posxx-coef,posyy-coef),(posxx-coef,posyy+coef)),fill=(255,0,0,255))
        w, h = draw.textsize(x[1],font=font)
        draw.text((posxx-w/2,posyy-h-coef),x[1].decode("utf8"),(0,0,0,255),font=font)
      if x[0]=="town":
        font = ImageFont.truetype("DejaVuSans.ttf", 8+pow(self.zoom-8,2))
        coef=self.zoom/4
        draw.polygon(((posxx+coef,posyy+coef),(posxx+coef,posyy-coef),(posxx-coef,posyy-coef),(posxx-coef,posyy+coef)),fill=(255,129,235,255))
        w, h = draw.textsize(x[1],font=font)
        draw.text((posxx-w/2,posyy-h-coef),x[1].decode("utf8"),(0,0,0,255),font=font)
      if x[0]=="village":
        font = ImageFont.truetype("DejaVuSans.ttf", 10+pow(self.zoom-10,2))
        coef=self.zoom/8
        draw.polygon(((posxx+coef,posyy+coef),(posxx+coef,posyy-coef),(posxx-coef,posyy-coef),(posxx-coef,posyy+coef)),fill=(255,129,235,255))
        w, h = draw.textsize(x[1],font=font)
        draw.text((posxx-w/2,posyy-h-coef),x[1].decode("utf8"),(0,0,0,255),font=font)
      if x[0]=="camp":
        font = ImageFont.truetype("DejaVuSans.ttf", 9+pow(self.zoom-9,2))
        coef=self.zoom/4
        #if len(x[1])>10:
        #  towrite=x[1].decode("utf8")[0:15]+"-"
        #else:
        #  towrite=x[1]
        towrite="Primitiv"
        draw.polygon(((posxx+coef,posyy+coef),(posxx-coef,posyy+coef),(posxx,posyy-coef)),fill=(0,130,0,255))
        w, h = draw.textsize(towrite,font=font)
        draw.text((posxx-w/2,posyy-h-coef),towrite,(0,130,0,255),font=font)




        #f1=open(self.layer1+"/"+str(self.zoom)+"/"+str(x)+"/"+str(y)+".png")
        #f2=open(self.layer2+"/"+str(self.zoom)+"/"+str(x)+"/"+str(y)+".png")
        #ol1=Image.open(f1)
        #ol2=Image.open(f2)
        #posx=x/self.bound1.x*sizex
        #posy=x/self.bound1.x*sizex
        #ol1.convert("RGBA")
        #back.paste(ol1,((x-self.bound1.x)*256,(y-self.bound1.y)*256))
        #ol2.convert("RGBA")
        #back.paste(ol2,((x-self.bound1.x)*256,(y-self.bound1.y)*256),ol2)
        #
        #f1.close()
        #f2.close()

    back.show()
    back.save(self.result)
             
bound1=getTile(10,56.2,7.860718)
bound2=getTile(10,54.7,13.002319)
#gt=getTiles(10,bound1,bound2,"http://a.www.toolserver.org/tiles/osm-no-labels","png","nolabels")
#gt=getTiles(10,bound1,bound2,"http://tile.lonvia.de/cycling","png","lonviacycle")
#gt=getTiles(8,bound1,bound2,"http://toolserver.org/~cmarqu/hill/","png","hillshading")
#os.system("sh lonviacycle/massconvert.sh")
#os.system("sh hillshading/massconvert.sh")
f=open("cities","r")
cities=[]
for line in f:
  llist=line.rstrip("\n").split(" ")
  if len(llist)==3:
    cities.append(("city",llist[0],(float(llist[2]),float(llist[1]))))
  elif len(llist)>3:
    llist2=(llist[0:-2],llist[-2],llist[-1])
    print llist2
    cities.append(("city",llist2[0],(float(llist2[2]),float(llist2[1]))))
f.close()
f=open("town","r")
for line in f:
  llist=line.rstrip("\n").split(" ")
  if len(llist)==3:
    cities.append(("town",llist[0],(float(llist[2]),float(llist[1]))))
  elif len(llist)>3:
    llist2=(" ".join(llist[0:-2]),llist[-2],llist[-1])
    print llist2
    cities.append(("town",llist2[0],(float(llist2[2]),float(llist2[1]))))
f.close()
f=open("village","r")
for line in f:
  llist=line.rstrip("\n").split(" ")
  if len(llist)==3:
    cities.append(("village",llist[0],(float(llist[2]),float(llist[1]))))
  elif len(llist)>3:
    llist2=(" ".join(llist[0:-2]),llist[-2],llist[-1])
    print llist2
    cities.append(("village",llist2[0],(float(llist2[2]),float(llist2[1]))))
f.close()
f=open("camping","r")
for line in f:
  llist=line.rstrip("\n").split(" ")
  if len(llist)==3:
    cities.append(("camp",llist[0],(float(llist[2]),float(llist[1]))))
  elif len(llist)>3:
    llist2=(" ".join(llist[0:-2]),llist[-2],llist[-1])
    print llist2
    cities.append(("camp",llist2[0],(float(llist2[2]),float(llist2[1]))))
ol=Overlay(10,bound1,bound2,("nolabels","lonviacycle"),cities,"out.png")
ol.makemap()
