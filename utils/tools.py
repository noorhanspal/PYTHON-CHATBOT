# import tempfile
# import subprocess
# import re

# # ============================
# # Python Code Executor
# # ============================

# def run_python_code(code):
#     try:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
#             f.write(code)
#             file_path = f.name

#         result = subprocess.run(
#             ["python", file_path],
#             capture_output=True,
#             text=True,
#             timeout=10
#         )

#         output = result.stdout if result.stdout else result.stderr
#         return output

#     except Exception as e:
#         return str(e)


# # ============================
# # Extract Python Code
# # ============================

# def extract_python_code(text):
#     pattern = r"```python(.*?)```"
#     matches = re.findall(pattern, text, re.DOTALL)

#     if matches:
#         return matches[0]

#     return None


import tempfile
import subprocess
import re
import os

def run_python_code(code):
    file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
            f.write(code)
            file_path = f.name

        result = subprocess.run(
            ["python", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout if result.stdout else result.stderr

    except Exception as e:
        return str(e)
    
    finally:
        if file_path and os.path.exists(file_path):
            os.unlink(file_path)


def extract_python_code(text):
    pattern = r"```python(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return matches[0]
    return None