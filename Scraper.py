from htmldom import htmldom
import re
import sys
from pygeocoder import Geocoder
from time import sleep
f= open('schools.csv','w',encoding='utf-8')
count=0
f.write("URL,Rank,School Name,Address,place,lat,long")
f.write('\n')
wll=0
g= Geocoder('174144268604','AIzaSyBwDjyf8qevMrJV_363m8sMhk1WlaAcJgc')

for x in range(1,23):
	print("Loading",end='')
	dom = htmldom.HtmlDom("http://www.usnews.com/education/best-high-schools/national-rankings/spp%2B100/page+"+str(x))
	dom = dom.createDom()
	school = dom.find("tbody>tr").has(".rankings-score") 
	#these are the various attributes of the schools.
	for row in school:
		count+=1
		url="http://www.usnews.com"+row.find(".school-name").find("a").attr("href")
		sname=row.find(".school-name").text().replace(',',"").replace("\n",'').replace('&amp;','&')
		f.write(sname)
		f.write(',')
		addr = ""
		for div in row.find(".school-address>div"):
			addr+=div.text().replace(',','')
			f.write(div.text().replace(',',''))
			addr+=" "
			f.write(" ")
		sleep(0.05)
		f.write(',')
		try:
			results = Geocoder.geocode(addr)
			(lat,lng)=results[0].coordinates
			f.write(str(lat))
			f.write(',')
			f.write(str(lng))
			f.write('\n')
			print(".",end="")
			continue
		except Exception:
			print("X",end="")
		f.write(',')
		f.write(row.find('.lead-value').text())
	print("PAGE",x,"DONE",end='')
	print('\n')
f.close()
print("DONE")
print("Scraped",count,"schools over",x,"pages.",wll,"failed lat & long",end='')
