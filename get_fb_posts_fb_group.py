import json
import datetime
import csv
import time
import re
from post import Custom_WP_XMLRPC
from post import fb_grap_picture
import urllib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
import xmlrpclib
from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods import media, posts
from difflib import SequenceMatcher
import difflib
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

app_id = "2150528968507557"
app_secret = "536ac272e65a4a5cb8b2966250e3c12c"  # DO NOT SHARE WITH ANYONE!
group_id = "543189115781206"

# input date formatted as YYYY-MM-DD
since_date = "2017-09-03"
until_date = "2017-09-15"

access_token = app_id + "|" + app_secret


def request_until_succeed(url):
    req = Request(url)
    success = False
    while success is False:
        try:
            response = urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL {}: {}".format(url, datetime.datetime.now()))
            print("Retrying.")

    return response.read()

# Needed to write tricky unicode correctly to csv


def unicode_decode(text):
    try:
        return text.encode('utf-8').decode()
    except UnicodeDecodeError:
        return text.encode('utf-8')


def getFacebookPageFeedUrl(base_url):

    # Construct the URL string; see http://stackoverflow.com/a/37239851 for
    # Reactions parameters
    fields = "&fields=message,link,created_time,type,name,id," + \
        "comments.limit(0).summary(true),shares,reactions" + \
        ".limit(0).summary(true),from"
    url = base_url + fields

    return url


def getReactionsForStatuses(base_url):

    reaction_types = ['like', 'love', 'wow', 'haha', 'sad', 'angry']
    reactions_dict = {}   # dict of {status_id: tuple<6>}

    for reaction_type in reaction_types:
        fields = "&fields=reactions.type({}).limit(0).summary(total_count)".format(
            reaction_type.upper())

        url = base_url + fields

        data = json.loads(request_until_succeed(url))['data']

        data_processed = set()  # set() removes rare duplicates in statuses
        for status in data:
            id = status['id']
            count = status['reactions']['summary']['total_count']
            data_processed.add((id, count))

        for id, count in data_processed:
            if id in reactions_dict:
                reactions_dict[id] = reactions_dict[id] + (count,)
            else:
                reactions_dict[id] = (count,)

    return reactions_dict


