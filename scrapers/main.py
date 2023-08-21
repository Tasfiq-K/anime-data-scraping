import os
import re
import time
import pickle
import random
import argparse
import pandas as pd
from tqdm import tqdm

from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from functions import get_categories, get_methods, paperLink, details


def main():

    category_links = get_categories('category_links')
    method_links = get_methods(category_links, 'method_links')
    paper_links = paperLink(method_links=method_links)
    paper_data = details(paper_links=paper_links)

    print(f"Details have been collected from {len(paper_data)} papers")

    return

if __name__ == "__main__":
    main()
