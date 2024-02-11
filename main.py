import pygame, sys
import pygame_gui
import colors
import cell_class
from collections import OrderedDict
import tkinter as tk
from tkinter import messagebox
import ai_integration
import json
import dice
import spritesheet
import webbrowser

# QUIZ CLASS
class QuizApp:
    def __init__(self, master, follow_ups):
        # Here, master is tk_obj
        self.options_var_quiz = None
        self.master = master
        self.master.title("Quiz")
        self.follow_ups = follow_ups

        master_window_width = 500
        master_window_height = 400
        self.master.geometry(f"{master_window_width}x{master_window_height}")

        # Center the Tkinter window
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate position for Tkinter window to be centered
        center_x = int((screen_width - master_window_width) / 2)
        center_y = int((screen_height - master_window_height) / 2)

        # Set geometry for centered placement
        self.master.geometry(f'{master_window_width}x{master_window_height}+{center_x}+{center_y}')

        self.info_label = None

        self.questions, self.options, self.correct_answers = [], [], []

        for i in self.follow_ups:
            self.questions.append(i['question'])
            self.options.append(i['options'])  # Here, it is a list
            self.correct_answers.append(i['correct_answer'])

        # print(self.questions, self.options, self.correct_answers)
        self.current_question_index = 0
        # self.options_var_quiz = tk.StringVar(value="")
        self.create_widgets()

    def create_widgets(self):
        # Clear existing widgets (if any), especially important for subsequent questions
        for widget in self.master.winfo_children():
            widget.destroy()

        print("QUESTION = ", self.questions[self.current_question_index])
        print("OPTIONS = ", self.options[self.current_question_index])
        print("ANSWER = ", self.correct_answers[self.current_question_index])

        self.question_label = tk.Label(self.master, text=self.questions[self.current_question_index], wraplength=400)
        self.question_label.pack()

        self.options_var_quiz = tk.StringVar(value="none")
        self.options_var_quiz.set(None)

        options_quiz = self.options[self.current_question_index]

        for idx, option_text in enumerate(options_quiz):
            option_radio_quiz = tk.Radiobutton(self.master, text=option_text, variable=self.options_var_quiz,
                                          value=str(idx + 1), command=self.check_answer_quiz)
            option_radio_quiz.pack()

        self.next_button = tk.Button(self.master, text="Next", command=self.next_question)
        # self.next_button.pack()

    def next_question(self):
        # Increment the question index and update widgets for the next question
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.create_widgets()  # Re-create widgets for the next question
        else:
            self.close_window()  # No more questions, close the quiz

    def extend_window_with_info_quiz(self, info_text):
        self.info_label = tk.Label(self.master, text=info_text, wraplength=400)  # Recreate new label with info
        self.info_label.pack()

    def close_window(self):
        self.master.destroy()

    def check_answer_quiz(self):
        selected_option = self.options_var_quiz.get()

        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.DISABLED)

                self.next_button.pack()

        if selected_option == "1":
            if self.options[self.current_question_index][0] == self.correct_answers[self.current_question_index]:
                self.extend_window_with_info_quiz("You got it right!")
            else:
                self.extend_window_with_info_quiz("You are wrong!")

        else:
            if self.options[self.current_question_index][1] == self.correct_answers[self.current_question_index]:
                self.extend_window_with_info_quiz("You got it right!")
            else:
                self.extend_window_with_info_quiz("You are wrong!")

