#!/bin/bash
pip install selenium
apt-get update # to update ubuntu to correctly run apt install
apt install chromium-chromedriver
mv /usr/lib/chromium-browser/chromedriver /usr/bin

git clone https://github.com/MatticateeSurgoen/water-data-web-scrapping-part2

cd water-data-web-scrapping-part2
pip3 install -r requirements.txt

if [ "$#" -eq 0 ]; then
  python3 scraper2.py 
elif [ "$#" -eq 1 ]; then
  python3 scraper2.py $1 
elif [ "$#" -eq 2 ]; then
  python3 scraper2.py $1 $2
fi
mv output.csv ..
cd ..
rm -rf water-data-web-scrapping-part2
rm install.sh
