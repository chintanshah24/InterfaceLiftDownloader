from lxml import html
import requests
import urllib2
import os

def getList(url):

	"""
	This function takes a url as a parameter, extracts .jpg file names from href attribute and stores it in a list.
	It then calls downloadFiles passing the list as a parameter.

	"""

	url_to_use=url
	header={'User-agent': 'Mozilla/5.0'}
	page=requests.get(url_to_use,headers=header)
	tree=html.fromstring(page.text)
	n=tree.xpath('//*[@id="page"]/div[4]/div[1]/p[2]/b[2]/text()')
	no_of_pages=int(n[0])
	list_of_urls=tree.xpath('//*[@id="wallpaper"]/div/div/div[@class="preview"]/div[2]/div/a/@href')
	

	for i in range(2,no_of_pages+1):
		url_to_use=url_to_use+'index'+str(i)+'.html'
		page=requests.get(url_to_use,headers=header)
		url_to_use=url
		tree=html.fromstring(page.text)
		temp_list=tree.xpath('//*[@id="wallpaper"]/div/div/div[@class="preview"]/div[2]/div/a/@href')
		list_of_urls=list_of_urls+temp_list

	print("Downloading files.....")
	downloadFiles(list_of_urls)

def downloadFiles(list_of_urls,path="imgs/"):

	"""
	This takes the list as a parameter and downloads them onto the harddisk into a imgs folder
	"""

	for i in range(0,len(list_of_urls)):
		print("Downloading file "+str(i+1))
		url='http://interfacelift.com'+list_of_urls[i]	
		#this line checks if imgs directory doesn't exist, it creates one
		if not os.path.exists(path):
			os.makedirs(path)
		filename=path+url.split("/")[-1]
		opener=urllib2.build_opener()
		opener.addheaders=[('User-agent','Mozilla/5.0')]
		img=opener.open(url)
		localFile=open(filename,'wb')
		localFile.write(img.read())
		localFile.close()

	print("Done downloading.....")

# Just edit this url to whatever suits you, making sure the resolution is a part of the url, best suggestion is to make a url from the site itself
getList("http://interfacelift.com/wallpaper/downloads/rating/wide_16:10/2880x1800/")
