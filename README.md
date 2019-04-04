# bittorrent_crawler
This script is used to collect the list of peers in a bittorrent swarm.
The details about the PEX application layer messagens can be found in http://www.ufjf.br/pgcc/files/2014/06/ThiagoGuarnieri.pdf

Dependencies
sudo apt-get install python-libtorrent
sudo apt-get install python-pip
pip install geoip2

Free geolite databases at https://dev.maxmind.com/geoip/geoip2/geolite2/

Calling
python crawler.py

Folder structure
crawler.py
|--- database (geolite files)

|--- downloaded (downloaded torrent chunks)

|--- logs (data from the swarm)

|--- torrent (torrent files)

