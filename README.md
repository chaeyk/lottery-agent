# 간단설명

로또와 연금복권을 커맨드라인으로 구매할 수 있다.

# PC에서 개발/실행하기

## 준비

```bash
pip3 install -r requirements.txt
```

.env.sample 파일을 .env 로 복사하고 본인 계정을 세팅한다.

* DHL_USERID : 동행복권 계정
* DHL_PASSWORD : 동행복권 비밀번호
* TLG_BOTTOKEN : 텔레그램 봇 토큰
* TLG_CHATID : 텔레그램 메시지 수신 아이디

텔레그램 세팅은 안해도 된다. 세팅하고 싶다면 [여기](https://www.keywordontop.com/%EA%B5%AC%EA%B8%80seo/%ED%85%94%EB%A0%88%EA%B7%B8%EB%9E%A8-%EB%B4%87/)를 참고.

## 실행

### 구매
```bash
python3 main.py [--headless/--no-headless] buy [-h] [--lo40 n] [--lp72 n] [--dryrun/--no-dryrun]
```

* --headless : 브라우저를 화면에 보여주지 않은 상태로 실행한다
* -h : 도움말
* --lo40 : 로또 구매 수량
* --lp72 : 연금복권 구매 수량
* --dryrun : 구매 직전까지만 실행하고 멈춘다

### 당첨 확인
```bash
python3 main.py [--headless/--no-headless] check {lo40,lp72}
```

* --headless : 브라우저를 화면에 보여주지 않은 상태로 실행한다
* -h : 도움말
* lo40 : 로또 6/45
* lp72 : 연금복권 720+
