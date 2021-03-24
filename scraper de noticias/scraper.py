import requests
import lxml.html as html
import os
import datetime
import pandas as pd


HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//a[@class="economiaSect"]/@href' 
XPATH_TITLE = '//*[@id="vue-container"]/div[2]/div[1]/div[1]/div/div[2]/h2/a/text()'
XPATH_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_BODY ='//div[@class="html-content"]/p/text()'


def parse_notice(link, df, today, i):
    # verify that the link works
    # parse the html structure
    # save the data we want in a csv file
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)

            try:
                # I had trouble getting the title so I used your link and trimmed it a bit
                title = link.replace("https://www.larepublica.co/economia/", "").replace("-", " ") 
                summary = parsed.xpath(XPATH_SUMMARY)[0]
                body = parsed.xpath(XPATH_BODY)

                # Para convertirlo en un string
                data_body = "".join(body)   

                df.iloc[i] = (title, summary, data_body)
                df.to_csv("{}/News.csv".format(today))
                

            except IndexError:
                print("Index Error")
                return
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def parse_home():
    # in charge that the main page loads
    # parsing the HTML structure
    # take the links we want from the page,
    # create a folder that has the name of the current day and finally iterate through each link
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)
            today = datetime.date.today().strftime('%d-%m-%Y')

            # limit is 9 News
            df = pd.DataFrame(columns=['Title', 'Summary', 'Body'], index=range(10))
            i = 0
            if not os.path.isdir(today):
                os.mkdir(today)
            
            for link in links_to_notices:
                parse_notice(link, df, today, i)
                i = i + 1 

        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve)


def run():
    parse_home()
    

if __name__ == "__main__":
    run()