def processFacebookPageFeedStatus(status):

    # The status is now a Python dictionary, so for top-level items,
    # we can simply call the key.

    # Additionally, some items may not always exist,
    # so must check for existence first
    status_id = status['id']
    status_type = status['type']

    status_message = '' if 'message' not in status else \
        unicode_decode(status['message'])
    link_name = '' if 'name' not in status else \
        unicode_decode(status['name'])
    status_link = '' if 'link' not in status else \
        unicode_decode(status['link'])

    # Time needs special care since a) it's in UTC and
    # b) it's not easy to use in statistical programs.

    status_published = datetime.datetime.strptime(
        status['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + \
        datetime.timedelta(hours=-5)  # EST
    status_published = status_published.strftime(
        '%Y-%m-%d %H:%M:%S')  # best time format for spreadsheet programs
    status_author = unicode_decode(status['from']['name'])
    status_author_id= unicode_decode(status['from']['id'])

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
        status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
        status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else status['shares']['count']

    return (status_id, status_message, status_author,status_author_id, link_name, status_type,
            status_link, status_published, num_reactions, num_comments, num_shares)


def scrapeFacebookPageFeedStatus(group_id, access_token, since_date, until_date):

    with open('{}_facebook_statuses.csv'.format(group_id), 'w') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "status_author", "link_name",
                    "status_type", "status_link", "status_published",
                    "num_reactions", "num_comments", "num_shares", "num_likes",
                    "num_loves", "num_wows", "num_hahas", "num_sads", "num_angrys",
                    "num_special"])

        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        # /feed endpoint pagenates througn an `until` and `paging` parameters
        until = ''
        paging = ''
        base = "https://graph.facebook.com/v2.9"
        node = "/{}/feed".format(group_id)
        parameters = "/?limit={}&access_token={}".format(100, access_token)
        since = "&since={}".format(since_date) if since_date \
            is not '' else ''
        until = "&until={}".format(until_date) if until_date \
            is not '' else ''

        print("Scraping {} Facebook Group: {}\n".format(
            group_id, scrape_starttime))

        while has_next_page:
            until = '' if until is '' else "&until={}".format(until)
            paging = '' if until is '' else "&__paging_token={}".format(paging)
            base_url = base + node + parameters + since + until + paging
            url = getFacebookPageFeedUrl(base_url)
            statuses = json.loads(request_until_succeed(url))
            reactions = getReactionsForStatuses(base_url)

            for status in statuses['data']:

                # Ensure it is a status with the expected metadata
                if 'reactions' in status:
                    status_data = processFacebookPageFeedStatus(status)
                    xmlrpc_object = Custom_WP_XMLRPC()
                    wpUrl = 'http://jualhewan123.com/xmlrpc.php'
                    articleTitle="";
                    # WordPress Username
                    wpUserName = 'admin'
                    # WordPress Password
                    wpPassword = 'mypassword'

                    # Post Title
                    articleTitle = "Jual"
                    # Post Body/Description
                    source =status_data[1];
                    source_msg="";
                    try:
                        source_msg = unicode(source, 'utf-8')
                    except TypeError:
                        source_msg =source

                    temp = source_msg.split(" ")[:4];
                    title="";
                    for i in range(0,len(temp)):
                        title = title + " " + temp[i]

                    articleTitle = title
                    articleContent = status_data[2] +" : "+source_msg +" \n" + "kontak <a href='https://facebook.com/"+status_data[3]+"'> "\
                                     + status_data[2] +"</a>";
                    # list of tags

                    text2 = "angsa anjing anoa antelop arwana ayam babi badak bajing bangau bebek bekantan bekicot belalang belatung belibis belut beo berang beruang beruk beruk betet betok biawak bintang biribiri bison blekok buaya bulu babi bunglon burung cacing camar capung cencorang cendrawasih cere cerek cheetah cicak codot cucakrawa cumicumi dara domba duyung elang entok gabus gagak gajah gapih garuda gelatik gorila gurame gurita hamster harimau hiena hiu iguana ikan itik jalak jangkrik jerapah kadal kakatua kaki seribu kalajengking kalkun kalong kambing kampret kangguru kapibara kasuari katak kebo kecebong kodok kecoa kecoak kelabang keledai kelelawar kelinci kenari keong kepiting kera kerang kerapu kerbau kijang koala kobra kodok koi koi komodo kucing kuda kudanil kudaponi kumbang kupu kupu kura kuskus kutu labalaba lalat lalatbuah laler landak landaklaut laron lebah lele lemur lintah lipan lipas lobster lumbalumba lutung lutung luwak macan macankumbang macantutul makarel maleo mambruk marmut maskoki merak merpati milkat monyet mujaer musang ngengat nila nyamuk onta orangutan oskar owa panda parkit patin paus pelatuk penyu perkutut pesut pinguin pipit piranha piton rajawali rayap rubah rusa salmon sanca sapi sapu sapu semut sepat serigala siamang singa siput soang sotong tangkasi tapir tarantula tarsius tawon tekukur tengiri teri teripang terwelu tikus tiram todak tomcat trenggiling tuna tupai uburubur udang ular ularderik ularsendok ulat undurundur unta walet wauwau wereng yuyu zebra";
                    articleTags = ['jual hewan']
                    articleCategories = ["umum"]
                    data_hewan = text2.split(" ");
                    for hewan in data_hewan:
                        if (hewan in source_msg):
                            tag ="jual "+hewan
                            articleTags.append(tag);
                            articleCategories.append(hewan);

                    # list of Categories
                    try:

                        urlPoto =fb_grap_picture(status_data[6]);
                        if (len(articleTitle) >= 2 and len(urlPoto)):
                            xmlrpc_object.post_article(wpUrl, wpUserName, wpPassword, articleTitle, articleCategories,
                                                       articleContent, articleTags,
                                                       urlPoto)
                        else:
                            print "invalid_kontent";
                            print source_msg;
                            print status_data[6];
                    except IndexError:
                        pass



                    # calculate thankful/pride through algebra
                    #num_special = status_data[7] - sum(reactions_data)
                    #w.writerow(status_data + reactions_data + (num_special,))

                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print("{} Statuses Processed: {}".format
                          (num_processed, datetime.datetime.now()))

            # if there is no next page, we're done.
            if 'paging' in statuses:
                next_url = statuses['paging']['next']
                until = re.search('until=([0-9]*?)(&|$)', next_url).group(1)
                paging = re.search(
                    '__paging_token=(.*?)(&|$)', next_url).group(1)

            else:
                has_next_page = False

        print("\nDone!\n{} Statuses Processed in {}".format(
              num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(group_id, access_token, since_date, until_date)


# The CSV can be opened in all major statistical programs. Have fun! :)
