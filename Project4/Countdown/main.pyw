import random
from tkinter import *
import datetime


class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.count = 0
        self.imgcount = 0
        self.date = "05/14/2022/09/00"
        self.initUI()

    def initUI(self):

        # Gooey setup
        self.master.title("Countdown Clock")
        self.master.geometry("1280x800")
        self.master.attributes("-fullscreen", True)
        self.master.bind("x", quit)
        self.pack(fill=BOTH, expand=1)

        # laoding Images
        bgimages = ["test.png", "Bg_2.png", "Bg_3.png", "Bg_4.png", "Bg_5.png", "Bg_6.png", "Bg_7.png", "Bg_8.png", "Bg_9.png", "Bg_10.png", "Bg_11.png",]
        mainImages = ["normalbg1.png", "normalbg2.png", "normalbg3.png", "normalbg4.png", "normalbg5.png", "normalbg6.png"]
        self.images = []
        self.nimages = []
        for i in range(len(bgimages)-1):
            img = PhotoImage(file=bgimages[i])
            self.images.append(img)
        for i in range(len(mainImages)-1):
            img = PhotoImage(file=mainImages[i])
            self.nimages.append(img)

        # Images
        img = PhotoImage(file="normalbg1.png")
        self.bg = Label(self, image=img)
        self.bg.image = img
        self.bg.place(x=0, y=0)

        # Time Labels
        time = self.count_date(self.date)

        self.secondlbl = Label(self, text=time, fg="White", font=("helvetica", 40), bg="#050619")
        self.minutelbl = Label(self, text=time, fg="White", font=("helvetica", 40), bg="#050619")
        self.hourlbl = Label(self, text=time, fg="White", font=("helvetica", 40), bg="#050619")
        self.daylbl = Label(self, text=time, fg="White", font=("helvetica", 40), bg="#050619")

        self.secondlbl2 = Label(self, text="Sec", fg="White", font=("helvetica", 20), bg="#050619")
        self.minutelbl2 = Label(self, text="Min", fg="White", font=("helvetica", 20), bg="#050619")
        self.hourlbl2 = Label(self, text="Hrs", fg="White", font=("helvetica", 20), bg="#050619")
        self.daylbl2 = Label(self, text="Days", fg="White", font=("helvetica", 20), bg="#050619")

        # Time Label Placement
        self.secondlbl.place(x=460, y=30)
        self.minutelbl.place(x=355, y=30)
        self.hourlbl.place(x=250, y=30)
        self.daylbl.place(x=120, y=30)

        self.secondlbl2.place(x=470, y=85)
        self.minutelbl2.place(x=360, y=85)
        self.hourlbl2.place(x=258, y=85)
        self.daylbl2.place(x=133, y=85)

        # Spinners
        self.moSpinner = Spinbox(self, from_=1, to=12)
        self.daySpinner = Spinbox(self, from_=1, to=31)
        self.yearSpinner = Spinbox(self, from_=2021, to=2030)
        self.hourSpinner = Spinbox(self, from_=1, to=24)
        self.minuteSpinner = Spinbox(self, from_=1, to=59)

        # Buttons
        self.date_pick_bttn = Button(self, text="Set Date", command=self.setDate, bg="green", font=("helvetica", 7))
        self.popout_bttn = Button(self, text="Open/Close Set Date Menu", command=self.popout, bg="Black", fg="Blue")
        self.popout_bttn.place(y=10, x=1040)
        self.popout = 1
        self.x = 10000
        self.y = 10000

        # Spinner Placement
        self.popout = 1
        self.day = Label(text="day")
        self.month = Label(text="month")
        self.year = Label(text="year")
        self.minute = Label(text="minute")
        self.hour = Label(text="hour")

    def place_spinners(self):
        self.placements_x = [1050, 1150, 1050, 1150, 1100, 1100]
        self.placements_y = [100 + self.y, 100 + self.y, 200 + self.y, 200 + self.y, 300 + self.y, 400 + self.y]
        self.label_placements_x = [1050, 1150, 1050, 1150, 1100, 1100]
        self.label_placements_y = [70 + self.y, 70 + self.y, 170 + self.y, 170 + self.y, 270 + self.y, 370 + self.y]
        self.moSpinner.place(x=self.placements_x[0], y=self.placements_y[0], width=35)
        self.day.place(x=self.label_placements_x[1], y=self.label_placements_y[1])
        self.month.place(x=self.label_placements_x[0], y=self.label_placements_y[0])
        self.year.place(x=self.label_placements_x[2], y=self.label_placements_y[2])
        self.minute.place(x=self.label_placements_x[4], y=self.label_placements_y[4])
        self.hour.place(x=self.label_placements_x[3], y=self.label_placements_y[3])
        self.daySpinner.place(x=self.placements_x[1], y=self.placements_y[1], width=35)
        self.yearSpinner.place(x=self.placements_x[2], y=self.placements_y[2], width=50)
        self.hourSpinner.place(x=self.placements_x[3], y=self.placements_y[3], width=35)
        self.minuteSpinner.place(x=self.placements_x[4], y=self.placements_y[4], width=35)
        self.date_pick_bttn.place(x=self.placements_x[5], y=self.placements_y[5])

        # Popout items
        self.popout_bttn = Button(self, text="Open Set Date Menu", command=self.popout, bg="White", fg="Blue")
        self.x = 10000
        self.y = 10000

    def setDate(self):
        month = self.moSpinner.get()
        day = self.daySpinner.get()
        year = self.yearSpinner.get()
        hours = self.hourSpinner.get()
        minutes = self.minuteSpinner.get()

        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if int(day) <= days_in_month[len(month) - 1]:
            self.date = str(month) + "/" + str(day) + "/" + str(year) + "/" + str(hours) + "/" + str(minutes)
        else:
            pass

    def count_date(self, date):
        date = datetime.datetime.strptime(date, "%m/%d/%Y/%H/%M")
        now = datetime.datetime.now()
        if date > now:
            timeleft = date - now
        else:
            timeleft = now - now
        return timeleft

    def update(self):
        self.count += 1
        secondsv = StringVar()
        minutesv = StringVar()
        hoursv = StringVar()
        daysv = StringVar()
        time = self.count_date(self.date)
        totalsec = time.seconds
        currentsec = totalsec % 60
        totalmin = totalsec // 60
        currentmin = totalmin % 60
        totalhours = totalmin // 60
        currenthour = totalhours % 60
        currentday = time.days
        if self.count > 10000 and totalsec > 0 and totalhours > 0 and totalmin > 0 and currentday > 0:
            self.count =0
            newImage = random.choice(self.nimages)
            self.bg.config(image=newImage)
            self.bg.image = newImage

        if self.count > 500 and totalsec == 0 and totalhours == 0 and totalmin == 0 and currentday == 0:
            print(self.count)
            self.count = 0
            newImage = self.images[self.imgcount]
            self.imgcount+=1
            if self.imgcount>len(self.images)-1:
                self.imgcount=0
            self.bg.config(image=newImage)
            self.bg.image = newImage
        if currentsec < 10:
            secondsv = "0" + str(currentsec)
        else:
            secondsv = str(currentsec)
        if currentmin < 10:
            minutesv = "0" + str(currentmin) + " : "
        else:
            minutesv = str(currentmin) + " : "
        if currenthour < 10:
            hoursv = "0" + str(currenthour) + " : "
        else:
            hoursv = str(currenthour) + " : "
        if currentday < 10:
            daysv = "00" + str(currentday)
        elif currentday < 100:
            daysv = "0" + str(currentday)
        else:
            daysv = str(currentday)

        self.secondlbl.config(text=secondsv)
        self.minutelbl.config(text=minutesv)
        self.hourlbl.config(text=hoursv)
        self.daylbl.config(text=daysv)

        self.master.after(1, self.update)


    def popout(self):
        if self.popout == 0:
            self.x = 10000
            self.y = 10000
            self.popout = 1
        elif self.popout == 1:
            self.x = 0
            self.y = 0
            self.popout = 0
        self.place_spinners()


def main():
    root = Tk()
    app = Application(root)
    root.after(1, app.update)
    root.mainloop()


main()

# 1024x600
