venv_name=venv

#virtualenv --always-copy -p python3 $venv_name
python3 -m venv $venv_name
source $venv_name/bin/activate
pip install -r requirements.txt
