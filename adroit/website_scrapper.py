import urllib2
from BeautifulSoup import BeautifulSoup

page = urllib2.urlopen("http://www.trackload.com/cgi-bin/rapidtrk.cgi?MAWB=205-39923332")
soup = BeautifulSoup(page)
print soup.prettify()