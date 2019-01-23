# inventory
An Inventory App Web App Which monitors from goods storage to sales and shipment and Many More Developed With Django

To Get Started 
On your local server on an Ubuntu Machine 

Create a virtual environment. 
sudo pip install virtualenv to install virtual environment
sudo pip install virtualenvwrapper to install virtual environment wrapper
mkvirtualenv (your virtual environment name) 
it sets up necessary python packages to start your development then you see the name in rounded brackets before your machine's username. 
If you get "command error" on creating the virtual environment.
sudo gedit .bashrc and add this at the bottom of the script 
#Virtualenvwrapper settings 
export WORKON_HOME = $HOME/.virtualenvs
export PROJECT_HOME = $HOME/Projects
source /usr/local/bin/virtualenvwrapper.sh

then save and run source ~/.bashrc to effect changes
then run mkvirtualenv again. 
sudo pip install -r requirements.txt to install all necessary dependencies and apps. 

python manage.py makemigrations and migrate 

python manage.py createsuperuser to create an admin account which can be accessed via localhost:port/admin 

If you encounter a "no auth_profile table" error, then do the makemigrations and migrate one after the other for each individual 3rd party app in the settings.py file. and run the createsuperuser again. 

configure the mail settings to enable email sending on password reset. 

python manage.py runserver to start your server 
