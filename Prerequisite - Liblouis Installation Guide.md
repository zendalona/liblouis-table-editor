## Liblouis Installation Steps:

### For Linux (Ubuntu/Debian/Kali):
1. Install liblouis and its dependencies:

````bash
sudo apt-get update
````
````bash 
sudo apt-get install liblouis-bin liblouis-data python3-louis
````

2. Verify installation:
````bash 
which lou_translate
ls /usr/share/liblouis/tables
````
 

### For Windows:
1. Download the latest liblouis release from: https://github.com/liblouis/liblouis/releases
2. Extract the downloaded zip file
3. Copy the extracted folder to "C:\Program Files\liblouis" (remove extra word from name only extracted as 'liblouis')
4. Make sure the following structure exists:
   - C:\Program Files\liblouis\bin\lou_translate.exe
   - C:\Program Files\liblouis\share\liblouis	ables

5. Add liblouis to Windows PATH:
   a. Press Windows + R, type 'sysdm.cpl' and press Enter \n
   b. Go to 'Advanced' tab
   c. Click 'Environment Variables'
   d. Under 'User variables', find and select 'Path'
   e. Click 'Edit'
   f. Click 'New'
   g. Add 'C:\Program Files\liblouis\bin'
   h. Click 'OK' on all windows
   i. Restart your terminal/command prompt

