import requests
from urllib.parse import quote

class NaverLandComplexFinder:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Whale/3.26.244.21 Safari/537.36'
        }

    def find_complex_id(self, keyword):
        """
        아파트 이름으로 단지 ID를 찾습니다.
        
        Args:
            keyword (str): 아파트 이름 (예: "창신쌍용2단지")
            
        Returns:
            str: 단지 ID 또는 None (찾지 못한 경우)
        """
        try:
            # 키워드 URL 인코딩
            encoded_keyword = quote(keyword)
            search_url = f'https://m.land.naver.com/search/result/{encoded_keyword}'
            
            # 첫 번째 요청 - 리다이렉트 URL 얻기
            response = requests.head(
                search_url,
                headers=self.headers,
                allow_redirects=False
            )
            
            if response.status_code == 302:
                # 리다이렉트 URL에서 complex ID 추출
                location = response.headers.get('location', '')
                if 'complex/info/' in location:
                    complex_id = location.split('complex/info/')[1].split('?')[0]
                    return complex_id
                    
            print(f"단지 ID를 찾을 수 없습니다. 키워드: {keyword}")
            return None
            
        except Exception as e:
            print(f"에러 발생: {e}")
            return None

def main():
    finder = NaverLandComplexFinder()
    
    # 테스트
    keywords = [
        "중화동 한신"
    ]
    
    for keyword in keywords:
        print(f"\n{keyword} 검색 중...")
        complex_id = finder.find_complex_id(keyword)
        
        if complex_id:
            print(f"단지 ID: {complex_id}")
        else:
            print("단지 ID를 찾을 수 없습니다.")

if __name__ == "__main__":
    main()