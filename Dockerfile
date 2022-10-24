FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/app

RUN apt-get update
RUN apt-get update --fix-missing
# RUN apt-get install -y libzbar0
RUN apt-get install ffmpeg libsm6 libxext6  -y
# SELENIUM/CHROME
RUN apt install -y unzip xvfb libxi6 libgconf-2-4

RUN apt -y install default-jdk
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add 
RUN bash -c "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' >> /etc/apt/sources.list.d/google-chrome.list"
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN apt -y update
RUN apt -y install google-chrome-stable
RUN wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver 
RUN chown root:root /usr/bin/chromedriver 
RUN chmod +x /usr/bin/chromedriver
RUN wget https://selenium-release.storage.googleapis.com/3.141/selenium-server-standalone-3.141.59.jar 
RUN mv selenium-server-standalone-3.141.59.jar selenium-server-standalone.jar 
RUN wget http://www.java2s.com/Code/JarDownload/testng/testng-6.8.7.jar.zip 
RUN unzip testng-6.8.7.jar.zip 
# RUN xvfb-run java -Dwebdriver.chrome.driver=/usr/bin/chromedriver -jar selenium-server-standalone.jar 
# RUN chromedriver --url-base=/wd/hub 



RUN pip install -r requirements.txt

COPY ./entrypoint.sh .
COPY . .
