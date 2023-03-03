def split_ids_into_chunks(source: str, output: str, chunk_size: int):
    with open(source) as f, open(output, 'wt+') as out:
        for i, line in enumerate(f.readlines(), start=1):
            line = line.replace('"', '')
            if i % chunk_size == 1:
                line = "export GIDS=" + line
            if i % chunk_size:
                line = line.replace("\n", ",")
            out.write(line)


split_ids_into_chunks("ids/ids-water-polo-w.txt", "ids/env-water-polo-w.txt", 100)
