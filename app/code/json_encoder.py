import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            return str(obj)
        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
	print("Test")
	date = datetime.datetime.now()
	print(json.dumps(date, cls=DateEncoder))
