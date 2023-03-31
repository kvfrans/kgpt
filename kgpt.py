import click
import openai
from termcolor import colored
import os
import inspect

@click.command()
@click.argument('args', nargs=-1)
def kgpt_script(args):
    # read openai key from openai_key.txt
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'kgpt_openai_key.txt')

    if (len(args) >= 1 and args[0] == 'key') or not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
        # prompt user to paste key and create file.
        val = input(colored('Please paste in your OpenAI API Key', 'red'))
        with open(file_path, 'w') as f:
            f.write(val)
    
    with open(file_path, 'r') as f:
        key = f.read()
        openai.api_key = key


    if len(args) < 1:
        error()
        return
    if args[0] == 'code' or args[0] == 'c' or args[0] == '-c':
        if len(args) < 2:
            error()
            return
        code(args[1:])
    elif args[0] == 'bash' or args[0] == 'b' or args[0] == '-b':
        if len(args) < 2:
            error()
            return
        bash(args[1:])
    elif args[0] == 'fix' or args[0] == 'f' or args[0] == '-f':
        fix(args[1:])

def error():
    print(colored('Please enter a command and an argument.', 'red'))
    print(colored('kgpt code {decription}', 'green') + ' will generate Python code that accomplishes the specified objective.')
    print('    Example: '+colored('kgpt code "using numpy create a 5x5 checkerboard of 1 and 0"', 'yellow'))
    print(colored('kgpt bash {decription}', 'green') + ' will generate terminal commands that accomplishes the specified objective.')
    print('    Example: '+colored('kgpt bash "create a file named test.txt"', 'yellow'))
    print(colored('kgpt fix {run command} ', 'green') + ' will run a program and automatically fix small errors.')
    print('    Example: '+colored('kgpt fix "python test.py"', 'yellow'))

def code(args):
    # Concat args into a string.
    args = ' '.join(args)

    base_prompt = [
        {"role": "system", "content": "You are a programming assistant. Your job is to generate code that accomplishes a specified objective. If the programming language is not specified, use Python. If multiple lines of code are required, put each line on a new line. Do not explain the code. DMake sure to install all dependencies."},
        {"role": "user", "content": "Give me a code to {}".format(args)},
    ]

    # run the string into a chatgpt api.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=base_prompt,
        temperature=0,
        max_tokens=1000,
        request_timeout=15,
    )
    resp_content = response["choices"][0]['message']['content']

    if '```' in resp_content:
        splits = resp_content.split('```')
        pre = splits[0]
        command = splits[1]
        post = splits[2]

        if len(pre) > 0 and pre[-1] == '\n':
            pre = pre[:-1]
        if command[:7] == 'python\n':
            command = command[7:]
        if len(post) > 0 and post[0] == '\n':
            post = post[1:]

        print(colored(pre, 'green'))
        print(colored(command, 'yellow'))
        print(colored(post, 'green'))
    else:
        command = resp_content
        print(colored(command, 'yellow'))


def bash(args):
    # Concat args into a string.
    args = ' '.join(args)

    base_prompt = [
        {"role": "system", "content": "You are a programming assistant. Your job is to generate bash commands that perform the specified action. Reply with only the commands and nothing else. If multiple commands are required, put each command on a new line."},
        {"role": "user", "content": "Give me a bash terminal command to {}".format(args)},
    ]

    # run the string into a chatgpt api.
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=base_prompt,
        temperature=0,
        max_tokens=1000,
        request_timeout=15,
    )
    resp_content = response["choices"][0]['message']['content']

    # if any lines are only a newline, remove them.
    resp_content = resp_content.replace('\n\n', '\n')

    # If code contains ```, extract this string.
    if '```' in resp_content:
        splits = resp_content.split('```')
        pre = splits[0]
        command = splits[1]
        post = splits[2]
        print(colored(pre, 'green'))
        print(colored(command, 'yellow'))
        print(colored(post, 'green'))
    else:
        command = resp_content
        print(colored(command, 'yellow'))

    val = input("Execute command? (y/n): ")
    if val == 'y':
        import os
        os.system(command)


def fix(args):
    args = ' '.join(args)

    # execute the bash code in 'args', log the result.
    import subprocess
    import json

    result = subprocess.run(args, shell=True, capture_output=True)
    if result.stderr:
        error = result.stderr.decode('utf-8')
    if result.stdout:
        print(colored("Your code has no errors!", "green"))
        return
    
    print("Error:\n" + colored(error, "red"))

    prompt = [
        {"role": "system", "content": "You are a programming assistant. You will be given an error message. Please identify the file that is causing the error, and print the location of that file. Begin your response with [LOCATION], followed by a space, followed by the location of the file. On the next line, print [LINE NUMBER] followed by a space, followed by the line number of the error."},
        {"role": "user", "content": "Erorr:\n{}".format(error)},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        max_tokens=1000,
        request_timeout=15,
    )
    resp_content = response["choices"][0]['message']['content']
    print(colored(resp_content, 'yellow'))
    
    error_file = resp_content.split('\n')[0].split('[LOCATION] ')[1]
    error_line_number = int(resp_content.split('\n')[1].split('[LINE NUMBER] ')[1]) - 1


    file_content = open(error_file, 'r').read()

    prompt = [
        {"role": "system", "content": "You are a programming assistant. You will be given the contents of a file, along with an error message. Print a fixed version of the line of code causing the error. Begin your response with [FIX], followed by a space, followed by the fixed line of code. Do not describe your code. Do not print the original line. Only print the fixed line of code."},
        {"role": "user", "content": "File:\n===={}\n====\n\nError:\n===={}\n====".format(file_content, error)},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=prompt,
        temperature=0,
        max_tokens=1000,
        request_timeout=15,
    )
    resp_content = response["choices"][0]['message']['content']
    proposed_fix = resp_content.split('[FIX] ')[1]

    original_line = file_content.split('\n')[error_line_number]
    original_whitespace = original_line.split(original_line.strip())[0]
    print(colored("=======", 'yellow'))
    print(colored("[ORIGINAL] {}".format(original_line.strip()), 'yellow'))
    print(colored("[FIXED] {}".format(proposed_fix), "green"))

    total_fix = original_whitespace + proposed_fix

    val = input("Apply fix? (y/n): ")
    if val == 'y':
        with open(error_file, 'r') as file:
            data = file.readlines()
        data[error_line_number] = total_fix+'\n'
        with open(error_file, 'w') as file:
            file.writelines(data)

if __name__ == '__main__':
    kgpt_script()


