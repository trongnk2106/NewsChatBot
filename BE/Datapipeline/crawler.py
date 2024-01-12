import argparse
import tqdm
from utils import get_urls_of_type, write_content
import json
from datetime import datetime, timedelta
article_type_dict = {
    0: "thoi-su",
    1: "the-gioi",
    2: "kinh-doanh",
    3: "bat-dong-san",
    4: "khoa-hoc",
    5: "giai-tri",
    6: "the-thao",
    7: "phap-luat",
    8: "giao-duc",
    9: "suc-khoe",
    10: "doi-song"
}

def crawl_urls(urls):
    index_len = len(str(len(urls)))
           
    contents = []
    with tqdm.tqdm(total=len(urls)) as pbar:
        for i, url in enumerate(urls):
            file_index = str(i+1).zfill(index_len)
            output_fpath = "".join(["/url_", file_index, ".txt"])
            content = write_content(url)
            # print(content)
            if not content:
                print(url)
            else:
                
                date_url = content["date"].split(",")[1].strip()
                format_data = "%d/%m/%Y"
                date_url = datetime.strptime(date_url, format_data).strftime('%d/%m/%Y')

                
                if datetime.now().strftime('%d/%m/%Y') > date_url:
                    # print('here asdfjksa jasj fkjask f')
                    break
                contents.append(content)
            pbar.update(1)
    #contents = list({"title":title,"date":date,"description":description,"paragraphs":list(paragraphs)})
    return contents

def run(article_type=4, total_pages=1):

    return crawl_urls(get_urls_of_type(article_type, total_pages))

def crawler_main():
    data_date = []
    for i in range(0,11):
        print("-"*15)
        print(article_type_dict[i])
        print("-"*15)
        a = run(article_type=i, total_pages=5)
        data_date.append(a)
    return data_date


# data = crawler_main()
# print(len(data))

# if __name__ == "__main__":
#     data_date = []
#     for i in range(0,11):
#         print("-"*15)
#         print(article_type_dict[i])
#         print("-"*15)
#         a = main(article_type=i, total_pages=5)
#         data_date.append(a)
        
#     print(data_date[0])
#         with open(f'vnexpress\\vnexpress_{article_type_dict[i]}.jsonl', 'w', encoding='utf-8') as json_file:
#             for i in a:
#                 json.dump(i, json_file, ensure_ascii=False)
#                 json_file.write('\n')
'''
article_type_dict = {
    0: "thoi-su",
    1: "the-gioi",
    2: "kinh-doanh",
    3: "bat-dong-san",
    4: "khoa-hoc",
    5: "giai-tri",
    6: "the-thao",
    7: "phap-luat",
    8: "giao-duc",
    9: "suc-khoe",
    10: "doi-song"
}
'''