import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
import os
from bs4 import BeautifulSoup
import urllib

########################### Read Me First ###############################

def fb_grap_picture(u):
    u=u.replace("www","mobile");
    result=[]
    urlData = urllib.urlopen(u);
    data = str(urlData.readlines())
    bs = BeautifulSoup(data, 'lxml');
    imgUrl = bs.find_all('img');
    for x in imgUrl:
        if "scontent" in x.get('src'):
            return x.get('src');
            #
    return result;


class Custom_WP_XMLRPC:
    def post_article(self, wpUrl, wpUserName, wpPassword, articleTitle, articleCategories, articleContent, articleTags,
                     PhotoUrl):
        self.path = os.getcwd() + "\\00000001.jpg"
        self.articlePhotoUrl = PhotoUrl
        self.wpUrl = wpUrl
        self.wpUserName = wpUserName
        self.wpPassword = wpPassword
        # Download File
        f = open(self.path, 'wb')
        print self.path,self.articlePhotoUrl
        f.write(urllib.urlopen(self.articlePhotoUrl).read())
        f.close()
        # Upload to WordPress
        client = Client(self.wpUrl, self.wpUserName, self.wpPassword)
        filename = self.path
        # prepare metadata
        data = {'name': 'picture.jpg', 'type': 'image/jpg', }
        # read the binary file and let the XMLRPC library encode it into base64
        with open(filename, 'rb') as img:
            data['bits'] = xmlrpc_client.Binary(img.read())
        response = client.call(media.UploadFile(data))
        attachment_id = response['id'];
        print attachment_id;
        # Post
        post = WordPressPost()
        post.title = articleTitle
        post.content = articleContent
        post.terms_names = {'post_tag': articleTags, 'category': articleCategories}
        post.post_status = 'publish'
        post.thumbnail = attachment_id
        post.id = client.call(posts.NewPost(post))
        print 'Post Successfully posted. Its Id is: ', post.id


#########################################
# POST & Wp Credentials Detail #
#########################################