# RSQ CLASS
class RSQ:
    def __init__(self, rsq_obj):
        self.question_label = None
        self.rsq_obj = rsq_obj
        self.rsq_obj.title("Real Life Scenario Question")
        self.generated_questions = None
        # self.rsq_obj.configure(background='#008080')
        # self.cash_networth_int = 100000  # Initial amount
        # self.cash_networth = "$" + str(self.cash_networth_int)
        rsq_window_width = 500
        rsq_window_height = 400
        self.rsq_obj.geometry(f"{rsq_window_width}x{rsq_window_height}")

        # Center the Tkinter window
        screen_width = self.rsq_obj.winfo_screenwidth()
        screen_height = self.rsq_obj.winfo_screenheight()

        # Calculate position for Tkinter window to be centered
        center_x = int((screen_width - rsq_window_width) / 2)
        center_y = int((screen_height - rsq_window_height) / 2)

        # Set geometry for centered placement
        self.rsq_obj.geometry(f'{rsq_window_width}x{rsq_window_height}+{center_x}+{center_y}')

        # self.rsq_obj.geometry("500x500")  # Width x Height in pixels
        self.info_label = None  # Placeholder for the additional information label

        # GPT HERE
        user_input = 'Please create a real-life financial scenario question with four options relevant to investments, risk management, savings, insurance, taxes, retirement, debt, asset allocation, IRA, liquidity, etc.'
        system_input = '''
                Generate output in a json format where there is a "question" field containing a real-life financial scenario question,
                an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
                an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
                Each follow-up question should also have "question", 
                "options" field with two options, and "correct_answer" field.
                '''

        self.generated_questions = ai_integration.generate_ai_questions(user_input, system_input)

        # PARSE JSON
        try:
            parsed_questions = json.loads(self.generated_questions)
        except Exception:
            print("Failed to parse JSON data. Check the format of 'generated_questions'.")
            sys.exit()

        self.main_question = parsed_questions["question"]
        self.options = parsed_questions["options"]
        self.correct_answer = parsed_questions["correct_answer"]
        self.explanation = parsed_questions["explanation"]
        self.follow_ups = parsed_questions["follow_ups"]

        # After all pre-processing is done and ready. Go for widget creation.
        self.create_widgets()

    def create_widgets(self):
        # Here question_label should be CHATGPT question
        self.question_label = tk.Label(self.rsq_obj, text=self.main_question, wraplength=350)
        self.question_label.pack()

        self.options_var = tk.StringVar()
        self.options_var.set(None)

        # Information Option should be CHATGPT question
        options = [(self.options[0], "1"), (self.options[1], "2"), (self.options[2], "3"), (self.options[3], "4")]

        for text, value in options:
            self.option_radio = tk.Radiobutton(self.rsq_obj, text=text, variable=self.options_var, value=value, command=self.check_answer)
            self.option_radio.pack()

        self.thank_you_button = tk.Button(self.rsq_obj, text="Thank You", command=lambda: self.start_quiz(self.follow_ups))
        self.okay_button = tk.Button(self.rsq_obj, text="Okay", command=self.close_window)
        # self.ok_button.pack()

    def extend_window_with_info(self, info_text):
        if self.info_label:  # Check if the label already exists
            self.info_label.configure(text=info_text)  # Update text if label exists
        else:
            self.info_label = tk.Label(self.rsq_obj, text=info_text, wraplength=400)  # Create new label with info
            self.info_label.pack()

    def close_window(self):
        self.rsq_obj.destroy()

    def start_quiz(self, follow_ups):
        for widget in self.rsq_obj.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.destroy()

        response = messagebox.askquestion("Quiz", "Would you like to take a quiz on the failed topic?")
        if response == 'no':
            self.close_window()
        else:
            self.close_window()
            quiz_tk_obj = tk.Tk()
            app = QuizApp(quiz_tk_obj, follow_ups)
            quiz_tk_obj.mainloop()

    def check_answer(self):
        selected_option = self.options_var.get()

        for widget in self.rsq_obj.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.DISABLED)

        if selected_option == "1":
            if self.options[0] == self.correct_answer:
                # Here the parameter is CHATGPT info
                creative_explanation = ""
                self.extend_window_with_info("You got it right!\n" + self.explanation + "\n" + creative_explanation)
                # cash_networth = "$" + str(cash_networth_int)
                self.okay_button.pack()
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is " + self.correct_answer + ".\n" + self.explanation + "\n" + creative_explanation)

                # cash_networth = "$" + str(cash_networth_int)
                self.thank_you_button.pack()

            # messagebox.showinfo("Congratulations", "You got it right!")
            # self.rsq_obj.destroy()
        elif selected_option == "2":
            if self.options[1] == self.correct_answer:
                # Here the parameter is CHATGPT info
                creative_explanation = ""
                self.extend_window_with_info("You got it right!\n" + self.explanation + "\n" + creative_explanation)

                # cash_networth = "$" + str(cash_networth_int)
                self.okay_button.pack()
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is " + self.correct_answer + ".\n" + self.explanation + "\n" + creative_explanation)


                # cash_networth = "$" + str(cash_networth_int)
                self.thank_you_button.pack()
            # messagebox.showinfo("Wrong", "You are wrong")
            # self.rsq_obj.destroy()
            # response = messagebox.askquestion("Try Again", "Oops! That's incorrect. Would you like to try again?")
            # if response == 'no':
            #     self.master.destroy()
            # else:
            #     self.reset_quiz()
        elif selected_option == "3":
            if self.options[2] == self.correct_answer:
                # Here the parameter is CHATGPT info
                creative_explanation = ""
                self.extend_window_with_info("You got it right!\n" + self.explanation + "\n" + creative_explanation)

                # cash_networth = "$" + str(cash_networth_int)
                self.okay_button.pack()
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is " + self.correct_answer + ".\n" + self.explanation + "\n" + creative_explanation)


                # cash_networth = "$" + str(cash_networth_int)
                self.thank_you_button.pack()

        elif selected_option == "4":
            if self.options[3] == self.correct_answer:
                # Here the parameter is CHATGPT info
                creative_explanation = ""
                self.extend_window_with_info("You got it right!\n" + self.explanation + "\n" + creative_explanation)

                # cash_networth = "$" + str(cash_networth_int)
                self.okay_button.pack()
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is " + self.correct_answer + ".\n" + self.explanation + "\n" + creative_explanation)

                # cash_networth = "$" + str(cash_networth_int)
                self.thank_you_button.pack()


