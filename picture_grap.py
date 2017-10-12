from bs4 import BeautifulSoup
import urllib

def fb_grap_picture(u):
    u=u.replace("www","mobile");
    result=[]
    urlData = urllib.urlopen(u);
    data = str(urlData.readlines())
    bs = BeautifulSoup(data, 'lxml');
    imgUrl = bs.find_all('img');
    for x in imgUrl:
        if "scontent" in x.get('src'):
            result.append(x.get('src'));
            #
    return result;

print fb_grap_picture('https://www.facebook.com/photo.php?fbid=10210823931253743&set=gm.1214864741946970&type=3');