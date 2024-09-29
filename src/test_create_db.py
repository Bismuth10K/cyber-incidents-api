from db import init_database, transform_csv

if __name__ == "__main__":
    init_database()
    transform_csv("data/cyber-operations-incidents.csv", "data/q3-cyber-operations-incidents.csv")