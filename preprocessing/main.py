from preprocess import populate_milvus

if __name__ == "__main__":
    populate_milvus(
        json_paths=[
            # "data/applicance.json",
            # "data/computers.json",
            # "data/game_controller.json",
            # "data/headphones.json",
            # "data/keyboards.json",
            # "data/photo_printer.json",
            # "data/soundbar.json",
            "data/comic_books.json",
            "data/desks.json",
            "data/vr_gaming.json",
            "data/smartwatches.json",
            "data/fitness_trackers.json",
        ]
    )
