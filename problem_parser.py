class Problem:
    def __init__(self, text, initialization, check, meta={}):
        self.text = text
        self.initialization = initialization
        self.check = check
        self.meta = meta

    @classmethod
    def from_file(cls, filename):
        return cls(*get_from_file(filename))

    def statment(self):
        return self.text

    def execute(self, user_code):
        exec(self.initialization, globals())
        exec("result = " + user_code, globals())
        exec("correct = " + self.check, globals())
        return correct


def get_indentation(line):
    return len(line) - len(line.lstrip())


def read_paragraph(text, line_index):
    lines = text.split("\n")[line_index + 1:]
    indentation = get_indentation(lines[0])
    result = []
    for l in lines:
        if get_indentation(l) >= indentation:
            result.append(l.strip())
        else: break

    return "\n".join(result)


def parse_variables(code, initialization):
    variables = []
    text = []
    #Iterate over stripped lines
    for line in (l.strip() for l in code.split("\n")):
        var_name, rest = (s.strip() for s in line.split("="))
        if "#" in rest:
            var_code, var_description = (s.strip() for s in rest.split("#"))
        #If not description, simply add "A " + the type
        else:
            var_code = rest

            #Initialize in case it uses some module
            exec(initialization, globals())
            var_description = f"A variable of type {type(eval(var_code)).__name__}"

        text.append(f"{var_name}: {var_description}")
        variables.append(f"{var_name} = {var_code}")

    text = ["Variables available:"] + [f"\t{line}" for line in text]
    return "\n".join(text), "\n".join(variables)


def parse_problem(code):
    text = ""
    #Always import random, in case user wants between
    initialization = ""
    check = ""
    for i,line in enumerate(code.split("\n")):
        #Only non-indented (sections) matter
        if get_indentation(line) != 0:
            continue

        section = line.split(":")[0]
        if section == "statment":
            #We need to add this before as its the first thing that
            #the user should read
            text = read_paragraph(code, i) + "\n" + text
        elif section == "check":
            check = read_paragraph(code, i)
        elif section == "initialization":
            initialization = read_paragraph(code, i) + "\n" + initialization
        elif section == "variables":
            v_paragraph = read_paragraph(code, i)


    v_text, v_code = parse_variables(v_paragraph, initialization)
    text += v_text
    initialization += "\n" + v_code
    return text, initialization, check


def get_from_file(filename):
    with open(filename, "r") as f:
        text = "".join(l for l in f.readlines() if not l.strip().startswith("#"))

    return parse_problem(text)


if __name__ == "__main__":
    fname = input("Enter a file to read: ")
    prob = Problem.from_file(fname)

    print(prob.statment())
    #Check that the user hasnt introduced that by error
    while (user_answer := input("Enter your answer: ")).strip() == "": pass

    is_correct = prob.execute(user_answer)
    if is_correct:
        print("Well done!")
    else:
        print("Do better next...")
