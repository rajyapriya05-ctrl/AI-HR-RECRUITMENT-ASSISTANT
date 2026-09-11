import traceback
from common.ollama_client import generate

def main():
    prompt = "Connectivity test: hello from patched client"
    try:
        out = generate(prompt, model='qwen3:8b')
    except Exception as e:
        out = "ERROR:\n" + traceback.format_exc()

    print(out)
    # Save to file for easy sharing
    with open("demo/ollama_test_output.txt", "w", encoding="utf-8") as f:
        f.write(out)

if __name__ == '__main__':
    main()
