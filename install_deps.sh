sudo -E apt update

sudo -E apt -y install python python-pip libwebp5 libwebp-dev
[[ $? > 0 ]] && { echo "[$(date +"%T")] [ERROR] APT installation failed."; exit 1; }

LC_ALL=C sudo -E pip install -r requirements.txt
[[ $? > 0 ]] && { echo "[$(date +"%T")] [ERROR] Python packages installation failed."; exit 1; }

echo "[$(date +"%T")] [INFO] Done!"
