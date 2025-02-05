from google.ai.generativelanguage_v1beta.types import content
import google.generativeai as genai
import json

class make_to_object():
    def __init__(self):
        generation_config = {
        "temperature": 0,
        "top_p": 0.0,
        "top_k": 40,
        "max_output_tokens": 400,
        "response_schema": content.Schema(
            type = content.Type.OBJECT,
            required = ["Status","tp","sl","price","buy_now","stop_order"],
            properties = {
            "Status": content.Schema(
                type = content.Type.STRING,
                description="관망(Watch and Wait)의 경우 hold,포지션 청산의 경우 stop,매수는 buy(long),매도는 sell(short)입니다.",
                enum = ["hold", "sell", "buy","stop"]
            ),
            "tp": content.Schema(
                type = content.Type.NUMBER,
            ),
            "sl": content.Schema(
                type = content.Type.NUMBER,
            ),
            "price": content.Schema(
                type = content.Type.NUMBER,
            ),
            "buy_now": content.Schema(
                description="시장가로 즉시 구매 해야하는 경우 True를 반환합니다.",
                type = content.Type.BOOLEAN,
            ),
            "stop_order": content.Schema(
                description="포지션 청산의 경우 True를 반환합니다.",
                type = content.Type.BOOLEAN,
            ),
            },
        ),
        "response_mime_type": "application/json",
        }
        self.model = genai.GenerativeModel(
          model_name="gemini-2.0-flash-exp",
          generation_config=generation_config,
          system_instruction="입력된 내용을 천천히 읽어본 다음 롱(Long), 숏(Short), 관망(Watch and Wait), 청산(Stop)인지 꼼꼼히 살펴본 다음에 object로 변환하세요.",
        )
        self.chat_session = self.model.start_chat(
          history=[
          ]
        )
        pass
    
    def make_it_object(self,inputs:str):
        response = self.chat_session.send_message(inputs)
        dict = json.loads(response.text)
        return dict
    
    
if __name__ == '__main__':
    test = make_to_object()
    value = test.make_it_object("""<Result>
    Watch and wait.
    Hold the current sell position.
    Current position is profitable and moving towards TP.
    Will watch the price action and wait to see if it reaches the Take Profit level of 2.5.
    </Result>""")
    print(value)