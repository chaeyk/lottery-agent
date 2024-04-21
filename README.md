# 간단설명

로또와 연금복권을 커맨드라인으로 구매할 수 있다.

# PC에서 개발/실행하기

## 준비

```bash
pip3 install -r requirements.txt
```

.env.sample 파일을 .env 로 복사하고 DHL_USERID, DHL_PASSWORD를 본인 계정으로 설정한다.

## 실행

```bash
python3 main.py [-h] [--lo40 n] [--lp72 n] [--dryrun/--no-dryrun] [--headless/--no-headless] {buy,check}
```

* -h : 도움말
* --lo40 : 로또 구매 수량
* --lp72 : 연금복권 구매 수량
* --dryrun : 구매 직전까지만 실행하고 멈춘다
* --headless : 브라우저를 화면에 보여주지 않은 상태로 실행한다
* buy : 구매
* check : 당첨 결과 조회
