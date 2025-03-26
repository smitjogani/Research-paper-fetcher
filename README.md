# Fetch Research Paper

This project fetches research papers from PubMed using their API and extracts relevant details such as title, authors, and company affiliations.

## Code Organization

```
p-task/
├── get_papers_list.py   # Main script to fetch and process research papers
├── results.csv          # Example output file containing processed paper details
├── pyproject.toml       # Project metadata and dependencies
└── README.md            # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd p-task
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, if using `pyproject.toml`:
   ```bash
   pip install .
   ```

## Execution

To execute the program, run the following command:

```bash
python get_papers_list.py "<search-query>" -f <output-filename>
```

- Replace `<search-query>` with your PubMed search term.
- Replace `<output-filename>` with the desired name for the output CSV file (default: `pubmed_results.csv`).

Example:
```bash
python get_papers_list.py "cancer treatment" -f results.csv
```

## Additional Notes

- Ensure Python 3.13 or higher is installed.
- The script uses the PubMed API to fetch data. Make sure you have an active internet connection.
