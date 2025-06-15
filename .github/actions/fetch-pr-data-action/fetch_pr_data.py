import sys
import requests
import csv

def fetch_prs(token, repo_name):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    prs = []
    page = 1

    while True:
        url = f"https://api.github.com/repos/{repo_name}/pulls?state=closed&per_page=100&page={page}"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ Error accessing repo: {response.status_code} {response.text}")
            return []

        data = response.json()
        if not data:
            break

        prs.extend(data)
        page += 1

    return prs

def save_to_csv(prs):
    with open('pull_requests.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["PR Title", "Additions", "Reviewers"])

        for pr in prs:
            title = pr.get('title', 'N/A')
            additions = pr.get('additions', 0)
            reviewers = [reviewer['login'] for reviewer in pr.get('requested_reviewers', [])]
            writer.writerow([title, additions, ", ".join(reviewers)])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("❌ Usage: python fetch_pr_data.py <GitHub_Token> <Repo_Name>")
        sys.exit(1)

    token = sys.argv[1]
    repo_name = sys.argv[2]

    print(f"🔵 Fetching PRs for repo: {repo_name}...")
    prs = fetch_prs(token, repo_name)

    if prs:
        print(f"🟢 Total PRs fetched: {len(prs)}")
        save_to_csv(prs)
        print(f"✅ CSV file 'pull_requests.csv' created successfully!")
    else:
        print("⚠️ No PRs found or there was an error.")
