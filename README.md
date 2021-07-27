# Greenhouse extractor

This project extracts the data from greenhouse and restructures it into a event style database.

The database diagram can be found here: https://miro.com/app/board/o9J_l86oZgU=/

## Populate the database

- Start a postgresql database for local development
- Create a file `.env.local`: `touch .env.local`
- In this file add the 2 databases strings (ours and greenhouse's):
```
GREENHOUSE_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
CANONICAL_DATABASE_URL=postgresql://USER:PASSWORD@HOST:PORT/DATABASE
```
- `dotrun exec yarn run migrate`
- Have fun querying your new database.

## Run the project

- Once the database is populated
- Add the harvest API key to your `.env.local`:
```
HARVEST_API_KEY=THE_SECRET_KEY
```
- In a terminal, run the command `dotrun`
- You can access the dashboard on your browser at: http://0.0.0.0:8501/