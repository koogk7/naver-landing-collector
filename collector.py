import json
import requests
from datetime import datetime
import time
import pandas as pd

class NaverLandCrawler:
    def __init__(self):
        # 기본 헤더 설정 - 최소한의 필수 헤더만 유지
        self.headers = {
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IlJFQUxFU1RBVEUiLCJpYXQiOjE3NDM5MTkxNDgsImV4cCI6MTc0MzkyOTk0OH0.YicQ6aMVNFj7XZRmQNzgEDe9iYFY5NlSizXtgTSyxlU',
            'referer': f'https://new.land.naver.com/complexes',
            'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
        }
        
        # 기본 쿠키 설정 - 모든 쿠키 유지
        self.cookies = {
            'NNB': 'RKPVCOURWP7GI',
            '_ga_6Z6DP60WFK': 'GS1.2.1713770041.3.0.1713770041.60.0.0',
            'ASID': '753493040000019108b25d8900000050',
            '_ga_451MFZ9CFM': 'GS1.1.1728458076.5.0.1728458079.0.0.0',
            '_ga_ZGQY5GH55D': 'GS1.1.1729060969.4.0.1729060969.0.0.0',
            '_ga': 'GA1.2.1171424670.1688221582',
            '_ga_TSE3G32LNF': 'GS1.2.1733316886.1.1.1733316896.0.0.0',
            '_fwb': '121CubBGkypFZ4Nx8HIUz7I.1733660682483',
            'NAC': 'mcfdC4A8beZbD',
            '_fwb': '2113B9NvUyQWnIsPHiqc9FM.1738307893948',
            'nstore_session': 'y3njDD885DYFLk1OgqJU5xOB',
            'nstore_pagesession': 'iJOKIwqrvVgr8wsMLf0-222607',
            'nid_inf': '1916934630',
            'NID_JKL': 'BN9cqDucJiXic+XRUV3kOzNxVf8aKl8PGgrvOeay+lI=',
            'NACT': '1',
            'SRT30': '1743919128',
            'SRT5': '1743919128',
            '_naver_usersession_': '5tjWM3V75b9ksLc9GEt3lg==',
            'nhn.realestate.article.rlet_type_cd': 'A01',
            'nhn.realestate.article.trade_type_cd': '""',
            'nhn.realestate.article.ipaddress_city': '1100000000',
            'page_uid': 'i/4hbwqVOsCssFvPESCssssss8V-352109',
            'landHomeFlashUseYn': 'Y',
            'REALESTATE': 'Sun%20Apr%2006%202025%2014%3A59%3A11%20GMT%2B0900%20(Korean%20Standard%20Time)',
            'BUC': 'CYjIlmUqpN9ofrwkh_j2d2sP3mBUSML4GUOHfzMQ2f8=',
        }

    def get_complex_articles(self, complex_no, page=1):
        """아파트 단지의 매물 정보를 가져옵니다."""
        url = f'https://new.land.naver.com/api/articles/complex/{complex_no}'
        
        # 파라미터 설정
        params = {
            'realEstateType': 'APT:ABYG:JGC:PRE',
            'tradeType': '',
            'tag': '::::::::',
            'rentPriceMin': '0',
            'rentPriceMax': '900000000',
            'priceMin': '0',
            'priceMax': '900000000',
            'areaMin': '0',
            'areaMax': '900000000',
            # 빈 값은 파라미터 키만 전달
            'oldBuildYears': None,
            'recentlyBuildYears': None,
            'minHouseHoldCount': None,
            'maxHouseHoldCount': None,
            'showArticle': 'false',
            'sameAddressGroup': 'true',
            'minMaintenanceCost': None,
            'maxMaintenanceCost': None,
            'priceType': 'RETAIL',
            'directions': '',
            'page': page,
            'complexNo': complex_no,
            'buildingNos': '',
            'areaNos': '',
            'type': 'list',
            'order': 'rank'
        }

        try:
            # None 값을 가진 파라미터는 키만 전달되도록 처리
            params = {k: v for k, v in params.items() if v is not None}
            
            response = requests.get(
                url,
                headers=self.headers,
                cookies=self.cookies,
                params=params,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"에러 발생: {response.status_code}")
                print(f"응답 내용: {response.text[:500]}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"요청 중 에러 발생: {e}")
            return None

    def parse_articles(self, data):
        """매물 정보를 파싱하여 DataFrame으로 변환합니다."""
        if not data or 'articleList' not in data:
            print("파싱할 데이터가 없습니다.")
            return pd.DataFrame()

        articles = []
        for article in data['articleList']:
            parsed_article = {
                '매물번호': article['articleNo'],
                '아파트명': article['articleName'],
                '거래유형': article['tradeTypeName'],
                '층정보': article['floorInfo'],
                '가격': article['dealOrWarrantPrc'],
                '면적': f"{article['area2']}㎡",
                '방향': article['direction'],
                '확인일자': article['articleConfirmYmd'],
                '특징': article['articleFeatureDesc'],
                '태그': ', '.join(article.get('tagList', [])),
                '동': article['buildingName'],
                '중개사무소': article['realtorName']
            }
            articles.append(parsed_article)
            
        return pd.DataFrame(articles)

    def save_to_excel(self, df, complex_no):
        """수집한 데이터를 엑셀 파일로 저장합니다."""
        if df.empty:
            print("저장할 데이터가 없습니다.")
            return

        current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'naver_land_{complex_no}_{current_time}.xlsx'
        df.to_excel(filename, index=False)
        print(f"데이터가 {filename}에 저장되었습니다.")

def main():
    try:
        crawler = NaverLandCrawler()
        
        # 아파트 단지 번호 입력
        complex_no = input("아파트 단지 번호를 입력하세요 (예: 824는 상봉 한신아파트): ")
        
        # 데이터 수집
        print(f"\n{complex_no} 단지의 매물 정보를 수집중입니다...")
        data = crawler.get_complex_articles(complex_no)
        
        if data:
            # 데이터 파싱
            df = crawler.parse_articles(data)
            
            if not df.empty:
                # 엑셀 파일로 저장
                crawler.save_to_excel(df, complex_no)
                
                # 결과 출력
                print("\n수집된 매물 정보:")
                print(f"총 {len(df)}개의 매물이 수집되었습니다.")
                print("\n첫 5개 매물 미리보기:")
                print(df.head())
            else:
                print("수집된 매물이 없습니다.")
        else:
            print("데이터 수집에 실패했습니다.")
            
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")

if __name__ == "__main__":
    main()
