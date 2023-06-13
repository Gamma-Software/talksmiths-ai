import argparse
from talksmith.core.run import Core


def arg_parser():
    parser = argparse.ArgumentParser(description='Talksmith AI. Talk to realistic bots.')
    parser.add_argument('interface', choices=["cli", "streamlit"], help='Which interface you want to use to talk to the bot')

    args = parser.parse_args()
    return args

# Entry point of the script
def main():
    print("---Starting Talksmith---")
    args = arg_parser()
    if args.interface == "streamlit":
        print("Starting Streamlit interface")
        import os
        os.system("streamlit run talksmith/streamlit_entrypoint.py")
    else:
        core = Core(interface=args.interface)
        core.run()
    print("---Exiting Talksmith---")
