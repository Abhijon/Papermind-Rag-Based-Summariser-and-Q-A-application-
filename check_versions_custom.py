import importlib.metadata

packages = [
    # Core & Web
    "Flask",
    "Werkzeug",
    "Jinja2",
    "click",
    "itsdangerous",
    "MarkupSafe",
    "blinker",
    "colorama",

    # LangChain Ecosystem
    "langchain",
    "langchain-community",
    "langchain-google-genai",

    # Vector DB & Embeddings
    "faiss-cpu",
    "sentence-transformers",

    # LLMs & APIs
    "google-generativeai",
    "transformers",
    "tokenizers",
    "huggingface-hub",
    "safetensors",

    # PDF & Utils
    "PyMuPDF",
    "PyMuPDFb",
    "youtube-transcript-api",

    # Data & ML
    "numpy",
    "torch",
    "tensorflow",
    "tensorflow-intel",
    "keras",
    "tensorboard",

    # Others
    "python-dotenv",
    "requests",
    "urllib3",
    "certifi",
    "charset-normalizer",
    "idna",
    "tqdm",
    "PyYAML",
    "regex",
    "packaging",
    "filelock",
    "sympy",
    "networkx",
    "protobuf",
    "grpcio",
    "markdown",
    "absl-py",
    "astunparse",
    "cachetools",
    "flatbuffers",
    "gast",
    "google-auth",
    "google-auth-oauthlib",
    "google-pasta",
    "h5py",
    "libclang",
    "ml-dtypes",
    "mpmath",
    "oauthlib",
    "opt-einsum",
    "pyasn1",
    "pyasn1-modules",
    "requests-oauthlib",
    "rsa",
    "six",
    "tensorboard-data-server",
    "tensorflow-estimator",
    "tensorflow-io-gcs-filesystem",
    "termcolor",
    "typing_extensions",
    "wrapt",
    "fsspec"
]

print("Library Versions:")
for package in packages:
    try:
        version = importlib.metadata.version(package)
        print(f"{package}: {version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"{package}: Not found")
