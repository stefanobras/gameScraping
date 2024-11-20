# gameScraping
*A Python script that uses web scraping to fetch all games from a specific console and year range, ranking them by a weighted score.*  

Have you ever wanted to explore games from a specific console but didn’t know where to start? Or maybe you’re looking for a list of the best games for each system? Here’s your solution:  

Run this script by entering the following command in the integrated terminal of the project folder:  
```bash
python games.py console:CONSOLE-ID year:DESIRED-YEAR-RANGE
```

Console IDs:  
-**Atari 2600:** 2600  
-**Nintendo Entertainment System:** nes  
-**Sega Master System:** sms  
-**Super Nintendo Entertainment System:** snes  
-**Sega Genesis:** gen  
-**Game Boy:** gb  
-**PlayStation:** ps  
-**Nintendo 64:** n64  
-**Sega Saturn:** saturn  
-**Game Boy Color:** gbc  
-**PlayStation 2:** ps2  
-**Nintendo GameCube:** gcn  
-**Xbox:** xbox  
-**Dreamcast:** dc  
-**Game Boy Advance:** gba  
-**Nintendo Wii:** wii  
-**PlayStation 3:** ps3  
-**Xbox 360:** xbox-360  
-**Nintendo DS:** nds  
-**PlayStation Portable:** psp  
-**PlayStation 4:** ps4  
-**Xbox One:** xbox-one  
-**Nintendo Wii U:** wii-u  
-**Nintendo 3DS:** 3ds  
-**Nintendo Switch:** nintendo-switch  
-**PlayStation 5:** ps5  
-**Xbox Series X/S:** xbox-4  
-**PC:** pc  

Example Usage:  
```bash
python games.py console:n64 year:1996-2001
```

Running the above command will open IGN’s website on Chrome (requiring ChromeDriver). The script will automatically navigate through the games, clicking on each one to compile their information.

⚠ Note: This process might take some time, depending on the number of games being scraped. Additionally, the script may occasionally crash unexpectedly. To avoid losing progress, it is recommended to scrape games in smaller batches.

Once completed, the script will generate a JSON file containing all the games ranked by a weighted score, factoring in the number of reviews for each title.

The script can be interrupted by entering 'q' in the console. This will save and rank the games scraped up to that point.  
To help with managing multiple files, an additional script, combine_json.py, is included. It allows you to merge two files while preserving the ranking of the games.
