# Cayena Challenge 🌶️

This challenge consists of constructing a **Analytical Platform** on which data analysts
can run queries and build basic data visualization.
The object of analysis for this challenge is the book information from the [BooksToScrape website](https://books.toscrape.com), however, there is no API, nor other method of easy data extraction available for the books present on this website, thus requiring a **Web Scraping** solution to be built. Also, there's a need of comparing how prices/stock changed for the books over the time, creating the need for a daily ETL job to be ran.

## How to use the platform

**Requirements:** Docker and Docker Compose installed on your machine.


1. Clone the repo and *cd* into the new directory
    ```sh
    git clone https://github.com/muriloxyz/cayena-challenge.git && cd cayena-challenge
    ```
2. Make sure the PostgreSQL data volume is readable and under your ownership everytime before you initialize the docker-compose script
    ```sh
    chmod 777 data
    chown -R $USER:$USER data
    ```
3. Initialize the docker-compose script:
    ```sh
    docker-compose up -d
    ```
4. Access the data platform (**SqlPad**) within ``http://localhost:3000``. The default user is ``cayena@cayena.com``, and it's password is ``cayena``. (Mindblown 🤯)
5. Select your connection ``Postgres Database`` and start analysing your data inside the ``book_info`` table. 
6. Write your most beautiful queries!

For more info and how to use the SqlPad analytical platform (plus on how to build visualizations), please refer to the [SqlPad Docs](https://getsqlpad.com/#/).

## Main takeaways

- If you need daily data updates updates, keep the docker containers running! There's a cron job scheduled to scrape the website every day, 3am UTC time (00:00 Brazilian time). It will scrape the website and store all the processed data into the book_info table, leaving it ready for analysis;
- It is possible to trigger the job manually! But you'll need to enter the worker container to execute the python job;
- The ``data`` directory is a docker volume used by the PostgreSQL container, and contains all of it's data.

## Architecture
![Architecture-Diagram](https://user-images.githubusercontent.com/43562753/159823744-949c49a1-0b38-4d7d-941b-73edea8601cb.png)

Description of the 3 containers used for this challenge:

- **Worker**: Responsible for running the ETL job with the help of the configured cron scheduling. It uses 4 threads for faster web scraping. Uses a python/ubuntu base image.
- **Pgsql**: Docker image provided by the PostgreSQL team. Simply hosts a database in which all treated data is stored.
- **Sqlpad**: Docker image provided by the Sqlpad team. It creates an locally hosted web analytics platform which connects to the Pgsql container for data.

## Reference
Here are the main articles I needed in the making of this challenge:

- [BeautifulSoup Tutorial](https://realpython.com/beautiful-soup-web-scraper-python/)
- [Sharing a list through multiple threads](https://stackoverflow.com/questions/23623195/multiprocessing-of-shared-list)
- [Setting up cron](https://stackoverflow.com/questions/37015624/how-to-run-a-cron-job-inside-a-docker-container)
- [Creating a table with Postgre's Docker Image](https://stackoverflow.com/questions/38713597/create-table-in-postgresql-docker-image)
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [SqlPad Docs](https://getsqlpad.com/#/)