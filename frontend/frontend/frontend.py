import reflex as rx
import requests


class State(rx.State):
    question: str = ""
    answer: str = ""

    def set_question(self, value: str):
        self.question = value

    def ask(self):
        try:
            response = requests.post(
                "http://localhost:8000/chat",
                json={"text": self.question},
            )
            self.answer = response.json().get("answer", str(response.json()))
        except Exception as e:
            self.answer = str(e)


def index():
    return rx.center(
        rx.vstack(
            rx.heading("Chat com Agno"),

            rx.input(
                placeholder="Digite sua pergunta...",
                value=State.question,
                on_change=State.set_question,
                width="400px",
            ),

            rx.button("Perguntar", on_click=State.ask),

            rx.text(State.answer),
        )
    )


app = rx.App()
app.add_page(index)