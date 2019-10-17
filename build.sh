# exit on the first error found
set -o errexit

green=$'\e[1;32m'
end=$'\e[0m'

log () {
    printf "${green}[wikidata-gazetteer] ${1}${end}\n"
}

if ! type "sudo" > /dev/null; then
    log "installing sudo"
    apt-get install sudo
fi

log "Update Package Lists"
sudo apt-get update

log "Install System Dependencies"
sudo apt-get install -y pylint python3-venv zip

log "Clear out Previous Python Virtual Environment if it Exists"
rm -fr venv

log "Create and Enter Python Virtual Environment"
python3 -m venv venv
source ./venv/bin/activate

echo "Install Python Dependencies"
pip install -r requirements.txt

echo "Create Gazetteer"
python3 create_gazetteer_from_wikidata.py

echo "Create Set of Place Titles"
python3 create_place_titles.py

echo "need to write tests later"

echo "Zip Pickled Python Set"
zip -r /tmp/place_titles.pickle.zip /tmp/place_titles.pickle

echo "Zip Gazetteer"
zip -r /tmp/wikidata-gazetteer.tsv.zip /tmp/wikidata-gazetteer.tsv
