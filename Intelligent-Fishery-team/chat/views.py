from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from zhipuai import ZhipuAI
import logging

# 配置 zhipuai
client = ZhipuAI(api_key="6d68490c8139243f1db3a23f7e0c0cfc.PEOqiLlL7MSwiRVc")  # 填写您自己的APIKey
model = "glm-4"  # 用于配置大模型版本

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def query(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            question = data['query']
            print(question)

            # 调用 zhipuai API 进行模型推理
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": question},
                ],
            )
            print(response.choices[0].message)

            if response and response.choices:
                completion_message = response.choices[0].message
                answer = completion_message.content if hasattr(completion_message, 'content') else "抱歉，我无法回答您的问题。"
            else:
                answer = "抱歉，我无法回答您的问题。"

            response = JsonResponse({"answer": answer})
            response["Access-Control-Allow-Origin"] = "*"
            return response

        elif request.method == 'OPTIONS':
            response = JsonResponse({"message": "Options request"})
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type"
            return response

    except Exception as e:
        logger.error(f"Error processing request: {e}", exc_info=True)
        response = JsonResponse({"error": str(e)}, status=500)
        response["Access-Control-Allow-Origin"] = "*"
        return response

    return JsonResponse({"error": "Invalid request method"}, status=405)
