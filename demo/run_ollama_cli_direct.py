import subprocess
from pathlib import Path


def main():
    prompt = "Connectivity test from CLI"
    cmd = ["ollama", "generate", "qwen3:8b", "--text", prompt]
    out = ""
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=120)
    except subprocess.CalledProcessError as e:
        out = f"CALLED PROCESS ERROR:\n{e.output}"
    except FileNotFoundError:
        out = "ERROR: ollama CLI not found in PATH"
    except Exception as e:
        out = f"ERROR: {e}"

    out_path = Path(__file__).resolve().parent / "ollama_cli_output.txt"
    out_path.write_text(out, encoding="utf-8")
    print(out)


if __name__ == '__main__':
    main()
