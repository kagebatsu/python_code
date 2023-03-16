import tkinter as tk
import requests
import html

### WEBB 2023 - EN LRC GRAMMAR PROJECT ###
### FOR NOTHING IN PARTICULAR ###
##########################################
class TriviaGame:
    """
    The `TriviaGame is a quiz game that generates trivia questions from the Open Trivia Database API.
    It has a GUI built with Tkinter that displays a question with multiple-choice answers, and allows the user
    to input their answer.After each answer, it displays whether the answer was correct or not,
    updates the user's score, and automatically generates a new question.
    """
    def __init__(self, master):
        self.master = master
        self.master.geometry("500x500")
        self.master.title("Trivia Game")
        self.score = 0
        self.total_questions = 0
        self.question_text = tk.StringVar()
        self.answer_text = tk.StringVar()
        self.user_answer_text = tk.StringVar()
        self.question_label = tk.Label(self.master, textvariable=self.question_text, font=("Arial", 20))
        self.answer_label = tk.Label(self.master, textvariable=self.answer_text, font=("Arial", 14))
        self.user_answer_entry = tk.Entry(self.master, textvariable=self.user_answer_text, font=("Arial", 14))
        self.score_label = tk.Label(self.master, text="Score: " + str(self.score) + "/" + str(self.total_questions),
                                    font=("Arial", 14))
        self.check_answer_button = tk.Button(self.master, text="Check Answer", font=("Arial", 14),
                                              command=self.check_answer)
        self.question_label.pack()
        self.answer_label.pack()
        self.user_answer_entry.pack()
        self.check_answer_button.pack()
        self.score_label.pack()

        self.get_question()

    def get_question(self):
        """
        The get_question method retrieves a trivia question from the Open Trivia Database API and formats it for
        display in the game interface.

        It uses the requests library to make a GET request to the API and retrieves a JSON object containing the
        question and answer options. The method then extracts the question, correct answer, and incorrect answers
        from the JSON object and formats them into a string.

        The formatted question is displayed in the game interface using the question_text variable.
        The correct answer is also stored in the TriviaGame object for use in the check_answer method.
        """
        self.user_answer_text.set("")
        self.answer_text.set("")
        self.total_questions += 1
        url = "https://opentdb.com/api.php?amount=1&type=multiple"
        response = requests.get(url)
        question_data = response.json()['results'][0]
        question = html.unescape(question_data['question'])
        correct_answer = html.unescape(question_data['correct_answer'])
        incorrect_answers = [html.unescape(answer) for answer in question_data['incorrect_answers']]
        answers = incorrect_answers + [correct_answer]
        answers.sort()
        question_formatted = f"{question}\n\n"
        for i in range(len(answers)):
            question_formatted += f"{i+1}. {answers[i]}\n"
        self.question_text.set(question_formatted)
        self.correct_answer = correct_answer

    def check_answer(self):
        user_answer = self.user_answer_text.get()
        if user_answer == self.correct_answer:
            self.score += 1
            self.answer_text.set("Correct!")
            self.get_question()
        else:
            self.answer_text.set(f"Incorrect. The correct answer was {self.correct_answer}.")
            self.get_question()

        self.score_label.config(text="Score: " + str(self.score) + "/" + str(self.total_questions))


if __name__ == '__main__':
    root = tk.Tk()
    trivia_game = TriviaGame(root)
    root.mainloop()
