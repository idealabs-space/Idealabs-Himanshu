import os
import requests
import math

class JobSearchAgent:
    """
    This agent queries the Serper API to find relevant job postings based on:
    1. The candidate's dynamic skill list
    2. The city specified by the user
    It chunks the skill list and queries multiple job sites (Indeed, LinkedIn, Glassdoor, Monster).
    """

    def __init__(self):
        self.api_key = os.getenv("SERPER_API_KEY")
        self.url = "https://google.serper.dev/search"

    def search_jobs(self, skills, city, chunk_size=5):
        """
        1. Chunks the skill list to avoid overly long queries (which can reduce search results).
        2. For each chunk of skills, queries Serper with multiple sites in a single search.
        3. Combines and deduplicates all results into one dictionary.

        :param skills: list of user-extracted skills
        :param city: city where the user wants to find jobs
        :param chunk_size: how many skills to include per query (default=5)
        :return: combined data with a top-level key 'organic' containing merged results
        """
        if not skills:
            # If no skills are found, do a generic search
            return self._make_serper_request(
                query=f"jobs in {city} site:indeed.com OR site:linkedin.com OR site:glassdoor.com OR site:monster.com"
            )

        # We chunk the skill list to create multiple queries
        all_results = []
        num_skills = len(skills)
        num_chunks = math.ceil(num_skills / chunk_size)

        for i in range(num_chunks):
            start_index = i * chunk_size
            end_index = start_index + chunk_size
            skill_subset = skills[start_index:end_index]

            # Build an "AND" query with the subset (ensures these skills appear in job listings)
            skills_str = " AND ".join(skill_subset)

            query = (
                f"jobs in {city} for {skills_str} "
                "site:indeed.com OR site:linkedin.com OR site:glassdoor.com OR site:monster.com"
            )

            # Make the Serper request for this subset
            data = self._make_serper_request(query)
            if data and "organic" in data:
                all_results.extend(data["organic"])

        # Combine everything into one structure with a single "organic"
        combined_data = {"organic": []}
        seen_links = set()
        for item in all_results:
            link = item.get("link")
            if link not in seen_links:
                seen_links.add(link)
                combined_data["organic"].append(item)

        return combined_data

    def _make_serper_request(self, query):
        """
        Helper to call Serper with a single query
        """
        payload = {
            "q": query,
            "gl": "us",  # US-based search results
            "hl": "en"   # English
        }
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }
        try:
            # Increase timeout if needed
            response = requests.post(self.url, json=payload, headers=headers, timeout=40)
            return response.json()
        except Exception as e:
            print(f"Error in Serper job search: {e}")
            return {}
