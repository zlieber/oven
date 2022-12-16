
class Curve:
    def __init__(self, name, spec):
        self.name = name
        self.spec = spec

    def getxy(self):
        x = [0.0]
        y = [25.0]

        for l in list(self.spec.split('\n')) + [ "-3 25 0" ]:
            if not l:
                continue
            words = l.split(' ')
            curr_x = x[-1]
            curr_y = y[-1]
            temp = float(words[1])
            dpm = float(words[0])
            dwell = float(words[2])
            time = (temp - curr_y) / (dpm * 60)
            if time < 0:
                raise Exception("Negative time: %s" % self.spec)
            x.append(curr_x + time)
            y.append(temp)
            x.append(curr_x + time + dwell)
            y.append(temp)

        return x, y
