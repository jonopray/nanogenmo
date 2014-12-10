#Written by Wes Bland

class PlotPoint:

    def __init__(self, name, number):
        self.plot_name=name
        self.id_num=number
        self.who=[]
        self.when=[]
        self.where=[]
        
    def add_char(self, character):
        self.who.append(character)
        
    def add_date(self, date):
        self.when.append(date)
        
    def add_where(self, location):
        self.where.append(location)
        
    def display_info(self):
        print self.plot_name
        print self.id_num
        for name in self.who:
            print name
        for date in self.when:
            print date
        for location in self.where:
            print location
        
#Example:
pp1=PlotPoint("The Death of Ned Stark",1)
pp1.add_char("Ned Stark")
pp1.add_char("Joeffery Baratheon")
pp1.add_where("King's Landing")
pp1.add_where("The Sept of Baelor")

pp1.display_info()