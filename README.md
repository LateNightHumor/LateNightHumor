## LateNight Humor

### Description
The LateNightHumor project is dedicated to the data collection and analysis of jokes retrieved from the LexisNexis Database. 
There are several aspects to this project, namely, the retrieval of corpuses from the Bulletin Frontruner's Last Laughs section, 
the storage of these corpuses in both a human readable and quickly accessible format, the parsing of these corpuses to detail specific jokes, 
the tagging of important meta data such as dates, locations, people and other geospatial data, and the presentation of 
this data in a user-friendly, accessible manner. In addition to these process goals, we also wish to be able to frequently be able to update
this database on a daily basis to minimize processing. 

## Setup

Once the codebase is pulled, all one needs to do is create a `config.ini` file in the same form as the `default.ini` file.
After creation, simply run the `driver.py` script and it'll begin initializing the database. It should provide
estimated completion times and will generate a db file as specified in the `config.ini` as well as a csv with the appropriate data.

## Continuous Updates

To be implemented.