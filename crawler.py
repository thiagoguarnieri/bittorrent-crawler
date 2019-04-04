import os
import sys
import time
import libtorrent as lt
import re
import pygeoip
import geoip2.database

#------------------------------------------------------------------------------#
# store peer information that are not yet stored on the peer array
def insertPeer(peer_array,peer_info):
    exists = False
    #getting IP
    ip_info = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(peer_info.ip))
    #compare if user is already on the list
    if ip_info is not None:
        for p in peer_array:
            #captando Ips da lista
            ip_curr = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(p.ip))
            #comparando 
            if ip_curr.group(0) == ip_info.group(0):
                exists = True
                #break
        if exists == False:
			try:
				rs = gi4.city(ip_info.group(0))
				sa = as4.asn(ip_info.group(0))
				peer_info.country_name = rs.country.name
				peer_info.country_code = rs.country.iso_code
				peer_info.city = rs.city.name
				peer_info.region_name = rs.subdivisions.most_specific.iso_code
				peer_info.aut_system = sa.autonomous_system_number
			except:
				peer_info.country_name = "empty"
				peer_info.country_code = "empty"
				peer_info.city = "empty"
				peer_info.region_name = "empty"
				peer_info.aut_system = "empty"
			finally:
				#insercao de peer
				peer_array.append(peer_info)
     
#------------------------------------------------------------------------------#
#save the log data when the current swarm collection is finished
def store_peers(torrent_info,torrent_peers,file_name, total_peers, total_seeds):
    
    f = open(file_name, 'w')
    metadata = "#META\n"
    metadata += torrent_info.name()+"\n" #nome
    metadata += str(torrent_info.info_hash())+"\n" #hash
    metadata += str(torrent_info.num_files())+"\n" #num arquivos
    metadata += str(torrent_info.total_size())+"\n" # tam total
    metadata += torrent_info.creator()+"\n" #criador
    metadata += str(torrent_info.priv())+"\n" #privado
    metadata += "\n#TRACKERS\n"
    for j in torrent_info.trackers():
        metadata += j.url+"\n"
        metadata +=  str(j.source)+"\n"
    metadata += "\n#FILES\n"
    for t in torrent_info.files():
        metadata += t.path+"\n"
        #---------#
        ext = re.search(r'\.\w+$', t.path)
        if ext == None:
            metadata += "no_ext\n"
        else:
            metadata += ext.group()+"\n"
            
        metadata +=str(t.size)+"\n" 
        if hasattr(t, 'executable_attribute'):
            metadata += str(t.executable_attribute)+"\n" 
        else:
            metadata += "false\n"  
        #---------#
    metadata += "\n#SUMMARY\n"
    metadata += "col: " + str(len(torrent_peers)) + " kno: " + str(total_peers) +  " sed: " + str(total_seeds) + "\n"
    
    metadata += "\n#PEERS\n"
    f.write(metadata)
    for p in torrent_peers:
        ipa = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', str(p.ip))
        port = re.findall(r'\d+', str(p.ip))
        peer_info = ipa.group(0) + "," + port[4] + "," + str(p.source) + "," + str(p.country_name) + \
            "," + str(p.country_code) + "," + str(p.city) + "," + str(p.region_name) + "," + str(p.aut_system) +   "\n"
        f.write(peer_info.encode())
    f.close()
    
#------------------------------------------------------------------------------#
#request new peers to the trackers
def make_collect(counter):
    
    s = hs[counter].status()
    print "\n" + infos[counter].name()

    #get new peer list
    arr = hs[counter].get_peer_info()

    print "available peers ", str(len(globpeers[counter])), " known peers ", str(s.list_peers), " seeds ", str(s.list_seeds) 

    #insert new peers in the list
    for p in arr:
        insertPeer(globpeers[counter], p)
    
    #increment counter timer
    cnt[counter] = cnt[counter] + 1
    
    #searching for new peers
    hs[counter].force_dht_announce()
    if cnt[counter]/40 == 0:
        hs[counter].force_reannounce()

    #if no new peers in 40s then save and stop
    if cnt[counter] > 40:
        avail_peers[counter] = len(globpeers[counter])
        known_peers[counter] = s.list_peers
        if old_avail_peers[counter] == avail_peers[counter] and old_known_peers[counter] == known_peers[counter]:
			print("peers indexed")
			finishd[counter] = 1;
			file_name = "logs/"+ str(hs[counter].info_hash()) + ".txt"
			st = hs[counter].status()
			store_peers(infos[counter],globpeers[counter],file_name,st.list_peers,st.list_seeds) 
        #reset counter
        cnt[counter] = 0
        old_avail_peers[counter] = avail_peers[counter]
        old_known_peers[counter] = known_peers[counter]
#------------------------------------------------------------------------------#
#MAIN EXECUTION
#------------------------------------------------------------------------------#
base_torrent = 1; #first torrent
total_torrent = 3; #number of torrents
ses = lt.session()
ses.listen_on(6881, 6891)

#finished
finishd = list()

#setting sessions variables
settings = ses.settings()
settings.num_want = 300
settings.max_peerlist_size = 0 #no limit
settings.announce_to_all_tiers = 1
settings.download_rate_limit = 60000;
settings.upload_rate_limit = 300000;
ses.set_settings(settings)
ses.start_dht()

#------------------------------------------#
#geolocation
gi4 = geoip2.database.Reader('database/GeoLite2-City.mmdb')
as4 = geoip2.database.Reader('database/GeoLite2-ASN.mmdb')
#------------------------------------------#
#adding torrents
 #array de headers
hs = list();
#array de infos
infos = list();

print("reading torrents")

#LOADING TORRENTS
for i in range(0,total_torrent):
    loaded = False
    while loaded == False:
        try:
			#directory to place torrents
            e = lt.bdecode(open("torrents/"+str(i+base_torrent)+".torrent", 'rb').read())
            info = lt.torrent_info(e)
            loaded = True
        except:
            base_torrent = base_torrent + 1
            loaded = False
            print("error reading torrents")
    #------------------------#
    infos.append(info)
    #directory to put temp downloaded data
    h = ses.add_torrent(info, "downloaded/")
    hs.append(h)

#setting priorities to zero to not save chunks
for i in range(0,total_torrent):
    pieces = hs[i].piece_priorities()
    for x in range(0,len(pieces)-1):
        pieces[x] = 0
    hs[i].prioritize_pieces(pieces)

#global peer list
globpeers = list()
for i in range(0,total_torrent):
    globpeers.append(list())

#control peer variables
known_peers = list()
avail_peers = list()
old_avail_peers = list()
old_known_peers = list()
for i in range(0,total_torrent):
    known_peers.append(1)
    avail_peers.append(0)
    old_avail_peers.append(0)
    old_known_peers.append(1)

#counter
cnt = list()
for i in range(0,total_torrent):
    cnt.append(0)
    finishd.append(0)

#main loop
while (True):
	completed = 1
	print "Count: ", cnt[0]
	for i in range(0,total_torrent):
		#updating peers
		if finishd[i] == 0:
			make_collect(i)
			completed = 0
	time.sleep(2)
    
	if completed == 1:
		sys.exit()
    
	os.system('clear')
#-----------------------------------------------------------------------------#
