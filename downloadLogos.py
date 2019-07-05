import pandas as pd
import numpy as np
from urllib import parse
import pymysql
import time
from google_images_download import google_images_download

def get_code():
    # class instantiation
    response = google_images_download.googleimagesdownload()

    # 한국 상장된 기업의 리스트
    url = 'kind.krx.co.kr/corpgeneral/corpList.do'
    params = {'method' : 'download'}
    params['searchType'] = 13

    params_string = parse.urlencode(params)
    re_url = parse.urlunsplit(['http', url , '', params_string, ''])
    df = pd.read_html(re_url, header=0)[0]
    df.종목코드 = df.종목코드.map('{:06d}'.format)
    df2 = df.rename(columns = {'회사명':'Coname','종목코드':'crpno','업종':'category','주요제품':'item','상장일':'listedday','결산월':'settlemonth','대표자명':'ceo','홈페이지':'url','지역':'region'})

    for index, row in df2.iterrows() :
        if row['crpno'] == None :
            continue
        coname = row['Coname']
        arguments = { "keywords": coname, "limit": 1, "print_urls": True }
        paths = response.download(arguments)
        print(paths)
        

if __name__ == "__main__":
    get_code()