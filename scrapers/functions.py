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

def get_categories(f_name, pickle_dir='pickle_files'):

    """ This function downloads the category links from the given URL and saves the file file in a directory
        URL: "https://paperswithcode.com/methods"
        Arguments: Takes two arguements
        f_name: (str) name of the pickle file, which wiil be saved inside the pickle_dir 
        returns: a list containing all the links
    """
    # initializing the driver and firefox profile
    webdriver_path = "/usr/local/bin/geckodriver"
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options=options)

    main_page = "https://paperswithcode.com/methods"

    driver.get(main_page)

    links = [link.get_attribute('href') for link in driver.find_elements(By.CSS_SELECTOR, '.card > a')]
    # print(links)

    # print(f"Total links: {len(links)}")
    driver.close()

    if not os.path.exists(pickle_dir):
        os.mkdir(pickle_dir)

        with open(os.path.join(pickle_dir, f_name), "wb") as f:
            pickle.dump(links, f)
    else:
        with open(os.path.join(pickle_dir, f_name), "wb") as f:
            pickle.dump(links, f)



    # with open(os.path.join(dir_name, f_name), "wb") as f:    # writing the file in byte mode
    #     pickle.dump(links, f)   # pickling/dumping the file

    return links



def get_methods(categories, f_name, file_to_load=None, pickle_dir='pickle_files') :

    """ This function collects the links listed in the categories collected using the get_categories function.
        loads the file if provided, else gets the returned list from the get_categories function
        arguments: 
            categories: a list containing the category links
            f_name: name of the pickle file, which will be saved in the pickle_dir
            file_to_load: name of the file to load, default None
        
        returns: a list cointaining the method links from each categories
    """

    if file_to_load:
        with open(os.path.join(pickle_dir, file_to_load), 'rb') as f:
            links = pickle.load(f)
    else:
        links = categories

    # with open("pickle_files/category_links", "rb") as f:
    # links = pickle.load(f)
    
    method_links = []
    
    # initializing the driver and firefox profile
    webdriver_path = "/usr/local/bin/geckodriver"
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options=options)

    for link in tqdm(links):
        driver.get(link)
        time.sleep(random.randint(1, 5))
        methods = [method_link.get_attribute('href') for method_link in driver.find_elements(By.CSS_SELECTOR, '.method-image > a')]
        # print(methods)
        # print(len(methods))
        method_links.extend(methods)
    
    # print(len(method_links))

    with open(os.path.join(pickle_dir, f_name), "wb") as f:
        pickle.dump(method_links, f)

    driver.close()

    return method_links

def paperLink(method_links, file_name=None, dump_file='all_paper_links', pickle_dir='pickle_files'):

    """ This function collects all the Urls of the paper and saves them in a file called 'all_paper_links (defualt)
        arguments:
                file_name: provide a file name to load the method links, otherwise it will load them using the returned item from
                           get_methods functions, default None
                dump_file: name of the file in which the links will be saved.
        returns: list containing all the links of the papers
    """

    # checking if the directory exists for the pickle files
    path = pickle_dir
    if file_name:
        if os.path.exists(path):
            with open(os.path.join(path, file_name), "rb") as f:
                urls = pickle.load(f)
        else:
            # print to the console if path doesn't exist
            print(f"Directory {path} doesn't exist, make sure to create/have one.")
            return 
    else:
        urls = method_links

    disabled_class = "paginate_button page-item next disabled"
    all_paper_links = []

    # initializing the driver and firefox profile
    webdriver_path = "/usr/local/bin/geckodriver"   # path to the webdriver
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options=options)
    
    for idx, url in enumerate(tqdm(urls)):
        # print(f"Link {idx}")
        driver.get(url)
        
        time.sleep(random.randint(2, 5))

        page_list = driver.find_element(By.CLASS_NAME, 'dataTables_paginate.paging_simple_numbers').find_elements(By.TAG_NAME, 'li')
        is_class = page_list[-1].get_attribute('class')

        while is_class != disabled_class:
            try:

                # try to collect the link of the papers adding to the all_paper_links
                # searches for the 'next' button waits 1 second after finding and then clicks it

                time.sleep(1)
                paper_links = [paper_link.get_attribute('href') for paper_link in\
                                driver.find_elements(By.CLASS_NAME, "black-links > a")]
                all_paper_links.extend(paper_links)
                page_list = driver.find_element(By.CLASS_NAME, 'dataTables_paginate.paging_simple_numbers').find_elements(By.TAG_NAME, 'li')
                page_list[-1].location_once_scrolled_into_view
                time.sleep(1)
                
                page_list[-1].click()   # clicking the "next button"

                page_list = driver.find_element(By.CLASS_NAME, 'dataTables_paginate.paging_simple_numbers').find_elements(By.TAG_NAME, 'li')
                is_class = page_list[-1].get_attribute('class')
                
            except StaleElementReferenceException:

                # same process as previous, but only works if an StaleElementReferenceException is raised

                paper_links = [paper_link.get_attribute('href') for paper_link in  driver.find_elements(By.CLASS_NAME, "black-links > a")]
                all_paper_links.extend(paper_links)
                page_list = driver.find_element(By.CLASS_NAME, 'dataTables_paginate.paging_simple_numbers').find_elements(By.TAG_NAME, 'li')
                page_list[-1].location_once_scrolled_into_view
                time.sleep(1)

                page_list[-1].click()   # clicking the "next button"

                page_list = driver.find_element(By.CLASS_NAME, 'dataTables_paginate.paging_simple_numbers').find_elements(By.TAG_NAME, 'li')
                is_class = page_list[-1].get_attribute('class')
        
        with open(os.path.join(path, dump_file), "wb") as f:  # creates a file inside the 'path' dir with 'dump_file' name
            pickle.dump(all_paper_links, f)
        # with open(os.path.join(path, dump_file), "wb") as f:  # creates a file inside the 'path' dir with 'dump_file' name
        #      json.dump(all_paper_links, f)
        
    print(f"All done")
    print(f"Total Paper links: {len(all_paper_links)}")

    driver.close()  # closing the driver
    
    return all_paper_links


