# Octane Data Extraction using API

This project was initiated by me during my internship at Infineon Technologies with aim to develop a solution for Octane data extraction using API for a specific team that lacked technical skills required to develop a program that utilizes API to export and process data.

## Task Specification
The solution for Octane data extraction using API was assigned to develop that:

* Authenticate API connection using client ID and password
* Retrieve data based on last modified datetime from API using cookie
* Process and export the data to oracle database, and
* Loop the extraction process for all API connections in the oracle database

## Implementation and Solution Method
The solution was developed using the python programming language and PyCharm as the IDE. The implantation of the solution began with brainstorming and discussion sessions with one of the key people that is involved in service product management. After several meetings, the solution was developed and continuously improved for a period of three months.

Version 1 to 3 of the program functioned as a POC which authenticates the API connection, retrieves and exports data to the oracle database. Version 4 of the program which included data processing was used to develop a template which was circulated to other colleagues to test out the program. The program was developed further until beta versions (V7 & V8).

A senior system architect of Infineon Technologies gave some suggestions for significant improvements to the program. Along with V9, a separate program called ‘octane_database_encryption.py’ was created to encrypt and decrypt database connections.

Stable versions of the program were released as V9, V10, and V11 with minor bug fixes.

## Results of Task/Project
At the end of the project, V11 is the last version of the solution that accomplished the goal of the project. With the developed solution, it is now possible to extract Octane data using API. Moreover, the developed program can iterate and process multiple APIs at once with the click of a single button.

## Advantage, Disadvantage, and Suggestions for Task Improvement
In terms of advantages, the solution is easy to use, saves a lot of time by manually checking in Octane directly, and is flexible to be adopted by different workspaces as long as it follows the provided guidelines for field names and values. The solution can be easily tweaked with minimal python programming knowledge. Comments present in the program make it easier for the staff to inspect and modify code segments. All database connections in the program are encrypted with a unique key which ensures data security. The program also performs advanced processing on feature fields and only updates recent changes based on last modified datetime.

In terms of disadvantages, there is a big learning curve to fully understand how the solution works. Due to the non-standard practice for the fields, often the name and format of data contained are very different from one workspace to another. This, in turn, increases the code complexity by implementing exception blocks specific for workspaces.

In terms of suggestions, the name and format of data contained in the field can be standardized to prevent workspace unique exception handling. Implementation of such practice will reduce the code complexity and be prone to fewer errors.

## Usage
* The program requires a valid API client ID and password to authenticate and retrieve data.
* The program supports multiple API connections stored in the oracle database.
* Run 'octane_database_encryption.py' to encrypt and decrypt the database connections.
* Run 'octane_api_v11.py' to extract and process data from the API.

## Dependencies
* Python 3.6 or higher
* PyCharm IDE
* Oracle database connection
