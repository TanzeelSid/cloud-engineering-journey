import json
import os
import sys

import requests

GITHUB_USER = os.environ.get("GITHUB_USER", "octocat")  # env var with default
TOKEN = os.environ.get("GITHUB_TOKEN")                  # optional; never hardcode
URL = f"https://api.github.com/users/{GITHUB_USER}"


def fetch_user(url):
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()          # turns 404/500 into an exception
        return resp.json()
    except requests.exceptions.Timeout:
        print("Error: request timed out")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    return None


def main():
    data = fetch_user(URL)
    if data is None:
        sys.exit(1)

    with open("output.json", "w", encoding="utf-8") as f:   # file I/O: write
        json.dump(data, f, indent=2)
    with open("output.json", encoding="utf-8") as f:        # file I/O: read back
        saved = json.load(f)

    print("Name:        ", saved.get("name") or saved["login"])
    print("Public repos:", saved["public_repos"])
    print("Followers:   ", saved["followers"])


if __name__ == "__main__":
    main()