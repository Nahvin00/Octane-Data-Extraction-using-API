# Octane Data Extraction using API

## Problem statement
ALM Octane is a web-based application lifecycle management platform that enables teams to collaborate easily, manage the product delivery pipeline, and visualize the impact of changes. Octane was used to manage all of the service products related to MFW. Octane also provides an API to retrieve and process data. Unfortunately, the MFW team lacked technical skills required to develop a program that utilizes API to export and process these data.

## Task specification
A solution for Octane data extraction using API was assigned to develop that:
* Authenticate API connection using client ID and password
* Retrieve data based on last modified datetime from API using cookie
* Process and export the data to oracle database, and
* Loop the extraction process for all API connections in oracle database

## Implementation and solution method
The implantation of the solution first began with a few brainstorming and discussion session with Mr. Tat Sern, who is one of the key people that is involved in service product management. After several meetings, the solution for Octane data extraction using API was developed using the python programming language and PyCharm as the IDE. This solution was continuously developed for a period of three (3) months which went on until 11 versions. Table below shows the description for each version.

<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/55419300/230069182-b56e5241-06da-4174-b0ae-07ecf6520364.png">
</p>

Version 1 to 3 of the program functions as a POC which authenticates the API connection, retrieves and exports data to the oracle database. Version 4 of the program which included data processing was used to develop a template which was circulated to other colleagues to test out the program. Upon completion of V4, the python code developed to retrieve data from Octane API was presented and explained to nine (9) other colleagues representing different teams in IT FSC MFW. The program was developed further until beta versions (V7 & V8). As the first solution for Octane data extraction using API was developed, an invitation was extended to present the program to one of the senior system architects of Infineon Technologies. He gave some suggestions for the significant improvement of the program such as to encrypt database connections to make it more secure and limit attempts of API callback to reduce stress on Octane platform. Along with V9, a separate program called ‘octane_database_encryption.py’ was created to encrypt and decrypt database connections. Architecture of the V9 is as illustrated in the figure below.

<p align="center" width="100%">
    <img width="50%" src="https://user-images.githubusercontent.com/55419300/230066908-ff0504b5-7f68-48b0-a670-88cfde49fc43.png">
</p>

Stable version of the program was released as V9, V10 and V11 with minor bug fixes. There was a total of two (2) database tables that were involved in this project which are ‘AA_OCTANE_DB’ and ‘AA_OCTANE_HIST’. ‘AA_OCTANE_DB’ table is responsible for storing API connections whereas the ‘AA_OCTANE_HIST’ table is used to store feature data. Figure below shows the ERD of both tables respectively.

<p align="center" width="100%">
    ERD of ‘AA_OCTANE_DB’ table
</p>
<p align="center" width="100%">
    <img width="30%" src="https://user-images.githubusercontent.com/55419300/230044182-93f929fd-ed42-4074-ae39-025cd82b95c7.png">
</p>
<p align="center" width="100%">
    ERD of ‘AA_OCTANE_HIST’ table
</p>
<p align="center" width="100%">
    <img width="30%" src="https://user-images.githubusercontent.com/55419300/230044218-8fc5a2b6-ad65-479e-abe4-6f172bda9299.png">
</p>

## Results of task/project
At the end of the project, V11 is the last version of the solution that accomplished the goal of the project. Since this is a task that would be scheduled, GUI was not emphasized for this project. With the developed solution, it is now possible to extract Octane data using API. Moreover, the developed program can iterate and process multiple APIs at once with the click of a single button.

## Advantage, disadvantage and suggestion for task improvement
In terms of advantage, the solution is easy to use which saves a lot of time by manually checking in Octane directly. It was also developed with the intention of making it flexible to be adopted by different workspaces as long as it follows the provided guidelines for field names and values. The solution can be easily tweaked with minimal python programming knowledge. Comments present in the program makes it easier for the staff to inspect and modify code segments. All database connections in the program are encrypted with a unique key which ensures data security. The program also performs advanced processing on feature fields and only updates recent changes based on last modified datetime.

In terms of disadvantage, there is a big learning curve to fully understand how the solution works. Apart from that, due to the non-standard practice for the fields, often the name and format of data contained are very different from one workspace to another. This in turn, increases the code complexity by implementing exception blocks specific for workspaces.

In terms of suggestions, the name and format of data contained in the field can be standardized to prevent workspace unique exception handling. Implementation of such practice will reduce the code complexity and be prone to fewer errors.
