# syllybles
Song Lyric Phonetic Analysis
A Python project that transcribes text from English to the International Phonetic Alphabet to study the phonetic structure and rhyme scheme of music.
Utilizes the APIs from Spotify to pull data for songs in a playlist, Genius to search for song  lyrics, and Webster Dictionary for word lookups. 
Incoming data is cleaned utilizing Pandas and Regex libraries. An algorithm that uses SQLite3 tables splits phonetic words into their corresponding syllables, and those syllables into their component parts.
Along the way, meta-deta is generated and stored in a database for future reference.
Includes logic for several redundancy checks to reduce total API calls and prevent duplicate entries into the database. 

Currently on hiatus pending further research.
