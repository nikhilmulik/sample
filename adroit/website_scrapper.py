import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("")
soup = BeautifulSoup(page)
print soup.prettify()