class QuestionPopper:
    def __init__(self, qp_obj, type):
        self.question_label = None
        self.qp_obj = qp_obj
        self.type = type
        self.generated_questions = None
        self.qp_obj.title("Real Life Scenario Question")
        rsq_window_width = 500
        rsq_window_height = 400
        self.qp_obj.geometry(f"{rsq_window_width}x{rsq_window_height}")

        # Center the Tkinter window
        screen_width = self.qp_obj.winfo_screenwidth()
        screen_height = self.qp_obj.winfo_screenheight()

        # Calculate position for Tkinter window to be centered
        center_x = int((screen_width - rsq_window_width) / 2)
        center_y = int((screen_height - rsq_window_height) / 2)

        # Set geometry for centered placement
        self.qp_obj.geometry(f'{rsq_window_width}x{rsq_window_height}+{center_x}+{center_y}')

        # self.rsq_obj.geometry("500x500")  # Width x Height in pixels
        self.info_label = None  # Placeholder for the additional information label
        # name = None
        user_input, system_input = None, None
        if type == "ADP":
            user_input = 'Please create a Trivia question about the company ADP about its primary services and solutions, human resource, locations, payroll services, HCM solutions, stocks and shares, data security, client base, innovations, etc.'
            system_input = '''
                            Generate output in a json format where there is a "question" field containing the trivia question,
                            an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
                            an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
                            Each follow-up question should also have "question", 
                            "options" field with two options, and "correct_answer" field.
                            '''

        elif type == "FISERV":
            user_input = 'Please create a Trivia question about the company FISERV about its products, competitiveness in the financial sector, contribution to financial industry, digital banking, fintech, security of financial transactions, client base, locations, etc.'
            system_input = ''' Generate output in a json format where there is a "question" field containing the trivia question,
                                        an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
                                        an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
                                        Each follow-up question should also have "question", 
                                        "options" field with two options, and "correct_answer" field.
                                        '''

        elif type == "RUTGERS":
            user_input = 'Please create a Trivia question about the school RUTGERS about its locations, its alumni, history, sports, interesting facts, etc.'
            system_input = ''' Generate output in a json format where there is a "question" field containing the trivia question,
                                                    an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
                                                    an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
                                                    Each follow-up question should also have "question", 
                                                    "options" field with two options, and "correct_answer" field.'''

        elif type == "VANGUARD":
            user_input = 'Please create a Trivia question about the company VANGUARD about its investment philosophy, unique ownership structure, retirement plans, target-date strategy, stocks and shares, passive investment, ESG factors, etc.'
            system_input = ''' Generate output in a json format where there is a "question" field containing the trivia question,
                                                    an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
                                                    an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question. 
                                                    Each follow-up question should also have "question", 
                                                    "options" field with two options, and "correct_answer" field.
                                                    '''

        elif type == "CHANCE":
            pass
            # user_input = 'Please create a real-life financial scenario question with four options.'
            # system_input = '''
            #                 Generate output in a json format where there is a "question" field containing a real-life financial scenario question,
            #                 an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
            #                 an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question.
            #                 Each follow-up question should also have "question",
            #                 "options" field with two options, and "correct_answer" field.
            #                 '''
        else:
            url = 'https://investor.vanguard.com/corporate-portal'
            # Open the website in the default browser
            webbrowser.get('windows-default').open(url)
            self.close_window()
            return

            # user_input = 'Please create a Trivia question about the how someone would make wise investments, mutual bonds, gold loans, stocks, shares, trading, etc. '
            # system_input = ''' Generate output in a json format where there is a "question" field containing the trivia question,
            #                                                     an "options" field with an array of four options, a "correct_answer" field specifying the correct option,
            #                                                     an "explanation" field explaining why the answer is correct, and a "follow_ups" field that is an array containing five follow-up questions relevant to the main question.
            #                                                     Each follow-up question should also have "question",
            #                                                     "options" field with two options, and "correct_answer" field.
            #                                                     '''

        # GPT HERE
        if user_input and system_input:
            self.generated_questions = ai_integration.generate_ai_questions(user_input, system_input)

        # PARSE JSON
        try:
            parsed_questions = json.loads(self.generated_questions)
        except Exception:
            print("Failed to parse JSON data. Check the format of 'generated_questions'.")
            #sys.exit()
            self.close_window()
            return

        self.main_question = parsed_questions["question"]
        self.options = parsed_questions["options"]
        self.correct_answer = parsed_questions["correct_answer"]

        # if type == "ITIP":
        #     print("awdawdawdasdawd")
        #     self.question_label = tk.Label(self.qp_obj, text=self.main_question + "\n" + self.correct_answer, wraplength=350)
        #     self.question_label.pack()
        #     self.okay_button = tk.Button(self.qp_obj, text="Okay", command=self.close_window)
        #     self.okay_button.pack()
        # else:
        self.create_widgets()

    def create_widgets(self):
        # Here question_label should be CHATGPT question
        self.question_label = tk.Label(self.qp_obj, text=self.main_question, wraplength=350)
        self.question_label.pack()

        self.options_var = tk.StringVar()
        self.options_var.set(None)

        # Information Option should be CHATGPT question
        options = [(self.options[0], "1"), (self.options[1], "2"), (self.options[2], "3"), (self.options[3], "4")]

        for text, value in options:
            self.option_radio = tk.Radiobutton(self.qp_obj, text=text, variable=self.options_var, value=value, command=self.check_answer)
            self.option_radio.pack()

        self.okay_button = tk.Button(self.qp_obj, text="Okay", command=self.close_window)
        # self.ok_button.pack()

    def extend_window_with_info(self, info_text):
        if self.info_label:  # Check if the label already exists
            self.info_label.configure(text=info_text)  # Update text if label exists
        else:
            self.info_label = tk.Label(self.qp_obj, text=info_text, wraplength=400)  # Create new label with info
            self.info_label.pack()

    def close_window(self):
        self.qp_obj.destroy()

    def check_answer(self):
        selected_option = self.options_var.get()

        for widget in self.qp_obj.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                widget.config(state=tk.DISABLED)

        self.okay_button.pack()

        if selected_option == "1":
            if self.options[0] == self.correct_answer:
                # Here the parameter is CHATGPT info
                self.extend_window_with_info("You got it right!\n")
            else:
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is: " + self.correct_answer)

        elif selected_option == "2":
            if self.options[1] == self.correct_answer:
                self.extend_window_with_info("You got it right!\n")
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is: " + self.correct_answer)

        elif selected_option == "3":
            if self.options[2] == self.correct_answer:
                # Here the parameter is CHATGPT info
                self.extend_window_with_info("You got it right!\n")
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is: " + self.correct_answer)

        elif selected_option == "4":
            if self.options[3] == self.correct_answer:
                # Here the parameter is CHATGPT info
                self.extend_window_with_info("You got it right!\n")
            else:
                creative_explanation = ""
                self.extend_window_with_info("You are wrong.\n" + "The correct answer is: " + self.correct_answer)

