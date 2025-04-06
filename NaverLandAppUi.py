from collector import NaverLandCrawler
from naver_land_complex_finder import NaverLandComplexFinder
from naver_land_keyword_searcher import NaverLandKeywordSearcher

class NaverLandCLI:
    def __init__(self):
        self.searcher = NaverLandKeywordSearcher()
        self.complex_finder = NaverLandComplexFinder()
        self.crawler = NaverLandCrawler()

    def run(self):
        while True:
            print("\n=== 네이버 부동산 매물 검색기 ===")
            keyword = input("검색어를 입력하세요 (종료: q): ").strip()
            
            if keyword.lower() == 'q':
                break
                
            if not keyword:
                print("검색어를 입력해주세요.")
                continue
                
            try:
                # 1. 키워드로 아파트 검색
                results = self.searcher.search(keyword)
                
                if not results:
                    print("검색 결과가 없습니다.")
                    continue
                
                # 검색 결과 출력
                print("\n=== 검색 결과 ===")
                for idx, result in enumerate(results, 1):
                    print(f"[{idx}] {result}")
                
                # 2. 결과 중에서 선택
                while True:
                    try:
                        choice = input("\n매물을 조회할 아파트 번호를 선택하세요 (이전: b): ").strip()
                        
                        if choice.lower() == 'b':
                            break
                            
                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(results):
                            selected = results[choice_idx]
                            
                            # ComplexId 찾기
                            complex_id = self.complex_finder.find_complex_id(selected)
                            if not complex_id:
                                print("매물 정보를 찾을 수 없습니다.")
                                continue
                                
                            # 매물 정보 가져오기
                            print(f"complexId {complex_id}")
                            articles = self.crawler.get_complex_articles(complex_id)['articleList']
                            
                            print(f"\n=== {selected} 매물 정보 ===")
                            if not articles:
                                print("매물이 없습니다.")
                            else:
                                for idx, article in enumerate(articles, 1):
                                    print(f"\n[매물 {idx}]")
                                    print(article)
                            
                            input("\n계속하려면 Enter를 누르세요...")
                            break
                            
                        else:
                            print("올바른 번호를 입력해주세요.")
                            
                    except ValueError:
                        print("숫자를 입력해주세요.")
                    except Exception as e:
                        print(f"오류 발생: {str(e)}")
                        break
                        
            except Exception as e:
                print(f"검색 중 오류 발생: {str(e)}")

def main():
    app = NaverLandCLI()
    app.run()

if __name__ == "__main__":
    main()