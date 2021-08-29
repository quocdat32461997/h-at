pip3 install -r requirements.txt
python3 -m spacy download en
git clone https://github.com/huggingface/neuralcoref.git
pip3 install -r neuralcoref/requirements.txt
pip3 install -e neuralcoref/.
