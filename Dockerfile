FROM python:3.11-slim

# 컨테이너 안에서의 작업 디렉토리
WORKDIR /app

# 의존성 먼저 복사(캐시 활용), 뒤에 "." 표시는 현재 폴더인 /app 
COPY requirements.txt .

# 컨테이너 안에서 pip을 실행하는 단계 nocachedir은 pip 다운로드 캐시를 남기지 말라는 뜻
RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
# 내 프로젝트의 src폴더를 컨테이너 /app/src 로 복사
# “현재는 데모용 목적으로 모델을 이미지에 포함했으며, 실제 환경에서는 S3 등 외부 스토리지에서 로드하도록 확장 가능하다”
COPY src/ src/
COPY models/ models/

# 포트 설정 메타 정보
EXPOSE 8000

#실행명령
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]

