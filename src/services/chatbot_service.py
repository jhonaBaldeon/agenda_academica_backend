import os
from openai import OpenAI
from typing import List, Dict
from ..schemas.chatbot_schema import ChatMessage


class ChatbotService:
    def __init__(self):
        self.token = os.environ.get("GITHUB_TOKEN", "")
        if not self.token:
            raise ValueError("GITHUB_TOKEN environment variable is not set")
        self.endpoint = "https://models.github.ai/inference"
        self.model = "openai/gpt-4.1"

        self.client = OpenAI(
            base_url=self.endpoint,
            api_key=self.token,
        )

        self.system_prompt = """Eres un asistente académico útil para la Agenda Académica. 
Ayudas a padres, docentes y estudiantes con información sobre:
- Cursos y actividades académicas
- Seguimiento de tareas y tareas pendientes
- Rendimiento académico
- Información sobre el progreso de los alumnos

Sé amable, profesional y proporciona información clara y concisa."""

    def chat(self, message: str, history: List[ChatMessage] = None) -> str:
        messages = [
            {
                "role": "system",
                "content": self.system_prompt,
            }
        ]

        if history:
            for msg in history:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                messages=messages, temperature=1.0, top_p=1.0, model=self.model
            )

            return response.choices[0].message.content
        except Exception as e:
            return f"Lo siento, hubo un error al procesar tu solicitud: {str(e)}"


chatbot_service = ChatbotService()


def get_chatbot_service() -> ChatbotService:
    return chatbot_service
