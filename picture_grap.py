from bs4 import BeautifulSoup
import urllib

urlData = urllib.urlopen("https://mobile.facebook.com/photo.php?fbid=1327262447383250&set=gm.1213564898743621&type=3");
data = str(urlData.readlines())
print data
bs = BeautifulSoup(data,'lxml');
imgUrl = bs.find_all('img');
for x in imgUrl:
    if "scontent" in x.get('src'):
        urllib.urlretrieve(x.get('src'), "plane.jpg")
#