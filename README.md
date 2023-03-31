# kgpt

`kgpt` is a tiny utility that can integrate AI assistance into your development process. It can help generate terminal commands, code snippets, or automatically fix small errors. I built this tool for myself, but you can use it!

Install it with:
```
pip install git+https://github.com/kvfrans/kgpt.git
```

### Generate terminal commands from natural descriptions
`kgpt bash {description}` or `kgpt b {...}` creates a terminal command to solve your task. For example,
```
> kgpt b add readme to git, commit and push

====OUTPUT====
Assuming you are in the root directory of your git repository, you can use the following commands:


git add README.md
git commit -m "Add README.md"
git push


Note: Replace `README.md` with the name of your file if it's different. Also, make sure you have the necessary permissions to push to the remote repository.
==============

> Execute command? (y/n): y
(The above commands then run)
```

### Generate code snippets from natural descriptions

`kgpt code {description}` or `kgpt c {}` creates python code that solves your task. For example,
```
> kgpt c using numpy create a 5x5 checkerboard of 1 and 0

====OUTPUT====
import numpy as np

# Create a 5x5 array of zeros
arr = np.zeros((5, 5), dtype=int)

# Set alternate elements to 1
arr[::2, ::2] = 1
arr[1::2, 1::2] = 1

print(arr)
==============

Running the code results in:
[[1 0 1 0 1]
 [0 1 0 1 0]
 [1 0 1 0 1]
 [0 1 0 1 0]
 [1 0 1 0 1]]

```

### Automatically debug small errors

`kgpt fix {command to run program}` or `kgpt f {}` can automatically debug small errors. Pass in a python command as the argument. For example,

Given a file errortest.py with contents:
```
def test():
    x = 3
    x +== 6
    print(x)

test()
```

You could then run
```
> kgpt f python errortest.py

====OUTPUT====
[LOCATION] /Users/kvfrans/Documents/kgpt/errortest.py
[LINE NUMBER] 5
=======
[ORIGINAL] x +== 6
[FIXED] x += 6
==============

> Apply fix? (y/n): y
(The file would then be edited with the fixed line of code inserted.)

```

### Add API Key
To re-add your OpenAI API key, run `kgpt key`