def hard_code_cells(cell_array):
    # TYPE
    cell_array[0].type = "GO"

    rsq_list = [1, 5, 7, 9, 10, 15, 17, 21, 22]
    for i in rsq_list:
        cell_array[i].type = "RSQ"

    adp_list = [2, 13, 16]
    for i in adp_list:
        cell_array[i].type = "ADP"

    vanguard_list = [3, 14]
    for i in vanguard_list:
        cell_array[i].type = "VANGUARD"

    fiserv_list = [11, 20]
    for i in fiserv_list:
        cell_array[i].type = "FISERV"

    itip_list = [6, 12, 18]
    for i in itip_list:
        cell_array[i].type = "ITIP"

    chance_list = [4, 8, 19]
    for i in chance_list:
        cell_array[i].type = "CHANCE"

    cell_array[23].type = "RUTGERS"

    # IMAGE SET
    cell_array[0].set_image("Rasters/go_flag.svg")
    cell_array[1].set_image("Rasters/rsq.svg")
    cell_array[2].set_image("Rasters/adp.png")
    cell_array[3].set_image("Rasters/vanguard.png")
    cell_array[4].set_image("Rasters/chance_alt.svg")
    cell_array[5].set_image("Rasters/rsq.svg")
    cell_array[6].set_image("Rasters/bulb.svg")
    cell_array[7].set_image("Rasters/rsq.svg")
    cell_array[8].set_image("Rasters/chance_alt.svg")
    cell_array[9].set_image("Rasters/rsq.svg")
    cell_array[10].set_image("Rasters/rsq.svg")
    cell_array[11].set_image("Rasters/fiserv.png")
    cell_array[12].set_image("Rasters/bulb.svg")
    cell_array[13].set_image("Rasters/adp.png")
    cell_array[14].set_image("Rasters/vanguard.png")
    cell_array[15].set_image("Rasters/rsq.svg")
    cell_array[16].set_image("Rasters/adp.png")
    cell_array[17].set_image("Rasters/rsq.svg")
    cell_array[18].set_image("Rasters/bulb.svg")
    cell_array[19].set_image("Rasters/chance_alt.svg")
    cell_array[20].set_image("Rasters/fiserv.png")
    cell_array[21].set_image("Rasters/rsq.svg")
    cell_array[22].set_image("Rasters/rsq.svg")
    cell_array[23].set_image("Rasters/Rutgers.jpg")

