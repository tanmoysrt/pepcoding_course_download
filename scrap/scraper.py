#!/usr/bin/env python
# coding: utf-8


from bs4 import BeautifulSoup
import pandas as pd

def scrap_And_save(html_filename,output_csv_filename):
    content = ""
    df = pd.DataFrame(columns=["title","url"])
    with open(f"./{html_filename}","r") as file:
        content = file.read()
    soup = BeautifulSoup(content,features="lxml")
    lists =  soup.find_all("li",attrs={"class":"searchRow"})
    for i in lists[::-1]:
        df=df.append({"title":str(i.find("a").text).strip(),"url":str(i.find("a",href=True)['href'])},ignore_index=True)
    print(f"Total Record : {df.shape[0]}")
    df.to_csv(output_csv_filename,index=False)


if __name__ == "__main__":
    input_file = input("Enter the filname of input file : ")
    output_file = input("Enter the filename of output csv file : ")
    scrap_And_save(input_file,output_file)





