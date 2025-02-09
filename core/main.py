import argparse
from core import db_manager, config_manager, executor

def main():
    parser = argparse.ArgumentParser(description="HakInfinit Framework")
    parser.add_argument('target', help="Target IP address or hostname")
    args = parser.parse_args()

    # Load configuration
    config = config_manager.load_config()

    # Initialize database
    db_manager.init_db(config['database'])

    # Execute scanning and enumeration
    executor.run(args.target, config)

if __name__ == "__main__":
    main()
