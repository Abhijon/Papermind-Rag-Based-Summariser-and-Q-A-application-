"""Verify RAG packages are installed"""

print("Checking RAG packages installation...\n")

packages_status = {}

# Check langchain
try:
    import langchain
    packages_status['langchain'] = f"✓ Installed (v{langchain.__version__})"
except ImportError as e:
    packages_status['langchain'] = f"✗ Not installed: {e}"

# Check langchain-community
try:
    import langchain_community
    packages_status['langchain-community'] = "✓ Installed"
except ImportError as e:
    packages_status['langchain-community'] = f"✗ Not installed: {e}"

# Check faiss
try:
    import faiss
    packages_status['faiss-cpu'] = "✓ Installed"
except ImportError as e:
    packages_status['faiss-cpu'] = f"✗ Not installed: {e}"

# Check python-dotenv
try:
    import dotenv
    packages_status['python-dotenv'] = "✓ Installed"
except ImportError as e:
    packages_status['python-dotenv'] = f"✗ Not installed: {e}"

# Print results
print("=" * 50)
for package, status in packages_status.items():
    print(f"{package:25} {status}")
print("=" * 50)

# Check if all core packages are installed
all_installed = all("✓" in status for status in packages_status.values())
if all_installed:
    print("\n✓ All RAG packages are installed successfully!")
    print("\nYou can now build the Q&A feature!")
else:
    print("\n✗ Some packages are missing. Please install them.")
