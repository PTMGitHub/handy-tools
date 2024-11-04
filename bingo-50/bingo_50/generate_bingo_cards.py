import random

# Step 1: Function to generate a 5x5 Bingo card with specific number ranges
def generate_bingo_card():
    # Generate columns based on the specified number ranges
    column1 = random.sample(range(1, 11), 5)  # Numbers from 1 to 10
    column2 = random.sample(range(11, 21), 5)  # Numbers from 11 to 20
    column3 = random.sample(range(21, 31), 5)  # Numbers from 21 to 30
    column4 = random.sample(range(31, 41), 5)  # Numbers from 31 to 40
    column5 = random.sample(range(41, 51), 5)  # Numbers from 41 to 50

    # Create the 5x5 grid
    card = [
        [column1[0], column2[0], column3[0], column4[0], column5[0]],
        [column1[1], column2[1], column3[1], column4[1], column5[1]],
        [column1[2], column2[2], "Free", column4[2], column5[2]],  # Center is a free space
        [column1[3], column2[3], column3[3], column4[3], column5[3]],
        [column1[4], column2[4], column3[4], column4[4], column5[4]]
    ]

    return card

# Step 2: Updated function to generate HTML for a single Bingo card (5x5 grid with free space)
def generate_bingo_card_html(card):
    html = '<div class="bingo-card">\n'
    for row in card:
        for num in row:
            # Each number is inside a clickable div
            if num == "Free":
                html += f'    <div class="bingo-cell free-space" onclick="toggleCell(this)">{num}</div>\n'
            else:
                html += f'    <div class="bingo-cell" onclick="toggleCell(this)">{num}</div>\n'
    html += '</div>\n'
    return html

# Step 3: Function to generate the full HTML page for each person with updated 5x5 grid styling
def generate_html_page(name, bingo_card1, bingo_card2, bingo_card3):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bingo for {name}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            .bingo-wrapper {{
                margin-bottom: 50px;
                width: 100%;
                max-width: 500px;
            }}
            .bingo-card {{
                display: grid;
                grid-template-columns: repeat(5, 1fr);
                gap: 5px;
            }}
            .bingo-cell {{
                display: flex;
                justify-content: center;
                align-items: center;
                background-color: white;
                border: 2px solid #333;
                font-size: 20px;
                font-weight: bold;
                color: #555;
                cursor: pointer;
                transition: background-color 0.3s, color 0.3s;
                aspect-ratio: 1;  /* Makes each cell a square */
            }}
            .bingo-cell.free-space {{
                background-color: #28a745;
                color: white;
                cursor: default;
            }}
            .bingo-cell.clicked {{
                background-color: #28a745;
                color: white;
            }}
            @media (max-width: 600px) {{
                .bingo-cell {{
                    font-size: 16px;
                }}
            }}
            @media (max-width: 400px) {{
                .bingo-cell {{
                    font-size: 14px;
                }}
            }}
        </style>
    </head>
    <body>
        <h1>Bingo for {name}</h1>
        <div class="bingo-wrapper">
            <h2>Bingo Card 1</h2>
            {generate_bingo_card_html(bingo_card1)}
            <h2>Bingo Card 2</h2>
            {generate_bingo_card_html(bingo_card2)}
            <h2>Bingo Card 3</h2>
            {generate_bingo_card_html(bingo_card3)}
        </div>
        <footer>
            Click the numbers to mark them as called.
        </footer>
        <script>
            function toggleCell(element) {{
                element.classList.toggle('clicked');
            }}
        </script>
    </body>
    </html>
    '''

# Step 4: Function to generate HTML files for each person in the list
def generate_html_files_for_names(names):
    for name in names:
        # Generate two Bingo cards for each person
        bingo_card1 = generate_bingo_card()
        bingo_card2 = generate_bingo_card()
        bingo_card3 = generate_bingo_card()
        # Generate the HTML content
        html_content = generate_html_page(name, bingo_card1, bingo_card2, bingo_card3)

        # Write the content to an HTML file with the person's name
        filename = f"bingo_pages/{name.lower().replace(' ', '_')}.html"
        with open(filename, "w") as file:
            file.write(html_content)
        print(f"Generated HTML file for {name}: {filename}")

# Step 5: List of names and generating the HTML files
names = ["Alice", "Bob", "Charlie", "David"]
generate_html_files_for_names(names)
