#!/bin/bash
# 风之翼灵
# www.fungj.com
# 一键安装docker到Debian12的脚本
# 国内用户注意docker源，该脚本基于官方安装脚本修改

echo "Add Docker's official GPG key:"
apt-get update -y
apt-get install ca-certificates curl gnupg -y
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

echo "Add the repository to Apt sources:"
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
apt-get update -y

apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "Enable Docker at startup"
systemctl enable docker

echo "Verify the Docker installation by running the hello-world image "
docker run hello-world