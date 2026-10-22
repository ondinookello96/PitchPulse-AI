import asyncio
import os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient

load_dotenv()

# Custom credential class to satisfy agent_framework's .get_token() requirement using your API key
class SimpleApiCredential:
    def __init__(self, api_key: str):
        self._api_key = api_key

    def get_token(self, *scopes, **kwargs):
        # Return a dummy access token object with the API key
        class Token:
            def __init__(self, token):
                self.token = token
                self.expires_on = 32503680000  # Far future timestamp
        return Token(self._api_key)

async def main():
    # Pass our custom credential object
    credential = SimpleApiCredential(os.environ["AZURE_OPENAI_API_KEY"])
    
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=credential
    )

    test_agent = Agent(
        name="ScoutAgent",
        client=client,
        instructions="You are a Premier League tactical analyst. Reply in one punchy sentence."
    )

    response = await test_agent.run("Arsenal just inverted their left-back into central midfield at minute 60. What does this create?")
    print("\n--- Response from Microsoft Foundry ---")
    print(response.text)

if __name__ == "__main__":
    asyncio.run(main())