def run_main(level_str):
    global dice_number, state_open
    dice_number, state_open = None, False
    pygame.init()

    MAIN_WIDTH, MAIN_HEIGHT = 800, 800
    CELL_WIDTH, CELL_HEIGHT = 100, 150
    CORNER_CELL_WIDTH, CORNER_CELL_HEIGHT = 150, 150
    CELL_BORDER_WIDTH, CELL_BORDER_COLOR = 4, colors.BLACK

    SCREEN = pygame.display.set_mode((MAIN_WIDTH, MAIN_HEIGHT))
    pygame.display.set_caption("Educative Financial Hack - " + level_str.upper())
    SCREEN.fill(colors.CREAM_COLOR)

    # DEFAULT_CELL = pygame.Rect(INITIAL_X_POS, INITIAL_Y_POS, CELL_WIDTH, CELL_HEIGHT)

    # Initial position for left_top is (0, 0) for first cell
    CORNER_CELL_LEFT_TOP = pygame.Rect(0, 0, CORNER_CELL_WIDTH, CORNER_CELL_HEIGHT)
    # Initial position for right is (800 - Cell_Width, 0) for first cell
    CORNER_CELL_RIGHT_TOP = pygame.Rect((MAIN_WIDTH - CORNER_CELL_WIDTH), 0, CORNER_CELL_WIDTH, CORNER_CELL_HEIGHT)
    # Initial position for left_bottom
    CORNER_CELL_LEFT_BOTTOM = pygame.Rect(0, (MAIN_HEIGHT - CORNER_CELL_HEIGHT), CORNER_CELL_WIDTH, CORNER_CELL_HEIGHT)
    # Initial position for right_bottom
    CORNER_CELL_RIGHT_BOTTOM = pygame.Rect((MAIN_WIDTH - CORNER_CELL_WIDTH), (MAIN_HEIGHT - CORNER_CELL_HEIGHT), CORNER_CELL_WIDTH, CORNER_CELL_HEIGHT)

    # DRAWING
    rect_corner_left_top = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, CORNER_CELL_LEFT_TOP, CELL_BORDER_WIDTH)  # Corner Cell -Left Top
    rect_corner_right_top = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, CORNER_CELL_RIGHT_TOP, CELL_BORDER_WIDTH)  # Corner Cell -Right Top
    rect_corner_left_bot = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, CORNER_CELL_LEFT_BOTTOM, CELL_BORDER_WIDTH)  # Corner Cell -Left Bottom # START
    rect_corner_right_bot = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, CORNER_CELL_RIGHT_BOTTOM, CELL_BORDER_WIDTH)  # Corner Cell -Right Bottom

    # DICT FOR EACH CELL OBJECT
    cell_array = {}

    dud = rect_corner_left_bot
    for i in range(24):
        if i == 0:
            cell_array[i] = rect_corner_left_bot
            dud = rect_corner_left_bot
            continue
        elif i < 6:
            cell_array[i] = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, (*dud.rect_obj.topright, CELL_WIDTH, CELL_HEIGHT), CELL_BORDER_WIDTH)
            dud = cell_array[i]
        elif i == 6:
            cell_array[i] = rect_corner_right_bot
            dud = rect_corner_right_bot
            continue
        elif 6 < i < 12:
            X, Y = dud.rect_obj.topleft
            cell_array[i] = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, (X, Y - CELL_WIDTH, CELL_HEIGHT, CELL_WIDTH), CELL_BORDER_WIDTH)
            dud = cell_array[i]
        elif i == 12:
            cell_array[i] = rect_corner_right_top
            dud = rect_corner_right_top
            continue
        elif 12 < i < 18:
            X, Y = dud.rect_obj.topleft
            cell_array[i] = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, (X - CELL_WIDTH, Y, CELL_WIDTH, CELL_HEIGHT), CELL_BORDER_WIDTH)
            dud = cell_array[i]
        elif i == 18:
            cell_array[i] = rect_corner_left_top
            dud = rect_corner_left_top
            continue
        elif 18 < i < 24:
            cell_array[i] = cell_class.Cell(SCREEN, CELL_BORDER_COLOR, (*dud.rect_obj.bottomleft, CELL_HEIGHT, CELL_WIDTH), CELL_BORDER_WIDTH)
            dud = cell_array[i]

    # This func is only for cell hard coding; doesn't return anything
    hard_code_cells(cell_array)

    # Button properties
    button_color = colors.SCARLET
    button_hover_color = colors.SCARLET_HOVER
    font = pygame.font.Font("C:\Windows\Fonts\8514fix.fon", 30)

    # Roll dice Button
    roll_dice_btn = pygame.Rect(330, 590, 150, 50)  # x, y, width, height
    roll_dice_btn_text = "Roll the dice!"

    def draw_button(surface, rect, color, text):
        pygame.draw.rect(surface, color, rect)  # Draw button
        text_surf = font.render(text, True, colors.BLACK)
        # Center text on button
        surface.blit(text_surf, text_surf.get_rect(center=rect.center))

    def is_button_hovered(rect):
        mouse_pos = pygame.mouse.get_pos()  # Get mouse position
        return rect.collidepoint(mouse_pos)  # Check if mouse is over the button

    # NETWORTH CASH
    cash_image = pygame.image.load(f'Rasters/dollar_cash.svg')
    cash_networth_int = 100000
    cash_networth = "$" + str(cash_networth_int)
    text_surface = font.render(cash_networth, True, colors.BLACK)
    text_rect = text_surface.get_rect()

    image_x, image_y = 350, 140  # Starting position of the image
    text_x = image_x + cash_image.get_width() + 10  # Position text to the right of the image
    text_y = image_y + (cash_image.get_height() - text_rect.height) // 2  # Vertically center text with the image

    SCREEN.blit(cash_image, (image_x, image_y))
    SCREEN.blit(text_surface, (text_x, text_y))

    # background = SCREEN.copy()

    # DINOSAUR MOVEMENT START
    sprite_sheet_image = pygame.image.load('Rasters/doux.png').convert_alpha()
    sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

    # animation_list = []
    # last_update = pygame.time.get_ticks()
    # animation_cooldown = 10
    # frame = 0
    x_con, y_con = 50, 700  # CENTER AT START
    # dice = 100000

    start_static = sprite_sheet.get_image(1, 24, 24, 3, colors.CREAM_COLOR)
    SCREEN.blit(start_static, (x_con, y_con))

    # BACKGROUND IMAGE
    bg_image = pygame.image.load('Rasters/center_logo.png').convert_alpha()
    image_width, image_height = bg_image.get_size()
    # Calculate the position to center the image
    image_x = (MAIN_WIDTH - image_width) // 2
    image_y = (MAIN_HEIGHT - image_height) // 2 + 5  # Finesse

    SCREEN.blit(bg_image, (image_x, image_y))


    pygame.display.update()

    curr_position_doux_coor = rect_corner_left_bot.rect_obj.center
    curr_position_doux_index = 0

    # for x in range(5, 11):
    #     animation_list.append(sprite_sheet.get_image(x, 24, 24, 3, colors.CREAM_COLOR))

    # Game Loop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click occurred within the button's rectangle
                if roll_dice_btn.collidepoint(pygame.mouse.get_pos()):
                    dice_image, dice_number = dice.roll_dice()
                    SCREEN.blit(dice_image, (MAIN_WIDTH // 2 - dice_image.get_width() // 2, MAIN_HEIGHT // 2 - dice_image.get_height() // 2))
                    pygame.display.update()
                    # Wait for a moment to show the image (you can adjust this time)
                    pygame.time.delay(1000)

            # elif event.type == pygame.USEREVENT:
            #     # Real-life Scenario Question
            #     rsq_tk_obj = tk.Tk()
            #     app = RSQ(rsq_tk_obj)
            #     rsq_tk_obj.mainloop()

        if dice_number:
            if state_open:
                print(curr_position_doux_index)
                if cell_array[curr_position_doux_index].type == "RSQ":
                    rsq_tk_obj = tk.Tk()
                    app = RSQ(rsq_tk_obj)
                    rsq_tk_obj.mainloop()
                # elif cell_array[curr_position_doux_index].type == "ITIP":
                #     pass
                # elif cell_array[curr_position_doux_index].type == "CHANCE":
                #     pass
                else:
                    qp_tk_obj = tk.Tk()
                    app = QuestionPopper(qp_tk_obj, cell_array[curr_position_doux_index].type)
                    qp_tk_obj.mainloop()

                dice_number = None
                state_open = False

        if is_button_hovered(roll_dice_btn):
            draw_button(SCREEN, roll_dice_btn, button_hover_color, roll_dice_btn_text)
        else:
            draw_button(SCREEN, roll_dice_btn, button_color, roll_dice_btn_text)

                # Check if the click is within any cell rect
                # mouse_pos = event.pos  # Get mouse position
                # for cell in cell_array.values():
                #     if cell.rect_obj.collidepoint(mouse_pos):
                #         show_popup()  # Show the popup if a cell is clicked
                #         break  # Exit the loop after showing the popup

        # pygame.display.update()
        # ###############
        if dice_number:
            state_open = True
            # prev_index = curr_position_doux_index
            # prev_cell = cell_array[prev_index]  # This is Object here
            curr_position_doux_index = (curr_position_doux_index + dice_number) % 24
            if curr_position_doux_index == 1:
                rect_to_transfer_to = (160, 700)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 2:
                rect_to_transfer_to = (260, 700)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 3:
                rect_to_transfer_to = (360, 700)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 4:
                rect_to_transfer_to = (460, 700)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 5:
                rect_to_transfer_to = (560, 700)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 6:
                rect_to_transfer_to = (700, 700)  # BECAUSE 6 is CORNER
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 7:
                rect_to_transfer_to = (700, 560)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 8:
                rect_to_transfer_to = (700, 460)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 9:
                rect_to_transfer_to = (700, 360)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 10:
                rect_to_transfer_to = (700, 260)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 11:
                rect_to_transfer_to = (700, 160)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 12:
                rect_to_transfer_to = (700, 55) # BECAUSE 12 is CORNER
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 13:
                rect_to_transfer_to = (570, 55)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 14:
                rect_to_transfer_to = (470, 55)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 15:
                rect_to_transfer_to = (370, 55)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 16:
                rect_to_transfer_to = (270, 55)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 17:
                rect_to_transfer_to = (170, 55)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 18:
                rect_to_transfer_to = (50, 55) # BECAUSE 18 is CORNER
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 19:
                rect_to_transfer_to = (50, 155)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 20:
                rect_to_transfer_to = (50, 255)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 21:
                rect_to_transfer_to = (50, 355)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 22:
                rect_to_transfer_to = (50, 455)
                SCREEN.blit(start_static, rect_to_transfer_to)
            elif curr_position_doux_index == 23:
                rect_to_transfer_to = (50, 555)
                SCREEN.blit(start_static, rect_to_transfer_to)
            # rect_to_transfer_to = cell_array[curr_position_doux_index].rect_obj.center
            pygame.display.update()

        # if dice_number:
        #     curr_position_doux_x, curr_position_doux_y = curr_position_doux[0] * dice_number, curr_position_doux[1] * dice_number
        #     curr_position_doux = (curr_position_doux_x, curr_position_doux_y)
        #     print(curr_position_doux)
        #
        #     while state_open:
        #
        #         pygame.display.flip()
        #
        #         if (x_con, y_con) == curr_position_doux:
        #             state_open = False
        #             continue
        #
        #         current_time = pygame.time.get_ticks()
        #
        #         if current_time - last_update >= animation_cooldown:
        #             frame += 1
        #             last_update = current_time
        #             if frame >= len(animation_list):
        #                 frame = 0
        #
        #             if x_con < 36 and y_con > 35:
        #                 y_con -= 1
        #
        #             if x_con > 34 and y_con < 36:
        #                 x_con += 1
        #
        #             if x_con > 699 and y_con < 700:
        #                 y_con += 1
        #
        #             if x_con > 34 and y_con > 699:
        #                 x_con -= 1
        #
        #         # print(x_con, y_con)
        #
        #         SCREEN.blit(animation_list[frame], (x_con, y_con))
        #         pygame.display.flip()

        pygame.display.flip()

    pygame.quit()

# run_main()