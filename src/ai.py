from provider import error


class AI:
    def __init__(self, prompt: str) -> None:
        self.prompt: str = prompt

    def GetFromOpenAI(self, api_key: str) -> str:
        from provider import openai

        return openai.GetResponse(self.prompt, api_key)

    def GetFromGenAI(self, api_key: str) -> str:
        from provider import genai

        return genai.GetResponse(self.prompt, api_key)

    def GetFromGroq(self, api_key: str) -> str:
        from provider import groq

        return groq.GetResponse(self.prompt, api_key)

    def GetFromAnthropic(self, api_key: str) -> str:
        from provider import anthropic

        return anthropic.GetResponse(self.prompt, api_key)

    def GetFromOpenRouter(self, api_key: str) -> str:
        from provider import openrouter

        return openrouter.GetResponse(self.prompt, api_key)


AIError = error.AIError
