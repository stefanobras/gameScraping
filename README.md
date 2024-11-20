# gameScraping
*A python script that uses web scraping to fetch all games from a certain console and year range and ranks them.*

So, If you ever wanted to play games from a certain console but you didn't know which ones, or maybe you just wanted a list of the best games for each system here's your solution:

Basically you can run this script by typing this into the integrated terminal of this project's folder:
python games.py console:CONSOLE-ID year:DESIRED YEAR RANGE

Use this Console IDs:
Atari 2600: 2600
Nintendo Entertainment System: nes
Sega Master System: sms
Super Nintendo Entertainment System: snes
Sega Genesis: gen
Game Boy: gb
PlayStation: ps
Nintendo 64: n64
Sega Saturn: saturn
Game Boy Color: gbc
PlayStation 2: ps2
Nintendo GameCube: gcn
Xbox: xbox
Dreamcast: dc
Game Boy Advance: gba
Nintendo Wii: wii
PlayStation 3: ps3
Xbox 360: xbox-360
Nintendo DS: nds
PlayStation Portable: psp
PlayStation 4: ps4
Xbox One: xbox-one
Nintendo Wii U: wii-u
Nintendo 3DS: 3ds
Nintendo Switch: nintendo-switch
PlayStation 5: ps5
Xbox Series X/S: xbox-4
PC: pc

Example usage:
python games.py console:n64 year:1996-2001

Doing this will open IGN's website on Chrome (this is why ChromeDrive is needed) and the script will automatically click on each one of the games and compile their info. This of course, may take a long time depending on the amount of games. Afterwards, the script will create a JSON file with all games ranked by a weighted score taking into consideration the amount of reviews.
