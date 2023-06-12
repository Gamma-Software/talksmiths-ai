
# Get user input and process it
def get_user_input(chatgpt_chain):
    while True:
        user_input = input(f"\nYour message: ")
        if user_input.lower() == 'exit':
            export_input = input(f"\nNice talking to you. Do you want to export our conversation? (Y/N): ")
            if export_input.lower() == 'y':
                # Access the memory
                memory = chatgpt_chain.memory.load_memory_variables({})
                # Save chat history in memory
                export_chat_history(memory, "human_assistant_messages.txt")
            break
        else:
            error_message = run_async(process_input(chatgpt_chain, user_input))
            if error_message is not None:
                break