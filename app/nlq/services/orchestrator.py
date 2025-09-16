import requests
from django.conf import settings
from app.connections.models import Connection
from app.schema_registry.models import SchemaCache
from app.queries.models import PromptExample

class LLMOrchestrator:
    """
    This service constructs the prompt for the LLM and calls the provider.
    """
    def __init__(self, connection: Connection, prompt: str):
        self.connection = connection
        self.prompt = prompt
        self.schema_cache = self._get_schema_cache()
        self.few_shot_examples = self._get_few_shot_examples()

    def _get_schema_cache(self):
        try:
            return SchemaCache.objects.get(connection=self.connection)
        except SchemaCache.DoesNotExist:
            # In a real app, we might trigger introspection here or raise an error.
            # For now, we'll proceed with an empty schema.
            return None

    def _get_few_shot_examples(self):
        return PromptExample.objects.filter(connection=self.connection)

    def _build_system_prompt(self) -> str:
        """
        Constructs the detailed system prompt for the LLM.
        """
        dialect = self.connection.get_driver_display()

        system_prompt = f"You are an expert {dialect} data analyst. Your task is to write a single, safe, read-only SQL SELECT statement to answer the user's question.\n"
        system_prompt += "Do not produce any explanation, only the SQL query.\n"

        if self.schema_cache:
            system_prompt += "\n--- Database Schema ---\n"
            # In a real implementation, we would be more intelligent about which tables/columns to include
            # based on the user's prompt (e.g., using embeddings). For now, we include everything.
            for table in self.schema_cache.payload_json.get('tables', []):
                table_name = table.get('name')
                columns = ", ".join([col.get('name') for col in table.get('columns', [])])
                system_prompt += f"Table {table_name}: ({columns})\n"

        if self.few_shot_examples.exists():
            system_prompt += "\n--- Examples ---\n"
            for example in self.few_shot_examples:
                system_prompt += f"Question: {example.question}\nSQL: {example.sql}\n"

        return system_prompt

    def generate_sql(self) -> str:
        """
        Calls the external LLM provider to generate the SQL.
        """
        system_prompt = self._build_system_prompt()

        # This is a placeholder for a real API call.
        # In a real app, you would use a library like `requests` or the provider's SDK.
        llm_url = settings.LLM_PROVIDER_URL
        api_key = settings.LLM_API_KEY

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "gpt-4-turbo", # This would be configurable
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.0,
        }

        # MOCK RESPONSE - In a real scenario, we would make the request.
        # try:
        #     response = requests.post(llm_url, json=payload, headers=headers, timeout=15)
        #     response.raise_for_status()
        #     return response.json()['choices'][0]['message']['content']
        # except requests.RequestException as e:
        #     # Handle API errors
        #     return f"Error: Could not connect to LLM provider. {e}"

        # For now, return a mock SQL statement for testing purposes.
        return "SELECT id, name, email FROM users WHERE email LIKE '%@example.com%';"
