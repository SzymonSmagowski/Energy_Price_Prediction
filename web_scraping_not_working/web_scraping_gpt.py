import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the website
url = "https://www.pse.pl/dane-systemowe/plany-pracy-kse/plan-koordynacyjny-5-letni/wielkosci-podstawowe"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Print the HTML content (uncomment the next line for debugging)
    # print(soup.prettify())

    # Find all tables on the page
    tables = soup.find_all('table')

    # Check if there are tables on the page
    if tables:
        # Iterate through tables and try to find the desired one
        for table in tables:
            # Check for specific attributes or structure that may identify the target table
            if 'table-bordered' in table.get('class', []):
                # Extract data from the table
                data = []
                for row in table.find_all('tr'):
                    row_data = [cell.text.strip() for cell in row.find_all(['td', 'th'])]
                    data.append(row_data)

                # Create a DataFrame using pandas
                df = pd.DataFrame(data[1:], columns=data[0])

                # Display the DataFrame
                print(df)

                # Save the DataFrame to a CSV file if needed
                # df.to_csv('output.csv', index=False)

                # Exit the loop once the table is found
                break
        else:
            print("Target table not found on the page.")
    else:
        print("No tables found on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)