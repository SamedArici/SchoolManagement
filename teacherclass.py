class TeacherClass:
    def __init__(self,teacherid,classid):
        self.teacherid = teacherid
        self.classid = classid

    @staticmethod
    def createClass(obj):
        list = []

        if isinstance(obj,tuple):
            list.append(TeacherClass(obj[0],obj[1]))

        else:
            for i in obj:
                list.append(TeacherClass(i[0],i[1]))

        return list