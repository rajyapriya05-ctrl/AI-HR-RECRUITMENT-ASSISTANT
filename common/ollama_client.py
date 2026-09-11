import json
import logging
import os
import requests
import os
import json
import subprocess
import logging
import shutil
from typing import Optional

logger = logging.getLogger(__name__)


class OllamaClient:
    def __init__(self, model: Optional[str] = None, host: Optional[str] = None):
        self.model = model or os.environ.get("OLLAMA_MODEL", "qwen3:8b")
        self.host = host or os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
        # Allow overriding or locating the ollama CLI executable
        self.ollama_path = os.environ.get("OLLAMA_CLI_PATH") or shutil.which("ollama")

    def _generate_cli(self, prompt: str, temperature: float = 0.2) -> Optional[str]:
        if not self.ollama_path:
            logger.debug("ollama CLI not found in PATH and OLLAMA_CLI_PATH not set")
            return None

        cmd = [
            self.ollama_path,
            "generate",
            self.model,
            "--text",
            prompt,
            "--temperature",
            str(temperature),
        ]
        try:
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, timeout=60)
            return output
        except FileNotFoundError:
            logger.debug("ollama CLI not found at path: %s", self.ollama_path)
            return None
        except subprocess.CalledProcessError as e:
            logger.debug("ollama CLI returned non-zero: %s", e.output)
            return None
        except Exception as e:
            logger.debug("ollama CLI failed: %s", e)
            return None

    def _generate_http(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> Optional[str]:
        try:
            import requests

            url = f"{self.host}/api/generate"
            payload = {"model": self.model, "prompt": prompt, "max_tokens": max_tokens, "temperature": temperature}
            resp = requests.post(url, json=payload, timeout=10)
            if resp.status_code == 200:
                try:
                    data = resp.json()
                except Exception:
                    return resp.text
                # Try common shapes
                if isinstance(data, dict) and "output" in data:
                    return data["output"]
                return json.dumps(data)
            else:
                logger.debug("HTTP generate returned status %s", resp.status_code)
                return None
        except Exception as e:
            logger.debug("HTTP generate failed: %s", e)
            return None

    def generate(self, prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        """Generate text using Ollama. Prefer CLI generation, with HTTP API as fallback."""
        # Prefer CLI first because many local setups use CLI-installed models without a running server.
        cli_out = self._generate_cli(prompt, temperature=temperature)
        if cli_out:
            return cli_out

        # Try HTTP API next
        http_out = self._generate_http(prompt, max_tokens=max_tokens, temperature=temperature)
        if http_out:
            return http_out

        raise RuntimeError("Both Ollama CLI and HTTP API generation failed or are unavailable")


def generate(prompt: str, model: Optional[str] = None, host: Optional[str] = None) -> str:
    client = OllamaClient(model=model, host=host)
    return client.generate(prompt)
