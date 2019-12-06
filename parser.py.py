import csv
import xml.etree.ElementTree as ET


def get_abst_title(parse_file):
    tree = ET.parse(parse_file)
    root = tree.getroot()
    titles = []
    for item in root.findall("./PubmedArticle/MedlineCitation/Article"):
        title_parse = item.find("ArticleTitle").text
        titles.append(title_parse)
        print(title_parse)
    return(titles)


def pub_det(parse_file):
    tree = ET.parse(parse_file)
    root = tree.getroot()
    for item in root.findall("./PubmedArticle"):
        title_prase = item.find("MedlineCitation/Article/ArticleTitle").text
        print("Title: ", title_prase)
        journal_name = item.find("MedlineCitation/Article/Journal/Title").text
        print("Journal: ", journal_name)
        pub_date = item.find("MedlineCitation/DateRevised")
        print("Published Date: ",
              pub_date.find("Day").text, "/",
              pub_date.find("Month").text, "/",
              pub_date.find("Year").text)
        authors = item.find("MedlineCitation/Article/AuthorList")
        print("Authors: ")
        for author in authors:
            if author.attrib['ValidYN'] == "Y":
                print(author.find("Initials").text,
                      author.find("ForeName").text,
                      author.find("LastName").text)

        citations = item.find("PubmedData/ReferenceList")
        if citations is None:
            print("Citations: 0")
        else:
            print("Citations: ", len(citations))


def key_det(parse_file):
    tree = ET.parse(parse_file)
    root = tree.getroot()
    for item in root.findall("./PubmedArticle"):
        title_prase = item.find("MedlineCitation/Article/ArticleTitle").text
        print("Title: ", title_prase)
        keywords = item.find("MedlineCitation/KeywordList")
        print("keywords: ")
        if keywords is None:
            print("No keywords for this article")
        else:
            for keys in keywords.findall('Keyword'):
                print(keys.text)


def abst_str(parse_file):
    tree = ET.parse(parse_file)
    root = tree.getroot()
    for item in root.findall("./PubmedArticle/MedlineCitation/Article"):
        title_prase = item.find("ArticleTitle").text
        print("Title: ", title_prase)
        abst = item.find("Abstract")
        if abst is None:
            print("No Abstract")
            continue
        if abst.find("AbstractText") is None:
            print("No Abstract")
        else:
            if not abst.find("AbstractText").attrib.keys():
                print("Abstract Type: Unstructured Abstract")
            else:
                print("Abstract Type: Structured Abstract")
                for label in abst.iter("AbstractText"):
                    try:
                        print(label.attrib['Label'])
                    except KeyError:
                        print("part of abstract with diff structure")
                        for child in label:
                            print(child.tag, child.attrib)


def to_csv(parse_file, csv_file='sample.csv'):
    tree = ET.parse(parse_file)
    root = tree.getroot()
    fields = ['Abstract_ID', "Abstract_Title",
              "Authors", "Journal",
              "Year_of_Publication", "Number_of_Citations",
              "Structured(y/n)", "Structure_labels", "Text"]
    total_data = []
    for item in root.findall("./PubmedArticle"):
        complete_data = {}
        art_id = item.find("MedlineCitation/PMID").text
        complete_data[fields[0]] = art_id
        title_prase = item.find("MedlineCitation/Article/ArticleTitle").text
        print("Title: ", title_prase)
        complete_data[fields[1]] = title_prase
        journal_name = item.find("MedlineCitation/Article/Journal/Title").text
        print("Journal: ", journal_name)
        complete_data[fields[3]] = journal_name
        pub_date = item.find("MedlineCitation/DateRevised")
        print("Published Date: ",
              pub_date.find("Day").text, "/",
              pub_date.find("Month").text, "/",
              pub_date.find("Year").text)
        pub_date_txt = pub_date.find("Day").text + "/" + pub_date.find("Month").text + "/" + pub_date.find("Year").text
        complete_data[fields[4]] = pub_date_txt
        authors = item.find("MedlineCitation/Article/AuthorList")
        print("Authors: ")
        auth_list = []
        for author in authors:
            if author.attrib['ValidYN'] == "Y":
                print(author.find("Initials").text,
                      author.find("ForeName").text,
                      author.find("LastName").text)
                auth_list.append(author.find("Initials").text + " " +
                                 author.find("ForeName").text + " " +
                                 author.find("LastName").text)
        complete_data[fields[2]] = auth_list
        citations = item.find("PubmedData/ReferenceList")
        cite_num = 0
        if citations is None:
            print("Citations: 0")
        else:
            print("Citations: ", len(citations))
            cite_num = len(citations)
        complete_data[fields[5]] = cite_num
        keywords = item.find("MedlineCitation/KeywordList")
        print("keywords: ")
        if keywords is None:
            print("No keywords for this article")
        else:
            for keys in keywords.findall('Keyword'):
                print(keys.text)
        abst = item.find("MedlineCitation/Article/Abstract")
        if abst is None:
            print("No Abstract")
            total_data.append(complete_data)
            continue
        if abst.find("AbstractText") is None:
            print("No Abstract")
        else:
            if not abst.find("AbstractText").attrib.keys():
                print("Abstract Type: Unstructured Abstract")
                complete_data[fields[6]] = False
                complete_data[fields[8]] = abst.find("AbstractText").text
            else:
                print("Abstract Type: Structured Abstract")
                complete_data[fields[6]] = True
                complete_data[fields[8]] = abst.find("AbstractText").text
                labs = []
                for label in abst.iter("AbstractText"):
                    try:
                        print(label.attrib['Label'])
                        labs.append(label.attrib['Label'])
                    except KeyError:
                        print("part of abstract with diff structure")
                        for child in label:
                            print(child.tag, child.attrib)
                complete_data[fields[7]] = labs
        total_data.append(complete_data)
        print(complete_data)
    print(total_data)
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(total_data)


if __name__ == '__main__':
    to_csv("example.xml")
