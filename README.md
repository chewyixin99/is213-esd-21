# Project Directory
----------------------
ESD_PROJECT_22
	| complex
	| database	
	| hawker
	| kong
	| microservices
	| docker-compose.yml

----------------------
## Instructions for loading up the database:
1. Import the file esd_sql.sql from the folder esd_project_22/database in localhost/phpmyadmin.

----------------------
## Setting up Kong
1. In the command line, ensure that we are in the main directory (esd_project_22)
2. Run the command 
	cd kong 
3. You should now be in the directory esd_project_22/kong
4. Run the following command 
	docker-compose up

----------------------
## Setting up Konga
1. Once Kong is up, log into your Konga account. Konga can be accessed via http://localhost:1337
2. On the sidebar, go to SNAPSHOTS
3. Click Import From File, and navigate to the folder esd_project_22
4. Click on the json file esd_snapshot.json, and click Open
5. Go back to Konga, you should see the snapshot you just created
6. Click on the Details and click Restore
7. Tick all the checkboxes, and click Import Objects
8. You should see an overview of the snapshot you just restored.
	services	imported: 10	failed: 0
	routes		imported: 16	failed: 0
	consumers	imported: 1	failed:0
	…
	The rest should be 0

9. If the expected result at 8 is not observed, repeat step 7.
10. You are now ready to test the API services at http://localhost:8000/<route>

----------------------
## Setting up microservices
1. Within the main directory esd_project_22 on a separate terminal, run the following command
	docker-compose up 

----------------------
## Running the Vue App
1. In the command line, ensure that we are in the main directory (esd_project_22)
2. Run the command
	npm install
followed by the command
	npm run serve
4. The app is now accessible via http://localhost:8080
