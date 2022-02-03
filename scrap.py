import csv

import requests
from bs4 import BeautifulSoup

ROOT_URL = "https://in.kompass.com"
PAGE_URL = f"{ROOT_URL}/a/beverages/04/"
data = [("COMPANY_NAME", "COMPANY_LINK", "COMPANY_LOCATION")]


def get_data():
    print(f"Fetching the data from {PAGE_URL}")
    payload = {}
    headers = {
        "Cookie": "_k_cty_lang=en_IN; JSESSIONID=18113164F7B66E6D84EFEBE195CCCC47; ROUTEID=.2",
        "user-agent": "",
    }
    try:
        response = requests.request("GET", PAGE_URL, headers=headers, data=payload)
        print("Data is successfully fetched...")
        return response.text
    except Exception as e:
        print(e)


def process_data():
    print("Parsing the data from web page started....")
    input_data = get_data()
    soup = BeautifulSoup(input_data, "html.parser")
    results = soup.find(id="resultatDivId")
    job_elements = results.find_all("div", class_="prod_list")
    for job_element in job_elements:
        company_name = job_element.find("span", class_="titleSpan").text.strip()
        company_link = ROOT_URL + job_element.find("a")["href"]
        company_location = job_element.find("span", class_="placeText").text.strip()
        data.append((company_name, company_link, company_location))
    print("Data parsed and ready to write to CSV file")


def write_to_csv():
    print("Writing the data to CSV file started....")
    with open("output.csv", "w") as f:
        csv_writer = csv.writer(f)
        for record in data:
            csv_writer.writerow(record)
    print("Data has been wriiten to the file...")


if __name__ == "__main__":
    process_data()
    write_to_csv()
