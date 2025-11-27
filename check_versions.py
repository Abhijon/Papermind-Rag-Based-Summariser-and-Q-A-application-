import json
import urllib.request
import sys

def get_latest_version(package_name):
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                return data["info"]["version"]
    except Exception as e:
        # print(f"Error fetching {package_name}: {e}")
        pass
    return None

packages = [
    "absl-py", "astunparse", "blinker", "cachetools", "certifi", "charset-normalizer",
    "click", "colorama", "filelock", "Flask", "flatbuffers", "fsspec", "gast",
    "google-auth", "google-auth-oauthlib", "google-pasta", "grpcio", "h5py",
    "huggingface-hub", "idna", "itsdangerous", "Jinja2", "keras", "libclang",
    "Markdown", "MarkupSafe", "ml-dtypes", "mpmath", "networkx", "numpy",
    "oauthlib", "opt-einsum", "packaging", "pipeline", "protobuf", "pyasn1",
    "pyasn1-modules", "PyMuPDF", "PyMuPDFb", "PyYAML", "regex", "requests",
    "requests-oauthlib", "rsa", "safetensors", "six", "sympy", "tensorboard",
    "tensorboard-data-server", "tensorflow", "tensorflow-estimator", "tensorflow-intel",
    "tensorflow-io-gcs-filesystem", "termcolor", "tokenizers", "torch", "tqdm",
    "transformers", "typing_extensions", "urllib3", "Werkzeug", "wrapt",
    "youtube-transcript-api", "langchain", "langchain-community",
    "langchain-google-genai", "faiss-cpu", "sentence-transformers", "python-dotenv"
]

new_requirements = []
for pkg in packages:
    ver = get_latest_version(pkg)
    if ver:
        new_requirements.append(f"{pkg}=={ver}")
    else:
        new_requirements.append(pkg)

with open("requirement_new.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(new_requirements))
