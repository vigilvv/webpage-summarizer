import subprocess


def main():
    print("Hello from webpage-summarizer!")

    md = """
# Hello from Python!

## Hello again!

### Hi hi

#### hi hi

# Man

**Bold Text** and *italic text* with a list:

- Item 1
- Item 2
- Item 3
"""

    md1 = "# Hello\n\n**Bold**\n\n- Item 1\n- Item 2"

    # subprocess.run(['glow', '-'], input=md.encode())
    # # print(md)
    # print("# Hello\n\n**Bold**\n\n- Item 1\n- Item 2")
    subprocess.run(['glow', '-'], input=md.encode('utf-8'))


if __name__ == "__main__":
    main()
