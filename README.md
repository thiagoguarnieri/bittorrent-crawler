# bittorrent_crawler
This script is used to collect the list of peers in a bittorrent swarm.<br/>
The details about the PEX application layer messagens can be found in http://www.ufjf.br/pgcc/files/2014/06/ThiagoGuarnieri.pdf

Dependencies<br/>
sudo apt-get install python-libtorrent<br/>
sudo apt-get install python-pip<br/>
pip install geoip2<br/>

Free geolite databases at https://dev.maxmind.com/geoip/geoip2/geolite2/

Calling<br/>
python crawler.py

Folder structure<br/>
crawler.py<br/>
|--- database (geolite files)<br/>
|--- downloaded (downloaded torrent chunks)<br/>
|--- logs (data from the swarm)<br/>
|--- torrent (torrent files)<br/>

