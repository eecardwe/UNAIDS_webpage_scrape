# finalproj
507 Final Project

## Background
This past summer, I worked on the community mobilization team at UNAIDS in Geneva, Switzerland. The team is responsible for working with 'civil society' and community partners to uplift the voices of people in the communinites impacted by HIV and AIDS. The focus of our work was often on what we called 'key populations', or populations in which rates of new infection are still on the rise despite continued downward trends in the general world population. These key populations included:

1. Men who have sex with men (MSM)
2. People who inject drugs (PWID)
3. Sex workers
4. Transgender people

Occassionally a fifth group is included:
5. Prisoners and other incarcerated people

There are often many barriers to invidiuals that fall into these five categories when seeking treatment or prevention, which is one of the reasons we see increasing rates of infection in these populations. In some countries, it is illegal identify as a member in one or several of these communities. 

For this report, I was interested in exploring the news coverage of these community groups to see if certain countries were over or under-represented in terms of their news coverage. It would be interesting for a future report to explore UNAIDS reports of community activisim compared to news coverage representation. It may also be interesting to explore the comparison of the illegality of identifying as one of these community groups compared to news representation of their existance. My hypothesis is that news underrreports activities where activities are legal for fear of persecution.

## Necessary Installations
Before running the program, the following packages must be installed on your device: 
* requests
* json
* BeautifulSoup
* re
* os
* urllib
* sqlite3
* csv
* pandas
* numpy
* string
* pycountry
* plotly
* PIL
* wordcloud
* matplotlib

## Project Functions & Capabilities

### Functions 

#### make_request_using_cache
This function takes a url as input and either pulls the existing, cached data from the cache.json file or makes a new request to the url and caches the request results. The function returns the request results.

#### init_db()
This function does not take any input. It creates a database with three tables in Sqlite3: Countries, Stories, and Mentions. It also sets up the table headers, data types to be contined in the cells, and both Primary and Foreign keys. 

#### scrape_unaids()
This function does not take any input. It uses the make_request_using_cache function to make a request to the 'https://www.unaids.org/en/topic/community/stories' webpage, uses BeautifulSoup to parse the results and find links to articles on this page, and crawls to each link to collect additional data: particularly the names of any countries mentioned in a given article. Each unique article mentioning a country is then added to the 'country_mention_count' which calculates the total number of unique articles mentioning the name of a given country (one article mentioning the same country multiple times only counts as +1 unique article mention). The function returns a dictionary containing key, value pairs of country and mention count, respectively.

#### scrape_unaids_words()
This function similarly takes no input and uses the make_request_using_cache functionto make a request to the communiy stories webpage on the UNAIDS website. It then scrapes the links to articles contained on the site and then follows the links to each article contained on the page. It then collects the title and contents of each article and returns a key, value pair representing the two items collected, respectively. 

#### insert_table_data()
This function takes country_mention_count as input (the dictionary returned by scrape_unaids_words) and populates the database table 'Mentions' with the results. It also takes a csv file (COUNTRIESJSON) and populates another table, 'Countries', with the results. The two tables are linked by the country name contained in each ("Country" in the Mentions table and "EnglishName" in the Countries table). Nothing is returned as a result. However, the database is populated and the results are visible by opening the database and exploring the tables in Sqlite.

#### insert_table_words
This function takes the article_words dictionary returned by the scrape_unaids_words function and uses them to populate the 'Stories' table in the COMDB database. Nothing is returned as a result. However, the database is populated and the results are visible by opening the database and exploring the tables in Sqlite.

#### plot_mention_freq()
This function does not take any inputs. It pulls data from the database uses it to create a map with countries color-coded based on the number of articles mentioning that specific country. 

#### plot_mention_pop()
This function does not take any inputs. It pulls data from the database and creates a scatterplot comparing the population of a given country (x-axis) to the number of unique articles mentioning that same country (y-axis). 

#### pie_chart()
This function takes either 'Country' or 'Region' as input. It pulls data from the database on the number of unique articles mentioning each country. If 'Country' is input, it then displays the number of articles mentioning each country as a pie chart visualization. If 'Region' is input, the function aggregates country mentions into their greater region, and then uses a pie chart to visually represent the volume of articles mentioning countries from that region.

#### word_cloud()
This function takes no inputs. It pulls data from the 'Stories' table in the database and calculates the most commonly used words thoughout all 102 articles. It then creates a visual representation, or word cloud, of these words, using the size of each word to indicate the number of mentions.

#### menu()
This function does not take any inputs and is the default function in the program. It briefly describes the visualizaton functions available to the user and prompts them to select one to display. 

## Running the Program
To run the program, be sure all appropriate installations have been installed (listed above). Then, simply use the command line to run the program using >>> python finalproj.py

Thanks! I hope you like my project!!
