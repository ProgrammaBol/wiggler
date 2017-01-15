#!/bin/sh
echo  '#-------------------------------------------#'
echo  '# wiggler prerequisites installer for Linux #'
echo  '#-------------------------------------------#'
echo  '#   installing PyGame   #'
sudo apt-get install --assume-yes python-pygame
echo  '#  installing wxPython  #'
sudo apt-get install --assume-yes python-wxgtk3.0
echo  '#    installing pip     #'
sudo apt-get install --assume-yes python-pip
pip install --upgrade pip
echo  '#   installing jinja2   #'
pip install jinja2
