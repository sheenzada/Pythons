from openai import OpenAI

class CoffeeAI:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def recommend_coffee(self, mood, weather):
        prompt = f"""
        User mood: {mood}
        Weather: {weather}

        Recommend one coffee drink with:
        - drink name
        - short reason
        - estimated price
        """

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional coffee expert."},
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content