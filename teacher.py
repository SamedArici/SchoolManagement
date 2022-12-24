class Teacher:
    def __init__(self,id,name,surname,TC,birthdate,gender,branchid):
        self.TC = TC
        self.name = name
        self.surname = surname
        self.birthdate = birthdate
        self.gender = gender
        self.branchid = branchid

        if id is None:
            self.id = 0
        else:
            self.id = id

    @staticmethod
    def createTeacher(obj):
        list = []

        if isinstance(obj, tuple):
            list.append(Teacher(obj[0],obj[1],obj[2],obj[3],obj[4],obj[5],obj[6]))
        
        else:
            for i in obj:
                list.append(Teacher(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
        
        
        return list