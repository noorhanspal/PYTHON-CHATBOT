import tempfile
import subprocess
import re
import os

def run_python_code(code):

    dangerous = ["os.remove", "shutil", "subprocess", "open(", "eval(", "exec("]
    for keyword in dangerous:
        if keyword in code:
            return f"⚠️ Dangerous code detected: '{keyword}' - Execution blocked!"

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
        return "\n\n".join(matches)  # ✅ Saare blocks ek saath
    return None