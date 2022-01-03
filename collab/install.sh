#!/bin/bash
pip3 install selenium
apt-get update # to update ubuntu to correctly run apt install
apt install chromium-chromedriver
mv /usr/lib/chromium-browser/chromedriver /usr/bin

git clone https://github.com/MatticateeSurgoen/water-data-web-scrapping-part2

cd water-data-web-scrapping-part2
pip3 install -r requirements.txt

if [ "$#" -eq 0 ]; then
  python3 scraper2.py --headless
elif [ "$#" -eq 2 ]; then
  python3 scraper2.py $1 $2 --headless
fi
#mv output.csv ..
#cd ..
#rm -rf water-data-web-scrapping-part2
#rm install.sh
