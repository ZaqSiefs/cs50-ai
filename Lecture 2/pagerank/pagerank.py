import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    transition_prob = dict()

    if (len(corpus[page]) > 0):
        damping_prob = (1 - damping_factor) / len(corpus)
        transition_prob = dict.fromkeys(corpus.keys(), damping_prob)

        for link in corpus[page]:
            transition_prob[link] += damping_factor / len(corpus[page])
    else:
        for p in corpus:
            transition_prob[p] = 1 / len(corpus)

    return transition_prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pagerank_total = dict.fromkeys(corpus.keys(), 0)

    page = random.choice(list(corpus.keys()))
    pagerank_total[page] += 1

    for _ in range(n):
        transition = transition_model(corpus, page, damping_factor)
        page = random.choices(list(transition.keys()), weights=list(transition.values()), k=1)[0]
        pagerank_total[page] += 1

    return {key: value / n for key, value in pagerank_total.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    pagerank = dict.fromkeys(corpus.keys(), 1 / N)
    damping_prob = (1 - damping_factor) / N

    delta = dict.fromkeys(corpus.keys(), 1)
    TOLERANCE = 0.001

    while any(change >= TOLERANCE for change in list(delta.values())):
        for page in corpus:
            # List of pages to iterate for the summation
            # if page has no links, treat as if it links to all pages - otherwise only links in page
            i_set = [key for key, links in corpus.items() if len(links) == 0 or page in links]
            # value of the summation
            i_sum = 0

            # perform summation
            for i in i_set:
                numlinks = len(corpus[i]) if len(corpus[i]) > 0 else N
                i_sum += damping_factor * (pagerank[i] / numlinks)

            # finish equation
            cur_rank = damping_prob + i_sum
            delta[page] = abs(pagerank[page] - cur_rank)
            pagerank[page] = cur_rank

    return pagerank


if __name__ == "__main__":
    main()
