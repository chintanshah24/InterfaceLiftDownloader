from lxml import html
import requests
import sys
import urllib2
import os


def get_list_of_image_urls(url):
    """
	This function takes a url as a parameter, extracts .jpg file names from href attribute and stores it in a list.
	It then returns that list

	"""

    url_to_use = url
    header = {'User-agent': 'Mozilla/5.0'}
    page = requests.get(url_to_use, headers=header)
    tree = html.fromstring(page.text)
    n = tree.xpath('//*[@id="page"]/div[4]/div[1]/p[2]/b[2]/text()')
    no_of_pages = int(n[0])
    list_of_urls = tree.xpath('//*[@id="wallpaper"]/div/div/div[@class="preview"]/div[2]/div/a/@href')

    for i in range(2, no_of_pages + 1):
        url_to_use = url_to_use + 'index' + str(i) + '.html'
        page = requests.get(url_to_use, headers=header)
        url_to_use = url
        tree = html.fromstring(page.text)
        temp_list = tree.xpath('//*[@id="wallpaper"]/div/div/div[@class="preview"]/div[2]/div/a/@href')
        list_of_urls = list_of_urls + temp_list

    return list_of_urls


def download_images(list_of_urls, path="imgs/"):
    """
	This takes the list as a parameter and downloads them onto the harddisk into a imgs folder
	"""

    for url in list_of_urls:
        print("Downloading file " + url)
        absolute_url = 'http://interfacelift.com' + url
        # this line checks if imgs directory doesn't exist, it creates one
        if not os.path.exists(path):
            os.makedirs(path)
        filename = path + absolute_url.split("/")[-1]
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        img = opener.open(absolute_url)
        localFile = open(filename, 'wb')
        localFile.write(img.read())
        localFile.close()

    print("Done downloading.....")


if __name__ == 'main':
    url = str(sys.argv[1])
    if len(url) > 0:
        list_of_urls = get_list_of_image_urls(url)
        download_images(list_of_urls)
    else:
        raise ValueError("Input URL required!")