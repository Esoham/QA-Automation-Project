import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

# Project structure
structure = {
    '.vscode': {},
    '.github/workflows': {},
    'src': {
        'pages': {},
        'tests': {},
        'api': {},
        'utils': {},
        'performance': {},
    },
    'config': {},
    'data': {},
    'docs': {},
    'reports': {},
}

# Create directories
for dir, subdirs in structure.items():
    create_directory(dir)
    for subdir in subdirs:
        create_directory(os.path.join(dir, subdir))

# Create some basic files
create_file('.gitignore', '*.pyc\nvenv/\n__pycache__/\n')
create_file('README.md', '# FarmFresh Tester\n\nQA Automation project for GreenGrocer')
create_file('requirements.txt', 'selenium\npytest\nrequests\nlocust\n')
create_file('pytest.ini', '[pytest]\npython_files = test_*.py')

# Create a basic test file
test_content = """
def test_example():
    assert True, "This is a placeholder test"
"""
create_file(os.path.join('src', 'tests', 'test_example.py'), test_content)

print("Project structure created successfully!")
