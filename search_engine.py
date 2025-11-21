import os
import re
import sys
from bs4 import BeautifulSoup
from collections import defaultdict, Counter

class SearchEngine:
    """
    A simple search engine that indexes HTML documents and allows for keyword searching.
    Uses an inverted index for efficient retrieval and term frequency for ranking results.
    """
    def __init__(self, webpages_dir="webpages"):
        """
        Initialize the search engine with necessary data structures.
        
        Args:
            webpages_dir (str): Directory containing HTML files to index
        """
        self.webpages_dir = webpages_dir
        self.inverted_index = defaultdict(set)          # term -> set(documents)
        self.term_frequency = defaultdict(Counter)      # term -> Counter({doc: freq})
        self.stopwords = self._load_stopwords()
        self.documents = []                             # list of indexed docs
        self.document_urls = {}                         # filename -> URL
        self._load_url_mapping()

    def _load_stopwords(self):
        """Return a small set of common stopwords."""
        return {
            "a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
            "in", "on", "at", "to", "for", "with", "by", "about", "like",
            "from", "of", "as", "this", "that", "these", "those", "it", "its"
        }

    def _load_url_mapping(self):
        """Load filename → URL mapping from webpages/input.txt."""
        try:
            with open("webpages/input.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("//"):
                        parts = line.split(" ", 1)
                        if len(parts) == 2:
                            filename, url = parts
                            self.document_urls[filename] = url
            print(f"Loaded {len(self.document_urls)} URL mappings")
        except FileNotFoundError:
            print("URL mapping file not found. URLs will not be displayed.")
        except Exception as e:
            print(f"Error loading URL mapping: {e}")

    def parse_document(self, filename):
        """
        Parse HTML file → extract text → tokenize → update indexes.
        """
        filepath = os.path.join(self.webpages_dir, filename)

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text()
            tokens = re.findall(r"\b\w+\b", text.lower())

            filtered_tokens = [
                token for token in tokens
                if token not in self.stopwords and len(token) > 1
            ]

            term_counts = Counter(filtered_tokens)

            for token in term_counts:
                self.inverted_index[token].add(filename)
                self.term_frequency[token][filename] = term_counts[token]

            print(f"Indexed document: {filename} with {len(term_counts)} unique terms")
            return True

        except Exception as e:
            print(f"Error parsing {filename}: {e}")
            return False

    def build_index(self):
        """Index all HTML files in the webpages directory."""
        print(f"Building index from documents in '{self.webpages_dir}'...")
        self.documents = []

        for filename in os.listdir(self.webpages_dir):
            if filename.endswith(".html") or filename.endswith(".htm"):
                if self.parse_document(filename):
                    self.documents.append(filename)

        print(f"Indexing complete. {len(self.documents)} documents indexed with {len(self.inverted_index)} unique terms.")

    def search(self, query):
        """Search for documents matching ALL query terms (AND semantics)."""
        if not query.strip():
            print("Empty query. Please enter some search terms.")
            return []

        terms = re.findall(r"\b\w+\b", query.lower())
        filtered_terms = [t for t in terms if t not in self.stopwords and len(t) > 1]

        if not filtered_terms:
            print("Query contains only stopwords. Please use more specific terms.")
            return []

        matching_docs = None

        for term in filtered_terms:
            if term in self.inverted_index:
                if matching_docs is None:
                    matching_docs = self.inverted_index[term].copy()
                else:
                    matching_docs &= self.inverted_index[term]
            else:
                print(f"Term '{term}' not found in any document.")
                return []

        if not matching_docs:
            print("No documents found matching all query terms.")
            return []

        ranked_results = []
        for doc in matching_docs:
            score = sum(self.term_frequency[term][doc]
                        for term in filtered_terms
                        if term in self.term_frequency)
            ranked_results.append((doc, score))

        ranked_results.sort(key=lambda x: x[1], reverse=True)
        return ranked_results

    def display_results(self, results):
        """Print search results with document URLs."""
        if not results:
            print("No results to display.")
            return

        print(f"\nFound {len(results)} matching documents:")
        print("-" * 50)
        for i, (doc, score) in enumerate(results, 1):
            url = self.document_urls.get(doc, "URL not available")
            print(f"{i}. {doc} (Relevance score: {score})")
            print(f"   URL: {url}")
        print("-" * 50)

    def run_interactive(self):
        """Launch interactive search mode."""
        self.build_index()

        print("\n🔍 Mini Search Engine")
        print("Type 'exit' to quit")

        while True:
            query = input("\nEnter search query: ")
            if query.lower() == "exit":
                print("Exiting search engine. Goodbye!")
                break

            results = self.search(query)
            self.display_results(results)


def main():
    """Run in test mode (generate output.txt) or interactive mode."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":

        engine = SearchEngine()
        engine.build_index()

        test_queries = [
            "",
            "the and is",
            "nonexistentterm",
            "threats",
            "cloud security",
            "cyber attack",
            "malware crypto"
        ]

        output_path = "output.txt"

        with open(output_path, "w", encoding="utf-8") as outfile:

            original_stdout = sys.stdout
            sys.stdout = outfile   # Redirect once

            for query in test_queries:
                print(f"Query: '{query}'")
                results = engine.search(query)
                engine.display_results(results)
                print("\n" + "="*60 + "\n")

            sys.stdout = original_stdout  # Restore stdout

        print(f"Test output saved to {output_path}")

    else:
        engine = SearchEngine()
        engine.run_interactive()


if __name__ == "__main__":
    main()
