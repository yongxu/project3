Final Project - CSCI4511W
==================


Repository for Happy - Poison game

For this final project we have extended the functionality of the Happy Poison game first introduced during the study of __*Chapter 5 - Adversarial Search*__ [Artificial Intelligence a Modern Approach](http://www.amazon.com/Artificial-Intelligence-Modern-Approach-Edition/dp/0136042597).  This expansion allows for a user-playable "Happy" sprit (depecited as a blue wizard) or an AI controlled "Happy" which will run autonomously against *n* amount of *Poison*

## Dependencies
#####NPM - Backend Package Manger

    $ npm install

####Bower - Web package manager
    $ bower install
####Gulp - Realtime Testing

    $ npm install gulp

many of these things may require *sudo*

####Usage
###### Local Server
+ Using gulp open a port to be run in the browser

        $ gulp
+ By default is [http://localhost:3000/](http://localhost:3000/)
######Game View
<img src="http://i.imgbox.com/yrTSsv09.png" width="500px" height="300px" />
######Code View
+ Python code in here is executed
+ Is initially stored in <code>project3/app/code/code.py</code>
<img src="http://i.imgbox.com/xWNYtzTC.png" width="500px" height="300px" />
### Live Demo 
+ Can be viewed at [yongxuren.com](yongxuren.com)



#### Implementation
+ Using a BREDTH FIRST SEARCH (BFS) the dragon sprites will atttempt to catch the blue wizard
+ Using a ALPHA-BETA-SEARCH the dragon sprites will attempt to catch the blue wizard
