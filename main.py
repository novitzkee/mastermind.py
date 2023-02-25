from game import ConfigPrompt, Game


if __name__ == '__main__':
    with open("resources/instruction.txt", 'r') as welcome_text_file:
            text = welcome_text_file.read().rstrip().split('\n\n')

    config_prompt = ConfigPrompt({
        "greeting": text[0],
        "instruction": text[1],
        "difficulty_warn": text[2],
        "ready_ack": text[3]
    })

    game = Game(config_prompt.get())
    game.play()