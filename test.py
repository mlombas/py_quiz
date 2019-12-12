text = """
import random

a = random.uniform(-1e6, 1e6)
b = random.uniform(-1e6, 1e6)
result = a
correct = True
"""
exec(text)

print(correct)
