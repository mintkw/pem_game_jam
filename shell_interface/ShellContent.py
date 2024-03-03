import pygame as pg


class Shell:
    def __init__(self, prompt: str, font: pg.font, width: int, screen, color):
        self.text = ['']  # list of lines displayed in the shell
        self.font = font
        self.width = width
        self.first_active_line = 0
        self.current_line = 0
        self.prompt = prompt
        self.line_height = font.size('a')[1] + 1  # base each line's height on the height of the font
        self.max_line_length = width // font.size('a')[0]  # max length that a line is allowed to be
        self.input_boxes = [pg.Rect(0, 0, width, self.line_height)]  # going to draw one rect per line.
        self.screen = screen
        self.color = color

    def add_input_box(self):
        self.input_boxes.append(pg.Rect(0, self.line_height * self.current_line, self.width, self.line_height))

    def enter_command(self):
        # freeze the lines that were active
        self.text[self.first_active_line] = self.prompt + self.text[self.first_active_line]

        # placeholder- run command and get some output back
        output_text = "command not found command not found command not found command not found command not found\nenter something else"

        self.output_text(output_text)

        # start new line
        self.current_line += 1

        self.add_input_box()
        self.text.append('')

        # update line
        self.first_active_line = self.current_line

    def backspace(self):
        # if the current line is done, move up one line
        if len(self.text[self.current_line]) == 0 and self.current_line > self.first_active_line:
            self.current_line -= 1
            self.text.pop(-1)
            self.input_boxes.pop(-1)

        self.text[self.current_line] = self.text[self.current_line][:-1]

    def clear_current_command(self):
        for i in range(self.first_active_line, self.current_line + 1):
            self.text[i] = ''

        while self.current_line > self.first_active_line:
            self.current_line -= 1
            self.text.pop(-1)
            self.input_boxes.pop(-1)

    def enter_character(self, char):
        self.text[self.current_line] += char

        # if length is max, start a new one
        if self.current_line == self.first_active_line:
            max_input_length = self.max_line_length - len(self.prompt)
        else:
            max_input_length = self.max_line_length

        if len(self.text[self.current_line]) >= max_input_length - 1:
            self.current_line += 1
            self.add_input_box()
            self.text.append('')

    def render(self):
        self.screen.fill((30, 30, 30))
        # Render the current text.
        txt_surfaces = []
        for line in range(self.first_active_line):
            txt_surfaces.append(self.font.render(self.text[line], True, self.color))
        txt_surfaces.append(self.font.render(self.prompt + self.text[self.first_active_line], True, self.color))
        for line in range(self.first_active_line+1, self.current_line+1):
            txt_surfaces.append(self.font.render(self.text[line], True, self.color))

        # Blit the text.
        for i in range(len(txt_surfaces)):
            surface = txt_surfaces[i]
            input_box = self.input_boxes[i]
            self.screen.blit(surface, (input_box.x+5, input_box.y+5))

    def split_on_newline_and_wrap(self, text) -> list[str]:
        """
        Takes a text, splits at each newline character,
        and wraps it to fit in the window.
        """
        text = text.split('\n')

        output = []

        for block in text:
            while len(block) >= self.max_line_length:
                output.append(block[:self.max_line_length])
                block = block[self.max_line_length:]

            output.append(block)

        return output

    def output_text(self, text):
        text = self.split_on_newline_and_wrap(text)

        for line in text:
            self.current_line += 1
            self.text.append(line)
            self.add_input_box()

