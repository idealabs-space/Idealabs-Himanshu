import csv
import pandas as pd

class CSVWriterAgent:
    """
    This agent takes the job search results, filters them for trustworthy/genuine sites,
    calculates match scores, sorts them, and writes the top N to a CSV.
    """

    def __init__(self, filename="job_results.csv"):
        self.filename = filename

    def save_jobs_to_csv(self, search_data: dict, user_skills: list, top_n=10):
        """
        1. Filter for Indeed/LinkedIn/Glassdoor/Monster results.
        2. Calculate match scores based on how many user_skills appear in the snippet (case-insensitive).
        3. Sort by match score, then keep top N.
        4. **Always** create (or overwrite) a CSV file with columns: [Title, Link, Snippet, MatchScore].
           - If no results are found, we still create an empty CSV with those headers.
        """

        organic_results = search_data.get('organic', [])

        # Build a list of relevant job records
        jobs_with_scores = []
        if organic_results:
            for item in organic_results:
                link = item.get("link", "")
                # Accept if link contains any of these domains
                if any(site in link for site in ["indeed.com", "linkedin.com", "glassdoor.com", "monster.com"]):
                    title = item.get("title", "N/A")
                    snippet = item.get("snippet", "N/A")

                    # Calculate match score
                    snippet_lower = snippet.lower()
                    match_score = sum(
                        1 for skill in user_skills if skill.lower() in snippet_lower
                    )

                    jobs_with_scores.append({
                        "Title": title,
                        "Link": link,
                        "Snippet": snippet,
                        "MatchScore": match_score
                    })

            # Sort descending by match score
            jobs_with_scores.sort(key=lambda x: x["MatchScore"], reverse=True)

            # Take only the top N
            jobs_with_scores = jobs_with_scores[:top_n]

        else:
            print("No 'organic' results found from the search. Creating an empty CSV.")

        # Now create/write the CSV (even if there are no job rows)
        df = pd.DataFrame(jobs_with_scores, columns=["Title", "Link", "Snippet", "MatchScore"])
        df.to_csv(self.filename, index=False, encoding="utf-8")

        return self.filename