def details(paper_links, dir_name='pickle_files', csv_path='csv_files', file_name=None):
    # checking if the directory exists for the pickle files
    if file_name:
        if os.path.exists(dir_name):
            with open(os.path.join(dir_name, file_name), "rb") as f:
                urls = pickle.load(f)
                urls = list(set(urls))
        else:
            # print to the console if path doesn't exist
            print(f"Directory {dir_name} doesn't exist, make sure to create/have one.")
    
    else:
        urls = paper_links

    # urls = pd.read_csv('csv_files/problem_urls.csv')
    # columns = ['index', 'URLs', 'title', 'abstract', 'datasets_used', 'dataset_links', 'methods', 'tasks']
    data = []
    problem_data = []

    # initializing the driver and firefox profile
    webdriver_path = "/usr/local/bin/geckodriver"   # path to the webdriver
    options = Options()
    options.set_preference('profile', webdriver_path)
    driver = Firefox(options=options)
    

    for idx, url in enumerate(tqdm(urls)):
    # for idx, url in enumerate(tqdm(urls['URLs'])):
        
        # driver.set_page_load_timeout(300)
        try:
            driver.get(url)
            time.sleep(1)
            index = idx
            URLs = url 
            title = driver.find_element(By.CLASS_NAME, 'paper-title').find_element(By.TAG_NAME, 'h1').text
            abstract = driver.find_element(By.CLASS_NAME, 'paper-abstract').find_element(By.TAG_NAME, 'p').text
            tasks = [task.text for task in driver.find_element(By.CLASS_NAME, 'paper-tasks').find_elements(By.TAG_NAME, 'a')]
            datasets = [dataset.text for dataset in driver.find_element(By.CLASS_NAME, "paper-datasets").find_elements(By.TAG_NAME, 'a')]
            dataset_links = [link.get_attribute('href') for link in driver.find_element(By.CLASS_NAME, "paper-datasets")\
                            .find_elements(By.TAG_NAME, 'a')]
            methods = [method.text for method in driver.find_elements(By.CLASS_NAME, 'method-section > a')]    

            data.append({
                "index": index,
                "URLs": URLs,
                "title": title,
                "abstract": abstract, 
                "datasets_used": datasets,
                "dataset_links": dataset_links,
                "methods": methods,
                "tasks": tasks
            })


            path = csv_path
            df = pd.DataFrame(data=data, columns=data[0].keys())
        
            if not os.path.exists(path):
                os.mkdir(path)
                df.to_csv(os.path.join(path, "data_papersWithCode.csv"), index=False)
            else:
                df.to_csv(os.path.join(path, "data_papersWithCode.csv"), index=False)
        
        except TimeoutException:

            problem_data.append({
                "URLs": url 
            })
            path = csv_path
            p_df = pd.DataFrame(data=problem_data, columns=problem_data[0].keys())
            
            if not os.path.exists(path):
                os.mkdir(path)
                p_df.to_csv(os.path.join(path, "problem_urls.csv"), index=False)
            else:
                p_df.to_csv(os.path.join(path, "problem_urls.csv"), index=False)
            
            continue


    driver.close()

    return data