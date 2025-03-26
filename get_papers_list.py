import requests
import pandas as pd
import argparse
import re

# PubMed API base URL
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
PUBMED_FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

# Function to fetch PubMed paper IDs based on a search query
def fetch_pubmed_paper_ids(query, max_results=10):
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()  # Raise an error if request fails
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])

# Function to fetch paper details (title, authors, etc.)
def fetch_paper_details(paper_id):
    params = {
        "db": "pubmed",
        "id": paper_id,
        "retmode": "xml"
    }
    response = requests.get(PUBMED_FETCH_URL, params=params)
    response.raise_for_status()
    return response.text

# Function to extract relevant details from paper data
def extract_paper_info(paper_xml):
    title_match = re.search(r"<ArticleTitle>(.*?)</ArticleTitle>", paper_xml)
    title = title_match.group(1) if title_match else "N/A"

    authors = re.findall(r"<LastName>(.*?)</LastName>.*?<Affiliation>(.*?)</Affiliation>", paper_xml, re.DOTALL)
    author_list = []
    company_authors = []

    for last_name, affiliation in authors:
        author_info = {"Name": last_name, "Affiliation": affiliation}
        author_list.append(author_info)

        # Identify company-affiliated authors (simple heuristic)
        if re.search(r"pharma|biotech|inc\.|ltd\.|corp\.|gmbh", affiliation, re.IGNORECASE):
            company_authors.append(last_name)

    return {
        "Title": title,
        "Authors": author_list,
        "Company_Affiliations": ", ".join(company_authors) if company_authors else "None"
    }

# Function to save results in CSV format
def save_to_csv(results, filename="pubmed_results.csv"):
    df = pd.DataFrame(results)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")

# Main function to execute the program
def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed API and filter company-affiliated authors.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename", default="pubmed_results.csv")
    args = parser.parse_args()

    print(f"Searching PubMed for: {args.query}")
    
    paper_ids = fetch_pubmed_paper_ids(args.query)
    if not paper_ids:
        print("No papers found for the given query.")
        return

    results = []
    for paper_id in paper_ids:
        print(f"Fetching details for Paper ID: {paper_id}")
        paper_xml = fetch_paper_details(paper_id)
        paper_info = extract_paper_info(paper_xml)
        results.append(paper_info)

    save_to_csv(results, args.file)

if __name__ == "__main__":
    main()
