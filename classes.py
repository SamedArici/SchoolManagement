class Class:
    def __init__(self,id,name):
        self.name = name
        if id is None:
            self.id = 0
        else: self.id = id

    @staticmethod
    def createClass(obj):

        list = []

        if isinstance(obj,tuple):
            list.append(Class(obj[0],obj[1]))
        
        else:
            for i in obj:
                list.append(Class(i[0],i[1]))

        return list
