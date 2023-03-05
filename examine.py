class examine():
    def __init__(self):
        pass
    def examine_file(file_path):
        # examine the file and return the data
        file_data = 'File path: ' + file_path
        print(file_data)
        return file_data
    def close_app(self, button):
        # close the app
        App.get_running_app().stop()