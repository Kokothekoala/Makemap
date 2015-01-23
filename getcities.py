from imposm.parser import OSMParser

# simple class that handles the parsed OSM data.
class cityLister(object):
  citylist=[]
  townlist=[]
  villagelist=[]

  def nodes(self, nodes):
  # callback method for ways
    for osmid, tags, refs in nodes:
      if 'place' in tags and tags["place"]=="city":
        if "name" in tags:
          self.citylist.append((tags["name"],refs))
      if 'place' in tags and tags["place"]=="town":
        if "name" in tags:
          self.townlist.append((tags["name"],refs))
      if 'place' in tags and tags["place"]=="village":
        if "name" in tags:
          self.villagelist.append((tags["name"],refs))


class campingLister(object):
  campinglist=[]

  def nodes(self, nodes):
  # callback method for ways
    for osmid, tags, refs in nodes:
      if 'tourism' in tags and tags["tourism"]=="camp_site":
        if "name" in tags:
          if "Primitiv" in tags["name"] or "primitiv" in tags["name"]:
            self.campinglist.append(("Primitiv",refs))
          else:
            self.campinglist.append(("Camping",refs))

# instantiate counter and parser and start parsing
#c = cityLister()
#p = OSMParser(concurrency=4, nodes_callback=c.nodes)
#p.parse('denmark-latest.osm.pbf')
c=campingLister()
p = OSMParser(concurrency=4, nodes_callback=c.nodes)
p.parse('denmark-latest.osm.pbf')
#p.parse('dkcities.osm')

# done
f=open("camping",'w')
for camp in c.campinglist:
  f.write(camp[0].encode('utf8')+" "+str(camp[1][0])+" "+str(camp[1][1])+"\n")
f.close()
#f=open("cities",'w')
#for city in c.citylist:
#  f.write(city[0].encode('utf8')+" "+str(city[1][0])+" "+str(city[1][1])+"\n")
#f.close()
#f=open("town",'w')
#for town in c.townlist:
#  f.write(town[0].encode('utf8')+" "+str(town[1][0])+" "+str(town[1][1])+"\n")
#f.close()
#f=open("village",'w')
#for village in c.villagelist:
#  f.write(village[0].encode('utf8')+" "+str(village[1][0])+" "+str(village[1][1])+"\n")
#f.close()
