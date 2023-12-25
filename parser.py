import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from datetime import datetime

def main():
    URL_TEMPLATE = "https://tsumego-hero.com/users/leaderboard"
    r = requests.get(URL_TEMPLATE)
    print()
    if(r.status_code == 200):
        df = pd.DataFrame() 
        df['Name'] = ""
        df['Score'] = 0
        df['XP'] = 0


        data_line = bs(r.text, "html.parser")
        data_line = data_line.find("table", class_="dailyHighscoreTable")
        data_line = data_line.find_all("tr")
        for row in data_line:
            row_data = []
            td = row.find_all("td")
            b = row.find_all("b")
            
            score = td[2].text.replace('\t', '').replace('\r', '').replace('\n', '')
            score = score[:score.index(' ')]
            xp = b[2].text
            xp = xp[:xp.index(' ')]

            row_data = [int(b[0].text), b[1].text, int(score), int(xp)]    
            
            df = df.append(pd.Series(data=row_data[1:], index=df.columns, name=row_data[0]))
        print(df)
        time = datetime.now().strftime("%d.%m.%Y %H.%M.%S")
        file_name = f"data/{time}.csv"
        df.to_csv(file_name)
    return


if __name__ == "__main__":
    main()