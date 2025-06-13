# Инструкция по запуску кастомного Nginx в Docker

## Предварительно 
  
- Git (опционально, для клонирования репозитория)
``
 sudo apt update
 sudo apt install git
``   

- Установленный Docker (провереное решение)

``
 sudo apt-get install ca-certificates curl
 sudo install -m 0755 -d /etc/apt/keyrings
 sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
 sudo chmod a+r /etc/apt/keyrings/docker.asc
``

### Add the repository to Apt sources:

``
 echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
 sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
 sudo apt-get update   
 ``

##  Получение файлов проекта

``
 git clone https://github.com/(....)
 cd (....)
``

## Запуск Docker-билда

``
 docker-compose up -d --build
``
