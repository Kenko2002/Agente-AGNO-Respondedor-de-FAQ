import reflex as rx
import requests


class State(rx.State):
    question: str = ""
    loading: bool = False

    messages: list[dict] = [
        {
            "role": "assistant",
            "text": (
                "👋 **Olá! Sou o Assistente Virtual da Universidade.**\n\n"
                "Faça sua pergunta e eu vou tentar te responder da melhor maneira."
            ),
        }
    ]

    def set_question(self, value: str):
        self.question = value

    async def ask(self):
        if self.loading or not self.question.strip():
            return

        pergunta = self.question

        self.messages.append(
            {
                "role": "user",
                "text": pergunta,
            }
        )

        self.question = ""
        self.loading = True

        # Atualiza a tela imediatamente
        yield

        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"text": pergunta},
                timeout=120,
            )

            resposta = response.json().get(
                "answer",
                "Não foi possível obter resposta.",
            )

        except Exception as e:
            resposta = f"Erro: {e}"

        self.messages.append(
            {
                "role": "assistant",
                "text": resposta,
            }
        )

        self.loading = False

        yield


def chat_message(msg):
    return rx.cond(
        msg["role"] == "user",

        rx.hstack(
            rx.spacer(),

            rx.box(
                rx.text(msg["text"]),
                background="#2563EB",
                color="white",
                padding="14px",
                border_radius="16px",
                max_width="75%",
            ),

            width="100%",
            margin_bottom="10px",
        ),

        rx.hstack(

            rx.box(
                rx.markdown(msg["text"]),
                background="white",
                padding="14px",
                border="1px solid #E5E7EB",
                border_radius="16px",
                max_width="75%",
            ),

            rx.spacer(),

            width="100%",
            margin_bottom="10px",
        ),
    )


def index():
    return rx.center(

        rx.box(

            rx.vstack(

                rx.heading(
                    "🎓 Assistente Virtual da Universidade",
                    size="8",
                ),

                rx.text(
                    "Faça perguntas sobre os documentos oficiais da universidade.",
                    color="gray",
                    size="3",
                ),

                rx.box(

                    rx.foreach(
                        State.messages,
                        chat_message,
                    ),

                    rx.cond(
                        State.loading,

                        rx.hstack(
                            rx.spinner(size="3"),
                            rx.text(
                                "Consultando os documentos...",
                                color="gray",
                            ),
                            padding="12px",
                        ),
                    ),

                    width="100%",
                    height="75vh",
                    overflow_y="scroll",
                    background="#F9FAFB",
                    border="1px solid #E5E7EB",
                    border_radius="16px",
                    padding="20px",
                ),

                rx.hstack(

                    rx.input(
                        placeholder="Ex.: Como solicitar a colação de grau?",
                        value=State.question,
                        on_change=State.set_question,
                        disabled=State.loading,
                        flex="1",
                        size="3",
                    ),

                    rx.button(
                        "Perguntar",
                        on_click=State.ask,
                        disabled=State.loading,
                        width="160px",
                        size="3",
                    ),

                    width="100%",
                ),

                width="100%",
                spacing="5",
            ),

            width="85%",
            max_width="1500px",
            padding="30px",
            background="white",
            border_radius="20px",
            box_shadow="0 10px 30px rgba(0,0,0,0.08)",
        ),

        width="100%",
        min_height="100vh",
        background="#EEF2F7",
        padding="40px",
    )


app = rx.App()
app.add_page(index)