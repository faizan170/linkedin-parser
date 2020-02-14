import json
class Utils():
    def __init__(self):
        pass
    def saveJson(self, filePath, data, index=4):
        try:
            with open(filePath, "w+") as filePath:
                json.dump(data, filePath, indent=4)
        except:
            print("Cannot create file")
            