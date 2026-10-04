from .provider import anthropic, error, genai, groq, openai, openrouter


class AI:
    def __init__(self, prompt: str) -> None:
        self.prompt: str = prompt

    def GetFromOpenAI(self, api_key: str) -> str:
        return openai.GetResponse(self.prompt, api_key)

    def GetFromGenAI(self, api_key: str) -> str:
        return genai.GetResponse(self.prompt, api_key)

    def GetFromGroq(self, api_key: str) -> str:
        return groq.GetResponse(self.prompt, api_key)

    def GetFromAnthropic(self, api_key: str) -> str:
        return anthropic.GetResponse(self.prompt, api_key)

    def GetFromOpenRouter(self, api_key: str) -> str:
        return openrouter.GetResponse(self.prompt, api_key)


AIError = error.AIError
