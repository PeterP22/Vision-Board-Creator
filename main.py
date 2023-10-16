from PIL import Image, ImageDraw, ImageFont, ImageOps


def create_vision_board(images, titles=None, tasks=None, output_file="vision_board.jpg"):
    # Constants for the board
    BOARD_WIDTH = 1920
    BOARD_HEIGHT = 1080
    SIDE_PANEL_WIDTH = 400
    TOTAL_WIDTH = BOARD_WIDTH + SIDE_PANEL_WIDTH
    GAP = 50  # Gap for the title

    # Create a blank gradient canvas
    board = Image.new('RGB', (TOTAL_WIDTH, BOARD_HEIGHT), 'black')
    draw = ImageDraw.Draw(board)

    # Calculate size for each image based on the number of images
    single_image_width = BOARD_WIDTH // 3
    single_image_height = (BOARD_HEIGHT // 2) - GAP

    # Load fonts
    title_font = ImageFont.truetype("arial.ttf", size=20) if titles else None
    task_font = ImageFont.truetype("arial.ttf", size=14) if tasks else None

    positions = [(0, 0), (single_image_width, 0), (2 * single_image_width, 0),
                 (0, single_image_height + GAP), (single_image_width, single_image_height + GAP),
                 (2 * single_image_width, single_image_height + GAP)]

    for idx, image_path in enumerate(images):
        with Image.open(image_path) as img:
            img = img.resize((single_image_width, single_image_height))
            img = ImageOps.expand(img, border=5, fill='black')  # Add border to image

            # Place the image on the canvas
            board.paste(img, positions[idx])

            # Draw titles
            title_x = positions[idx][0] + (single_image_width // 2)
            title_y = positions[idx][1] + single_image_height + GAP // 4
            if titles:
                title_bbox = draw.textbbox((0, 0), titles[idx], font=title_font)
                w = title_bbox[2] - title_bbox[0]
                h = title_bbox[3] - title_bbox[1]
                draw.text((title_x - w / 2, title_y), titles[idx], font=title_font, fill="white")

    # Draw tasks in the side panel
    if tasks:
        # Draw side panel title
        side_panel_title = "How do we get there?"
        title_font_large = ImageFont.truetype("arial.ttf", size=30)
        title_bbox = draw.textbbox((0, 0), side_panel_title, font=title_font_large)
        w = title_bbox[2] - title_bbox[0]
        h = title_bbox[3] - title_bbox[1]
        title_x = BOARD_WIDTH + (SIDE_PANEL_WIDTH - w) // 2
        title_y = GAP // 2
        draw.text((title_x, title_y), side_panel_title, font=title_font_large, fill="white")

        task_y = title_y + h + GAP  # Adjust starting position for tasks after drawing the title

        for idx, task_list in enumerate(tasks):
            # Draw goal title in side panel
            title = titles[idx]
            title_bbox = draw.textbbox((0, 0), title, font=title_font)
            w = title_bbox[2] - title_bbox[0]
            h = title_bbox[3] - title_bbox[1]
            title_x = BOARD_WIDTH + (SIDE_PANEL_WIDTH - w) // 2
            draw.text((title_x, task_y), title, font=title_font, fill="white")
            task_y += h + 5

            # Draw tasks for the goal
            for task in task_list:
                task_bbox = draw.textbbox((0, 0), task, font=task_font)
                w = task_bbox[2] - task_bbox[0]
                h = task_bbox[3] - task_bbox[1]
                task_x = BOARD_WIDTH + (SIDE_PANEL_WIDTH - w) // 2
                draw.text((task_x, task_y), task, font=task_font, fill="white")
                task_y += h + 5

            # Add some space between tasks of different goals
            task_y += GAP

    board.save(output_file)


# Usage
images = ["universitydegree.jpg", "keenanLee.jpg", "cappucino.jpg", "jasonmamoa.jpg", "brotherhood.jpg", "sunlight.jpg"]
titles = ["Goal 1: Graduate University", "Goal 2: Powerlifting",
          "Goal 3: Morning coffee", "Goal 4: Unique look",
          "Goal 5: Brotherhood", "Goal 6: Vitamin D"]
tasks = [
    [">=5 x 50/10 pomodoros every day", "Be consistent", "Chip away it"],
    ["Follow the program", "3 meals day", "Sleep 8 hours"],
    ["Wake up and go straight away", "Local coffee shop", "2 splenda"],
    ["Jason mamoa hair", "Grow beard", "Tie hair back once long enough"],
    ["Be there for each other", "Be honest", "Be vulnerable"],
    ["Go outside", "Go for a walk", "Go to the beach"]
]
create_vision_board(images, titles, tasks)
