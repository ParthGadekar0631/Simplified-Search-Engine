# 🔍 Simplified Search Engine – CS 600 Project
## 📌 Project Overview

This project implements a mini Search Engine based on Section 23.6 (Search Engine) of the course textbook.
It indexes a small collection of web pages, removes common stopwords, and allows users to perform keyword-based searches with ranked outputs.

The system demonstrates how real search engines store, process, and retrieve textual information efficiently.

## 🔥 Key Features

- HTML Parsing: Extracts text content from web pages using BeautifulSoup
- Stopword Removal: Filters out common English words such as the, is, and, of.
- Inverted Index: Maps every keyword to all documents containing that keyword.
- Efficient Search: Supports AND-based query processing.
- Ranking Algorithm: Ranks results based on total term frequency across query terms.
- Test Mode: Automatically generates output for predefined queries including boundary conditions.
- Interactive Mode: Allows users to perform searches through the terminal.

## 🛠 Technologies Used

- Python
- BeautifulSoup4 (HTML parsing)
- Regular Expressions (re) (tokenization)
- Collections: defaultdict, Counter, set (data structures)
- File I/O for reading webpages and generating output

## 📁 Project Structure

```bash
project_folder/
│
├── search_engine.py          # Main program file
├── output.txt                # Output file generated in test mode
├── README.md                 # Project documentation
│
└── webpages/                 # Dataset folder
    ├── input.txt             # filename → URL mapping
    ├── apple-zero-days-sophisticated-attacks.html
    ├── android-pre-downloaded-malware-crypto-wallets.html
    ├── cisa-alleged-oracle-cloud-breach.html
    ├── cve-program-cuts-cyber-sector.html
    ├── multiple-group-exploiting-ntlm-flaw.html
    └── trump-chris-krebs-resigns-sentinelone.html
```
## 📊 How It Works
1. Data Loading & Preprocessing
- Reads all .html files from the webpages/ directory.
- Parses each page using BeautifulSoup.
- Extracts text and tokenizes it using regular expressions.
- Removes stopwords and single-character words.

2. Index Construction
Builds an inverted index
→ term → set(documents)
Builds a term frequency map
→ term → Counter({doc: count})

3. Searching
Processes user queries similarly (tokenize + stopword removal).
Performs AND semantics:
Only documents containing all query terms are returned.
Ranks results using total term frequency across query terms.

4. Output

Each result includes:
Document name
Relevance score
Original source URL (from input.txt)




## 🎯 Future Improvements

- Implement TF-IDF for more advanced ranking
- Add OR / NOT query support
- Support phrase-based queries
- Integrate PageRank-style ranking using hyperlink analysis

## 🤝 Contribution

Feel free to fork, modify, or extend the project with more ranking algorithms or datasets!

## 📄 License

This project is developed as part of CS 600 – Advanced Algorithm Design & Implementation and is intended for academic use.