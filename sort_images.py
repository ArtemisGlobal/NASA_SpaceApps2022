from datetime import datetime


class Image:
    def __init__(self, image_name, file_dir, collect_date, instrument):
        self.image_name = image_name
        self.file_dir = file_dir
        self.collect_date = collect_date
        self.instrument = instrument


def sort_date(image_list):
    return sorted(image_list, key=lambda r: datetime.strptime(r.collect_date, "%m/%d/%y"))


def sort_object(image_list):
    return sorted(image_list, key=lambda r: r.image_name)
