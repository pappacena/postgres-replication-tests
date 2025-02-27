import sys
import os
from time import sleep
import datetime

from sqlalchemy import create_engine


def main():
    max_id_ever = None
    error_start_date = None
    backward_id_counter = 0
    failure_recovery_counter = 0
    engine = create_engine(
        os.environ["DATABASE_URL"],
        echo=False,
    )
    engine.execute("CREATE TABLE IF NOT EXISTS test (id serial PRIMARY KEY, num integer, data varchar);")

    i = 0
    while True:
        i += 1
        sleep(1)
        try:
            result = engine.execute("SELECT max(id) as max_id FROM test;")
            max_id = result.fetchall()[0][0]
            if max_id_ever is None or max_id > max_id_ever:
                max_id_ever = max_id
            if max_id < max_id_ever:
                backward_id_counter += 1
            if error_start_date is not None:
                print("Recovered from error after", datetime.datetime.now() - error_start_date)
                error_start_date = None
                failure_recovery_counter += 1

            engine.execute("INSERT INTO test (num, data) VALUES (1, 'foo');")
        except Exception as e:
            if error_start_date is None:
                error_start_date = datetime.datetime.now()
            print("ERROR:", e)
        print(
            "*** Backward ID counter:", backward_id_counter,
            "Max ID ever:", max_id_ever, "Current max ID:", max_id,
            "Failure recovery counter:", failure_recovery_counter
        )
        if i % 20 == 0:
            try:
                nodes = [dict(i) for i in engine.execute("SHOW POOL_NODES;")]
                # print nodes as a table
                print("Pool nodes:")
                print("|".join(i[:10].ljust(10) for i in nodes[0].keys()))  # header
                for node in nodes:
                    print("|".join(i.ljust(10) for i in node.values()))
                print()
            except:
                pass


if __name__ == "__main__":
    main()
