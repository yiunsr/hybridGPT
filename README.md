
# hybridGPT
* [nanoGPT](https://github.com/karpathy/nanoGPT)를 여러가지 방법으로 구조를 변경하면서 테스트 하는 프로젝트 입니다.

## 말뭉치
* 한국어 위키피디아 데이터
* 청와대 국민청원 데이터 아카이브
  * https://github.com/lovit/petitions_archive

* https://github.com/yiunsr/boddari
  * 위키뉴스
    * 크리에이티브 커먼즈 저작자표시 2.5 라이선스(CC-BY)
  * 국회도서관 책 서평
    * https://www.nanet.go.kr/datasearch/commant/selectWeekCommantList.do
    * 크리에이티브 커먼즈 저작자표시 라이선스(CC-BY)
  * 에이콘출판사 블로그
    * http://www.acornpub.co.kr/blog
    * 크리에이티브 커먼즈 코리아 저작자표시 2.0 대한민국 라이센스(CC-BY 2.0 KR)
  * airbnb_review
    * http://insideairbnb.com/get-the-data/
    * 크리에이티브 커먼즈 저작자표시 라이선스(CC-BY)
  * 글로벌 세계 대백과사전
    * https://ko.wikisource.org/wiki/%EA%B8%80%EB%A1%9C%EB%B2%8C_%EC%84%B8%EA%B3%84_%EB%8C%80%EB%B0%B1%EA%B3%BC%EC%82%AC%EC%A0%84
    * GFDL과 CC-BY-SA 3.0
  * 문화체육관광부_정책브리핑_정책뉴스
    * https://www.data.go.kr/data/15092245/fileData.do 
    * 공공누리 [제1유형] 출처표시
  * 문화체육관광부_정책브리핑_보도자료
    * https://www.data.go.kr/data/15092245/fileData.do
    * 공공누리 [제1유형] 출처표시
  * Andersen 단편선 번역
    * 공유마당(https://gongu.copyright.or.kr/gongu/main/main.do)
    * 기증저작물 자유이용
  * 방정환 단편소설
    * 저작권 만료
  * 유네스크 출판물 또는 자료
    * CC-BY-SA 3.0 IGO
  * 제세한 출처는 https://github.com/yiunsr/boddari 에서 확인 가능

## 학습데이터 정리와 인코딩 방법

### prepare01
* 문장 필터링
  * prepare01\tokenizer.py 에 코드 존재함
  * 한글, 숫자, 영대문자, 몇가지 문장기호를 포함하는 경우에만 수집한다.
  * 소괄호("(", ")")가 들어가는 경우 해당 부분을 제거한다.
  * 자주사용하는 종결형 어미로 문장이 종료되는 경우만 수집한다.
  * 한 line 당 2개 이상의 문장이 있고 300글자 이상일 때만 수지한다.
* 인코딩
  * 수집된 문장들에 대해 [kiwipiepy](https://github.com/bab2min/kiwipiepy) 형태소 분석기를 이용해 형태소로 분리한다.
  * BertWordPieceTokenizer
  * 
  ```
  좋은 글은 어떻게 써야 하는가를 알기 위해서는 우선 문장이란 무엇인가 하는 것부터 생각해 보아야 할 것이다. 
  =>
  좋/VA + 은/ETM + 글/NNG + 은/JX + 어떻/VA + 게/EC + 쓰/VV + 어야/EC + 하/VX + 는가/EC + 를/JKO + 알/VV + 기/ETN + 위하/VV + 어서/EC + 는/JX + 우선/MAG + 문장/NNG + 이란/JX + 무엇/NP + 이/VCP + ᆫ가/EC + 하/VV + 는/ETM + 것/NNB + 부터/JX + 생각/NNG + 하/XSV + 어/EC + 보/VX + 어야/EC + 하/VX + ᆯ/ETM + 것/NNB + 이/VCP + 다/EF + ./SF 
  =>
  좋 은 글 은 어떻 게 쓰 어야 하 는가 를 알 기 위하 어서 는 우선 문장 이란 무엇 이 ᆫ가 하 는 것 부터 생각 하 어 보 어야 하 ᆯ 것 이 다 .
  ```