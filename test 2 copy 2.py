import requests

def generate_text(prompt, api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": "gpt-4",
        "prompt": prompt,
        "temperature": 0.7,
        "max_tokens": 150
    }

    try:
        response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=data)
        response.raise_for_status()  # HTTP 에러 발생 시 예외를 발생시킵니다.
        answer = response.json().get('choices', [])[0].get('text')
        print(answer)
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # 예: 404 클라이언트 에러 또는 500 서버 에러 응답
    except Exception as err:
        print(f'An error occurred: {err}')

# 예제 사용 (API 키를 유효한 값으로 교체하세요)
generate_text("중력에 대해 알려줘", "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")
