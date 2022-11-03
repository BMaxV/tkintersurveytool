import datetime

class App:
    def __init__(self, question_fn=None):
        self.questions = []
        self.question_index = 0
        
        if question_fn is not None:
            with open(question_fn, "r") as f:
                string = f.read()
            self.questions+=load_questions_from_text(string)
            self.question_index = 0
            
            
    def load_next_question(self):
        if self.question_index >= len(self.questions):
            # all done, collect outputs and zero everything
            output_answers_to_csv(self.questions)
            self.questions = []
            self.active_var = None
            self.question_index = 0
            return None
        else:
            q=self.questions[self.question_index]
            return q
            
    def get_save_answer(self,index):
        answer=self.questions[self.question_index].option_list[index]
        self.questions[self.question_index].selected_answer = answer
        self.question_index += 1
        return answer
        
class Question:
    def __init__(self, question, option_list):
        self.question_text = question
        self.option_list = option_list
        self.selected_answer = None


def load_questions_from_text(string):
    """
    input format is
    question?,answer,answer,answer

    other is always added at the end automatically.
    """
    questions=[]
    string = string.split("\n")
    for line in string:
        if line == '':
            continue
        line = line.split(",")
        if len(line) <= 1:
            raise TypeError(
                "I don't think that's a valid question:" + str(line))

        questions.append(Question(line[0], line[1:]))
        
    return questions

def output_answers_to_csv(questions):
    """output format is
    question, given answer
    
    obviously only makes sense in connection with the input form
    """
    
    # append it, for easier data collection
    with open("output.csv", "a") as f:
        f.write("new entry," + datetime.datetime.now().isoformat() + "\n")
        for question in questions:
            f.write(
                ",".join(
                    (question.question_text,
                     question.selected_answer)) +
                "\n")
