from functions import get_categories, get_methods, paperLink, details

#  
def main():

    category_links = get_categories('category_links')
    method_links = get_methods(category_links, 'method_links')
    paper_links = paperLink(method_links=method_links)
    paper_data = details(paper_links=paper_links)

    print(f"Details have been collected from {len(paper_data)} papers")

    return

if __name__ == "__main__":
    main()
