"""Fetch pull request data from a GitHub repository and save it to a CSV file."""

import sys
import csv
import requests


def fetch_prs(api_token, repository_name):
    """Fetch closed pull requests from the given GitHub repository."""
    headers = {
        "Authorization": f"token {api_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    pull_requests = []
    page = 1

    while True:
        url = (
            f"https://api.github.com/repos/{repository_name}/pulls"
            f"?state=closed&per_page=100&page={page}"
        )
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            print("Error accessing repo:", response.status_code, response.text)
            return []

        data = response.json()
        if not data:
            break

        pull_requests.extend(data)
        page += 1

    return pull_requests


def save_to_csv(pull_requests):
    """Save PR title, additions, and reviewers to a CSV file."""
    with open('pull_requests.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PR Title", "Additions", "Reviewers"])

        for pr in pull_requests:
            title = pr.get('title', 'N/A')
            additions = pr.get('additions', 0)
            reviewers = [rev['login'] for rev in pr.get('requested_reviewers', [])]
            writer.writerow([title, additions, ", ".join(reviewers)])


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python fetch_pr_data.py <GitHub_Token> <Repo_Name>")
        sys.exit(1)

    GITHUB_TOKEN = sys.argv[1]
    REPO = sys.argv[2]

    print(f"Fetching PRs for repo: {REPO}...")
    PRS = fetch_prs(GITHUB_TOKEN, REPO)

    if PRS:
        print(f"Total PRs fetched: {len(PRS)}")
        save_to_csv(PRS)
        print("CSV file 'pull_requests.csv' created successfully!")
    else:
        print("No PRs found or there was an error.")
