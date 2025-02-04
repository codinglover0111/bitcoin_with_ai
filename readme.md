# 주의!!!!

이 프로그램은 절대로 수익을 절대로 보장 못합니다.
투자는 여러분의 선택입니다!


## 실행법

env에 환경변수를 넣고 나서 docker를 설치한 다음 아래 명령어를 실행합니다.

```
touch trading.log;docker run -d \
  --name trading-bot \
  --restart unless-stopped \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/trading.log:/app/trading.log \
  trading-bot
```

## TODO
- 웹 사이트 UI를 통해 상태 확인
- MYSQL 또는 xlsx를 통해 거래 내역을 저장하게 해야함
- 거래를 통하여 얼마나 이익을 봤는 지 통계를 내주는 기능
- 레버리지를 코딩으로 선택하는 기능
- 프롬프트를 마크다운을 통해 입력할수있게 함
