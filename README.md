<h2>Bittorrent Peer Crawler</h2>
This script is used to collect the list of peers in a bittorrent swarm.<br/>
This data can be used to construct swarm graph, discover peer geolocation, etc...<br/>
The details about the PEX application layer messagens can be found in http://www.ufjf.br/pgcc/files/2014/06/ThiagoGuarnieri.pdf

<h2>Dependencies</h2>
sudo apt-get install python-libtorrent<br/>
sudo apt-get install python-pip<br/>
pip install geoip2<br/>

Free geolite databases at https://dev.maxmind.com/geoip/geoip2/geolite2/

<h2>Calling</h2>
python crawler.py

<h2>Folder structure</h2>
crawler.py<br/>
|--- database (geolite files)<br/>
|--- downloaded (downloaded torrent chunks)<br/>
|--- logs (data from the swarm)<br/>
|--- torrent (torrent files)<br/>

