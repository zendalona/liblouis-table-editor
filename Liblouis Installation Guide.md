Liblouis Installation Steps

For Linux (Ubuntu/Debian/Kali):
1. Install liblouis and its dependencies:
   sudo apt-get update
   sudo apt-get install liblouis-bin liblouis-data python3-louis

2. Verify installation:
   which lou_translate
   ls /usr/share/liblouis/tables

For Windows:
1. Download the latest liblouis release from: https://github.com/liblouis/liblouis/releases
2. Extract the downloaded zip file
3. Copy the extracted folder to "C:\Program Files\liblouis" (Remove     extra word from name only extracted as 'liblouis')
4. Make sure the following structure exists:
   - C:\Program Files\liblouis\bin\lou_translate.exe
   - C:\Program Files\liblouis\share\liblouis	ables

5. Add liblouis to Windows PATH:
   a. Press Windows + R, type 'sysdm.cpl' and press Enter
   b. Go to 'Advanced' tab
   c. Click 'Environment Variables'
   d. Under 'User variables', find and select 'Path'
   e. Click 'Edit'
   f. Click 'New'
   g. Add 'C:\Program Files\liblouis\bin'
   h. Click 'OK' on all windows
   i. Restart your terminal/command prompt

Troubleshooting:
- If tables directory is not found, check these locations:
  - Linux: /usr/share/liblouis/tables
  - Linux: /usr/local/share/liblouis/tables
  - Windows: C:\Program Files\liblouis\share\liblouis	ables

- If lou_translate is not found:
  - Linux: Run 'sudo apt-get install liblouis-bin'
  - Windows: Make sure the bin directory is in your system PATH