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
                description="If you decide to Watch and wait, use the hold. sell if you are short if long. buy If you want to close the position, write stop.",
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
                description="Returns true if the position should be opened immediately, like buy at market price.",
                type = content.Type.BOOLEAN,
            ),
            "stop_order": content.Schema(
                description="Returns true if the position should be closed.",
                type = content.Type.BOOLEAN,
            ),
            },
        ),
        "response_mime_type": "application/json",
        }
        self.model = genai.GenerativeModel(
          model_name="gemini-2.0-flash-exp",
          generation_config=generation_config,
          system_instruction="In the <result> tag, write how you want to go long, short, watch and wait, or close. If there is no applicable value, please write 0.1.",
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