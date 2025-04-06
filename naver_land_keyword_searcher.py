import requests
from urllib.parse import quote
import re

class NaverLandKeywordSearcher:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }

    def search(self, keyword):
        """
        키워드로 아파트를 검색합니다.
        
        Args:
            keyword (str): 검색할 키워드
            
        Returns:
            list: 검색된 아파트 이름 목록
        """
        try:
            # 키워드 URL 인코딩
            encoded_keyword = quote(keyword)
            url = f'https://new.land.naver.com/api/autocomplete?keyword={encoded_keyword}'
            
            response = requests.get(url, headers=self.headers)
            print(response.status_code)
            
            if response.status_code == 200:
                # HTML 태그 제거하여 plain text 리스트 반환
                results = response.json()
                clean_results = []
                for result in results:
                    # HTML 태그 제거
                    clean_text = re.sub(r'<[^>]+>', '', result)
                    clean_results.append(clean_text)
                print(f'검색결과={clean_results}')
                return clean_results
            else:
                print(f"검색 실패: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"검색 중 오류 발생: {e}")
            return []

def main():
    searcher = NaverLandKeywordSearcher()
    
    # 테스트할 키워드 목록
    keywords = [
        "중화동 한신",
        "창신쌍용2단지",
        "면목동"
    ]
    
    for keyword in keywords:
        print(f"\n'{keyword}' 검색 결과:")
        results = searcher.search(keyword)
        
        if results:
            for idx, result in enumerate(results, 1):
                print(f"{idx}. {result}")
        else:
            print("검색 결과가 없습니다.")

if __name__ == "__main__":
    main()

