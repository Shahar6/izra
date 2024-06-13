These are the scripts I wrote to beat the online game https://izra.co.il/home
There's code that automates certain parts of the game, and has a minimal reaction time to do specific actions
In practice I ended up winning the 65th season of the game (first place), even tho I didn't spend too much time time playing, as a result of this practical code.

The python libraries I utilized the most are requests, threading, BeautifulSoup and re(regular expression)

As there's lots of I/O when communicating with a web server, I used multi-threads to efficiently send as many requests as possible, and I had synchronized them correctly
this can be seen best in bs2.py and collectors.py.
There's heavy usage of regular expressions in the code as well, for actions like sending workers to fields in manage_characters.py (need to get the exact amount of workers).

You can see that I'm using a specific user-agent, this is because at some point the game's moderator decided to block the user-agent used by python requests by default.
A few weeks later he had implemented rate-limiting on the game, allowing only 120 requests per IP per minute, what I did to go around this was use proxies, in collectors.py:
we can see the list ips, and the method switch_proxy, whenever I'd reach the 120 requests limit on a certain thread I'd get a specific timeout message from the server,
and if I got that message I'd call switch_proxy to randomly select a different proxy. 
This solution of random selection is much more simple and also proves to be more efficient than managing a list of used proxies shared by all the threads and resetting the list after each 60 seconds,
if a thread had selected a proxy that was already used up, it'd immediately select a new proxy and test it.

Another obstacle with this game was that some of the requests wouldn't be processed by the server, maybe due to it's own concurrency issues.
What I did to go around this is the methods getP and postP, those would run an infinite loop of sending the same request (get or post appropriately) with 1 second timeout, so if there's no response
it's going back to the start of the loop and sent again, and it breaks and returns the response when the correct status code is recieved. 

the next file to go over is clan_tax_hourly.py, in this game you can create a clan and have other users join you, and you can gather taxes once per day from the members.
I had found that if the clan head passes the leadership to someone else and then gets it back, he can gather taxes again, this is exactly what I do in clan_tax_hourly.py
I have all the users I manage gather gold for an hour and then transfer all of it to one clan leader, the alternative method of transferring resources would require the leader to attack
the members which costs attacking turns which are expensive to use in the game.

The last files I would like to explain are scout.py, read_xl.py and resource_data.xlsx.
scout.py would scan the entire game and write the users who have either lots of workers or lots of resources inside resource_data.xlsx, using the library xlsxwriter.
I also used the proxies here to speed it up as there are hundreds of thousands of requests required to scan the entire game and if I went at 120 / minute it would take too long.
read_xl.py is later used with openpyxl to read all the users from resource_data.xlsx (thousands) and quickly update their information inside resource_data.xlsx, instead of going over all the players in the game. 
(tens of thousands)

